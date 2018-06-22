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

import json
import logging
import os
import psutil
import requests
import socket
import sys

from datetime import datetime
from datetime import timezone
from time import sleep

from math import log as math_log

from configparser import ConfigParser as cpar
from configparser import ExtendedInterpolation

from country_list import countries_for_language
from langdetect import detect
from langdetect import lang_detect_exception

from nltk import tokenize as token
from nltk.corpus import stopwords

from colorama import init

from pymongo import MongoClient


# [DEFINITIONS] ============================================================= #
#
#

# [FUNCTIONS] =============================================================== #
#
#
# ------------------------------------------------------ <configuration file> #

# Configuration file handle.
config_fh = "../tweetspy.ini"

# Read in the configuration file.  File handle is set here but it's not the way
# it should be done.
config = cpar()
config._interpolation = ExtendedInterpolation()
config.read(config_fh)

# Get the absolute path to the config file and stash it into the config object
# so we can update the configuration file in real time.
conf_abpath = os.path.abspath(config_fh)
config.set('path', 'config_file', value=conf_abpath)

# Streamer configuration values.
check_in_interval = config.getint("streamer", "check_in_interval")


class ConfigurationOptions(object):
    """docstring for ConfigurationOptions"""
    def __init__(self, arg):
        super(ConfigurationOptions, self).__init__()
        self.arg = arg


def reload_config(config_file):

    config_file.read(config_file.get('path', 'config_file'))


def get_config(cfg_file=config):

    reload_config(config_file=cfg_file)

    return cfg_file


# --------------------------------------------------------- <general purpose> #

# Colors.
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

def ct(text, colour=WHITE):
    """The text coloring function for all standard out color text.

    """
    seq = "\x1b[1;%dm" % (30 + colour) + text + "\x1b[0m"
    return seq


def standard_path(fname="", path_type=None, rc=config):
    """This is how we assemble and verify absolute paths.

    Returns False if the path doesn't work.

    """
    # Get the absolute path to a raw tweet file via `fname`.  This is a file
    # written by the streamer to the shared file system containing tweets in
    # the form of binary data.
    if path_type == "tweet":
        target_dir = rc.get("path", "new_tweets_dir")
        target_path = os.path.join(target_dir.encode("UTF-8"), fname)
        return os.path.normpath(target_path)

    elif path_type == "logfile":
        target_path = os.path.join(
            rc.get("path", "log_dir"),
            fname)
        return os.path.normpath(target_path)

    else:
        raise TypeError("need to specify `path_type`")


def list_tweetdir(revrs=True, encoding="UTF-8", conf=config):

    # Get the directory path.
    tweet_dir = conf.get('path', 'new_tweets_dir')

    # Get the file handle extension for the relevant files.
    fh_ext = conf.get("streamer", "fh_ext")

    # Find and return the number of relevant files in the directory.
    tweets = os.listdir(tweet_dir)
    files = [fh.encode(encoding) for fh in tweets if fh.endswith(fh_ext)]
    if files:
        files.pop()
        files.sort(reverse=revrs)

    return files


def nearestpoweroftwo(num):
    """Helper function to find the next higher power of 2 to a given number.
    Such that the power of two is the smallest power of two larger than the
    supplied number.

    Helps find correct buffer sizes in bytes.

    Parameters
    ----------
    num : {int}
        The number of bytes for which you wish to find the smallest power of 2
        larger than.
        2 -> 4
        4 -> 8
        7 -> 8

    Returns
    -------
    int
        The integer value of the nearest power of two larger than num.

    """
    return pow(2, int(math_log(num, 2) + 1))


def tstamp(mode="log"):
    """The time-stamping function for all time time-stamping.

    """
    # For new stream cache files.
    if mode == "fh":
        return str(datetime.now().timestamp()).replace(".", "_")

    # For a log entry.
    elif mode == "log":
        log_d_frmt = config.get("logging", "t_frmt")
        return datetime.datetime.now().strftime(log_d_frmt)

    # For a new log file.
    elif mode == "log_fh":
        log_fh_frmt = config.get("logging", "fh_frmt")
        return datetime.datetime.now().strftime(log_fh_frmt)

    # For a database entry.
    elif mode == "db":
        db_d_frmt = config.get("mongo", "t_frmt")
        return datetime.now(timezone.utc).strftime(db_d_frmt)

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
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 0)
    s.connect(('<broadcast>', 0))
    ip, port = s.getsockname()
    s.shutdown(socket.SHUT_RDWR)
    s.close()
    return ip, port


