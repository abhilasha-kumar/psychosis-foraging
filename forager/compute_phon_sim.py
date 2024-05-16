
import numpy as np
import scipy
import pandas as pd
import nltk
from functools import lru_cache
from itertools import product as iterprod
import re
from tqdm import tqdm

@lru_cache()
def wordbreak(s):
    '''
        Description:
            Takes in a word (str) and an arpabet dictionary and returns a list of phonemes
        Args:
            (1) s (str): string to be broken into phonemes
        Returns:
            (1) phonemes (list, size: variable): list of phonemes in s 
    '''
    try:
        arpabet = nltk.corpus.cmudict.dict()
    except LookupError:
        nltk.download('cmudict')
        arpabet = nltk.corpus.cmudict.dict()
            
    s = s.lower()
    if s in arpabet:
        return arpabet[s]
    middle = len(s)/2
    partition = sorted(list(range(len(s))), key=lambda x: (x-middle)**2-x)
    for i in partition:
        pre, suf = (s[:i], s[i:])
        if pre in arpabet and wordbreak(suf) is not None:
            return [x+y for x,y in iterprod(arpabet[pre], wordbreak(suf))]
    return None

def normalized_edit_distance(w1, w2):
    '''
        Description: 
            Takes in two strings (w1, w2) and returns the normalized edit distance between them
        Args:
            (1) w1 (str): first word
            (2) w2 (str): second word
        Returns:
            (1) normalized_edit_distance (float): normalized edit distance between w1 and w2
    '''
    print(f"for {w1} and {w2}")
    w1_break = wordbreak(w1)[0]
    print("w1_break=", w1_break)
    w2_break = wordbreak(w2)[0]
    print("w2_break=", w2_break)
    print(round(1-nltk.edit_distance(w1_break,w2_break)/(max(len(w1_break), len(w2_break))),4))
    
normalized_edit_distance('sifaka', 'sphynx')
# normalized_edit_distance('abeja', 'painteddog')
# normalized_edit_distance('abeja', 'lightningbug')
# normalized_edit_distance('abeja', 'flyingfox')
# normalized_edit_distance('abeja', 'tigerfish')
# normalized_edit_distance('abeja', 'sifaka')
# normalized_edit_distance('abeja', 'sphynx')