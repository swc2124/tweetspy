

from tweepy import StreamListener
from time import gmtime, strftime, sleep
import json
import sys
import os

import codecs
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)


def ct(text, colour=WHITE):

    seq = "\x1b[1;%dm" % (30 + colour) + text + "\x1b[0m"

    return seq


langs = {'ar': 'Arabic', 'bg': 'Bulgarian', 'ca': 'Catalan', 'cs': 'Czech', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish', 'et': 'Estonian',
         'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French', 'hi': 'Hindi', 'hr': 'Croatian', 'hu': 'Hungarian', 'id': 'Indonesian', 'is': 'Icelandic', 'it': 'Italian', 'iw': 'Hebrew',
         'ja': 'Japanese', 'ko': 'Korean', 'lt': 'Lithuanian', 'lv': 'Latvian', 'ms': 'Malay', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian',
         'ru': 'Russian', 'sk': 'Slovak', 'sl': 'Slovenian', 'sr': 'Serbian', 'sv': 'Swedish', 'th': 'Thai', 'tl': 'Filipino', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu',
         'vi': 'Vietnamese', 'zh_CN': 'Chinese (simplified)', 'zh_TW': 'Chinese (traditional)'}

tweet_keys = [
    u'quote_count', u'contributors', u'truncated', u'text', u'is_quote_status', u'in_reply_to_status_id',
    u'reply_count', u'id', u'favorite_count', u'entities', u'retweeted', u'coordinates', u'timestamp_ms',
    u'source', u'in_reply_to_screen_name', u'id_str', u'retweet_count', u'in_reply_to_user_id', u'favorited',
    u'retweeted_status', u'user', u'geo', u'in_reply_to_user_id_str', u'lang', u'created_at', u'filter_level',
    u'in_reply_to_status_id_str', u'place']


class SListener(StreamListener):

    def __init__(self, api=None, fprefix='/root/SHARED/Tweets/'):

        self.api = api or API()

        self.counter = 0

        self.fprefix = fprefix

        self.output = codecs.open(fprefix + strftime("%Y%b%a%d-%H%M%S",
                                              gmtime()) + '.json', mode='w', buffering=int(10 * 1e6))

        self.delout = open('delete.txt', 'a')

        self.languages = []


    def on_data(self, data):

        raw_tweet = json.loads(data)

        if 'delete' in raw_tweet.keys():

            delete = json.loads(data)['delete']['status']

            if self.on_delete(delete['id'], delete['user_id']) is False:

                return False

        elif 'limit' in raw_tweet.keys():

            if self.on_limit(json.loads(data)['limit']['track']) is False:

                return False

        elif 'warning' in raw_tweet.keys():

            warning = json.loads(data)['warnings']

            print warning['message']

            return False

        elif 'text' in raw_tweet.keys():

            try:
                time = ct(
                    '[' + raw_tweet['created_at'].split(' ')[3] + ']  ', WHITE)

                fillin = (
                    raw_tweet['user']['screen_name'].encode("utf-8", 'replace'), 
                    raw_tweet['text'].encode("utf-8", 'replace'))

                sys.stderr.write('\n ' + '[' + str(self.counter) + ']' + '  ' + time + '@ '+ '%s: %s' % fillin)

                self.output.write(data + '\n')
            
            except UnicodeDecodeError, e:
                raw_tweet['text'].encode("utf-8", 'replace')
        

        self.counter += 1

        if self.counter >= 300:

            sys.exit(0)

            self.output.close()

            self.output = open(
                self.fprefix + strftime("%Y%b%a%d-%H%M%S", gmtime()) + '.json', 'w', int(10 * 1e6))

            oldcounter = self.counter

            self.counter = 0

            os.system('cat ~/SHARED/filesaved.txt')

            sys.stderr.write('\n     ----------------------------\n')

            sys.stderr.write(' --> [RESET COUNTER] : From [' +
                             str(oldcounter) + '] To [' + str(self.counter) + ']\n')

            sys.stderr.write(' --> [SAVED FILE]\n')

            sys.stderr.write(' --> [NEW FILE] : ' + self.fprefix +
                             strftime("%Y%b%a%d-%H%M%S", gmtime()) + '.json\n')

            sys.stderr.write('     ----------------------------\n')

        return

    def on_delete(self, status_id, user_id):

        self.delout.write(str(status_id) + "\n")

        return

    def on_limit(self, track):

        sys.stderr.write('limit' + str(track) + "\n")

        return

    def on_error(self, status_code):

        sys.stderr.write('Error: ' + str(status_code) + "\n")

        return False

    def on_timeout(self):

        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")

        time.sleep(60)

        return
