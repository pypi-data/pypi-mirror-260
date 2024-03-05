import fitz
import re
from pythainlp.util import normalize
# from .fixpdf import fix_unknown_char

from pythainlp.util import normalize
from pythainlp import (
    thai_lead_vowels,
    thai_digits,
    thai_below_vowels,
    thai_above_vowels,
    thai_follow_vowels,
    thai_characters,
    thai_tonemarks,
    thai_consonants,
)

from pythainlp.corpus import thai_words
from pythainlp.tokenize import Tokenizer, Trie
import re
from pythainlp.corpus import tnc
# from pdf2techX.constants import *
from .utils import replace_list, d, _list_d, not_change, tokenizer, replace_any_list

#Init Vars from utils.py
def Initialize_var():
    global replace_list, d, _list_d, not_change, tokenizer, replace_any_list
    
    replace_list = create_unknownmapping() + []
    replace_list += [(i.replace("า", "ำ"), i) for i in list(thai_words()) if "า" in i]
    replace_list += [(i.replace("ำ", "า"), i) for i in list(thai_words()) if "ำ" in i]
    replace_list += [(i.replace("ำ", "้ำ"), i) for i in list(thai_words()) if "ำ" in i]

    # innovestx pdf
    replace_any_list = [
        (r"([\u0E00-\u0E7F])2", r"\1" + "่"),
        (r"([\u0E00-\u0E7F])5", r"\1" + "้"),
        (r"([\u0E00-\u0E7F])H", r"\1" + "์"),
        (r"([\u0E00-\u0E7F])7", r"\1" + "้"),
        (r"([\u0E00-\u0E7F])!", r"\1" + "่"),
        (r"([\u0E00-\u0E7F])A", r"\1" + "้"),
        (r"([\u0E00-\u0E7F])J", r"\1" + "์"),
        (r"([กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ])\*", r"\1" + "็"),
        # [||||||||||||] handle this
        ("", "้"),
        ("", "่"),
        ("", "ี"),
        ("", "้"),
        ("", "๊"),
        ("", "็"),
        ("", "์"),
        ("", "ื"),
        ("", "้"),
        ("", "-"),
        ("", "-"),
        ("", "ิ"),
        ("", "ั"),
    ]

    d = {i: j for i, j in replace_list}
    _list_d = set(d.keys())
    not_change = set(["ทำ", "กระทำ"])

    word_list = (
        list(thai_words()) + [i for i, _ in replace_list] + [i for _, i in replace_list]
    )

    trie_word = Trie(word_list)
    tokenizer = Tokenizer(trie_word, engine="newmm")
    


def create_unknownmapping():
    _skip_unknown_list = []
    words = tnc.word_freqs()
    replace_word = []
    words.sort(key=lambda x: len(x[0]), reverse=True)
    for w, a in words:
        # TODO combination that only vowels need to be replace
        replacer = [x for x in thai_above_vowels] + [x for x in thai_tonemarks] + ["์"]
        double_replace = False
        if w in _skip_unknown_list:
            continue
        if len(w) <= 2:
            continue
        last_replace = False
        fw = ""
        fw2 = ""
        for i, t in enumerate(w):
            if t in replacer:
                if last_replace:
                    double_replace = True
                fw += "�"
                last_replace = True
            else:
                last_replace = False
                fw += t
        if double_replace:
            for i, t in enumerate(w):
                if t in replacer:
                    if last_replace:
                        double_replace = True
                        fw2 += "�"
                    else:
                        fw2 += t
                    last_replace = True
                else:
                    last_replace = False
                    fw2 += t
        if "�" in fw:
            replace_word.append((fw, w))
        if "�" in fw2:
            replace_word.append((fw2, w))
    return replace_word

def replace_w(w):
    if w in _list_d and w not in not_change:
        return d[w]
    return w

#Params 
# text : str to clean
# replace_list : list text and repl for .replace ex. [('\xf2231','a')]  //unicode //add description """"
# sub_list : list pattern and repl for re.sub  ex. [(([{thai_lead_vowels}])[ \t]", "\\1")]
def _clean_missing_1(text, replace_list = [], sub_list = []):
    """
    This Function use to clean pdf text ex.unicode , space
    Parameters:
        text : input text
        replace_list : Use to clean unicode only!!!!! 
            ex. Input list of tuple [('\uf70a','่')] -> \uf70a change to ' ่ '  
        sub_list : Use for cleaning according to the pattern.
            ex. Input list of tuple [(f'{your pattern}',f'{your replace word}')]
        
    """
    # Rule Based
    text = text.replace("\uf70a", "่")  # ไม้เอก
    text = text.replace("\uf70b", "้")  # ไม้โท
    text = text.replace("\uf70c", "๊")  # ไม้ตรี
    text = text.replace("\uf70e", "์")  #
    text = text.replace("\uf710", "้")
    text = text.replace("\uf712", "็")
    text = text.replace("\uf705", "๋")
    text = text.replace("\xa0", "\n")
    text = text.replace("", "ิ")
    text = text.replace("", "ี")
    text = text.replace("", "ื")
    text = text.replace("", "์")
    text = "".join([replace_w(w) for w in tokenizer.word_tokenize(text)])
    text = re.sub(f"([{thai_lead_vowels}])[ \t]", "\\1", text)
    text = re.sub(f"[ \t]([{thai_above_vowels}])", "\\1", text)
    text = re.sub(f"[ \t]([{thai_follow_vowels}])", "\\1", text)
    text = re.sub(f"[ำ]([{thai_above_vowels}])", "\\1ำ", text)
    text = re.sub(f"([{thai_above_vowels}])[ \t]([{thai_consonants}])", "\\1\\2", text)
    text = re.sub(f"([{thai_characters}])[ \t]([{thai_below_vowels}])", "\\1\\2", text)
    text = "".join([replace_w(w) for w in tokenizer.word_tokenize(text)])
    text = re.sub(
        f"([{thai_tonemarks}])[ \t]+([{thai_consonants}])", "\\1\\2", text
    )  # thai_below_vowels

    text = re.sub(f"([{thai_characters}])[ \t]+([{thai_tonemarks}])", "\\1\\2", text)

    for rp in replace_any_list:
        text = re.sub(rp[0], rp[1], text)
    text = text.replace(" )", ")")
    text = text.replace("( ", "(")
    text = text.replace(" ”", "”")
    text = text.replace("“ ", "“")
    text = text.replace(" ์", "์")
    text = text.replace(" ำ", "ำ")
    
    #User Custom Rule
    for txt,repl in replace_list:
        text = text.replace(txt, repl)
    
    for pattern,repl in sub_list:
        text = re.sub(pattern, repl, text)
    
    return normalize(text)

def fix_unknown_char(text: str) -> str:
    return _clean_missing_1(text)



