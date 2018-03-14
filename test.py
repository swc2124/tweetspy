# ============================================================================
# Author                : swc21
# Date                  : 2018-03-14 11:22:31
# Project               : GitHub
# File Name             : test
# Last Modified by      : swc21
# Last Modified time    : 2018-03-14 12:51:23
# ============================================================================
#
from collections import Counter
from collections import defaultdict

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from time import gmtime
from time import sleep
from time import strftime

import json
import numpy.random as rand
import os
import re
import socket
import string
import sys

emoticons_str = r"""
    (?:
        [:=;]               # Eyes
        [oO\-]?             # Nose (optional)
        [D\)\]\(\]/\\OpP]   # Mouth
    )"""
regex_str = [
    emoticons_str,
    # HTML tags
    r'<[^>]+>',
    # @-mentions
    r'(?:@[\w_]+)',
    # hash-tags
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",
    # URLs
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',
    # numbers
    r'(?:(?:\d+,?)+(?:\.?\d+)?)',
    # words with - and '
    r"(?:[a-z][a-z'\-_]+[a-z])",
    # other words
    r'(?:[\w_]+)',
    # anything else
    r'(?:\S)'
]
nums = []
for i in range(10000):
    nums.append(str(i))
    nums.append(str(i/1e1))
tokens_re = re.compile(r'('+'|'.join(regex_str)+')',
                       re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$',
                         re.VERBOSE | re.IGNORECASE)
punctuation = list(string.punctuation)
stop = [
    word.replace('"', '').replace(',', '').replace('[', '').replace(']', '')
    for word
    in json.dumps(
        stopwords.words('english')).split(' ')]
    + punctuation
    + ['rt', 'via', 'RT']


def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=True):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(
            token) else token.lower() for token in tokens]
    return tokens


OUT_PUT_PATH = 'SHARED/Tweet_Output/Clean_Words/'
JSON_PATH = 'SHARED/Tweets/'
OUTPUT_LIST = []
with open('/home/sol/CLUSTER_RAID/Tweets/'
          + os.listdir('/home/sol/CLUSTER_RAID/Tweets/')[45], 'r') as f:
    for tweet in f.readlines():
        print json.loads(tweet)
'''
    for raw_tweet in f:
        tweet       = json.loads(raw_tweet)
        tokens      = preprocess(tweet['text'].encode('ascii', 'ignore'))
        terms       = [ term for term in tokens 
                            if term not in stop 
                            and not term.startswith( ('#','@','http','/','~',':')) 
                            and term not in nums ] 
print terms
'''
