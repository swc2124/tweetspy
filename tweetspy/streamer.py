
""""
[description]

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from configparser import ConfigParser as cpar

from tweepy import OAuthHandler
from tweepy import Stream

from pymongo import MongoClient

from slistener import TweetspyStreamListener as TSL



if __name__ == '__main__':

    config = cpar()
    config.read("tweetspy.ini")

    con_key = config.get("streamer", "consumer_key")
    con_sec = config.get("streamer", "consumer_secret")
    acc_tok = config.get("streamer", "access_token")
    acc_sec = config.get("streamer", "access_token_secret")

    auth = OAuthHandler(con_key, con_sec)
    auth.set_access_token(acc_tok, acc_sec)

    mongodb_host = config.get("streamer", "mongodb_host")
    mongodb_port = config.getint("streamer", "mongodb_port")
    client = MongoClient(host=mongodb_host, port=mongodb_port)
    db = client["twitter"]

    stream = Stream(auth, TSL(config, db))

    try:
        stream.filter(track=["a","i","#"], async=True)
    except Exception as err:
        print(err)