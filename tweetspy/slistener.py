"""[summary]

[description]
"""
from tweepy import StreamListener

from .tweetspy_lib import PATH_NEW_TWEETS
from .tweetspy_lib import
from .tweetspy_lib import
from .tweetspy_lib import
from .tweetspy_lib import
from .tweetspy_lib import
from .tweetspy_lib import
from .tweetspy_lib import


class SListener(StreamListener):

    def __init__(self, api):
        super(SListener, self).__init__()
        self.buffer_size = int(3 * 1e6)
        self.api = api
        self.counter = 0
        self.fprefix = PATH_NEW_TWEETS
        fh0 = datetime.now().strftime("%Y%b%a%d-%H_%M_%S_%f") + '.json'
        self.output = open(self.fprefix + ,
                                  mode='w',
                                  buffering=self.buffer_size)
        self.delout = open('delete.txt', 'a')
        self.languages = []

    def on_data(self, data):

        raw_tweet = json.loads(data)

        if 'delete' in raw_tweet.keys():
            delete = raw_tweet['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False

        elif 'limit' in raw_tweet.keys():
            if self.on_limit(raw_tweet['limit']['track']) is False:
                return False

        elif 'warning' in raw_tweet.keys():
            warning = raw_tweet['warnings']
            print ct("[ ", YELLOW) + ct(warning['message'], RED) + ct(" ]", Yellow)
            return False

        elif 'text' in raw_tweet.keys():
            _space = 20 - len(raw_tweet['user']['screen_name'])
            _counter = ct('[ ', GREEN) + str(self.counter) + ct(' ]', GREEN)
            _time = ct('[ ', GREEN) + ct(raw_tweet['created_at'].split(' ')[3].encode("utf-8", 'replace'), WHITE) + ct(' ]', GREEN)
            _user = ct(raw_tweet['user']['screen_name'].encode("utf-8", 'replace'), MAGENTA)
            if raw_tweet['lang'] in langs.keys():

                _lang = ct('[ ', GREEN) + ct(langs[raw_tweet["lang"]], YELLOW) + ct(' ]', GREEN)
            else:
                _lang = ct('[ ', YELLOW) + ct("UNKNOWN", RED) + ct(' ]', YELLOW)

            _text = ct(raw_tweet['text'].encode("utf-8", 'replace'), CYAN)
            _message = _counter + "\t" + _time + " " + _lang + "\t" + ct(' @ ', BLUE) + _user + " " * _space + " : " + _text
            print _message.replace("\n", "")
            self.output.write(data + '\n')

        self.counter += 1
        if self.counter >= 300:
            # sys.exit()
            self.output.close()
            self.output = codecs.open(self.fprefix + datetime.now().strftime("%Y%b%a%d-%H_%M_%S_%f") + '.json',
                                      mode='w',
                                      buffering=self.buffer_size)
            oldcounter = self.counter
            self.counter = 0

            os.system('cat ~/SHARED/filesaved.txt')
            sys.stderr.write('\n     ----------------------------\n')
            sys.stderr.write(' --> [RESET COUNTER] : From [' +
                             str(oldcounter) + '] To [' + str(self.counter) + ']\n')
            sys.stderr.write(' --> [SAVED FILE]\n')
            sys.stderr.write(' --> [NEW FILE] : ' + self.fprefix +
                             datetime.now().strftime("%Y%b%a%d-%H_%M_%S_%f") + '.json\n')


            with open("/root/SHARED/tweetspy/kill.txt", "r") as ktxt:
                f = ktxt.readlines()
                if f[0] == '0\n':
                    if raw_input("\n --> Do you want to kill? yes/[no] :" in ["Y", "y", "YES", "Yes", "yes"]):
                        sys.stderr.write(" --> KILLED\n")
                        sys.stderr.write('     ----------------------------\n')
                        sys.exit(0)
                    else:
                        sys.stderr.write(" --> NOT KILLED\n")

            sys.stderr.write('     ----------------------------\n')
        return

    def on_delete(self, status_id, user_id):
        del_msg = ct("[ ", YELLOW) + ct("DELETE " + str(status_id), RED) + ct(" ]", YELLOW)
        _counter = ct('[ ', GREEN) + str(self.counter) + ct(' ]', GREEN)
        # _time = ct('[', GREEN) + ct(raw_tweet['created_at'].split(' ')[3].encode("utf-8", 'replace'), WHITE) + ct(']  ', GREEN)
        print _counter + "\t" + del_msg
        self.delout.write(str(status_id) + "\n")
        return

    def on_limit(self, track):
        lim_msg = ct("[ ", YELLOW) + ct("LIMIT " + str(track), RED) + ct(" ]", YELLOW)
        _counter = ct('[ ', GREEN) + str(self.counter) + ct(' ]', GREEN)
        # _time = ct('[', GREEN) + ct(raw_tweet['created_at'].split(' ')[3].encode("utf-8", 'replace'), WHITE) + ct(']  ', GREEN)
        print _counter + "\t" + lim_msg
        return

    def on_error(self, status_code):
        sys.stderr.write('Error: ' + str(status_code) + "\n")
        return False

    def on_timeout(self):
        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)

        return