def read_tweetfile(tweet_fh, config_file=config):

    # A list to put each tweet into.
    raw_tweets = []

    try:
        # Open the provided file handle.
        with open(tweet_fh, "rb") as rawfile:
            # Separate each tweet.
            for raw_tweet in rawfile.readlines():
                # Put tweet into list.
                raw_tweets.append(raw_tweet)

    except FileNotFoundError as err:
        print("<caught><exception>", err)

    # Remove this file from the shared file system.
    # TODO : Set attempt limit in configuration file.
    while os.path.isfile(tweet_fh):

        try:
            os.remove(tweet_fh)

        except Exception as err:
            print("<caught><exception>", err)
            # TODO : move timeout to configuration file
            sleep(1)


    print("<file handle removed>", tweet_fh)
    return raw_tweets


# ----------------------------------------------------------------- <logging> #
# Maybe make an object for logging too. That way the log could be better
# formatted and all parameters would be in one place.

#
log_fh = tstamp(mode="log_fh")

#
logfile_path = standard_path(fname=log_fh, path_type="logfile")

#
if os.path.isfile(logfile_path):
    lf_mode = "a"
else:
    lf_mode = "w"

#
logging.basicConfig(
    filename=logfile_path,
    filemode=lf_mode,
    format=config.get("log", "format"),
    datefmt=config.get("log", "datefmt"),
    style=config.get("log", "{"),
    level=config.get("log", "level")
)

def log(name):
    return logging.getLogger(name)



# ------------------------------------------------------------------ <stdout> #
# This is where all standard out reporting should be handled so there is a
# consistency in the format of reporting.  At the moment there are print
# statements and sys.stdout.write statements peppered all over the place.


def stdout(message, level="INFO", options=[]):
    """TODO

    [description]

    Parameters
    ----------
    message : {[type]}
        [description]
    level : {str}, optional
        [description] (the default is "INFO", which [default_description])
    options : {list}, optional
        [description] (the default is [], which [default_description])

    """
    pass


# ---------------------------------------------------------------- <mongo_db> #


def get_mongo_host_port(config_file=config):
    """Returns the host and port of the Mongo DB.

    """
    host = config_file.get("mongo", "mongodb_host")
    port = config_file.getint("mongo", "mongodb_port")
    return host, port


def get_mongodb(database):

    # Setup the MongoDB client.
    mongodb_host, mongodb_port = get_mongo_host_port()

    client = MongoClient(
        host=mongodb_host,
        port=mongodb_port,
        # document_class=dict,
        tz_aware=True,
        # connect=True,
        # maxPoolSize=200,
        # minPoolSize=0,
        # maxIdleTimeMS=None,
        # socketTimeoutMS=None,
        # connectTimeoutMS=None,
        appname="tweetspy",
        # event_listeners=[]
    )
    client.admin.command('ismaster')

    # If the database is valid, then return the requested database.
    # TODO client.list_databases()
    return client[database]


def insert_tweetfile(preped_tweets, collection):

    db = get_mongodb("twitter")

    tweetdb = db[collection]

    # insert into db.
    result = tweetdb.insert_many(preped_tweets)
    n_inserted = len(result.inserted_ids)
    acc = result.acknowledged
    print("<tweets inserted into db> [{}] [{}]".format(n_inserted, acc))


def insert_location(location, collection):

    db = get_mongoclient()

    tweetdb = db[collection]

    # insert into db.
    result = tweetdb.insert_one(location)
    n_inserted = len(result.inserted_ids)
    acc = result.acknowledged
    print("<tweets inserted into db> [{}] [{}]".format(n_inserted, acc))


# -------------------------------------------------------- <location manager> #

LanguageError = lang_detect_exception.LangDetectException

lang_dict = {
    'ar': 'Arabic',
    'bg': 'Bulgarian',
    'ca': 'Catalan',
    'cs': 'Czech',
    'da': 'Danish',
    'de': 'German',
    'el': 'Greek',
    'en': 'English',
    'English': 'English',
    'english': 'English',
    'eng': 'English',
    'es': 'Spanish',
    'et': 'Estonian',
    'fa': 'Persian',
    'fi': 'Finnish',
    'fr': 'French',
    'hi': 'Hindi',
    'hr': 'Croatian',
    'hu': 'Hungarian',
    'id': 'Indonesian',
    'is': 'Icelandic',
    'it': 'Italian',
    'iw': 'Hebrew',
    'ja': 'Japanese',
    'ko': 'Korean',
    'lt': 'Lithuanian',
    'lv': 'Latvian',
    'ms': 'Malay',
    'nl': 'Dutch',
    'no': 'Norwegian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'sr': 'Serbian',
    'sv': 'Swedish',
    'th': 'Thai',
    'tl': 'Filipino',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'vi': 'Vietnamese',
    'zh_CN': 'Chinese (simplified)',
    'zh_TW': 'Chinese (traditional)'
}

