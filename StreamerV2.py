# ====================================================================
# Author 				: swc21
# Date 					: 2018-03-14 09:40:57
# Project 				: ClusterFiles
# File Name 			: StreamerV2
# Last Modified by 		: swc21
# Last Modified time 	: 2018-03-14 11:07:40
# ====================================================================
#
# SOl Courtney Columbia U Department of Astronomy and Astrophysics NYC 2016
# swc2124@columbia.edu
#--[DESCRIPTION]---------------------------------------------------------#
'''
Date: May 2016
Handeler for twitter stream
'''
#--[PROGRAM-OPTIONS]------------------------------------------------------#
import os
import tweepy

from slistener import SListener
from time import gmtime
from time import sleep
from time import strftime
from tweepy import API
from tweepy import OAuthHandler
from tweepy import Stream
#--[PROGRAM-OPTIONS]------------------------------------------------------#
os.system('clear')
# if __name__ == '__main__':
Track = []
access_token = "631011579-NzyCtmF6bvAawqQ25dPfNe4jy7q7hA8bdjn5tddO"
access_token_secret = "LFrAMsOwi0xouD3xCGK0xGemHhrKl9OiQLFLmWDRc4dzD"
consumer_key = "K9MLJepL4Ojk2gxzxbTYAwZVT"
consumer_secret = "ntj2kjxbZeiMGWdTRnPNqB72gwppRTH5y35zUGgUyDIsz6OkKd"
print '\n-----------------------------------------------------------------------'
print 'setting up stream feed  : '+strftime("%Y_%m_%d_%H_%M_%S", gmtime())
print 'access_token         : '+access_token
print 'access_token_secret  : '+access_token_secret
print 'consumer_key         : '+consumer_key
print 'consumer_secret  : '+consumer_secret
print '-----------------------------------------------------------------------\n'
print 'attempting to start stream..'
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)
l = SListener(api=api)
try:
    print 'starting now'
    try:
        Stream(auth, l).filter(languages=["en"], track=[
            "a", "the", "I", "you", "u", 'THE', 'i'], async=True)
    except ProtocolError, e:
        print e
        Stream(auth, l).filter(languages=["en"], track=[
            "a", "the", "I", "you", "u", 'THE', 'i'], async=True)
except KeyboardInterrupt:
    stream.disconnect()
    print 'stream dissonected'
    raise
