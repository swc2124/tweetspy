# ============================================================================
# Author                : swc21
# Date                  : 2018-03-14 11:22:31
# Project               : GitHub
# File Name             : Client_test
# Last Modified by      : swc21
# Last Modified time    : 2018-03-14 12:36:53
# ============================================================================
# 

import socket
import sys

HOST, PORT = "localhost", 6005
data = " ".join(sys.argv[1:])

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().
sock.sendto(data + "\n", (HOST, PORT))
received = sock.recv(1024)

print "Sent:     {}".format(data)
print "Received: {}".format(received)