target_data_keys = [
    'country',
    'administrative_area_level_1',
    'administrative_area_level_2',
    'administrative_area_level_3',
    'administrative_area_level_4',
    'administrative_area_level_5',
    'locality',
    'sublocality',
    'sublocality_level_1',
    'sublocality_level_2',
    'sublocality_level_3',
    'sublocality_level_4',
    'sublocality_level_5',
    'postal_code',
    'postal_code_prefix',
    'postal_code_suffix',
]

#stop words.
stop_words = stopwords.words()


def location_manager_info(config=config):
    port = config.getint("locationmanager", "port")
    ip = config.get("locationmanager", "address")
    return (ip, port)


def location_manager_setup(config=config):

    address = location_manager_info(config)
    # Make, bind and set the socket to listen.
    svrsoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    svrsoc.bind(address)
    svrsoc.listen(config.getint("locationmanager", "n_backlog"))

    return svrsoc, socket.SHUT_RDWR, config


def process_location(from_twitter, from_web, targ_keys=target_data_keys):

    # New dictionary to return
    location_data = dict()

    # Time stamp this entry.
    location_data["db_time"] = tstamp(mode="db")

    # Add the location given by the twitter user.
    location_data['from_twitter'] = from_twitter

    # Add the formatted address from the Google query.
    location_data['formatted_address'] = from_web['formatted_address']

    # Break out each address component and keep those which are in `targ_keys`.
    # Remember that from_web['address_components'] is a list of dictionaries.
    for component in from_web['address_components']:

        # Remember that `component` is a dictionary (dict).
        # and component['types'] is a list of strings.
        for address_type in component['types']:

            # If the string is in our tarket_keys, then pull the long_name into
            # our data.
            if address_type in targ_keys:
                location_data[address_type] = component["long_name"]

    # Get the latitude and longitude.
    geo_keys = list(from_web['geometry'])
    if 'bounds' in geo_keys:
        location_data['bounds'] = from_web['geometry']['bounds']
    if 'location' in geo_keys:
        location_data['lat'] = from_web['geometry']['location']['lat']
        location_data['lng'] = from_web['geometry']['location']['lng']

    # Pull the types too.
    location_data['types'] = from_web['types']

    # And the place id.  Maybe this will be helpful later.
    location_data['place_id'] = from_web['place_id']

    # Return location data dictionary.
    return location_data


def tokenize_address(addr, lang='English', langs=lang_dict, nons=stop_words):

    if lang in list(langs):
        lang = langs[lang]

    return [
        element.lower()
        for element in token.word_tokenize(
            addr,
            language=lang,
            preserve_line=True)
        if element.isalpha() and element.lower() not in nons]


def translate_countries(lang="en"):
    try:
        return [
        country.lower()
        for country in list(dict(countries_for_language(lang)).values())]

    except Exception as err:
        return translate_countries(lang="en")


