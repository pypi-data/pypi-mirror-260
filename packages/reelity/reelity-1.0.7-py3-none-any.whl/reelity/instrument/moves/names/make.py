
'''
	
'''

'''
	create_instrument
	
	fields {
		"label": ""
	}
'''



import reelity.instrument.climate as instrument_climate

import os
from os.path import dirname, join, normpath
import pathlib
import sys

def play (fields):

	'''
	import reelity.instrument.climate as instrument_climate
	instrument_climate.build (CWD)

	import reelity.instrument.moon as mongo_node
	mongo_node.start (
		param = {
			"directory": "",
			"port": "27107"
		}
	)
	'''

	offline_climate = instrument_climate.retrieve ()
	instruments_paths = offline_climate ["paths"] ["instrument"]
	
	if ("label" not in fields):
		return {
			"status": "fail",
			"note": f'Please choose a "label" for the instrument.'
		}
	
	instrument_label = fields ["label"]
	instrument_path = str (normpath (join (instruments_paths, instrument_label)))

	if (os.path.isdir (instrument_path) != True):
		os.mkdir (instrument_path)
		instrument_climate.climate ["elected instrument"] ["path"] = instrument_path
		return {
			"status": "pass",
			"note": "instrument created"
		}
		
	else:
		instrument_climate.climate ["elected instrument"] ["path"] = instrument_path
		return {
			"status": "fail",
			"note": "There is already a directory at that path"
		}
