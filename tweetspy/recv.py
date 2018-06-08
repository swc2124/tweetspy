"""Test client system which will request work from a server (send.py).

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
    config_fh = './tweetspy/tweetspy.ini'

# =========================================================================== #
# Read in our configuration file values.
cfg = cparser()
cfg.read(config_fh)

svr_port = cfg.getint('fileserver', 'port')
print("file server port:", svr_port)

svr_ip = cfg.get('fileserver', 'address')
print("file server ip:", svr_ip)

buffer_size = cfg.getint('fileserver', 'buffer_size')
print("buffer size:", buffer_size)

svr_address = (svr_ip, svr_port)
print("file server address:", svr_address)

# =========================================================================== #
# Additional info about the fileserver.
svr_hname, svr_aliaslist, svr_iplist = socket.gethostbyaddr(svr_ip)

# =========================================================================== #
# Local machine info.
local_ip, local_port = get_ip_and_port()
local_hname = socket.gethostname()

# =========================================================================== #
# Run time boolean and misc values.
RUN = True
NEED_FILE = True
_dots = "."

# A record of known contacts.
conn_history = {}
known_hosts = list(conn_history.keys())

# =========================================================================== #
# Main program.
try:
    while RUN:
        if NEED_FILE:

            # Make a new socket with a new port.
            s = socket.socket()
            n_try = 0

            # Get a file handle from the server.
            while NEED_FILE:

                # Connect to server.
                if not s.connect_ex(svr_address):

                    try:
                        # Server information.
                        peer_ip, peer_port = s.getpeername()
                        peer_info = socket.gethostbyaddr(peer_ip)
                        print(
                            "\nconnected to",
                            peer_info[0],
                            "@",
                            peer_ip,
                            "on port:",
                            peer_port)
                        if not peer_info[0] in list(conn_history.keys()):
                            conn_history[peer_info[0]] = peer_info[1:]

                        # Receive data and more sender information.
                        file_handle = s.recv(buffer_size)
                        print("received file_handle")


                    except ConnectionResetError as err:
                        print("\nCaught [ ConnectionResetError ]", sep='')
                        print(err, sep='', end='\n\n', flush=True)

                    else:

                        # Adjust the boolean vale to escape this loop.
                        NEED_FILE = False

                        # Shutdown and close the socket.
                        s.shutdown(socket.SHUT_RDWR)
                        s.close()

                    finally:
                        pass

                # Report rolling status.
                else:
                    sys.stdout.write("\rwaiting for connection" + _dots)
                    sys.stdout.flush()
                    _dots += "."
                    if len(_dots) > 5:
                        _dots = "."
                        _msg = "\rwaiting for connection" + _dots + " " * 10
                        sys.stdout.write(_msg)
                        sys.stdout.flush()

                n_try += 1
                if n_try > 50:
                    # Make a new socket with a new port.
                    s = socket.socket()
                    n_try = 0

        # Is it a kill signal?
        if file_handle == b"KILL_CLIENT":
            # print("received kill order.")
            # print("setting RUN to False.")
            RUN = False

        # Do the file_handle.
        else:
            if process_fh(file_handle):
                NEED_FILE = True

except KeyboardInterrupt as err:
    print("\nshutting down program.")
    print(conn_history)
    sys.exit(0)

# =========================================================================== #