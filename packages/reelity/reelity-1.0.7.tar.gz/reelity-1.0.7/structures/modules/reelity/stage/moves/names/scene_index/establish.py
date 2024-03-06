



import pymongo

import reelity.stage.climate as instrument_climate
import reelity.stage.moon.connect as moon_connect

'''
	
'''
def perform (fields):
	moon_connection = moon_connect.start ()
	scene_1 = moon_connection ["scenes"] ["index"]

	name = "scene index"
	existing_document = scene_1.find_one ({
		"name": name
	})
	if existing_document:
		return {
			"status": "fail",
			"note": "That move has already occurred."
		}

	'''
		validate that has enough splendor
	'''
	move_number = str (scene_1.count_documents ({}) + 1)
	scene_1.insert_one ({
		"name": name,
		
		"last scene #": "1"
	})


	return {
		"status": "pass"
	}
	
	
	
	
#