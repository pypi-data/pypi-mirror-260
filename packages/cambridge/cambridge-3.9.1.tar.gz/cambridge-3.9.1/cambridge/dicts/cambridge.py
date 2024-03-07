import requests
import threading
import sys
import re
from ..console import c_print
from ..errors import ParsedNoneError, NoResultError, call_on_error
from ..log import logger
from ..utils import (
    make_a_soup,
    get_request_url,
    get_request_url_spellcheck,
    parse_response_url,
    replace_all,
    OP,
    DICT
)
from ..dicts import dict


CAMBRIDGE_URL = "https://dictionary.cambridge.org"
CAMBRIDGE_DICT_BASE_URL = CAMBRIDGE_URL + "/dictionary/english/"
CAMBRIDGE_SPELLCHECK_URL = CAMBRIDGE_URL + "/spellcheck/english/?q="

CAMBRIDGE_DICT_BASE_URL_CN = CAMBRIDGE_URL + "/dictionary/english-chinese-simplified/"
CAMBRIDGE_SPELLCHECK_URL_CN = CAMBRIDGE_URL + "/spellcheck/english-chinese-simplified/?q="
# CAMBRIDGE_DICT_BASE_URL_CN_TRADITIONAL = "https://dictionary.cambridge.org/dictionary/english-chinese-traditional/"
# CAMBRIDGE_SPELLCHECK_URL_CN_TRADITIONAL = CAMBRIDGE_URL + "/spellcheck/english-chinese-traditional/?q="


# ----------Request Web Resource----------
def search_cambridge(con, cur, input_word, is_fresh=False, is_ch=False, no_suggestions=False):
    if is_ch:
        req_url = get_request_url(CAMBRIDGE_DICT_BASE_URL_CN, input_word, DICT.CAMBRIDGE.name)
    else:
        req_url = get_request_url(CAMBRIDGE_DICT_BASE_URL, input_word, DICT.CAMBRIDGE.name)

    if not is_fresh:
        cached = dict.cache_run(con, cur, input_word, req_url, DICT.CAMBRIDGE.name)
        if not cached:
            fresh_run(con, cur, req_url, input_word, is_ch, no_suggestions)
    else:
        fresh_run(con, cur, req_url, input_word, is_ch, no_suggestions)


def fetch_cambridge(req_url, input_word, is_ch):
    """Get response url and response text for later parsing."""

    with requests.Session() as session:
        session.trust_env = False   # not to use proxy
        res = dict.fetch(req_url, session)

        if res.url == CAMBRIDGE_DICT_BASE_URL or res.url == CAMBRIDGE_DICT_BASE_URL_CN:
            logger.debug(f'{OP.NOT_FOUND.name} "{input_word}" in {DICT.CAMBRIDGE.name}')
            if is_ch:
                spell_req_url = get_request_url_spellcheck(CAMBRIDGE_SPELLCHECK_URL_CN, input_word)
            else:
                spell_req_url = get_request_url_spellcheck(CAMBRIDGE_SPELLCHECK_URL, input_word)

            spell_res = dict.fetch(spell_req_url, session)
            spell_res_url = spell_res.url
            spell_res_text = spell_res.text
            return False, (spell_res_url, spell_res_text)

        else:
            res_url = parse_response_url(res.url)
            res_text = res.text

            logger.debug(f'{OP.FOUND.name} "{input_word}" in {DICT.CAMBRIDGE.name} at {res_url}')
            return True, (res_url, res_text)


