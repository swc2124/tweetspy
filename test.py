# ====================================================================
# Author 				: swc21
# Date 					: 2018-03-14 09:40:57
# Project 				: ClusterFiles
# File Name 			: test
# Last Modified by 		: swc21
# Last Modified time 	: 2018-03-14 11:07:40
# ====================================================================
#
# SOl Courtney Columbia U Department of Astronomy and Astrophysics NYC 2016
# swc2124@columbia.edu
#--[DESCRIPTION]---------------------------------------------------------#
'''
Date: May 2016
Handeler for twitter json text
'''
#--[PROGRAM-OPTIONS]------------------------------------------------------#
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
emoticons_str = r"""
	(?:
		[:=;] 				# Eyes
		[oO\-]? 			# Nose (optional)
		[D\)\]\(\]/\\OpP] 	# Mouth
	)"""
regex_str = [
    emoticons_str,
    r'<[^>]+>', 																# HTML tags
    r'(?:@[\w_]+)', 															# @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", 											# hash-tags
    # URLs
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', 												# numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", 												# words with - and '
    r'(?:[\w_]+)', 																# other words
    r'(?:\S)' 																	# anything else
]
nums = []
for i in range(10000):
    nums.append(str(i))
    nums.append(str(i/1e1))
tokens_re = re.compile(r'('+'|'.join(regex_str)+')',
                       re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', 		re.VERBOSE | re.IGNORECASE)
punctuation = list(string.punctuation)
stop = [word.replace('"', '').replace(',', '').replace('[', '').replace(']', '') for word in json.dumps(
    stopwords.words('english')).split(' ')] + punctuation + ['rt', 'via', 'RT']


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
with open('/home/sol/CLUSTER_RAID/Tweets/'+os.listdir('/home/sol/CLUSTER_RAID/Tweets/')[45], 'r') as f:
    for tweet in f.readlines():
        print json.loads(tweet)
'''
	for raw_tweet in f:
		tweet 		= json.loads(raw_tweet)
		tokens 		= preprocess(tweet['text'].encode('ascii', 'ignore'))
		terms		= [ term for term in tokens 
							if term not in stop 
							and not term.startswith( ('#','@','http','/','~',':')) 
							and term not in nums ] 
print terms
'''
