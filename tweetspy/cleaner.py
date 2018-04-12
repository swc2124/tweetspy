# SOl Courtney Columbia U Department of Astronomy and Astrophysics NYC 2016
# swc2124@columbia.edu

#--[DESCRIPTION]---------------------------------------------------------#

'''
Date: May 2016

Handeler for twitter json text
'''

#--[PROGRAM-OPTIONS]------------------------------------------------------#

import json
import nltk
import os
import re
import socket
import string
import sys

from numpy.random import ranf
from datetime import datetime
from time import gmtime
from time import sleep
from time import strftime
from traceback import format_exc

from Udp_Client import Report

from nltk.tokenize import word_tokenize

from nltk.corpus import stopwords

nltk.data.path.append('/root/SHARED/nltk_data/')
OUT_PUT_PATH = '/root/SHARED/Tweet_Output/'
JSON_PATH = '/root/SHARED/Tweets/'
OUTPUT_LIST = []

#--[PROGRAM-OPTIONS]------------------------------------------------------#

general = ['gw', 'le', 'lo', 'll', 'lm', 'li', 'tn', 'tl', 'ls', 'th',
		   'ti', 'te', 'do', 'dj', 'yo', 'ya', 'dg', 'yb', 'da', 'dy',
		   'uy', 'ys', 'ahaha', 'dp', 'pffttt', 'l', 'btw', 'ea', 'et',
		   'rt', 'ul', 'rf', 'rm', 'ro', 'rj', 'wd', 'omg', 'ba', 'wa',
		   'ju', 'bn', 'wk', 'bi', 'wi', 'bk', 'wtf', 'bs', 'wy', 'om',
		   'oa', 'uni', 'ck', 'vid', 'cl', 'xc', 'ca', 'cf', 'cr', 'pr',
		   'pp', 'pa', 'pi', 'tk', 'hr', 'hi', 'ha', 'md', 'ma', 'ml',
		   'mi', 'us', 'mt', 'mv', 'ms', 'mr', 'ue', 'ae', 'ad', 'ak', 'vn',
		   'ay', 'vr', 'ar', 'ia', 'ie', 'ig', 'nb', 'ny', 'nt', 'fr', 'ft',
		   'fu', 'fa', 'fd', 'fe', 'fi', 'fl', 'sfeh', 'ki', 'kn', 'sk', 'kp',
		   'sn', 'sl', 'sf', 'nd', 'lk', 'gd', 'like', 'this']
punctuation = list(string.punctuation)
general_upper = [word.upper() for word in general]
general_cap = [word.title() for word in general]
stop = json.dumps(stopwords.words('english'))
stop = stop.replace('[', '').replace('"', '').replace(']', '').replace(' ', '')
stop = stop.split(',')
stop_upper = [word.upper() for word in stop]
stop_cap = [word.title() for word in stop]
letters = [letter for letter in
           string.ascii_lowercase +
           string.ascii_uppercase
           if letter not in
           ['a', 'A', 'I', 'i']]
nums = []
for i in range(10000):
    nums.append(str(i))
    nums.append(str(i / 1e1))
all_stops = general + general_upper + general_cap + letters + punctuation + stop + nums
emoticons_str = r"""
			(?:
				[:=;] 				# Eyes
				[oO\-]? 			# Nose (optional)
				[D\)\]\(\]/\\OpP]	# Mouth
			)"""
regex_str = [
    emoticons_str,
    r'<[^>]+>', 					# HTML tags
    r'(?:@[\w_]+)', 				# @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    # URLs
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', 	# numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", 	# words with - and '
    r'(?:[\w_]+)', 					# other words
    r'(?:\S)' 						# anything else
]
tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)


def tokenize(s):
    return word_tokenize(s)


def preprocess(s, lowercase=True):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token)
                  else token.lower()
                  for token in tokens]
    return tokens


def Clean_List_of_Sentence(tweet):
    keepers = []
    for word in tweet:
        if word.lower() in all_stops:
            # pass
            continue
        for x in punctuation:
            word.replace(x, '').replace(x + x, '').replace(x + x + x, '')
        if word.startswith(('#', '@', 'http', '//', '/', '~', ':', '\\n', '\\')):
            pass
            # continue
        if word.endswith(('#', '@', 'http', '//', '/', '~', ':', '\\n', '\\')):
            pass
            # continue
        if word == '':
            # pass
            continue
        marker = False
        new_word = ''
        word_len = len(word)
        for letter in word:
            if word.lower().count(letter.lower()) >= word_len // 2:
                # pass
                continue
            if letter in punctuation:
                pass
                # continue
            if letter in nums:
                pass
                # continue
            new_word += letter
            marker = True
        if new_word in all_stops:
            continue
        if marker == True:
            keepers.append(new_word.lower())
    return keepers


def getNetworkIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    return str(s.getsockname()[0])


BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
def ct(text, colour=WHITE):
    seq = "\x1b[1;%dm" % (30 + colour) + text + "\x1b[0m"
    return seq

host = "192.168.1.102"
port = 50000
server_address = (host, port)
hostname = socket.gethostname()
jobs_done = 0
report_jobs = 0
last_tweet = None
_slp_time = int(2. * ranf())

os.system("clear")
print ct(hostname, GREEN)
print ct("Starting after", GREEN), ct(str(_slp_time), YELLOW), ct("seconds...", GREEN)
for i in range(_slp_time):
    sys.stdout.write(ct("\rStarting in : ", GREEN) + ct(str(_slp_time - i), YELLOW) + ct(" seconds", GREEN))
    sys.stdout.flush()
    sleep(1)
