#SOl Courtney Columbia U Department of Astronomy and Astrophysics NYC 2016 
#swc2124@columbia.edu

#--[DESCRIPTION]---------------------------------------------------------#

'''
Date: May 2016

Handeler for twitter text parsing
'''

#--[PROGRAM-OPTIONS]------------------------------------------------------#
from numpy.random import ranf
from traceback import format_exc
from time import gmtime, strftime, sleep
import sys, os, socket

#--[PROGRAM-OPTIONS]------------------------------------------------------#

CLEANED_WORDS_PATH = '/root/SHARED/Tweets_Output/Clean_Words.json'

JSON_PATH = '/root/SHARED/Tweets/'

Host_dict = {
	'192.168.1.103': '44core-linux',
	'192.168.1.201': 'Wolf-01',
	'192.168.1.202': 'Wolf-02',
	'192.168.1.203': 'Wolf-03',
	'192.168.1.204': 'Wolf-04',
	'192.168.1.205': 'Wolf-05',
	'192.168.1.206': 'Wolf-06',
	'192.168.1.207': 'Wolf-07',
	'192.168.1.208': 'Wolf-08',
	'192.168.1.209': 'Wolf-09',
	'192.168.1.210': 'Wolf-10',
	'192.168.1.211': 'Wolf-11',
	'192.168.1.212': 'Wolf-12',
	'192.168.1.213': 'Wolf-13',
	'192.168.1.214': 'Wolf-14',
	'192.168.1.215': 'Wolf-15',
	'192.168.1.216': 'Wolf-16',
	'192.168.1.217': 'BPI-M1-01',
	'192.168.1.218': 'BPI-M1-02',
	'192.168.1.219': 'BPI-M1-03',
	'192.168.1.220': 'BPI-M1-04',
	'192.168.1.221': 'BPI-M1-05',
	'192.168.1.222': 'BPI-M1-06',
	'192.168.1.223': 'BPI-M1-07',
	'192.168.1.224': 'BPI-M1-08',
	'192.168.1.225': 'BPI-M1-09',
	'192.168.1.226': 'BPI-M1-10',
	'192.168.1.227': 'BPI-M1-11',
	'192.168.1.228': 'BPI-M1-12',
	'192.168.1.229': 'BPI-M1-13',
	'192.168.1.230': 'BPI-M1-14',
	'192.168.1.231': 'BPI-M1-15',
	'192.168.1.232': 'BPI-M1-16'}

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



jobs = [job for job in list_files(JSON_PATH) if not job.startswith(('.'))]
jobs.sort()
s = socket.socket()
host = str(getNetworkIp())
port = 50000
server_address = (str(host), port)
hostname = socket.gethostname()
s.bind(server_address)
s.listen(80)

# Clear and print
os.system('clear')
os.system("lsof -i :" + str(port))
print "Starting"
times_around = 0

try:
	while True:
		
		if times_around > 10:
			os.system("clear")
			times_around = 0
		
		# If there are jobs to do:
		if len(jobs):

			# Print something.
			print ct(str(len(jobs)), YELLOW), "Jobs in queue."
			print "Waiting for connection..."

			# Connect to a client worker.
			conn, client_address = s.accept()

			# If connection:
			if conn:

				# Print a little something.
				print "Connection from:", ct(Host_dict[client_address[0]], GREEN), "@", client_address

				# Pop a filename and print.
				file_name = jobs.pop(0)
				print "\tSending:", file_name
				
				# Send a file name to worker. 
				conn.send(file_name)
				print "\tDone"

				# Disconnect from client.
				print "\tClosing connection"
				conn.close()
				print "\tDone\n"

				# Add one to the prit length.
				times_around += 1

			# If no connection:
			else:
				print "No connection"

		# If there are no jobs to do:
		else:

			# Load Jobs and sort list
			print ct("Loading new job list...", YELLOW)
			
			# If there are no jobs:
			counter = 0
			while not len(jobs):

				jobs = [job for job in list_files(JSON_PATH) if not str(job).startswith(('.'))]
				sys.stdout.write("\r" + ct("Attempt : ", YELLOW) + ct(str(counter), GREEN))
				sys.stdout.flush()
				sleep(.5)
				counter += 1
			
			sys.stdout.write("\n")
			sys.stdout.flush()
			
			# Sort jobs.
			print "Sorting Jobs"
			jobs.sort()
			print "Done.\n"

except KeyboardInterrupt as err:

	print "Closing socket"
	#conn.close()
	s.close(socket.SHUT_RDWR)
	print "Done."


