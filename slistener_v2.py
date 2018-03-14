# ====================================================================
# Author 				: swc21
# Date 					: 2018-03-14 09:40:57
# Project 				: ClusterFiles
# File Name 			: slistener_v2
# Last Modified by 		: swc21
# Last Modified time 	: 2018-03-14 11:07:41
# ====================================================================
#
import json
import os
import sys
import threading

from time import gmtime
from time import sleep
from time import strftime
from tweepy import StreamListener


class SListener(StreamListener):
    def __init__(self, api=None, fprefix='SHARED/Tweets/'):
        self.api = api or API()
        self.counter = 0
        self.fprefix = fprefix
        self.output = open(fprefix+strftime("%Y%b%a%d-%H%M%S",
                                            gmtime())+'.json', 'w', int(10*1e6))
        self.delout = open('delete.txt', 'a')

    def on_data(self, data):
        if 'in_reply_to_status' in data:
            self.on_status(data)
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'limit' in data:
            if self.on_limit(json.loads(data)['limit']['track']) is False:
                return False
        elif 'warning' in data:
            warning = json.loads(data)['warnings']
            print warning['message']
            return False

    def on_data(self, data):
        def FUNCTIN(self, data):
            raw_tweet = json.loads(data)
            if 'text' in raw_tweet.keys():
                sys.stderr.write('\n['+str(self.counter)+']	'+'@%s: %s' % (
                    raw_tweet['user']['screen_name'], raw_tweet['text'].encode('ascii', 'ignore')))
            self.output.write(data+'\n')
            self.counter += 1
            # sleep(0.005)
            if self.counter >= 1000:
                os.system('clear')
                sys.stderr.write(' --> [SAVED FILE] \n')
                self.output.close()
                self.output = open(
                    self.fprefix+strftime("%Y%b%a%d-%H%M%S", gmtime())+'.json', 'w', int(10*1e6))
                sys.stderr.write(
                    ' --> [NEW FILE] : '+self.fprefix+strftime("%Y%b%a%d-%H%M%S", gmtime())+'.json\n')
                oldcounter = self.counter
                self.counter = 0
                sys.stderr.write(
                    ' --> [RESET COUNTER] : From ['+str(oldcounter)+'] To ['+str(self.counter)+']\n')
                sleep(2)
            return
        t = threading.Thread(target=FUNCTIN, args=(self, data))
        t.start()
        return

    def on_delete(self, status_id, user_id):
        self.delout.write(str(status_id) + "\n")
        return

    def on_limit(self, track):
        sys.stderr.write('limit'+str(track)+"\n")
        return

    def on_error(self, status_code):
        sys.stderr.write('Error: ' + str(status_code) + "\n")
        return False

    def on_timeout(self):
        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)
        return
