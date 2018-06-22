"""
----------------------
The File Server Script
----------------------

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys

from tweetspy_lib import make_serversocket
from tweetspy_lib import list_tweetdir

# =========================================================================== #
# Run time boolean and misc values.

# RUN global value.
RUN = True

# The list of files to send out.
filehandles = []

# =========================================================================== #

# The server socket, buffer size and shutdown flag.
serversocket, request_buffer_size, shutdown_how, minfiles = make_serversocket()

# =========================================================================== #
# Main program.
if __name__ == "__main__":

    try:

        while RUN:

            # If there are no more files to send, then reload.
            if not filehandles:

                msg = "\n<reloading file handles> "
                print(msg)

                # Waiting indicator.
                prgrs_mkr = "█"
                _mkr = prgrs_mkr
                prgrs_mkr_len = 50

                # Running counter
                n_waits = 0

                while len(filehandles) < minfiles:

                    # Running counter
                    n_waits += 1

                    # Every 100 cycles.
                    if n_waits % 100 == 0:

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

                    filehandles = list_tweetdir()
                    msg = "\r<reloading file handles> "

                sys.stdout.write("\r" + " " * (prgrs_mkr_len * 2))
                sys.stdout.write("\n")
                sys.stdout.flush()

            # Connect to a worker.
            workersocket, workeraddress = serversocket.accept()

            with workersocket:

                # Report connection
                print("\n<new connection>", workeraddress)

                # pop a file handle fro filehandles
                fh = filehandles.pop()

                # Send the fh.
                print("<fh size>", fh.__sizeof__(), "bytes")
                print("<sending fh>", fh)
                workersocket.send(fh)
                print("<fh sent>")

                # Close the connection.
                print("<closing connection>")
                workersocket.shutdown(shutdown_how)
                workersocket.close()
                print("<connection closed>")

            # Report number of remaining files.
            n_fhs = len(filehandles)
            if n_fhs % 10 == 0:
                print("\n<remaining file handles>", n_fhs)

    except KeyboardInterrupt as err:
        print("\n<caught><interrupt>", err)
        print("\n<<shutting down program>>")
        sys.exit(0)

# =========================================================================== #
