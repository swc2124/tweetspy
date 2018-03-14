# ====================================================================
# Author 				: swc21
# Date 					: 2018-03-14 09:40:57
# Project 				: ClusterFiles
# File Name 			: Twitter_Text_Cleaner
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
import json
import os
import re
import socket
import string
import sys

from time import gmtime
from time import sleep
from time import strftime
try:
    from Udp_Client import Report
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
except:
    os.system('clear')
    sys.exit(1)
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
                        'sn', 'sl', 'sf', 'nd', 'lk', 'gd']
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
    nums.append(str(i/1e1))
all_stops = general + general_upper + \
    general_cap + letters + punctuation + stop + nums
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
tokens_re = re.compile(r'('+'|'.join(regex_str)+')',
                       re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)


def tokenize(s):
    return word_tokenize(s)


def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token)
                  else token.lower()
                  for token in tokens]
    return tokens


def Clean_List_of_Sentence(tweet):
    keepers = []
    for word in tweet:
        if word in all_stops:
            continue
        for x in punctuation:
            word.replace(x, '').replace(x+x, '').replace(x+x+x, '')
        if word.startswith(('#', '@', 'http', '//', '/', '~', ':', '\\n', '\\')):
            continue
        if word.endswith(('#', '@', 'http', '//', '/', '~', ':', '\\n', '\\')):
            continue
        if word == '':
            continue
        marker = False
        new_word = ''
        word_len = len(word)
        for letter in word:
            if word.lower().count(letter.lower()) >= word_len//2:
                continue
            if letter in punctuation:
                continue
            if letter in nums:
                continue
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
    seq = "\x1b[1;%dm" % (30+colour) + text + "\x1b[0m"
    return seq


s = socket.socket()
host = str(getNetworkIp())
port = 40000
server_address = (str(host), port)
hostname = socket.gethostname()
os.system('clear')
#print >>sys.stderr, '\n'+ct(' -->',GREEN)+ct(' [',WHITE)+ct('STARTING UP',GREEN)+ct(']',WHITE)+ct('         [',WHITE)+ct(str(server_address[0]),MAGENTA)+ct(']',WHITE)+ct(' : ',GREEN)+ct('[',WHITE)+ct('PORT',CYAN)+ct(']',WHITE)+ct('[',WHITE)+ct(str(server_address[1]),MAGENTA)+ct(']',WHITE)
print >>sys.stderr, ' --> [STARTING UP] [%s] : [PORT] (%s)' % server_address
s.bind(server_address)
s.listen(5)
jobs_done = 0
last_tweet = None
while True:
    try:
        #print >>sys.stderr, '\n'+ct(' -->',WHITE)+ct(' [',WHITE)+ct('READY FOR CONNECTION',WHITE)+ct(']',WHITE)+ct('[',WHITE)+ct('JOBS DONE',WHITE)+ct(']',WHITE)+ct('     : ',CYAN)+ct('[',WHITE)+ct(str(jobs_done),CYAN)+ct(']',WHITE)
        print >>sys.stderr, ' --> [READY FOR CONNECTION] : '+ct('[', WHITE)+ct('JOBS DONE', YELLOW)+ct(
            ']', WHITE)+ct('     : ', CYAN)+ct('[', WHITE)+ct(str(jobs_done), CYAN)+ct(']', WHITE)
        buzzwords = []
        with open('/root/SHARED/Tweet_Code/buzzword.txt', 'r') as f:
            for word in f.readlines():
                buzzwords.append(word.replace('\n', ''))
        #print >>sys.stderr, '\n'+ct(' -->',WHITE)+ct(' [',WHITE)+ct('BUZZ-WORDS',WHITE)+ct(']',WHITE)
        #print >>sys.stderr, '\n --> [BUZZ-WORDS] : \n'
        #print >>sys.stderr, buzzwords
        conn, client_address = s.accept()
        try:
            file_name = conn.recv(128)
            print >>sys.stderr, '\n --> [CONNECTION] : [', client_address, ']\n'
            if file_name.startswith(('.')):
                conn.close()
                print >>sys.stderr, '\n\n --> [CONNECTION CLOSED] : ', file_name, '\n'
                break
            sleep(2)
            conn.close()
            print >>sys.stderr, '\n\n --> [CONNECTION CLOSED]\n'
            os.system('clear')
            os.system('cat /root/SHARED/start.txt')
            sleep(1)
            if os.path.isfile(JSON_PATH+file_name) and file_name.startswith(('20')):
                print >>sys.stderr, '\n 	--> [RECIEVED] : [', file_name, ']\n'
                print >>sys.stderr, ' 	--> [CHECKING FILE]\n'
                print >>sys.stderr, ' 	--> [LOADING INPUT FILE]\n'
                raw_tweets = []
                f = open(JSON_PATH+file_name, "r")
                for line in f.readlines():
                    if len(line) > 9:
                        raw_tweets.append(line)
                    else:
                        continue
                tweets = []
                for tweet in raw_tweets:
                    try:
                        tweets.append(json.loads(tweet))
                    except:
                        continue
                print >>sys.stderr, ' 	--> [INPUT FILE LOADED] : [', len(
                    tweets), '] Tweets \n'
                print >>sys.stderr, ' 	--> [DELETING INPUT FILE FROM INBOX]\n'
                sleep(1)
                try:
                    os.remove(JSON_PATH+file_name)
                    print >>sys.stderr, ' 	--> [DELETED]\n'
                except:
                    print >>sys.stderr, '\n\n 		--> [ERROR][FILE NOT DELETED]\n'
                print >>sys.stderr, ' 	--> [LOADING OUTPUT FILE]\n'
                print >>sys.stderr, ' 	--> [WORKING] : \n'
                last_tweet = None
                finished_tweets = []
                for tweet in raw_tweets:
                    if tweet == last_tweet:
                        continue
                    keepers = []
                    try:
                        tweet = json.loads(tweet)
                        token = preprocess(
                            tweet['text'].encode('ascii', 'ignore'))
                        cleaned = Clean_List_of_Sentence(token)
                    except:
                        continue
                    for word in cleaned:
                        if word[0] in string.ascii_lowercase:
                            with open('/root/SHARED/Tweet_Code/Words_By_Alpha/'+word[0].lower(), 'r') as word_check:
                                if word in word_check.read():
                                    keepers.append(word)
                                    finished_tweets.append(word)
                        if word in buzzwords:
                            os.system('cat /root/SHARED/buzz.txt')
                            with open('/root/SHARED/Tweet_Output/Buzzwords/'+word+'.txt', 'a') as buzzword:
                                buzzword.write(json.dumps(cleaned)+'\n')
                            with open('/root/SHARED/Tweet_Output/Buzzwords/fulltweet/'+word+'.txt', 'a') as buzzword:
                                buzzword.write(json.dumps(tweet)+'\n')
                            sleep(2)
                        if word.upper() in buzzwords:
                            os.system('cat /root/SHARED/buzz.txt')
                            with open('/root/SHARED/Tweet_Output/Buzzwords/'+word+'.txt', 'a') as buzzword:
                                buzzword.write(json.dumps(cleaned)+'\n')
                            with open('/root/SHARED/Tweet_Output/Buzzwords/fulltweet/'+word+'.txt', 'a') as buzzword:
                                buzzword.write(json.dumps(tweet)+'\n')
                            sleep(2)
                        if word.lower() in buzzwords:
                            os.system('cat /root/SHARED/buzz.txt')
                            with open('/root/SHARED/Tweet_Output/Buzzwords/'+word+'.txt', 'a') as buzzword:
                                buzzword.write(json.dumps(cleaned)+'\n')
                            with open('/root/SHARED/Tweet_Output/Buzzwords/fulltweet/'+word+'.txt', 'a') as buzzword:
                                buzzword.write(json.dumps(tweet)+'\n')
                            sleep(2)
                    jobs_done += 1
                    last_tweet = tweet
                    if len(keepers) == 0:
                        continue
                    print keepers
                with open(OUT_PUT_PATH+'Clean_Words/'+hostname+'.txt', "a") as clean_words:
                    clean_words.write('\n'+json.dumps(finished_tweets))
            else:
                print >>sys.stderr, '\n --> [FILE DOES NOT EXIST] : [' + \
                    JSON_PATH+file_name+']'
        finally:
            os.system('clear')
            os.system('cat ~/SHARED/finished.txt')
            Report(jobs_done)
            sleep(1)
    except KeyboardInterrupt:
        print >>sys.stderr, ' --> [PAUSED WORKER]'
        if raw_input(" --> Exit? [yes/No]") == "yes":
            print >>sys.stderr, ' --> [CLOSING WORKER]'
            sys.exit(0)
        else:
            continue
