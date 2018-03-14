# ============================================================================
# Author                : swc21
# Date                  : 2018-03-14 11:22:31
# Project               : GitHub
# File Name             : slistener
# Last Modified by      : swc21
# Last Modified time    : 2018-03-14 12:36:48
# ============================================================================
# 

import json
import os
import sys

from time import gmtime
from time import sleep
from time import strftime
from tweepy import StreamListener

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)


def ct(text, colour=WHITE):
    seq = "\x1b[1;%dm" % (30+colour) + text + "\x1b[0m"
    return seq


class SListener(StreamListener):
    def __init__(self, api=None, fprefix='/root/SHARED/Tweets/'):
        self.api = api or API()
        self.counter = 0
        self.fprefix = fprefix
        self.output = open(fprefix+strftime("%Y%b%a%d-%H%M%S",
                                            gmtime())+'.json', 'w', int(10*1e6))
        self.delout = open('delete.txt', 'a')

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
            time = ct('['+raw_tweet['created_at'].split(' ')[3]+']  ', WHITE)
            fillin = (ct(raw_tweet['user']['screen_name'], WHITE), ct(
                raw_tweet['text'].encode('ascii', 'ignore').replace('\n', ' '), CYAN))
            sys.stderr.write(
                '\n '+ct('['+str(self.counter)+']', GREEN)+'    '+time+ct('@ ', CYAN)+'%s: %s' % fillin)
            self.output.write(data+'\n')
        self.counter += 1
        if self.counter >= 200:
            self.output.close()
            self.output = open(
                self.fprefix+strftime("%Y%b%a%d-%H%M%S", gmtime())+'.json', 'w', int(10*1e6))
            oldcounter = self.counter
            self.counter = 0
            os.system('cat ~/SHARED/filesaved.txt')
            sys.stderr.write('\n     ----------------------------\n')
            sys.stderr.write(
                ' --> [RESET COUNTER] : From ['+str(oldcounter)+'] To ['+str(self.counter)+']\n')
            sys.stderr.write(' --> [SAVED FILE]\n')
            sys.stderr.write(' --> [NEW FILE] : '+self.fprefix +
                             strftime("%Y%b%a%d-%H%M%S", gmtime())+'.json\n')
            sys.stderr.write('     ----------------------------\n')
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
