


'''
	import reelity.stage.climate as stage_climate
	climate = stage_climate.retrieve ()
'''

import os
from os.path import dirname, join, normpath
import pathlib
import sys


climate = {
	"elected stage": {},
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
	stage_path = None
):		
	if (os.path.isdir (stage_path) != True):
		os.mkdir (stage_path)
		print ("The stage was made.")
	else:
		print ()
		print ("There's already something at the path of the stage.")
		print (stage_path)
		print ()

	#climate ["paths"] ["offline_good"] = offline_goods
	climate ["paths"] ["stage"] = stage_path
	

	return;


def retrieve ():
	return climate