"""
--------------------------
The Package Library Module
--------------------------

The individual scripts in this package require many functions to perform their
tasks.  Each script imports its functions from this library module.

In the future this single module could be broken into sub modules for sake of
organization.

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import sys
import os
import socket
from datetime import datetime
from configparser import ConfigParser as cpar
from configparser import ExtendedInterpolation

from colorama import init

from pymongo import MongoClient


# ========================================================================== #
# DEFINITIONS

# Null values.
twitterdb = None

# Configuration file handle.
config_fh = "tweetspy.ini"

# Read in the configuration file.  File handle is set here but it's not the
# way it should be done.
config = cpar()
config._interpolation = ExtendedInterpolation()
config.read(config_fh)

# Get the absolute path to the config file and stash it into the config object
# so we can update the configuration file in real time.
conf_abpath = os.path.abspath(config_fh)
config.set('path', 'config_file', value=conf_abpath)

# This will need to come from a text file.  A function can read that file and
# return a list of column names to keep.
keep_columns = [
    'created_at', 'description', 'followers_count',
    'friends_count', 'geo_enabled', 'id', 'id_str',
    'lang', 'location', 'name', 'profile_image_url',
    'profile_image_url_https', 'protected',
    'screen_name', 'statuses_count', 'time_zone',
    'url', 'verified'
]

# Colors.
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

# Streamer configuration values.
check_in_interval = config.getint("streamer", "check_in_interval")

# ========================================================================== #
# LOGGING

# Log file info from configuration file.
log_fh = config.get("logging", "log_filehandle")

# Extract the integer value for the logging level.
log_level = getattr(logging, config.get("logging", "log_level").upper(), None)

# Call the logging file object.
logging.basicConfig(filename=log_fh, level=log_level)

# ========================================================================== #
# FUNCTIONS
# <general purpose> -------------------------------------------------------- #


def ct(text, colour=WHITE):
    """The text coloring function for all standard out color text.

    """
    seq = "\x1b[1;%dm" % (30 + colour) + text + "\x1b[0m"
    return seq


def tstamp(mode="log"):
    """The time-stamping function for all time time-stamping.

    """
    if mode == "fh":
        return str(datetime.now().timestamp()).replace(".", "_")
    elif mode == "log":
        return str("[" + datetime.now().ctime() + "]")
    else:
        pass


def filehandle(pth, ext="JSON"):
    """The file handle making function for all file handle creations.

    """
    return os.path.join(pth, tstamp("fh") + os.path.extsep + ext)


def get_ip_and_port():
    """The network information function.

    """
    s = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_DGRAM,
        proto=0,
        fileno=None)
    s.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_BROADCAST, 1)
    s.connect(
        ('<broadcast>', 0))
    ip, port = s.getsockname()
    s.shutdown(socket.SHUT_RDWR)
    s.close()
    return ip, port

# <mongo_db> --------------------------------------------------------------- #


def get_mongo_host_port():
    """Returns the host and port of the Mongo DB.

    """
    host = config.get("mongo", "mongodb_host")
    port = config.getint("mongo", "mongodb_port")
    return host, port

# <streamer.py> ------------------------------------------------------------ #


def get_auth():
    """This way the configuration file is only in the lib and not called in
    the scripts.

    """
    con_key = config.get("streamer", "consumer_key")
    con_sec = config.get("streamer", "consumer_secret")
    acc_tok = config.get("streamer", "access_token")
    acc_sec = config.get("streamer", "access_token_secret")
    return con_key, con_sec, acc_tok, acc_sec

# <slistener.py> ----------------------------------------------------------- #


def new_stream_file():
    fh = filehandle(config.get("path", "new_tweets_dir"), ext="txt")
    n_tweets = config.getint("streamer", "n_tweets_per_file")
    n_bytes = config.getint("streamer", "n_bytes_per_tweet")
    buf_size = n_bytes * n_tweets
    return open(fh, mode="w", buffering=buf_size)


def save_rawtweets(tweets, ext="JSON"):
    dir_path = config.get('path', 'new_tweets_dir')
    fh = filehandle(dir_path, ext=ext)
    with open(fh, mode="w", buffering=2048) as f:
        for rtweet in tweets:
            f.write(rtweet)


def process_tweet(tweet, db, keep_cols=keep_columns):
    """This is how the system ingests a tweet into the database.

    """

    spaces = 25
    screen_name = tweet["user"]["screen_name"]
    location = tweet["user"]["location"]
    location_tag = {"location": location}
    user_tag = {"screen_name": screen_name}
    if not db.people.find_one(user_tag):
        try:
            db.people.insert_one(user_tag)
        except Exception as err:
            print(err)
        else:
            name_clr = BLACK
    else:
        name_clr = CYAN

    if location is not None and location != "None":

        if not db.location.find_one(location_tag):

            try:

                db.location.insert_one(location_tag)
            except Exception as err:
                print(err)
            else:
                loc_clr = BLACK
        else:
            loc_clr = GREEN
    else:
        loc_clr = BLACK

    # Make the message & print it.
    spc = " " * (spaces - len(screen_name))
    msg = "\n" + ct(screen_name, name_clr) + spc + ct(str(location), loc_clr)
    sys.stdout.write(msg)
    sys.stdout.flush()


# ========================================================================== #
# OPERATIONS

if __name__ == "tweetspy_lib":
    print(sys.version)
    print(__name__, "has been imported.")

    # This is for color output on windows machines.
    init()

    # Setup the MongoDB.
    mongodb_host, mongodb_port = get_mongo_host_port()
    client = MongoClient(host=mongodb_host, port=mongodb_port)

    # This is the database for everything.
    twitterdb = client["twitter"]

elif __name__ == "__main__":
    print("__main__:", __name__)

else:
    pass
