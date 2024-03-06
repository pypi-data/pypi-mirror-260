

import reelity.stage.moves.names.scene_index.freshest as scene_index_freshest



import pymongo

import reelity.stage.climate as instrument_climate
import reelity.stage.moon.connect as moon_connect

'''
	
'''
def perform (fields):
	moon_connection = moon_connect.start ()
	
	freshest = scene_index_freshest.perform ({}) ["fields"] ["freshest"];
	
	the_scene = moon_connection ["scenes"] [f"scene-{ freshest }"]
	the_moves = list (the_scene.find ({}, {"_id": 0}))
	
	return {
		"status": "pass",
		"fields": {
			"scene #": freshest,
			"moves": the_moves
		}
	}