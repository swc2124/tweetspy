# ============================================================================
# Author                : swc21
# Date                  : 2018-03-14 11:22:31
# Project               : GitHub
# File Name             : Twitter_Controller
# Last Modified by      : swc21
# Last Modified time    : 2018-03-14 12:29:28
# ============================================================================
# 

import os
import pickle
import socket
import sys

from threading import Thread
from time import gmtime
from time import sleep
from time import strftime
#--[PROGRAM-OPTIONS]------------------------------------------------------#
CLEANED_WORDS_PATH = '/root/SHARED/Tweets_Output/Clean_Words.json'
JSON_PATH = '/root/SHARED/Tweets/'
HOSTS = [
    '192.168.1.201', '192.168.1.202', '192.168.1.203', '192.168.1.204',
    '192.168.1.205', '192.168.1.206', '192.168.1.207', '192.168.1.208',
    '192.168.1.209', '192.168.1.210', '192.168.1.211', '192.168.1.212',
    '192.168.1.213', '192.168.1.214', '192.168.1.215', '192.168.1.216',
    '192.168.1.217', '192.168.1.218', '192.168.1.219', '192.168.1.220',
    '192.168.1.221', '192.168.1.222', '192.168.1.223', '192.168.1.224',
    '192.168.1.225', '192.168.1.226', '192.168.1.227', '192.168.1.228',
    '192.168.1.229', '192.168.1.230', '192.168.1.231', '192.168.1.232'
]
#--[PROGRAM-FUNCTIONS]----------------------------------------------------#
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)


def ct(text, colour=WHITE):
    seq = "\x1b[1;%dm" % (30+colour) + text + "\x1b[0m"
    return seq


def getNetworkIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]


def list_files(path):
    # returns a list of names (with extension, without full path) of all files
    # in folder path
    files = []
    for name in os.listdir(path):
        if name.endswith(('.json')):
            files.append(name)
    return files


while True:
    try:
        jobs = [job for job in list_files(
            JSON_PATH) if not str(job).startswith(('.'))]
        N_jobs = len(jobs)
        os.system('clear')
        print >>sys.stderr,  ct(' -->', GREEN)+ct(' [', WHITE)+ct('NUMBER OF JOBS IN QUEUE', CYAN)+ct(']', WHITE)+ct('[', WHITE)+ct(str(N_jobs), MAGENTA)+ct(
            ']', WHITE)+ct(' : ', GREEN)+ct('[', WHITE)+ct('NUMBER OF HOSTS', CYAN)+ct(']', WHITE)+ct('[', WHITE)+ct(str(len(HOSTS)), MAGENTA)+ct(']', WHITE)
        if N_jobs > len(HOSTS):
            os.system('clear')
            os.system('cat /root/SHARED/start.txt')
            sleep(2)
            for host in HOSTS:
                try:
                    s = socket.socket()
                    server_address = (str(host), 40000)
                    s.connect(server_address)
                    try:
                        print >>sys.stderr, '\n'+ct(' -->', GREEN)+ct(' [', WHITE)+ct('CONNECTIING', GREEN)+ct(']', WHITE)+ct('[', WHITE)+ct(str(server_address[0]), MAGENTA)+ct(
                            ']', WHITE)+ct(' : ', GREEN)+ct('[', WHITE)+ct('PORT', CYAN)+ct(']', WHITE)+ct('[', WHITE)+ct(str(server_address[1]), MAGENTA)+ct(']', WHITE)
                        file_name = jobs.pop(0)
                        N_jobs = len(jobs)
                        print >>sys.stderr, '\n'+ct(' -->', GREEN)+ct(' [', WHITE)+ct('SENDING', GREEN)+ct(
                            ']', WHITE)+ct('[', WHITE)+ct(str(file_name), CYAN)+ct(']', WHITE)
                        s.sendall(file_name)
                        sleep(.09)
                        print >>sys.stderr, '\n' + \
                            ct(' -->', GREEN) + \
                            ct(' [', WHITE)+ct('SENT', GREEN)+ct(']', WHITE)
                        sleep(.09)
                    finally:
                        print >>sys.stderr, '\n'+ct(' -->', YELLOW)+ct(' [', WHITE)+ct('DISCONNECTING', RED)+ct(
                            ']', WHITE)+ct('[', WHITE)+ct(str(server_address[1]), CYAN)+ct(']', WHITE)
                        s.close()
                        sleep(.09)
                        print >>sys.stderr, '\n' + \
                            ct(' -->', YELLOW) + \
                            ct(' [', WHITE)+ct('DISCONNECTED', RED)+ct(']', WHITE)
                        sleep(.09)
                        # os.system('clear')
                        print >>sys.stderr, ct(' -->', GREEN)+ct(' [', WHITE)+ct('NUMBER OF JOBS IN QUEUE', CYAN)+ct(']', WHITE)+ct('[', WHITE)+ct(str(N_jobs), MAGENTA)+ct(
                            ']', WHITE)+ct(' : ', GREEN)+ct('[', WHITE)+ct('NUMBER OF HOSTS', CYAN)+ct(']', WHITE)+ct('[', WHITE)+ct(str(len(HOSTS)), MAGENTA)+ct(']', WHITE)
                        sleep(1)
                except:
                    print >>sys.stderr, '\n --> [HOST] [%s] (%s): [UNAVAILABLE] \r' % server_address
                    sys.stderr.flush()
                    sleep(1)
            #os.system('ls '+JSON_PATH)
            sleep(2)
    except KeyboardInterrupt:
        print >>sys.stderr, ' --> [PAUSED CONTROLLER]'
        if raw_input(" --> Exit? [yes/No]") == "yes":
            print >>sys.stderr, ' --> [CLOSING CONTROLLER]'
            sys.exit(0)
        else:
            continue
