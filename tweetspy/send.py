"""Test server system which will answer requests for work from clients (recv.py).

This is just for testing and exploring design options.

"""
import os
import sys
import time
import socket

from configparser import ConfigParser as cparser

from tweetspy_lib import get_ip_and_port
from tweetspy_lib import process_fh

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
s = socket.socket()
s.bind(svr_address)
s.listen(n_backlog)

# =========================================================================== #
# Make fake jobs and run.
jobs = [str(i).encode() for i in os.listdir(os.path.curdir)]
try:

    # The main loop.
    RUN = True
    while RUN:

        if not len(jobs):
            job = input("enter job: ").encode()
            if job == b"KILL_SERVER":
                print("shutting down server")
                sys.exit(0)
            else:
                jobs.append(job)

        # Connect to a client worker.
        conn, client_address =  s.accept()
        print("request from", client_address)

        job = jobs.pop()
        print("sending:", job)
        conn.send(job)

        print("shutting down connection.")
        conn.shutdown(socket.SHUT_RDWR)

        print("closing connection.")
        conn.close()



except KeyboardInterrupt as err:
    print("\nshutting down program.")
    sys.exit(0)