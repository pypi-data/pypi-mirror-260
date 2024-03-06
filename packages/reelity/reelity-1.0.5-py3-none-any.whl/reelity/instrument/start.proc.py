




def add_paths_to_system (paths):
	from os.path import dirname, join, normpath
	import pathlib
	import sys
	
	this_folder = pathlib.Path (__file__).parent.resolve ()
	for path in paths:
		sys.path.insert (0, normpath (join (this_folder, path)))

add_paths_to_system ([
	'../../../modules',
	'../../../modules_pip'
])

from reelity.instrument import start_clique; start_clique ()