"""

done_jobs = []
HOLD_FH = False
times_around = 0
PORTS = [40000, 50000, 60000]
while True:

	try:
		jobs = [job for job in list_files(JSON_PATH) if not str(job).startswith(('.')) ]

		os.system('clear')
		print ct(' -->', GREEN) + ct(' [', WHITE) + ct('NUMBER OF JOBS IN QUEUE', CYAN) + ct(']', WHITE) + ct('[', WHITE) + ct(str(len(jobs)), MAGENTA) + ct(']', WHITE) + ct(' : ', GREEN) + ct('[', WHITE) + ct('NUMBER OF HOSTS', CYAN) + ct(']', WHITE) + ct('[', WHITE) + ct(str(len(HOSTS)), MAGENTA) + ct(']', WHITE)

		if len(jobs) > len(HOSTS):
			os.system('clear')
			os.system('cat /root/SHARED/start.txt')
			sleep(3)

			for host in HOSTS:
			
				s = socket.socket()
				server_address = (str(host), _port)

				if not HOLD_FH:
					if not len(jobs):
						break

					file_name = jobs.pop(0)
					while file_name in done_jobs:
						if not len(jobs):
							break
						file_name = jobs.pop(0)
					HOLD_FH = False
				print >>sys.stderr, '\n' + ct(' -->',GREEN)+ct(' [',WHITE)+ct('NUMBER OF JOBS IN QUEUE',CYAN)+ct(']',WHITE)+ct('[',WHITE)+ct(str(len(jobs)),MAGENTA)+ct(']',WHITE)+ct(' : ',GREEN)+ct('[',WHITE)+ct('NUMBER OF HOSTS',CYAN)+ct(']',WHITE)+ct('[',WHITE)+ct(str(len(HOSTS)),MAGENTA)+ct(']',WHITE) 
				sleep(ranf()/1e1)
				print >>sys.stderr, ct('\t -->',GREEN)+ct(' [',WHITE)+ct('CONNECTIING',GREEN)+ct(']',WHITE)+ct('[',WHITE)+ct(str(server_address[0]),YELLOW)+ct(']',WHITE)+ct(' : ',GREEN)+ct('[',WHITE)+ct('PORT',CYAN)+ct(']',WHITE)+ct('[',WHITE)+ct(str(server_address[1]),MAGENTA)+ct(']',WHITE) 
				sleep(ranf()/1e1)
				try:
					s.connect(server_address)
				except Exception as err:
					print >>sys.stderr, ct('\t -->',GREEN)+ct(' [',YELLOW)+ct('NOT SENT - SERVER BUSY',RED)+ct(']',YELLOW)
					HOLD_FH = True
					s.close()
					sleep(ranf())
					continue

				print >>sys.stderr, ct('\t -->',GREEN)+ct(' [',WHITE)+ct('SENDING',GREEN)+ct(']',WHITE)+ct('[',WHITE)+ct(str(file_name),BLUE)+ct(']',WHITE)
				_sent = s.send(file_name)
				
				if _sent < 33:
					print >>sys.stderr, ct('\t -->',GREEN)+ct(' [',YELLOW)+ct('NOT SENT - SERVER BUSY',RED)+ct(']',YELLOW)
					HOLD_FH = True
					s.close()
					sleep(ranf())
					continue

				else:
					done_jobs.append(file_name)
					print >>sys.stderr, ct('\t -->',GREEN)+ct(' [',WHITE)+ct('SENT',GREEN)+ct(']',WHITE)
					sleep(ranf()/1e1)
					print >>sys.stderr, ct('\t -->',GREEN)+ct(' [',WHITE)+ct('DISCONNECTING', GREEN)+ct(']',WHITE)+ct('[',WHITE)+ct(str(server_address[1]),CYAN)+ct(']',WHITE)
					s.close()
					sleep(ranf()/1e1)
					print >>sys.stderr, ct('\t -->',GREEN)+ct(' [',WHITE)+ct('DISCONNECTED', GREEN)+ct(']',WHITE)
					sleep(2 * ranf()/1e1)


				sleep(ranf())
			sleep(ranf())
			HOLD_FH = False
		sleep(ranf())

	except Exception as e:
		print "\n\n", format_exc()
		hold = raw_input("Press Enter to Continue.")

	except KeyboardInterrupt:
		print >>sys.stderr, ' --> [PAUSED CONTROLLER]'
		if raw_input(" --> Exit? [yes/No]") == "yes":
			print >>sys.stderr, ' --> [CLOSING CONTROLLER]'
			s.shutdown(socket.SHUT_RDWR)
			sys.exit(0)
		else:
			continue

s.shutdown(socket.SHUT_RDWR)
"""