



import os
import rich
import reelity.stage.moves as stage_moves

import reelity.stage.layer._clique as clique_layer

def start ():
	import click
	@click.group ("stage")
	def group ():
		pass

	'''
		stage make --layer-port 50002 --mongo-port 50003
	'''
	import click
	@group.command ("make")
	@click.option ('--layer-port', '-tp', default = '55500')
	@click.option ('--mongo-port', '-mp', default = '55501')
	@click.option ('--name', default = 'stage')
	def search (layer_port, mongo_port, name):	
		CWD = os.getcwd ();
	
		effect = stage_moves.perform (
			move = {
				"name": "make",
				"fields": {
					"CWD": CWD,
					"name": name,
					"layer port": "",
					"mongo port": ""
				}
			}
		)
		
		rich.print_json (data = effect)
	
		return;

	group.add_command (clique_layer.add ())

	return group




#