def fresh_run(con, cur, req_url, input_word, is_ch, no_suggestions=False):
    """Print the result without cache."""

    result = fetch_cambridge(req_url, input_word, is_ch)
    found = result[0]

    if found:
        res_url, res_text = result[1]
        soup = make_a_soup(res_text)
        response_word = parse_response_word(soup)

        first_dict = parse_first_dict(res_url, soup)

        parse_thread = threading.Thread(target=parse_and_print, args=(first_dict, res_url, True))
        parse_thread.start()
        # parse_thread.join()

        dict.save(con, cur, input_word, response_word, res_url, str(first_dict))
    else:
        if no_suggestions:
            sys.exit(-1)
        else:
            spell_res_url, spell_res_text = result[1]

            logger.debug(f"{OP.PARSING.name} {spell_res_url}")
            soup = make_a_soup(spell_res_text)
            nodes = soup.find("div", "hfl-s lt2b lmt-10 lmb-25 lp-s_r-20")
            suggestions = []

            if not nodes:
                print(NoResultError(DICT.CAMBRIDGE.name))
                sys.exit()

            for ul in nodes.find_all("ul", "hul-u"):
                if "We have these words with similar spellings or pronunciations:" in ul.find_previous_sibling().text:
                    for i in ul.find_all("li"):
                        sug = replace_all(i.text)
                        suggestions.append(sug)

            logger.debug(f"{OP.PRINTING.name} the parsed result of {spell_res_url}")
            dict.print_spellcheck(con, cur, input_word, suggestions, DICT.CAMBRIDGE.name, is_ch)


# ----------The Entry Point For Parse And Print----------

def parse_and_print(first_dict, res_url, new_line=False):
    """Parse and print different sections for the word."""

    logger.debug(f"{OP.PRINTING.name} the parsed result of {res_url}")

    attempt = 0
    while True:
        try:
            blocks = first_dict.find_all(
                "div", ["pr entry-body__el", "entry-body__el clrd js-share-holder", "pr idiom-block"]
            )
        except AttributeError as e:
            attempt = call_on_error(e, res_url, attempt, OP.RETRY_PARSING.name)
            continue
        else:
            if blocks:
                for block in blocks:
                    parse_dict_head(block)
                    parse_dict_body(block)
                # parse_dict_name(first_dict)
                if new_line:
                    print()
                return
            else:
                print(NoResultError(DICT.CAMBRIDGE.name))
                sys.exit()


def parse_first_dict(res_url, soup):
    """Parse the dict section of the page for the word."""

    attempt = 0
    logger.debug(f"{OP.PARSING.name} {res_url}")

    while True:
        first_dict = soup.find("div", "pr dictionary") or soup.find("div", "pr di superentry")
        if first_dict is None:
            attempt = call_on_error(ParsedNoneError(DICT.CAMBRIDGE.name, res_url), res_url, attempt, OP.RETRY_PARSING.name)
            continue
        else:
            break

    return first_dict


# ----------Parse Response Word----------
def parse_response_word(soup):
    "Parse the response word from html head title tag."

    temp = soup.find("title").text.split("-")[0].strip()
    if "|" in temp:
        response_word = temp.split("|")[0].strip().lower()

    elif "in Simplified Chinese" in temp:
        response_word = temp.split("in Simplified Chinese")[0].strip().lower()
    else:
        response_word = temp.lower()

    return response_word


# ----------Parse Dict Head----------
# Compared to Webster, Cambridge is a bunch of deep layered html tags
# filled with unbearably messy class names.
# No clear pattern, somewhat irregular, sometimes you just need to
# tweak your codes for particular words and phrases for them to show.


def parse_head_title(block):
    word = block.find("div", "di-title").text
    return word


def parse_head_info(block):
    info = block.find_all("span", ["pos dpos", "lab dlab", "v dv lmr-0"])
    if info is not None:
        temp = [i.text for i in info]
        type = temp[0]
        text = " ".join(temp[1:])
        return (type, text)
    return None


def parse_head_type(head):
    anc = head.find("span", "anc-info-head danc-info-head")
    posgram = head.find("div", "posgram dpos-g hdib lmr-5")
    if anc is not None:
        w_type = (anc.text + head.find("span", attrs={"title": "A word that describes an action, condition or experience."},).text)
        w_type = replace_all(w_type)
    elif posgram is not None:
        w_type = replace_all(posgram.text)
    else:
        w_type = ""
    return w_type


def parse_head_pron(head):
    w_pron_uk = head.find("span", "uk dpron-i").find("span", "pron dpron")
    if w_pron_uk is not None:
        w_pron_uk = replace_all(w_pron_uk.text).replace("/", "|")

    # In bs4, not found element returns None, not raise error
    us_dpron = head.find("span", "us dpron-i")
    if us_dpron is not None:
        w_pron_us = us_dpron.find("span", "pron dpron")
        if w_pron_us is not None:
            w_pron_us = replace_all(w_pron_us.text).replace("/", "|")
            c_print("[bold]UK [/bold]" + w_pron_uk + "[bold] US [/bold]" + w_pron_us, end="  ")
        else:
            c_print("[bold]UK [/bold]" + w_pron_uk, end="  ")


