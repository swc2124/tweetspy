#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from tweepy import StreamListener
from tweepy import Stream
from time import gmtime, strftime, sleep
import json
import sys
import os
from tweepy import Stream, OAuthHandler, API

from time import gmtime,strftime,sleep

import os, tweepy

import codecs
from kitchen.text.converters import getwriter
UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)


def ct(text, colour=WHITE):

    seq = "\x1b[1;%dm" % (30 + colour) + text + "\x1b[0m"

    return seq

class SListener(StreamListener):

    def __init__(self, api=None, fprefix='./'):
        self.api = api or API()
        self.counter = 0


    def on_data(self, data):
        raw_tweet = json.loads(data)

        types = []
        for key in raw_tweet.keys():

            print "\n", ct("[" + key + "]", GREEN)

            _typ = type(raw_tweet[key])

            if _typ == dict:
                for sub_key in raw_tweet[key]:
                    types.append((key, _typ, type(raw_tweet[key][sub_key])))
                    print " --> ", ct("[" + sub_key + "]", BLUE), type(raw_tweet[key][sub_key])
            else:
                types.append((key, _typ))
                print " --> ", type(raw_tweet[key])

        """
        if 'text' in raw_tweet.keys():
            try:
                time = '[' + raw_tweet['created_at'].split(' ')[3] + ']  '

                fillin = (
                    raw_tweet['user']['screen_name'].decode("utf-8", 'replace'), 
                    raw_tweet['text'].decode("utf-8", 'replace'))

                print '[' + str(self.counter) + ']' + '  ' + time + '@ '+ '%s: %s' % fillin
            
            except UnicodeDecodeError, e:
                print raw_tweet['text']
            except UnicodeEncodeError as e:
                print raw_tweet['text']
        """
        self.counter += 1
        if self.counter >= 1:
            print types
            Stream.disconnect()


access_token = "631011579-NzyCtmF6bvAawqQ25dPfNe4jy7q7hA8bdjn5tddO"
access_token_secret = "LFrAMsOwi0xouD3xCGK0xGemHhrKl9OiQLFLmWDRc4dzD"
consumer_key = "K9MLJepL4Ojk2gxzxbTYAwZVT"
consumer_secret = "ntj2kjxbZeiMGWdTRnPNqB72gwppRTH5y35zUGgUyDIsz6OkKd"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)
l = SListener(api=api)

ru_words = ["Лидочка", "Lidochka", "sonny", "солнечно", "odie", "Оди", "мой", "я", "с", "в", "Кот", "собака"]

try:
    Stream(auth,l).filter(track=[x.decode("utf-8") for x in ru_words],async=True)
except KeyboardInterrupt, e:
    Stream.disconnect()

