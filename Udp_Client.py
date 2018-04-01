#SOl Courtney Columbia U Department of Astronomy and Astrophysics NYC 2016 
#swc2124@columbia.edu

#--[DESCRIPTION]---------------------------------------------------------#

'''
Date: May 2016

UDP Client for the Cluster

'''

#--[PROGRAM-OPTIONS]------------------------------------------------------#

from subprocess import PIPE, Popen

from time import gmtime, strftime, sleep

import socket, time

import psutil


#--[PROGRAM-OPTIONS]------------------------------------------------------#


def bytes2human(n):
	symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
	prefix = {}
	for i, s in enumerate(symbols):
		prefix[s] = 1 << (i + 1) * 10
	for s in reversed(symbols):
		if n >= prefix[s]:
			value = float(n) / prefix[s]
			return '%.2f %s' % (value, s)
	return '%.2f B' % (n)

def get_cpu_temperature():
		try:
			output, _error = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE).communicate()
			return float(output[output.index('=') + 1:output.rindex("'")])
		except:
			return '1'

def get_cpu_freq():
	try:
		output, _error = Popen(['vcgencmd', 'measure_clock arm'], stdout=PIPE).communicate()
		return str(float(output[14:])/1e6)
	except:
		output, _error = Popen(['cat', '/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq'], stdout=PIPE).communicate()
		return str(float(output[:6])/1e3)

def get_cpu_volts():
	try:
		output, _error = Popen(['vcgencmd', 'measure_volts core'], stdout=PIPE).communicate()
		return str(output[5:11])
	except:
		return '1'

def Network_Traf(more=False):
	try:
		tot_before = psutil.net_io_counters()
		pnic_before = psutil.net_io_counters(pernic=True)
		interval = 0.5;
		time.sleep(interval)
		tot_after = psutil.net_io_counters()
		pnic_after = psutil.net_io_counters(pernic=True)
		return str(tot_after.bytes_sent), str(tot_after.bytes_recv).rstrip('\n')
	except:
		return '1','1'

def Log_File(jobs_done):

	cpu_temp 	= str(get_cpu_temperature()) 
	cpu_usage 	= str(psutil.cpu_percent())
	cpu_freq 	= get_cpu_freq()
	core_volts	= get_cpu_volts()
	free_ram 	= str(psutil.virtual_memory().percent)
	sent, recv 	= Network_Traf()
	hostname 	= str(socket.gethostname())
	return str(hostname+' '+str(jobs_done)+' '+cpu_temp+' '+cpu_usage+' '+cpu_freq+' '+core_volts+' '+free_ram+' '+sent+' '+recv)


def Report(jobs_done):


	sock = socket.socket()

	server_address = ('192.168.1.103', 15000)

	message = Log_File(jobs_done)

	try:
			
		#print >>sys.stderr, 'sending "%s"' % message
		sock.connect(server_address)
		sock.sendall(message)


	finally:

		#print >>sys.stderr, 'closing socket'
		sock.close()