def parse_head_tense(head):
    w_tense = replace_all(head.find("span", "irreg-infls dinfls").text)
    print(w_tense, end="  ")


def parse_head_domain(head):
    domain = replace_all(head.find("span", "domain ddomain").text)
    print(domain, end="  ")


def parse_head_usage(head):
    head_usage = head.find("span", "lab dlab")

    # NOTE: <span class = "var dvar"> </span>, attrs["class"] returns a list
    if head_usage is not None and head_usage.parent.attrs["class"] != ["var", "dvar"]:
        w_usage = replace_all(head_usage.text)
        return w_usage

    head_usage_next = head.find_next_sibling("span", "lab dlab")
    if head_usage_next is not None and head_usage_next.parent.attrs["class"] != ["var", "dvar"]:
        w_usage_next= replace_all(head_usage_next.text)
        return w_usage_next

    return ""


def parse_head_var(head):
    var_dvar = head.find("span", "var dvar")
    if var_dvar is not None:
        w_var = replace_all(var_dvar.text)
        print(w_var, end="  ")

    var_dvar_sib = head.find_next_sibling("span", "var dvar")
    if var_dvar_sib is not None:
        w_var = replace_all(var_dvar_sib.text)
        print(w_var, end="  ")


def parse_head_spellvar(head):
    for i in head.find_all("span", "spellvar dspellvar"):
        spell_var = replace_all(i.text)
        print(spell_var, end="  ")


def parse_dict_head(block):
    head = block.find("div", "pos-header dpos-h")
    word = parse_head_title(block)
    info = parse_head_info(block)

    if head:
        head = block.find("div", "pos-header dpos-h")
        w_type = parse_head_type(head)
        usage = parse_head_usage(head)

        if not word:
            word = parse_head_title(head)
        if w_type:
            c_print(f"\n[bold blue]{word}[/bold blue] [bold yellow]{w_type}[/bold yellow] {usage}")
        if head.find("span", "uk dpron-i"):
            if head.find("span", "uk dpron-i").find("span", "pron dpron"):
                parse_head_pron(head)

        if head.find("span", "irreg-infls dinfls"):
            parse_head_tense(head)

        if head.find("span", "domain ddomain"):
            parse_head_domain(head)

        parse_head_var(head)

        if head.find("span", "spellvar dspellvar"):
            parse_head_spellvar(head)

        print()
    else:
        c_print("[bold blue]" + word)
        if info:
            print(f"{info[0]} {info[1]}")


# ----------Parse Dict Body----------
def parse_def_title(block):
    d_title = replace_all(block.find("h3", "dsense_h").text)
    c_print("[red]" + "\n" + d_title.upper())

def parse_ptitle(block):
    p_title = block.find("span", "phrase-title dphrase-title").text
    p_info = block.find("span", "phrase-info dphrase-info")

    if p_info is not None:
        phrase_info = replace_all(p_info.text)
        print(f"\033[34;1m  {p_title}\033[0m \033[33;1m{phrase_info}\033[0m")
    else:
        print(f"\033[34;1m  {p_title}\033[0m")


def parse_def_info(def_block):
    """ def info tags like 'B1 [ C or U ]' """

    def_info = replace_all(def_block.find("span", "def-info ddef-info").text).replace(" or ", "/")
    return def_info


def print_meaning_lan(meaning_lan):
    if meaning_lan is not None:
        meaning_lan_words = meaning_lan.text.replace(";", "；").replace(",", "，")
        if not meaning_lan_words.startswith("（"):
            print(" ", end="")
        print("\033[34m" + meaning_lan_words + "\033[0m")
    else:
        print()


