"""
-----------------
The Worker Script
-----------------

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import socket

from tweetspy_lib import worker_setup
from tweetspy_lib import worker_process

# =========================================================================== #
# Run time boolean and misc values.

# RUN global value.
RUN = True

# NEED_FILE global value.
NEED_FILE = True

# Progress marker.
_dots = "|"

# A record of known contacts.
conn_history = {}

# Error history.
error_history = []

# =========================================================================== #
# Basic address information.

# Server address, buffer size and host machine name.
svr_address, buffer_size, hostname = worker_setup()

# =========================================================================== #
# Main program.
if __name__ == "__main__":

    try:

        # This is what a worker does.
        while RUN:

            # Get a file handle from the fileserver.
            if NEED_FILE:

                # Make a new socket with a new port.
                s = socket.socket()
                n_try = 0

                # Get a file handle from the server.
                while NEED_FILE:

                    # Connect to server.
                    # NOTE: s.connect_ex(address) returns 0 if connection,
                    # which is why we say "if not s.connect_ex(address):".
                    if not s.connect_ex(svr_address):

                        try:
                            # Server information.
                            peer_ip, peer_port = s.getpeername()
                            peer_info = socket.gethostbyaddr(peer_ip)
                            print(
                                "\n<connected> ",
                                peer_info[0],
                                "@",
                                peer_ip,
                                "on port:",
                                peer_port)

                            # Add this peer info to a running collection of
                            # connection history.
                            if not peer_info[0] in list(conn_history.keys()):
                                print("<new server>", peer_info[1:])
                                conn_history[peer_info[0]] = peer_info[1:]

                            # Receive data and more sender information.
                            file_handle = s.recv(buffer_size)
                            print("<received data>")

                        except ConnectionResetError as err:
                            print(
                                "\n<caught> [ ConnectionResetError ]",
                                sep='',
                                end="\n",
                                flush=True)
                            print(
                                "<error> ", err,
                                sep='',
                                end='\n\n',
                                flush=True)

                        else:
                            # Shutdown and close the socket.
                            print("<closing connection>")
                            s.shutdown(socket.SHUT_RDWR)
                            s.close()
                            print("<connection closed>")

                            # Adjust the boolean vale to escape this loop.
                            NEED_FILE = False

                    # Report rolling status.
                    else:
                        msg = "\r<requesting connection> "
                        sys.stdout.write(msg + _dots)
                        sys.stdout.flush()
                        _dots += "|"
                        if len(_dots) > 25:
                            _dots = "|"
                            _msg = msg + _dots + " " * 30
                            sys.stdout.write(_msg)
                            sys.stdout.flush()

                    n_try += 1
                    if n_try > 50 and NEED_FILE:
                        # Make a new socket with a new port.
                        print("\r<new socket>" + " " * 50)
                        s = socket.socket()
                        n_try = 0

            # Is it a kill signal?
            if file_handle == b"KILL_CLIENT":
                # print("received kill order.")
                # print("setting RUN to False.")
                RUN = False

            # Add additional custom flags here.
            elif file_handle == b"CUSTOM_SIGNAL":

                pass

            # =============================== #
            # CALL THE ACTUALL WORK FUNCTIONS #
            # =============================== #
            else:

                # Call the process function.  If it returns False, then put the
                # file handle into a list of bunk file handles and move on.
                # We can com collect there later.
                if not worker_process(file_handle):

                    # Append our error log.
                    error_history.append(file_handle)
                    print("<appended error history>", file_handle)

                # Reset global for new file.
                NEED_FILE = True

    except KeyboardInterrupt as err:
        print("\n<caught><interrupt>", err)
        print("<connection history>", conn_history)
        print("<error history>", error_history)
        print("\n<<shutting down program>>")
        sys.exit(0)

# =========================================================================== #