def verify_location(raw_location, config):

    en_countries = translate_countries()

    rc_sec = "locationmanager"

    # The name of the database.
    database_name = config.get(rc_sec, "db_name")
    base_url = config.get(rc_sec, "base_url")

    # The database.
    locationdb = get_mongodb(database_name)

    # Good locations from twitter collection.
    confirmed_locations = locationdb.confirmed

    # Unconfirmed locations.
    # Google sent something back that didn't resemble the search location.
    unconfirmed_locations = locationdb.unconfirmed

    # Locations from twitter which Google returned nothing.
    rejected_locations = locationdb.rejected

    good_requests = 0
    null_requests = 0
    max_requests = config.getint(rc_sec, "max_requests")
    requet_counter = config.getint(rc_sec, "total_requests")
    MIN_MATCHES = config.getint(rc_sec, "min_match")

    # Standardize the string.
    location = raw_location.lower()

    # First, define our tag for this location.
    location_tag = {"from_twitter": location}

    # Next, see if this location tag has already been successfully or
    # unsuccessfully identified.
    # If the location tag exists in the confirmed_locations database.
    result = confirmed_locations.find_one(filter=location_tag)
    if result:
        # Report.
        print(ct("[PRE-CONFIRMED]", GREEN), location, flush=True)
        return True

    result = unconfirmed_locations.find_one(filter=location_tag)
    if result:
        # Report.
        print(ct("[PRE-UNCONFIRMED]", BLACK), location, flush=True)
        return False

    ### Does not exist in the confirmed_locations database. ###

    # If the location tag exists in the rejected_locations database.
    result = rejected_locations.find_one(filter=location_tag)
    if result:
        # Report.
        print(
            ct("[PRE-REJECTED]", BLACK), ": {0}".format(location),
            flush=True)
        return False

    # Does not exist in the rejected_locations database.
    # we have never seen this location before so we will ask
    # Google.
    my_params = {"address": location} #, "key": api_key}

    # If we hit our limit of Google requests, we skip.
    if requet_counter > max_requests:
        print(
            "{4} ({0}/{1}) - {3} [{2}]".format(
                requet_counter,
                max_requests,
                ct(location, YELLOW),
                ct("skipped", MAGENTA),
                ct("Over request limit", RED)),
            flush=True)
        return False

    # Ask Google.
    # Did we find the correct location?
    MATCH = False

    # Request.
    response = requests.get(base_url, params=my_params)

    # Keep track of http requests.
    config.set(rc_sec, "total_requests", str(requet_counter + 1))

    # Convert to list of dictionaries.
    results = response.json()['results']

    # If Google has something to say.
    if results:

        # Track good requests.
        good_requests += 1

        # We want the first element of this list.
        web_location_data = results[0]

        # Process the returned location data.
        good_loc_data = process_location(
            location,
            web_location_data)
        formatted_address = good_loc_data["formatted_address"]

        try:
            _lang = detect(raw_location)
        except LanguageError as err:
            _lang = "en"

        lang = _lang
        if lang in list(lang_dict.keys()):
            lang = lang_dict[lang]

        web_elements = tokenize_address(formatted_address)
        user_elements = tokenize_address(raw_location, lang=lang)

        translated_countries = translate_countries(lang=_lang)

        n_matches = 0
        web_country_count = 0
        user_country_count = 0
        for web_element in web_elements:

            if web_element.lower() in [contry.lower() for contry in en_countries]:
                web_country_count += 1

            for user_element in user_elements:
                if user_element.lower() in [country.lower for country in translated_countries]:
                    user_country_count += 1

                if web_element == user_element:
                    n_matches += 1

        if (web_country_count == user_country_count and web_country_count):
            n_matches += 1

        if (len(web_elements) == len(user_elements) and len(web_elements)):
            n_matches += 1

        if n_matches >= MIN_MATCHES:
                MATCH = True

        if MATCH:
            # Insert this data into the confirmed_locations
            # database.
            result = confirmed_locations.insert_one(good_loc_data)

            # Report.
            print(
                ct("[ACCEPTED]", CYAN),
                location, ct("AS", MAGENTA),
                ct(":", YELLOW), formatted_address, flush=True)
            return True

        # Insert this data into the unconfirmed_locations
        # database.
        result = unconfirmed_locations.insert_one(good_loc_data)

        # Report.
        print(
            ct("[UNCONFIRMED]", YELLOW),
            location, ct("AS", MAGENTA),
            ct(":", YELLOW), formatted_address, flush=True)
        return False

    # If Google came up dry.
    # Track null requests.
    null_requests += 1

    # Add location_tag to rejected_locations database.
    rejected_locations.insert_one(location_tag)

    # Report.
    print(
        ct("[REJECTED]", RED),
        "{0}".format(location), flush=True)
    return False


# ------------------------------------------------------------------ <worker> #

def connet_to(process, cfg):

    s = socket.socket()
    if process == "locationmanager":
        address = location_manager_info(cfg)
        while s.connect_ex(address):
            pass
        # Server information.
        peer_ip, peer_port = s.getpeername()
        peer_info = socket.gethostbyaddr(peer_ip)
        return s


