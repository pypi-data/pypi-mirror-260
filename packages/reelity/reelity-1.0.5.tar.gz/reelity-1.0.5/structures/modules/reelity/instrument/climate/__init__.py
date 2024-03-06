
'''
	import reelity.instrument.climate as instrument_climate
	climate = instrument_climate.retrieve ()
'''

import os
from os.path import dirname, join, normpath
import pathlib
import sys


climate = {
	"elected instrument": {},
	"paths": {
		"frontend dist": str (
			normpath (join (
				pathlib.Path (__file__).parent.resolve (), 
				"../frontend"
			))
		)
	}
}

def build (
	instrument_path = None
):		
	if (os.path.isdir (instrument_path) != True):
		os.mkdir (instrument_path)
		print ("The instrument was made.")
	else:
		print ()
		print ("There's already something at the path of the instrument.")
		print (instrument_path)
		print ()

	#climate ["paths"] ["offline_good"] = offline_goods
	climate ["paths"] ["instrument"] = instrument_path
	

	return;


def retrieve ():
	return climate