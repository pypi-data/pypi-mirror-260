

'''

'''


import json
from os.path import dirname, join, normpath
import os
import traceback

import rich
from flask import Flask, request
import flask_cors

import reelity.stage.layer.utilities.generate_path_inventory as generate_path_inventory
import reelity.stage.climate as stage_climate
	
from .routes import connect_routes

def build (
	records = 1
):
	climate = stage_climate.retrieve ()

	print ("starting stage flask service")
	rich.print_json (data = {
		"variables": {
			"frontend dist": climate ["paths"] ["frontend dist"]
		}
	})

	app = Flask (__name__)
	flask_cors.CORS (app)
	
	'''
	
	'''
	vue_dist_inventory = generate_path_inventory.beautifully (
		climate ["paths"] ["frontend dist"]
	)
	#for entry in vue_dist_inventory:
	#	print (vue_dist_inventory [entry] ["path"])
	
	connect_routes (
		app,
		vue_dist_inventory
	)
	
	

	
	
	return app;