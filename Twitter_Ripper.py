# ============================================================================
# Author                : swc21
# Date                  : 2018-03-14 11:22:31
# Project               : GitHub
# File Name             : Twitter_Ripper
# Last Modified by      : swc21
# Last Modified time    : 2018-03-14 12:29:22
# ============================================================================
# 

try:
    from collections import Counter, defaultdict
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from time import gmtime, strftime, sleep
    import numpy.random as rand
    import string
    import re
    import json
    import socket
    import sys
    import os
except:
    os.system('clear')
    sys.exit(1)
OUT_PUT_PATH = 'SHARED/Tweet_Output/Clean_Words/'
JSON_PATH = 'SHARED/Tweets/'
OUTPUT_LIST = []
#--[PROGRAM-OPTIONS]------------------------------------------------------#
emoticons_str = r"""
	(?:
		[:=;] # Eyes
		[oO\-]? # Nose (optional)
		[D\)\]\(\]/\\OpP] # Mouth
	)"""
regex_str = [
    emoticons_str,
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    # URLs
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',
    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]
tokens_re = re.compile(r'('+'|'.join(regex_str)+')',
                       re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via', 'RT']
nums = []
for i in range(10000):
    nums.append(str(i))
    nums.append(str(i/1e1))


def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(
            token) else token.lower() for token in tokens]
    return tokens


jobs = os.listdir(JSON_PATH)
hostname = socket.gethostname()
OUTPUT_LIST = []
for job in jobs:
    with open(JSON_PATH+job, "r") as f:
        count_all = Counter()
        try:
            raw_tweet = json.loads(f.read())
            if 'text' in raw_tweet.keys():
                tokens = preprocess(
                    raw_tweet['text'].encode('ascii', 'ignore'))
                terms_all = [term for term in tokens]
                terms_only = [term for term in terms_all
                              if term not in stop
                              and not term.startswith(('#', '@', 'http', '/', '~', ':'))
                              and term not in nums]
            OUTPUT_LIST.append(terms_only)
            print len(OUTPUT_LIST), '	', terms_only, len(os.listdir(JSON_PATH))
        except ValueError:
            continue
        finally:
            os.remove(JSON_PATH+job)
    if len(OUTPUT_LIST) > 10000:
        print '\n'+len(OUTPUT_LIST)+'\n'
        with open(OUT_PUT_PATH+hostname+'.txt', "a") as f:
            for line in OUTPUT_LIST:
                f.write(str(line))
