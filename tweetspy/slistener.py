"""
---------------------------------
The TweetspyStreamListener Object
---------------------------------

What is this thing?

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from tweepy import StreamListener
from tweepy.models import Status
from tweepy.utils import import_simplejson

from tweetspy_lib import config
from tweetspy_lib import new_stream_file
from tweetspy_lib import check_in_interval
from tweetspy_lib import checkin_killstream
from tweetspy_lib import checkin_pausestream

json = import_simplejson()


class TweetspyStreamListener(StreamListener):

    def __init__(self):
        super(TweetspyStreamListener, self).__init__()
        self.count = 0
        self.buffer = new_stream_file()
        self.save_interval = config.getint('streamer', 'n_tweets_per_file')

    def on_connect(self):
        """Called once connected to streaming server.

        This will be invoked once a successful response
        is received from the server. Allows the listener
        to perform some work prior to entering the read loop.

        """
        return

    def on_data(self, raw_data):
        """Called when raw data is received from connection.

        Override this method if you wish to manually handle
        the stream data. Return False to stop stream and close connection.

        """
        data = json.loads(raw_data)

        if 'in_reply_to_status_id' in data:
            status = Status.parse(self.api, data)
            if self.on_status(status) is False:
                return False

        elif 'delete' in data:
            delete = data['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False

        elif 'event' in data:
            status = Status.parse(self.api, data)
            if self.on_event(status) is False:
                return False

        elif 'direct_message' in data:
            status = Status.parse(self.api, data)
            if self.on_direct_message(status) is False:
                return False

        elif 'friends' in data:
            if self.on_friends(data['friends']) is False:
                return False

        elif 'limit' in data:
            if self.on_limit(data['limit']['track']) is False:
                return False

        elif 'disconnect' in data:
            if self.on_disconnect(data['disconnect']) is False:
                return False

        elif 'warning' in data:
            if self.on_warning(data['warning']) is False:
                return False

        else:
            return False
            
        # If this tweet contains text.
        if "user" in list(data.keys()):

            # --------------------------------------------------------------- #
            # Stupid print for fun.
            uname = data["user"]["screen_name"]
            umsg = data["text"]
            nspc = (20 - len(uname))
            if nspc < 1:
                nspc = 1
            spc = " " * nspc
            if not umsg.startswith("RT"):
                print("<tweet>", uname, spc, umsg.replace("\n", ""))
            # --------------------------------------------------------------- #

            # Write the tweet to the buffer.
            self.buffer.write(raw_data)

            # Running counter.
            self.count += 1

            # If the buffer is full, then cycle the buffer.
            if self.count % self.save_interval == 0:
                self.swap_buffer()

            # If the counter is a check-in interval, do all the check-in tasks.
            if self.count % check_in_interval == 0:

                # Shutdown if the `runtime` `run` value is False.
                if checkin_killstream():
                    return False

                # pause if there are too many files in the new tweet directory.
                if not checkin_pausestream():
                    return False

    def swap_buffer(self):
        self.buffer.flush()
        self.buffer.close()
        self.buffer = new_stream_file()
        self.save_interval = config.getint('streamer', 'n_tweets_per_file')
        print("<new buffer>", self.buffer.__sizeof__(), "bytes")

    def keep_alive(self):
        """Called when a keep-alive arrived."""
        return

    def on_status(self, status):
        """Called when a new status arrives."""
        return

    def on_exception(self, exception):
        """Called when an un-handled exception occurs."""
        print("<caught><exception>", exception)
        self.count += 1
        return True

    def on_delete(self, status_id, user_id):
        """Called when a delete notice arrives for a status."""
        return

    def on_event(self, status):
        """Called when a new event arrives."""
        return

    def on_direct_message(self, status):
        """Called when a new direct message arrives."""
        return

    def on_friends(self, friends):
        """Called when a friends list arrives.

        friends is a list that contains user_id
        """
        return

    def on_limit(self, track):
        """Called when a limitation notice arrives."""
        return

    def on_error(self, status_code):
        """Called when a non-200 status code is returned."""
        print("<error><non-200 status code>", status_code)
        self.count += 1
        return True

    def on_timeout(self):
        """Called when stream connection times out."""
        return

    def on_disconnect(self, notice):
        """Called when twitter sends a disconnect notice."""
        return

    def on_warning(self, notice):
        """Called when a disconnection warning message arrives."""
        return
