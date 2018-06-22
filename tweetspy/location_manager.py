"""
---------------------------
The Location Manager Script
---------------------------

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import socket

from tweetspy_lib import location_manager_setup
from tweetspy_lib import verify_location
from tweetspy_lib import stop_words

# =========================================================================== #
# Run time boolean and misc values.

# RUN global value.
RUN = True

# Progress marker.
_dots = "|"

# A record of known contacts.
conn_history = {}

# Error history.
error_history = []

rc_sec = "locationmanager"

# =========================================================================== #
# Basic setup information.

serversocket, shutdown_how, config = location_manager_setup()

config.set(rc_sec, 'total_requests', value="0")

# =========================================================================== #
# Main program.
if __name__ == "__main__":

    try:

        while RUN:

            recv_sz = config.getint(rc_sec, "recv_sz")

            # Connect to a worker.
            print("<ready for connection>")
            workersocket, workeraddress = serversocket.accept()

            with workersocket:

                try:
                    # Report connection
                    print("\n<new connection> [{} port ({})]".format(*workeraddress))

                    reply = workersocket.recv(recv_sz)
                    location = reply.decode("UTF-8")
                    print("<received> [{}]".format(location))

                    result = verify_location(location, config)

                    if result:
                        reply = b"INSERT"
                    else:
                        reply = b"DENY"

                    print("<sending reply> [{}]".format(reply))
                    workersocket.send(reply)

                    # Close the connection.
                    print("<closing connection>")
                    workersocket.shutdown(shutdown_how)
                    workersocket.close()
                    print("<connection closed>")

                except ConnectionResetError as err:
                    print("<caught><exception> [{}]".format(err))

    except KeyboardInterrupt as err:
        print("\n<caught><interrupt>", err)
        print("\n<<shutting down program>>")
        sys.exit(0)

class ClassName(object):
    """docstring for ClassName"""
    def __init__(self, arg):
        super(ClassName, self).__init__()
        self.arg = arg