def worker_setup(config_file=config):

    svr_port = config_file.getint('fileserver', 'port')
    print("<file server port>", svr_port)

    svr_ip = config_file.get('fileserver', 'address')
    print("<file server ip>", svr_ip)

    buffer_size = config_file.getint('fileserver', 'buffer_size')
    print("<buffer size>", buffer_size, "Bytes")

    svr_address = (svr_ip, svr_port)
    print("<file server address>", svr_address)

    # Additional info about the fileserver.
    svr_hname, svr_aliaslist, svr_iplist = socket.gethostbyaddr(svr_ip)
    print("<server host-name>", svr_hname)

    # Local machine info.
    local_ip, local_port = get_ip_and_port()
    print("\n<local ip>", local_ip)
    print("<local port>", local_port)

    local_hname = socket.gethostname()
    print("<local host-name>", local_hname)

    return svr_address, buffer_size, local_hname


def prep_tweetfile(raw_tweets, check_key):

    # List of cleaned tweets to send to db.
    cleaned_tweets = []

    tweet_id = 0
    # Step through each tweet.
    for tweet_id, raw_tweet in enumerate(raw_tweets, 1):
        # Process the raw binary tweet data into JSON.
        tweet = json.loads(raw_tweet)

        # TODO : Maybe do some other operations here.

        # Put it into the list.
        if check_key in list(tweet):
            cleaned_tweets.append(tweet)

    print("<prepped tweets>", tweet_id)

    # Return list of clean tweets.
    return cleaned_tweets


def worker_process(tweet_fh, config=config):

    # Get the location manager info.
    location_manager_address = location_manager_info(config)

    # Get a verified absolute path to the binary file.
    fh_path = standard_path(fname=tweet_fh, path_type="tweet", rc=config)

    # Read data file from shared file system.
    # Load raw tweets into local memory from shared file system.
    raw_tweets = read_tweetfile(fh_path)

    # Convert the raw data into a list of Python dictionaries, each of which
    # representing a single tweet.  Pass the `check_key` to ensure we only add
    # tweets with a user to our list.
    cleaned_tweets = prep_tweetfile(raw_tweets, check_key="user")

    # The number of tweets in the cleaned list.
    n_tweets = len(cleaned_tweets)

    # Running counter of processed tweets.
    processed = 0

    to_db = []

    # Step through each tweet in the list.
    for tweet_id, tweet in enumerate(cleaned_tweets, 1):

        # The language.
        # NOTE : Not user language.
        lang = tweet["lang"]

        # User data.
        user = tweet["user"]

        # The user given location.
        user_location = user["location"]
        if not user_location:
            continue

        # The creation time.
        created_at = user["created_at"]

        # Verify location.
        try:
            conn = connet_to("locationmanager", config)
            conn.send(user_location.encode("UTF-8"))
            result = conn.recv(1024)

        except ConnectionResetError as err:
            print("<caught><exception> [{}]".format(err, color="red"))
            worker_process(tweet_fh, config=config)

        if result == b"INSERT":
            tweet["db_location_tag"] = user_location.lower()
            tweet["db_time"] = tstamp(mode="db")
            to_db.append(tweet)

    if to_db:
        insert_tweetfile(to_db, "tweets")

    return True


# ------------------------------------------------------------- <file server> #


def make_serversocket(config_file=config):

    svr_port = config_file.getint('fileserver', 'port')
    print("<file server port>", svr_port)

    svr_ip = config_file.get('fileserver', 'address')
    print("<file server ip>", svr_ip)

    rqst_buf_sz = config_file.getint('fileserver', 'request_bytes')
    print("<request buffer size>", rqst_buf_sz, "Bytes")

    svr_address = (svr_ip, svr_port)
    print("<file server address>", svr_address)

    n_backlog = config_file.getint('fileserver', 'n_backlog')
    print("<max backlogs>:", n_backlog)

    minfiles = config_file.getint('fileserver', 'min_fh')
    print("<min files to proceed>:", minfiles)

    # Local machine info.
    local_ip, local_port = get_ip_and_port()
    print("\n<local ip>", local_ip)
    print("<local port>", local_port)
    print("<local host-name>", socket.gethostname())

    # Make sure the configuration file address is the same as the local
    # address.
    if not svr_ip == "localhost":
        assert local_ip == svr_ip

    # Make, bind and set the socket to listen.
    svrsoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    svrsoc.bind(svr_address)
    svrsoc.listen(n_backlog)

    return svrsoc, rqst_buf_sz, socket.SHUT_RDWR, minfiles


# ------------------------------------------------------------- <streamer.py> #


def get_auth(config_file=config):
    """This way the configuration file is only in the lib and not called in
    the scripts.

    """
    # Debug log message.
    log("streamer").debug("getting authorization values")

    con_key = config_file.get("streamer", "consumer_key")
    con_sec = config_file.get("streamer", "consumer_secret")
    acc_tok = config_file.get("streamer", "access_token")
    acc_sec = config_file.get("streamer", "access_token_secret")
    return con_key, con_sec, acc_tok, acc_sec


