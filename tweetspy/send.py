"""Test server system which will answer requests for work from clients (recv.py).

This is just for testing and exploring design options.

"""
import os
import sys
import socket

from configparser import ConfigParser as cparser

from tweetspy_lib import get_ip_and_port
from tweetspy_lib import process_fh
from tweetspy_lib import tstamp

# =========================================================================== #
# Sort out or configuration file path.
args = sys.argv
if len(args) > 1:
    fh = args[1]
    if os.path.isfile(fh) and fh.endswith("ini"):
        config_fh = fh
else:
    config_fh = './tweetspy.ini'

# =========================================================================== #
# Read in our configuration file values.
cfg = cparser()
cfg.read(config_fh)

svr_port = cfg.getint('fileserver', 'port')
print("file server port:", svr_port)

svr_ip = cfg.get('fileserver', 'address')
print("file server ip:", svr_ip)

buffer_size = cfg.getint('fileserver', 'buffer_size')
print("buffer size:", buffer_size, "MB")

svr_address = (svr_ip, svr_port)
print("file server address:", svr_address)

n_backlog = cfg.getint('fileserver', 'n_backlog')
print("n backlogs allowed:", n_backlog)

# =========================================================================== #
# Local machine info.
local_ip, local_port = get_ip_and_port()
local_hname = socket.gethostname()

# =========================================================================== #
# Make sure the configuration file address is the same as the local address.
assert local_ip == svr_ip

# =========================================================================== #
# Make, bind and set the socket to listen.
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(svr_address)
serversocket.listen(n_backlog)

# =========================================================================== #
# The main loop.

try:

    RUN = True
    while RUN:

        job = tstamp()

        # Connect to a worker.
        (workersocket, workeraddress) = serversocket.accept()
        print("request from", workeraddress)

        print("sending:", job)
        conn.send(job)

        print("shutting down connection.")
        conn.shutdown(socket.SHUT_RDWR)

        print("closing connection.")
        conn.close()

except KeyboardInterrupt as err:
    print("\nshutting down program.")
    sys.exit(0)
