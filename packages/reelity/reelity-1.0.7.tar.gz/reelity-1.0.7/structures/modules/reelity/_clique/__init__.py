




#from reelity._clique.group import clique as clique_group

import reelity.instrument.clique as instrument_clique
import reelity.stage.clique as stage_clique

import click

def intro ():
	@click.group ()
	def group ():
		pass

	@click.command ("tutorial")
	def sphene_command ():	
		import pathlib
		from os.path import dirname, join, normpath
		this_directory = str (pathlib.Path (__file__).parent.resolve ())
		module_directory = str (normpath (join (this_directory, "..")));

		import carbonado
		carbonado.start ({			
			#
			#	This is the node from which the traversal occur.
			#
			"directory": module_directory,
			
			#
			#	This path is removed from the absolute path of share files found.
			#
			"relative path": module_directory
		})
		
		import time
		while True:
			time.sleep (1000)

	group.add_command (sphene_command)
	group.add_command (instrument_clique.start ())
	group.add_command (stage_clique.start ())
	
	return group;




#
