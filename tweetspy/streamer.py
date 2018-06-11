
""""
[description]

"""
from __future__ import print_function

from tweepy import OAuthHandler
from tweepy import Stream

from slistener import TweetspyStreamListener as TSL

from tweetspy_lib import get_auth
from tweetspy_lib import logging
from tweetspy_lib import tstamp

if __name__ == '__main__':

    # Get all 4 authorization values from helper library function.
    con_key, con_sec, acc_tok, acc_sec = get_auth()

    # Set the authorization handler.
    auth = OAuthHandler(con_key, con_sec)

    # Set access token and secret.
    auth.set_access_token(acc_tok, acc_sec)

    # Initialize the stream object.
    stream = Stream(auth, TSL())

    # Begin the filtered stream
    stream.filter(track=["a", "i", "#"], async=True)

    # Log completion.
    logging.info(tstamp() + "<END - streamer.py> ")
