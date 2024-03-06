


'''
	
'''

'''
	create_instrument
	
	fields {
		"label": ""
	}
'''


from multiprocessing import Process

import reelity.instrument.climate as instrument_climate
import reelity.instrument.moon as instrument_mongo

import os
from os.path import dirname, join, normpath
import pathlib
import sys

def perform (move):
	mongo_DB_directory = move ["mongo directory"]
	mongo_port = move ["mongo port"]

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
	
