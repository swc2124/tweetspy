"""[summary]

[description]

"""

import os
import sys
import json
from datetime import datetime
import tweepy
from colorama import init

init()

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

def ct(text, colour=WHITE):
    seq = "\x1b[1;%dm" % (30 + colour) + text + "\x1b[0m"
    return seq

def tstamp():
    return str(datetime.now().timestamp()).replace(".", "_")

def filehandle(pth, ext="JSON"):
    return os.path.join(pth, tstamp() + ext)

keep_columns = [
    'created_at', 'description', 'followers_count',
    'friends_count', 'geo_enabled', 'id', 'id_str',
    'lang', 'location', 'name', 'profile_image_url',
    'profile_image_url_https', 'protected',
    'screen_name', 'statuses_count', 'time_zone',
    'url', 'verified']

def prep_tweet(tweet, keep_cols=keep_columns):
    user_data = {}
    text = tweet["text"]
    for key in list(tweet["user"].keys()):
        if key in keep_cols:
            user_data[key] = tweet["user"][key]
            # print(key, ":", tweet["user"][key])
    return text, user_data

class TweetspyStreamListener(tweepy.StreamListener):

    def __init__(self, cfg, db):
        super(TweetspyStreamListener, self).__init__()
        self.count_good = 0
        self.count_bad = 0
        self.save_dir =  cfg.get("path", "new_tweets_dir")
        self.ext = os.path.extsep + 'JSON'
        self.db = db

    def on_data(self, data):
        spaces = 25
        tweet = json.loads(data)

        if not "user" in list(tweet.keys()):
            return True

        screen_name = tweet["user"]["screen_name"]
        location = tweet["user"]["location"]
        
        user_tag = {"screen_name": screen_name}
        if not self.db.people.find_one(user_tag):
            try:
                self.db.people.insert_one(user_tag)
            except Exception as err:
                print(err)
            else:
                name_clr = RED
        else:
            name_clr = CYAN
        try:
            self.db[screen_name].insert_one(tweet)
        except Exception as err:
            print(err)
        if not location:
            loc_clr = YELLOW
        else:
            loc_clr = GREEN
        spc = " " * (spaces - len(screen_name))
        msg = "\n" + ct(screen_name, name_clr) + spc + ct(str(location), loc_clr)
        sys.stdout.write(msg)
        sys.stdout.flush()
        if self.count_good > 1e5:
            return False
        self.count_good += 1
        return True

    def on_error(self, status):
        self.count_bad += 1
        print("Error:", status)
        return True

    def on_exception(self, exception):
        print(exception)
        return True




