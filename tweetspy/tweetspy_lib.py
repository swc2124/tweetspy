""""

[description]
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import nltk
import os
import psutil
import socket
import time

from subprocess import PIPE
from subprocess import Popen
from time import gmtime
from time import sleep
from time import strftime


nltk.data.path.append('/root/SHARED/nltk_data/')

hostname = socket.gethostname()

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

langs = {
    'ar': 'Arabic',
    'bg': 'Bulgarian',
    'ca': 'Catalan',
    'cs': 'Czech',
    'da': 'Danish',
    'de': 'German',
    'el': 'Greek',
    'en': 'English',
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

tweet_keys = [
    u'quote_count',
    u'contributors',
    u'truncated',
    u'text',
    u'is_quote_status',
    u'in_reply_to_status_id',
    u'reply_count',
    u'id',
    u'favorite_count',
    u'entities',
    u'retweeted',
    u'coordinates',
    u'timestamp_ms',
    u'source',
    u'in_reply_to_screen_name',
    u'id_str',
    u'retweet_count',
    u'in_reply_to_user_id',
    u'favorited',
    u'retweeted_status',
    u'user',
    u'geo',
    u'in_reply_to_user_id_str',
    u'lang',
    u'created_at',
    u'filter_level',
    u'in_reply_to_status_id_str',
    u'place'
]

syntax_en = {
    'PRP$': 'pronoun, possessive',
    'VBG': 'verb, present participle or gerund',
    'VBD': 'verb, past tense',
    'VBN': 'verb, past participle',
    'VBP': 'verb, present tense not 3rd person singular',
    'WDT': 'determiner, WH',
    'JJ': 'adjective or numeral, ordinal',
    'WP': 'pronoun, WH',
    'VBZ': 'verb, present tense 3rd person singular',
    'DT': 'determiner',
    'RP': 'particle',
    'NN': 'noun, common, singular or mass',
    'TO': '"to" as preposition or infinitive marker',
    'PRP': 'pronoun, personal',
    'RB': 'adverb',
    'NNS': 'noun, common plural',
    'NNP': 'noun, proper singular',
    'VB': 'verb, base form',
    'WRB': 'adverb, WH',
    'CC': 'conjunction, coordinating',
    'RBR': 'adverb, comparative',
    'CD': 'cardinal numeral',
    '-NONE-': 'No matching tags found',
    'EX': 'existential, there there',
    'IN': 'conjunction or subordinating preposition',
    'WP$': 'pronoun, possessive WH',
    'MD': 'modal auxiliary',
    'JJS': 'adjective, superlative',
    'JJR': 'adjective, comparative',
    'PDT': 'pre-determiner',
    'RBS': 'adverb, superlative',
    'FW': 'foreign word',
    'NNPS': 'noun, proper plural',
    'UH': 'interjection'
}

syntax_en_clr = {
    'NN': GREEN,
    'NNS': GREEN,
    'NNP': GREEN,
    'NNPS': GREEN,
    'MD': YELLOW,
    'JJR': YELLOW,
    'JJS': YELLOW,
    'JJ': YELLOW,
    'DT': YELLOW,
    'VBG': BLUE,
    'VBD': BLUE,
    'VBN': BLUE,
    'VBP': BLUE,
    'VBZ': BLUE,
    'VB': BLUE,
    'RBS': MAGENTA,
    'RBR': MAGENTA,
    'RB': MAGENTA,
    'WRB': MAGENTA,
    'PRP$': CYAN,
    'PRP': CYAN,
    'WP': CYAN,
    'WP$': CYAN,
    "IN": RED,
}

def getNetworkIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]


def get_track_words():
    pass


def ct(text, colour=WHITE):
    seq = "\x1b[1;%dm" % (30 + colour) + text + "\x1b[0m"
    return seq


def list_files(path):
    # returns a list of names (with extension, without full path) of all files
    # in folder path
    files = []
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            files.append(name)
    return files


def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.2f %s' % (value, s)
    return '%.2f B' % (n)


def get_cpu_temperature():
    try:
        output, _error = Popen(
            ['vcgencmd', 'measure_temp'], stdout=PIPE).communicate()
        return float(output[output.index('=') + 1:output.rindex("'")])
    except:
        try:
            output, _error = Popen(['sensors'], stdout=PIPE).communicate()
            temp = float(output.split("+")[1].split(" ")[0])
            return temp
        except OSError as e:
            return "0"


def get_cpu_freq():
    try:
        output, _error = Popen(
            ['vcgencmd', 'measure_clock arm'], stdout=PIPE).communicate()
        return str(float(output[14:]) / 1e6)
    except:
        output, _error = Popen(
            ['cat', '/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq'], stdout=PIPE).communicate()
        return str(float(output[:6]) / 1e3)


def get_cpu_volts():
    try:
        output, _error = Popen(
            ['vcgencmd', 'measure_volts core'], stdout=PIPE).communicate()
        return str(output[5:11])
    except:
        return '1'


def net_traf():
    interval = 0.005
    try:
        # tot_before = psutil.net_io_counters()
        # pnic_before = psutil.net_io_counters(pernic=True)
        time.sleep(interval)
        tot_after = psutil.net_io_counters()
        # pnic_after = psutil.net_io_counters(pernic=True)
        return str(int(tot_after.bytes_sent/1e6)), str(int(tot_after.bytes_recv/1e6)).rstrip('\n')
    except:
        return '0', '0'


def log_file(_jbsdn):
    cpu_temp = str(get_cpu_temperature())
    cpu_usage = str(psutil.cpu_percent())
    cpu_freq = get_cpu_freq()
    core_volts = get_cpu_volts()
    free_ram = str(psutil.virtual_memory().percent)
    sent, recv = net_traf()
    hostname = str(socket.gethostname())
    return str(hostname + ' ' + str(_jbsdn) + ' ' + cpu_temp + ' ' + cpu_usage + ' ' + cpu_freq + ' ' + core_volts + ' ' + free_ram + ' ' + sent + ' ' + recv)


def report(jobs_done):
    sock = socket.socket()
    server_address = ('192.168.1.103', 15000)
    message = log_file(jobs_done)
    try:
        #print >>sys.stderr, 'sending "%s"' % message
        sock.connect(server_address)
        sock.sendall(message)
    except Exception as e:
        print e
    finally:
        #print >>sys.stderr, 'closing socket'
        sock.close()
