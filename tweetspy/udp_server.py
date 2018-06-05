#SOl Courtney Columbia U Department of Astronomy and Astrophysics NYC 2016
#swc2124@columbia.edu

#--[DESCRIPTION]---------------------------------------------------------#

'''
Date: May 2016

UDP Server for the Cluster

'''

#--[PROGRAM-OPTIONS]------------------------------------------------------#

import socket

from time import gmtime, strftime,sleep

from astropy.table import Table

import numpy as np

import sys

import os

LOG_FILE = '/home/sol/CLUSTER_RAID/'

#--[PROGRAM-OPTIONS]------------------------------------------------------#


LookUp = {

	'Wolf-01': 0,
	'Wolf-02': 0,
	'Wolf-03': 0,
	'Wolf-04': 0,
	'Wolf-05': 0,
	'Wolf-06': 0,
	'Wolf-07': 0,
	'Wolf-08': 0,

	'Wolf-09': 0,
	'Wolf-10': 0,
	'Wolf-11': 0,
	'Wolf-12': 0,
	'Wolf-13': 0,
	'Wolf-14': 0,
	'Wolf-15': 0,
	'Wolf-16': 0,

	'BPI-M1-01': 0,
	'BPI-M1-02': 0,
	'BPI-M1-03': 0,
	'BPI-M1-04': 0,
	'BPI-M1-05': 0,
	'BPI-M1-06': 0,
	'BPI-M1-07': 0,
	'BPI-M1-08': 0,

	'BPI-M1-09': 0,
	'BPI-M1-10': 0,
	'BPI-M1-11': 0,
	'BPI-M1-12': 0,
	'BPI-M1-13': 0,
	'BPI-M1-14': 0,
	'BPI-M1-15': 0,
	'BPI-M1-16': 0
}

def getNetworkIp():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	s.connect(('<broadcast>', 0))
	return s.getsockname()[0]

s = socket.socket()
host = str(getNetworkIp())
port = 15000
server_address = (str(host), port)

hostname = socket.gethostname()
s.bind(server_address)
s.listen(100)

Names = ['Host', 'Jobs_done', 'CPU_temp', 'CPU_usage', 'CPU_freq', 'Core_volts',
		 'Ram_usage', 'Sent', 'Recv']

Dtype = ['S10', np.uint64,
         np.float16, np.float16, np.float16, np.float16, np.float16,
         np.uint64, np.uint64]

Log_Table = Table(names=Names, dtype=Dtype)

while True:

	conn, client_address = s.accept()
	data = conn.recv(2048)
	if data:
		_row = data.split(' ')
		_name = _row[0]
		_index = np.nonzero(Log_Table['Host']==_name)[0]

		if _name in Log_Table['Host']:
			LookUp[_name] += int(_row[1])
			_row[1] = LookUp[_name]
			Log_Table[_index] = _row
			Log_Table[_index]['Jobs_done'] = LookUp[_name]
		else:
			LookUp[_name] += int(_row[1])
			Log_Table.add_row(_row)

		Log_Table.sort("Jobs_done")
		Log_Table.reverse()
		conn.close()
		os.system('clear')
		Log_Table.pprint(max_lines=40, max_width=500, show_name=True, show_unit=True, show_dtype=False, align="^")

		Log_Table.write("./logtable", format="hdf5", path="data", append=True, overwrite=True)

