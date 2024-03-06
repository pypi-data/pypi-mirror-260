
'''


'''


import os

import reelity.instrument.sockets.clique_group as clique_group
import reelity.instrument.layer._clique as clique_layer

import reelity.stage.moves as stage_moves


def start ():
	import click
	@click.group ("instrument")
	def group ():
		pass
	
	
	'''
		instrument sockets --port 65000
	'''
	import click
	@group.command ("make")
	@click.option ('--layer-port', '-tp', default = '10000')
	@click.option ('--mongo-port', '-mp', default = '10001')
	@click.option ('--name', default = 'instrument-1')
	def search (layer_port, mongo_port, name):	
		CWD = os.getcwd ();
		effect = stage_moves.perform (
			move = {
				"name": "make",
				"fields": {
					"CWD": CWD,
					"name": name,
					"layer port": layer_port,
					"mongo port": mongo_port
				}
			}
		)

		return;
		
		
	
	group.add_command (clique_group.add ())
	group.add_command (clique_layer.add ())
	
	
	
	#group.add_command (instrument_clique_tracks ())
	#group.add_command (instrument_clique_socket ())
	#group.add_command (stage_clique ())
	
	#group ()
	
	return group




#