print ct("\nStarting Now\n", GREEN)
sleep(1 + ranf())

while True:

    # Start job.
    os.system('clear')
    os.system('cat /root/SHARED/start.txt')
    _dots = '.'
    
    ### MAKE SOCKET ###
    # Load socket.
    print "Loading socket"
    s = socket.socket()
    try:
        s.connect(server_address)
    except Exception as e:
        sleep(ranf())
        sys.stdout.write("\rwaiting for connection" + _dots)
        sys.stdout.flush()
        _dots += '.'
        continue
    else:
        print "Connecting to", server_address
        _dots = '.'
    finally:
        print "Done."
        print "\n"

    ### RECIEVE FILE NAME ###
    # Recieve filename.
    file_name = s.recv(512)
    while file_name == '':
        sys.stdout.write("\rWaiting for filename" + _dots)
        sys.stdout.flush()
        _dots += '.'
        sleep(ranf())
    print '\n\t--> [RECIEVED] : [', file_name, ']\n'
    print '\t--> [CHECKING FILE]\n'
    if not os.path.isfile(JSON_PATH + file_name):
        print '\t--> [BAD FILE]\n'
        continue
    elif not file_name.startswith(('20')):
        print '\t--> [BAD FILE]\n'
        continue

    ### LOAD INPUT FILE ###
    # Read in raw file.
    print '\t--> [LOADING INPUT FILE]\n'
    raw_tweets = []
    with open(JSON_PATH + file_name, "r") as f:
        for raw_tweet in f.readlines():
            if len(raw_tweet) > 1:
                raw_tweets.append(json.loads(raw_tweet))
    print '\t--> [INPUT FILE LOADED] : [', len(raw_tweets), '] Tweets \n'

    #### DELETE INPUT FILE FROM INBOX ###
    # Delete old file from SHARED drive.
    print '\t--> [DELETING INPUT FILE FROM INBOX]\n'
    while os.path.isfile(JSON_PATH + file_name):
        try:
            os.remove(JSON_PATH + file_name)
        except OSError as e:
            print '\t\t--> [ERROR][FILE NOT DELETED]'
        else:
            print '\t--> [DELETED]\n'

    ### BUZZ WORDS ###
    # Get buzwords.
    print "Getting Buzzwords"
    buzzwords = []
    with open('/root/SHARED/Tweet_Code/buzzword.txt', 'r') as f:
        for word in f.readlines():
            buzzwords.append(word.replace('\n', ''))
    print "Done."

    # Misc markers & values
    last_tweet_id = 0
    finished_tweets = []

    # Main loop for each tweet.
    for tweet in raw_tweets:

        # Check to see if this is a repeat.
        if tweet['id_str'] == last_tweet_id:
            print ct("\t--> [ last_tweet ]", YELLOW)
        
        # Words to keep.
        keepers = []

        # This tweet.
        #tweet = json.loads(tweet)

        # Process and clean.
        token = preprocess(tweet['text'].encode('ascii', 'ignore'))
        cleaned = Clean_List_of_Sentence(token)
        
        # TODO
        # Check each word against language specific dictionary.
        for word in cleaned:
            if tweet['lang'] == 'en':
                if word[0].encode("ascii", 'ignore') in string.ascii_lowercase:
                    with open('/root/SHARED/Tweet_Code/Words_By_Alpha/' + word[0].lower(), 'r') as word_check:
                        if word in word_check.read():
                            keepers.append(word)
                            finished_tweets.append(word)
            else:
                keepers.append(word)
                finished_tweets.append(word)

            ### BUZZ WORDS ###
            # Check if buzzword.
            _BUZZ_WORD = False
            if word in buzzwords:
                _BUZZ_WORD = True
            elif word.upper() in buzzwords:
                _BUZZ_WORD = True
            elif word.lower() in buzzwords:
                _BUZZ_WORD = True
            
            # If it is a buzz word:
            if _BUZZ_WORD:
                os.system('cat /root/SHARED/buzz.txt')
                _buzwrd_path = '/root/SHARED/Tweet_Output/Buzzwords/' + word + '.txt'
                if not os.path.isfile(_buzwrd_path):
                    _buzmode = "w"
                else:
                    _buzmode = "a"
                with open(_buzwrd_path, mode=_buzmode) as buzzword:
                    buzzword.write(json.dumps(cleaned) + '\n')
                with open('/root/SHARED/Tweet_Output/Buzzwords/fulltweet/' + word + '.txt', mode=_buzmode) as buzzword:
                    buzzword.write(json.dumps(tweet) + '\n')

        # Add one to counter.
        jobs_done += 1
        report_jobs +=1

        # Save last tweet.
        last_tweet_id = tweet['id_str']
        
        # If there are words:
        if len(keepers):
            print tweet['lang'], keepers

    ### LOG OUTPUT ###
    # Write all clean words to disc.
    with open(OUT_PUT_PATH + 'Clean_Words/' + hostname + '.txt', "a") as clean_words:
        clean_words.write('\n' + json.dumps(finished_tweets))

    ### REPORT ###
    # Report stats to Controller.
    try:
        Report(report_jobs)    
    # If error then skip
    except:
        print ' --> ' + ct('[CAN NOT REPORT TO UDP_Server]', RED)
    # If report worked:
    else:
        # If Report works then reset report_jobs.
        # Controller keeps active count.
        report_jobs = 0

    # Banner message.
    os.system('cat ~/SHARED/finished.txt')