'''
while FILES > 0. :
	delay = rand.randint(0,20)
	if delay>50:
		#print 'there are too few file to go around. I will sleep now for 100 seconds'
		for i in range(100):
			sleep(1)
			#print 'time until wake : ',i,'/100	 Jobs in queue : ',len(os.listdir(JSON_PATH))
	else:
		#print 'sleeping ',delay
		sleep(delay)
	print '[connecting to server] '
	sleep(2)
	with open('./worker_tempfile.txt','w') as f: 
		print '[receiving data]'
		data = s.recv(1024)
		if not data:
			break
		f.write(data)
	print '[files read from server]'
	sleep(1)
	print '[prepaing local list now]'
	sleep(1)
	filenames =[]
	with open('./worker_tempfile.txt','rb') as f:
		for name in f.read().split('|'):
			filenames.append(name)
	print '[workng now]'
	with open(OUT_PUT_PATH+hostname+'.txt', "a") as out:
		for file_name in filenames:
			if os.path.isfile(JSON_PATH+file_name):
				with open(JSON_PATH+file_name, "r") as f:
					count_all 		= Counter()
					raw_tweet 		= json.loads(f.read())
					if 'text' in raw_tweet.keys():
						tokens 			= preprocess(raw_tweet['text'].encode('ascii', 'ignore'))
						terms_all 		= [term for term in tokens]
						terms_only 		= [term for term in terms_all 
											if term not in stop 
											and not term.startswith(('#','@','http','/','~',':'))  
											and term not in nums ] 
						out.write(str(terms_only))
						print terms_only
						sleep(.5)
					else:
						print '[no keys for text]'
						sleep(.5)
			else:
				continue
			try:
				os.remove(JSON_PATH+file_name)
				#print 'file deleted'
			except:
				print '[file not deleted]'
	FILES = len(os.listdir(JSON_PATH))
	if FILES < 1000:
		#print 'there are too few file to go around. I will sleep now for 100 seconds'
		for i in range(40):
			sleep(1)
			#print 'time until wake : ',i,'/100	 Jobs in queue : ',len(os.listdir(JSON_PATH))
	print '[',FILES,'][files left in the queue]'
	delay = rand.randint(0,10)
	#print 'sleeping ',delay
	sleep(delay)
s.close()
'''
