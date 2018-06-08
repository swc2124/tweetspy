'''
---------------------
The UDP Server Module
---------------------
Date: May 2016

UDP Server for the Cluster

'''


s = socket.socket()
host = str(getNetworkIp())
port = 15000
server_address = (str(host), port)

hostname = socket.gethostname()
s.bind(server_address)
s.listen(100)

Names = ['Host', 'Jobs_done', 'CPU_temp',
		 'CPU_usage', 'CPU_freq', 'Core_volts',
		 'Ram_usage', 'Sent', 'Recv']

Dtype = ['S10', np.uint64, np.float16,
		 np.float16, np.float16, np.float16,
		 np.float16, np.uint64, np.uint64]

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

