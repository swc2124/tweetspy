

from tweepy import StreamListener
from time import sleep
from datetime import datetime

import json
import sys
import os

import codecs
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)


def ct(text, colour=WHITE):

    seq = "\x1b[1;%dm" % (30 + colour) + text + "\x1b[0m"

    return seq


langs = {'ar': 'Arabic', 'bg': 'Bulgarian', 'ca': 'Catalan', 'cs': 'Czech',
         'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English',
         'es': 'Spanish', 'et': 'Estonian', 'fa': 'Persian', 'fi': 'Finnish',
         'fr': 'French', 'hi': 'Hindi', 'hr': 'Croatian', 'hu': 'Hungarian',
         'id': 'Indonesian', 'is': 'Icelandic', 'it': 'Italian', 'iw': 'Hebrew',
         'ja': 'Japanese', 'ko': 'Korean', 'lt': 'Lithuanian', 'lv': 'Latvian',
         'ms': 'Malay', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish',
         'pt': 'Portuguese', 'ro': 'Romanian', 'ru': 'Russian', 'sk': 'Slovak',
         'sl': 'Slovenian', 'sr': 'Serbian', 'sv': 'Swedish', 'th': 'Thai',
         'tl': 'Filipino', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu',
         'vi': 'Vietnamese', 'zh_CN': 'Chinese (simplified)',
         'zh_TW': 'Chinese (traditional)'}

tweet_keys = [
    u'quote_count', u'contributors', u'truncated', u'text', u'is_quote_status', u'in_reply_to_status_id',
    u'reply_count', u'id', u'favorite_count', u'entities', u'retweeted', u'coordinates', u'timestamp_ms',
    u'source', u'in_reply_to_screen_name', u'id_str', u'retweet_count', u'in_reply_to_user_id', u'favorited',
    u'retweeted_status', u'user', u'geo', u'in_reply_to_user_id_str', u'lang', u'created_at', u'filter_level',
    u'in_reply_to_status_id_str', u'place']


class SListener(StreamListener):

    def __init__(self, api=None, fprefix='/root/SHARED/Tweets/'):
        self.buffer_size = int(3 * 1e6)
        self.api = api or API()
        self.counter = 0
        self.fprefix = fprefix
        self.output = codecs.open(self.fprefix + datetime.now().strftime("%Y%b%a%d-%H_%M_%S_%f") + '.json',
                                  mode='w',
                                  buffering=self.buffer_size)
        self.delout = open('delete.txt', 'a')
        self.languages = []

    def on_data(self, data):

        raw_tweet = json.loads(data)

        if 'delete' in raw_tweet.keys():
            delete = raw_tweet['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False

        elif 'limit' in raw_tweet.keys():
            if self.on_limit(raw_tweet['limit']['track']) is False:
                return False

        elif 'warning' in raw_tweet.keys():
            warning = raw_tweet['warnings']
            print ct("[ ", YELLOW) + ct(warning['message'], RED) + ct(" ]", Yellow)
            return False

        elif 'text' in raw_tweet.keys():
            _space = 20 - len(raw_tweet['user']['screen_name'])
            _counter = ct('[ ', GREEN) + str(self.counter) + ct(' ]', GREEN)
            _time = ct('[ ', GREEN) + ct(raw_tweet['created_at'].split(' ')[3].encode("utf-8", 'replace'), WHITE) + ct(' ]', GREEN)
            _user = ct(raw_tweet['user']['screen_name'].encode("utf-8", 'replace'), MAGENTA)
            if raw_tweet['lang'] in langs.keys():
                
                _lang = ct('[ ', GREEN) + ct(langs[raw_tweet["lang"]], YELLOW) + ct(' ]', GREEN)
            else:
                _lang = ct('[ ', YELLOW) + ct("UNKNOWN", RED) + ct(' ]', YELLOW)
            
            _text = ct(raw_tweet['text'].encode("utf-8", 'replace'), CYAN)
            _message = _counter + "\t" + _time + " " + _lang + "\t" + ct(' @ ', BLUE) + _user + " " * _space + " : " + _text
            print _message.replace("\n", "")
            self.output.write(data + '\n')

        self.counter += 1
        if self.counter >= 300:
            # sys.exit()
            self.output.close()
            self.output = codecs.open(self.fprefix + datetime.now().strftime("%Y%b%a%d-%H_%M_%S_%f") + '.json',
                                      mode='w',
                                      buffering=self.buffer_size)
            oldcounter = self.counter
            self.counter = 0

            os.system('cat ~/SHARED/filesaved.txt')
            sys.stderr.write('\n     ----------------------------\n')
            sys.stderr.write(' --> [RESET COUNTER] : From [' +
                             str(oldcounter) + '] To [' + str(self.counter) + ']\n')
            sys.stderr.write(' --> [SAVED FILE]\n')
            sys.stderr.write(' --> [NEW FILE] : ' + self.fprefix +
                             datetime.now().strftime("%Y%b%a%d-%H_%M_%S_%f") + '.json\n')
            

            with open("/root/SHARED/tweetspy/kill.txt", "r") as ktxt:
                f = ktxt.readlines()
                if f[0] == '0\n':
                    if raw_input("\n --> Do you want to kill? yes/NO :" in ["Y", "y", "YES", "Yes", "yes"]):
                        sys.stderr.write(" --> KILLED\n")
                        sys.stderr.write('     ----------------------------\n')
                        sys.exit(0)
                    else:
                        sys.stderr.write(" --> NOT KILLED\n")

            sys.stderr.write('     ----------------------------\n')
        return

    def on_delete(self, status_id, user_id):
        del_msg = ct("[ ", YELLOW) + ct("DELETE " + str(status_id), RED) + ct(" ]", YELLOW)
        _counter = ct('[ ', GREEN) + str(self.counter) + ct(' ]', GREEN)
        # _time = ct('[', GREEN) + ct(raw_tweet['created_at'].split(' ')[3].encode("utf-8", 'replace'), WHITE) + ct(']  ', GREEN)
        print _counter + "\t" + del_msg
        self.delout.write(str(status_id) + "\n")
        return

    def on_limit(self, track):
        lim_msg = ct("[ ", YELLOW) + ct("LIMIT " + str(track), RED) + ct(" ]", YELLOW)
        _counter = ct('[ ', GREEN) + str(self.counter) + ct(' ]', GREEN)
        # _time = ct('[', GREEN) + ct(raw_tweet['created_at'].split(' ')[3].encode("utf-8", 'replace'), WHITE) + ct(']  ', GREEN)
        print _counter + "\t" + lim_msg
        return

    def on_error(self, status_code):
        sys.stderr.write('Error: ' + str(status_code) + "\n")
        return False

    def on_timeout(self):
        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)

        return