# ------------------------------------------------------------ <slistener.py> #


def get_queue_size():
    """Helper function for check-in task for pausing the stream.

    Get the current number of relevant files in the `new_tweet_dir`.

    Returns
    -------
    int
        The current number of files in the 'new_tweet_dir'.

    """

    # Find the number of relevant files in the directory.
    n_files = len(list_tweetdir())

    # Debug log message.
    log("slistener").debug(str(n_files) + " files in queue")

    # Return integer value of the number of files.
    return n_files


def checkin_killstream(config_file=config):
    """Check-in task for killing the stream. Set from the configuration file
    runtime section.

    Configuration file updates each `check_in_interval`.

    Parameters
    ----------
    config_file : {configparser object}, optional
        This is the configuration file object for the entire program.
        (the default is config, which is set at the top of this script)

    Returns
    -------
    keep_alive : bool
        False to continue running or True to kill stream

    """
    # Reload the configuration file.
    reload_config(config_file)

    # Read the run value from the runtime section.
    keep_alive = config_file.getboolean('runtime', 'run')

    # If not run, then log, print & kill
    if not keep_alive:
        msg = "<<killing stream>>"
        print("\n" + msg)
        log("slistener").info("killing stream")
        return True

    # Or keep going quietly.
    else:
        return False


def checkin_pausestream(config_file=config):
    """Check-in task for pausing the stream. Set from the configuration file
    runtime section.

    Check the number of tweet files in the new_tweet_dir and signal a pause
    if there are more than `max_files`.

    Configuration file updates each `check_in_interval`.

    Parameters
    ----------
    config_file : {configparser object}, optional
        This is the configuration file object for the entire program.
        (the default is config, which is set at the top of this script)

    Returns
    -------
    pause : bool
        True to pause, False to continue

    """
    # Get the max_files parameter.
    max_size = config_file.getint("streamer", "max_files")

    # Compare the max_files parameter to the number of files in the directory.
    if get_queue_size() >= max_size:

        # If there are more files in the directory than the max_files, pause
        # the stream.
        log("slistener").info("stream paused")
        msg = "\r<stream paused>[file limit] "
        # log(msg)
        print(msg)

        # Waiting indicator.
        prgrs_mkr = "█"
        _mkr = prgrs_mkr
        prgrs_mkr_len = 50

        # Running counter
        n_waits = 0

        # Hold until there is more space in the directory.
        while get_queue_size() >= max_size:

            # Running counter
            n_waits += 1

            # Every 100 cycles.
            if n_waits % 100 == 0:

                # Check to see if a kill has been ordered.
                if checkin_killstream(config_file=config_file):
                    return False

                # Update the max size.
                max_size = config_file.getint("streamer", "max_files")

                # Write our message
                sys.stdout.write(msg + _mkr)
                sys.stdout.flush()

                # Add a progress marker.
                _mkr += prgrs_mkr

                # Reset the progress marker sequence.
                if len(_mkr) > prgrs_mkr_len:
                    _mkr = prgrs_mkr
                    _msg = msg + _mkr + " " * (prgrs_mkr_len + 5)
                    sys.stdout.write(_msg)
                    sys.stdout.flush()

        log("slistener").info("stream resumed")

    sys.stdout.write("\n")
    sys.stdout.flush()

    # Return True to keep the stream going.
    return True


def new_stream_file(config_file=config):
    log("slistener").info("new stream file")
    fh_ext = config_file.get("streamer", "fh_ext")
    fh = filehandle(config_file.get("path", "new_tweets_dir"), ext=fh_ext)
    n_tweets = config_file.getint("streamer", "n_tweets_per_file")
    n_bytes = config_file.getint("streamer", "n_bytes_per_tweet")
    buf_size = nearestpoweroftwo(n_bytes * n_tweets)
    return open(fh, mode="w", buffering=buf_size)


# [OPERATIONS] ============================================================== #
#
#
if __name__ == "tweetspy_lib":
    log(__name__).info(sys.version)
    log(__name__).info(__name__, "has been imported by", socket.gethostname())

    # This is for color output on windows machines.
    if psutil.WINDOWS:
        init()

elif __name__ == "__main__":

    print("__main__:", __name__)

else:

    pass

# =========================================================================== #
