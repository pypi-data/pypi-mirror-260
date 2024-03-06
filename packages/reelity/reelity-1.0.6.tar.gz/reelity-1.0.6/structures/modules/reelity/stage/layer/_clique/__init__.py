



import reelity.stage.layer.start_dev as flask_start_dev
import reelity.stage.moves as stage_moves

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
		stage layer start --label stage_1 --layer-port 50002 --mongo-port 50003
	'''
	import os
	import click
	@group.command ("start")
	@click.option ('--name', default = 'stage')
	@click.option ('--layer-port', '-sp', default = '50002')
	@click.option ('--mongo-port', '-mp', default = '50003')
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
		effect = stage_moves.perform (
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
		stage layer create_safe --label stage-1
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



