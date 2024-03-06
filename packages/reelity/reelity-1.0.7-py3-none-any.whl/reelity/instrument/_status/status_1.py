
'''
	python3 "_status/status.proc.py" "instrument/_status/status_1.py"
'''


import os

from os.path import dirname, join, normpath

import atexit
import pathlib
import shlex
import signal
import sys
import subprocess

this_directory_path = str (pathlib.Path (__file__).parent.resolve ())
instrument_start_path = str (normpath (join (this_directory_path, "../start.proc.py")))

def check_1 ():
	#os.system (f'python3 "{ instrument_start_path }" layer start')

	the_process = None

	def stop ():
		print ("atexit!");
		the_process.kill ()

	'''
		This might only work if this is called:
			process.wait () 
	'''
	print ("registering atexit stop")	
	atexit.register (stop)

	import time
	time.sleep (1)

	#command_string = f'python3 "{ instrument_start_path }" layer start'
	#popen_string = shlex.split (command_string);
	
	popen_string = [
		sys.executable,
		instrument_start_path,
		"layer",
		"start"
	]
	
	print ("popen_string:", popen_string)
	
	#
	#	https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true/4791612#4791612
	#
	the_process = subprocess.Popen (
		popen_string,
		#shell = True, 
		cwd = this_directory_path,
		
		preexec_fn = os.setsid
	)
	
	print ("process PID:", the_process.pid)
	
	import time
	time.sleep (1)
	
	os.killpg (os.getpgid (the_process.pid), signal.SIGTERM)
	the_process.kill ()
	print ('killed the process', the_process)
	
	time.sleep (2)
	
	print ()
	print ("got to here.")
	print ()

	return;
	
	
checks = {
	'check 1': check_1
}