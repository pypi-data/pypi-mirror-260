




'''
	import reelity.stage.moves.names.scene_index.freshest as scene_index_freshest
	freshest = scene_index_freshest.perform ({}) ["fields"] ["freshest"];
'''


import pymongo

import reelity.stage.climate as instrument_climate
import reelity.stage.moon.connect as moon_connect

'''
	
'''
def perform (fields):
	moon_connection = moon_connect.start ()
	scene_index = moon_connection ["scenes"] ["index"]

	documents = list (scene_index.find ({
		"name": "scene index"
	}))	
	if (len (documents) != 1):
		return {
			"status": "fail",
			"note": f"{ len (documents) } index documents found.  There should only be 1."
		}

	return {
		"status": "pass",
		"fields": {
			"freshest": documents [0] ["scene #"]
		}
	}
	
	
	
	
#