def print_meaning(meaning_b, usage_b, is_pmeaning):
    if is_pmeaning:
        print("  ", end="")

    if usage_b is not None:
        usage = replace_all(usage_b.text)
        meaning_words = replace_all(meaning_b.text).split(usage)[-1].replace(":", "")
        print("\033[34;1m: \033[0m" + usage + "\033[34m" + meaning_words + "\033[0m", end="")
    else:
        meaning_words = replace_all(meaning_b.text).replace(":", "")
        print("\033[34;1m: \033[0m" + "\033[34m" + meaning_words + "\033[0m", end="")


def parse_meaning(def_block, is_pmeaning=False):
    meaning_b = def_block.find("div", "def ddef_d db")
    usage_b = meaning_b.find("span", "lab dlab")

    print_meaning(meaning_b, usage_b, is_pmeaning)

    def_info = parse_def_info(def_block)
    if def_info:
        print("\033[1m " + "[" + def_info + "]" + "\033[0m", end="")

    # Print the meaning's specific language translation if any
    meaning_lan = def_block.find("span", "trans dtrans dtrans-se break-cj")
    print_meaning_lan(meaning_lan)


def parse_example(def_block, is_pexample=False):
    # NOTE:
    # suppose the first "if" has already run
    # and, the second is also "if", rather than "elif"
    # then, codes under "else" will also be run
    # meaning two cases took effect at the same time, which is not wanted
    # so, for exclusive cases, you can't write two "ifs" and one "else"
    # it should be one "if", one "elif", and one "else"
    # or three "ifs"
    for e in def_block.find_all("div", "examp dexamp"):
        if e is not None:
            example = replace_all(e.find("span", "eg deg").text)

            if is_pexample:
                print("  ", end="")

            # Print the exmaple's specific language translation if any
            example_lan = e.find("span", "trans dtrans dtrans-se hdb break-cj")
            if example_lan is not None:
                example_lan_sent = " " + example_lan.text.replace("。", "")
            else:
                example_lan_sent = ""

            if e.find("span", "lab dlab"):
                lab = replace_all(e.find("span", "lab dlab").text)
                c_print(
                    "[blue]"
                    + "|"
                    + "[/blue]"
                    + lab
                    + " "
                    + "[#757575]"
                    + example
                    + example_lan_sent
                )
            elif e.find("span", "gram dgram"):
                gram = replace_all(e.find("span", "gram dgram").text)
                c_print(
                    "[blue]"
                    + "|"
                    + "[/blue]"
                    + gram
                    + " "
                    + "[#757575]"
                    + example
                    + example_lan_sent
                )
            elif e.find("span", "lu dlu"):
                lu = replace_all(e.find("span", "lu dlu").text)
                c_print(
                    "[blue]"
                    + "|"
                    + "[/blue]"
                    + lu
                    + " "
                    + "[#757575]"
                    + example
                    + example_lan_sent
                )
            else:
                c_print("[blue]" + "|" + "[/blue]" + "[#757575]" + example + example_lan_sent)


def parse_synonym(def_block):
    s_block = def_block.find("div", re.compile("xref synonyms? hax dxref-w lmt-25"))

    if s_block is not None:
        s_title = s_block.strong.text.upper()
        c_print("[bold #757575]" + "\n  " + s_title)
        for s in s_block.find_all(
                "div", ["item lc lc1 lpb-10 lpr-10", "item lc lc1 lc-xs6-12 lpb-10 lpr-10"]
        ):
            s = s.text
            c_print("[#757575]" + "  • " + s)


def parse_see_also(def_block):
    see_also_block = def_block.find("div", re.compile("xref see_also hax dxref-w( lmt-25)?"))

    if see_also_block is not None:
        see_also = see_also_block.strong.text.upper()
        c_print("[bold #757575]" + "\n  " + see_also)

        for item in see_also_block.find_all("span", ["x-h dx-h", "x-p dx-p"]):
            c_print("[#757575]" + "  • " + item.text, end=" ")
            next_sibling = item.find_next_sibling("span")
            if next_sibling is not None:
                print(next_sibling.text)
            else:
                print()


