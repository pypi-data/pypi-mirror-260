



import reelity.instrument.layer.start_dev as flask_start_dev
import reelity.instrument.moves as instrument_moves

import atexit
import os
from os.path import dirname, join, normpath
import pathlib
import sys
		
		
def add ():
	import click
	@click.group ("layer")
	def group ():
		pass

	'''
		instrument layer start --label instrument_1 --layer-port 50000 --mongo-port 50001
	'''
	import os
	import click
	@group.command ("start")
	@click.option ('--name', default = 'instrument')
	@click.option ('--layer-port', '-sp', default = '50000')
	@click.option ('--mongo-port', '-mp', default = '50001')
	def start (name, layer_port, mongo_port):
		def stop ():
			print ("--")
			print ("layer start atexit!");
			print ("--")

		def stop_2 ():
			print ("--")
			print ("layer start atexit 2!");
			print ("--")
		
		atexit.register (stop)
		atexit.register (stop_2)
		
		'''
			This might only work if this is called:
				process.wait () 
		'''
		
	
		CWD = os.getcwd ();
		effect = instrument_moves.perform (
			move = {
				"name": "layer: start",
				"fields": {
					"CWD": CWD,
					"name": name,
					"layer port": layer_port,
					"mongo port": mongo_port
				}
			}
		)
	
		print ("effect:", effect)
	
		return;
	
		'''
		import sys
		from os.path import dirname, join, normpath
		import pathlib
		CWD = os.getcwd ();
		mongo_DB_directory = str (normpath (join (CWD, label, "mongo_DB_directory")))
		instrument_path = str (normpath (join (CWD, label)))
		
		import reelity.instrument.climate as instrument_climate
		instrument_climate.build (
			instrument_path = instrument_path
		)
		
		if (not os.path.exists (mongo_DB_directory)):			
			os.mkdir (mongo_DB_directory) 
			
		if (not os.path.isdir (mongo_DB_directory)):
			print ("There is already something at:", mongo_DB_directory)
			return;
		
		from multiprocessing import Process
		
		import reelity.instrument.moon as instrument_mongo
		mongo = Process (
			target = instrument_mongo.start,
			args = (),
			kwargs = {
				"params": {
					"DB_directory": mongo_DB_directory,
					"port": str (mongo_port)
				}
			}
		)
		mongo.start ()
	

		flask_server = Process (
			target = flask_start_dev.start,
			args = (),
			kwargs = {
				"port": service_port
			}
		)
		flask_server.start ()
		
	
		import time
		while True:
			time.sleep (1000)
		'''
		
		return;


	'''
		instrument layer create_safe --label instrument-1
	'''
	import click
	@group.command ("create_safe")
	@click.option ('--label', required = True)
	@click.option ('--port', '-np', default = '50000')
	def create_safe (label, port):	
		address = f"http://127.0.0.1:{ port }"
	
		import json
		from os.path import dirname, join, normpath
		import os
		import requests
		r = requests.patch (
			address, 
			data = json.dumps ({
				"label": "create safe",
				"fields": {
					"label": label
				}
			})
		)
		print (r.text)
		
		return;
		
	return group




#



