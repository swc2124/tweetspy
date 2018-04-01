#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# SOl Courtney Columbia U Department of Astronomy and Astrophysics NYC 2016
# swc2124@columbia.edu

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

#--[DESCRIPTION]-------------------------------------------------------------#

'''
Date: May 2016

Handeler for twitter stream
'''

#--[IMPORTS]-----------------------------------------------------------------#

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


#--[PROGRAM-OPTIONS]---------------------------------------------------------#

UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

ru_words = ["Лидочка", "солнечно", "odie", "Оди", 
            "мой", "я", "с", "в", "Кот", "собака"]

name_words = [ "odie", "Lidochka", "sonny"]

en_words = ["a", "the", "with", "I", "my"]

all_lists = [ru_words, name_words, en_words]

Track = []
for wrd_list in all_lists:
    for _wrd in wrd_list:
        Track.append(_wrd.decode("utf-8"))


access_token = "631011579-NzyCtmF6bvAawqQ25dPfNe4jy7q7hA8bdjn5tddO"
access_token_secret = "LFrAMsOwi0xouD3xCGK0xGemHhrKl9OiQLFLmWDRc4dzD"
consumer_key = "K9MLJepL4Ojk2gxzxbTYAwZVT"
consumer_secret = "ntj2kjxbZeiMGWdTRnPNqB72gwppRTH5y35zUGgUyDIsz6OkKd"

print('\n-------------------------------------------------------------------')
print('setting up stream feed\t:\t' + strftime("%Y_%m_%d_%H_%M_%S", gmtime()))
print('access_token\t\t\t:\t' + access_token)
print('access_token_secret\t:\t' + access_token_secret)
print('consumer_key\t\t:\t' + consumer_key)
print('consumer_secret\t:\t' + consumer_secret)
print('-------------------------------------------------------------------\n')
print('attempting to start stream..')

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)
l = SListener(api=api)

try:

    os.system('clear')
    print('starting now')
    Stream(auth, l).filter(track=Track, async=True)

except KeyboardInterrupt, e:

    Stream.disconnect()
    print('stream dissonected')
    raise