def parse_compare(def_block):
    compare_block = def_block.find("div", re.compile("xref compare hax dxref-w( lmt-25)?"))

    if compare_block is not None:
        compare = compare_block.strong.text.upper()
        c_print("[bold #757575]" + "\n  " + compare)
        for word in compare_block.find_all(
            "div", ["item lc lc1 lpb-10 lpr-10", "item lc lc1 lc-xs6-12 lpb-10 lpr-10"]
        ):
            item = word.a.text
            c_print("[#757575]" + "  • " + item + "[/#757575]", end="")

            usage = word.find("span", "x-lab dx-lab")
            if usage:
                usage = usage.text
                print(usage, end="")

            print()


def parse_usage_note(def_block):
    usage_block = def_block.find("div", "usagenote dusagenote daccord")

    if usage_block is not None:
        usagenote = usage_block.h5.text
        c_print("[bold #757575]" + "\n  " + usagenote)
        for item in usage_block.find_all("li", "text"):
            item = item.text
            c_print("[#757575]" + "    " + item)


def parse_def(def_block):
    if "phrase-body" in def_block.parent.attrs["class"]:
        parse_meaning(def_block, True)
        parse_example(def_block, True)
    else:
        parse_meaning(def_block)
        parse_example(def_block)

    parse_synonym(def_block)
    parse_see_also(def_block)
    parse_compare(def_block)
    parse_usage_note(def_block)

def parse_idiom(block):
    idiom_block = block.find("div", re.compile("xref idioms? hax dxref-w lmt-25 lmb-25"))

    if idiom_block is not None:
        idiom_title = idiom_block.h3.text.upper()
        c_print("[bold #757575]" + "\n" + idiom_title)
        for idiom in idiom_block.find_all(
            "div",
            [
                "item lc lc1 lpb-10 lpr-10",
                "item lc lc1 lc-xs6-12 lpb-10 lpr-10",
            ],
        ):
            idiom = idiom.text
            c_print("[#757575]" + "  • " + idiom)


def parse_sole_idiom(block):
    idiom_sole_meaning = block.find("div", "def ddef_d db")

    if idiom_sole_meaning is not None:
        print("\033[34m" + idiom_sole_meaning.text + "\033[0m")
    parse_example(block)
    parse_see_also(block)


def parse_phrasal_verb(block):
    pv_block = block.find("div", re.compile("xref phrasal_verbs? hax dxref-w lmt-25 lmb-25"))

    if pv_block is not None:
        pv_title = pv_block.h3.text.upper()
        c_print("[bold #757575]" + "\n" + pv_title)
        for pv in pv_block.find_all(
            "div",
            ["item lc lc1 lc-xs6-12 lpb-10 lpr-10", "item lc lc1 lpb-10 lpr-10"],
        ):
            pv = pv.text
            c_print("[#757575]" + "  • " + pv)


def parse_dict_body(block):
    subblocks = block.find_all("div", ["pr dsense", "pr dsense dsense-noh"])

    if subblocks:
        for subblock in subblocks:
            # Comment out because it looks superfluous.
            # if subblock.find("h3", "dsense_h"):
            #     parse_def_title(subblock)

            for child in subblock.find("div", "sense-body dsense_b").children:
                try:
                    if child.attrs["class"] == ["def-block", "ddef_block"]:
                        parse_def(child)

                    if child.attrs["class"] == [
                        "pr",
                        "phrase-block",
                        "dphrase-block",
                        "lmb-25",
                    ] or child.attrs["class"] == ["pr", "phrase-block", "dphrase-block"]:
                        parse_ptitle(child)

                        for i in child.find_all("div", "def-block ddef_block"):
                            parse_def(i)
                except Exception:
                    pass

    else:
        idiom_sole_block = block.find("div", "idiom-block")
        if idiom_sole_block is not None:
            parse_sole_idiom(idiom_sole_block)

    parse_idiom(block)
    parse_phrasal_verb(block)


# ----------Parse Dict Name----------
def parse_dict_name(first_dict):
    if first_dict.small is not None:
        dict_info = replace_all(first_dict.small.text).strip("(").strip(")")
        dict_name = dict_info.split("©")[0]
        dict_name = dict_name.split("the")[-1]
    else:
        dict_name="Cambridge Dictionary"
    c_print(f"[#757575]{dict_name}", justify="right")
