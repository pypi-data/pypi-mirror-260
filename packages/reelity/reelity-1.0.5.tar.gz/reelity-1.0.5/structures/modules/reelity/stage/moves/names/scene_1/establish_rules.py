



import pymongo

import reelity.stage.climate as instrument_climate
import reelity.stage.moon.connect as moon_connect

'''
	{
		"rules": {
			"change >=": "1/2"
		},
		"scenes": {
			"moves per scene": "100"
		},
		"escrow": {
			"scene limit": 100
		},
		"fees": {
			"price": 1000
		}
	}
'''
def perform (fields):
	moon_connection = moon_connect.start ()
	scene_1 = moon_connection ["scenes"] ["scene-1"]

	move = "scene 1: establish rules"

	existing_document = scene_1.find_one ({
		"move": move
	})
	if existing_document:
		return {
			"status": "fail",
			"note": "That move has already occurred."
		}

	move_number = str (scene_1.count_documents ({}) + 1)

	scene_1.insert_one ({
		"move": move,
		"move #": move_number,
		
		"rules": {
			"rules": {
				"change >=": "1/2"
			},
			"scenes": {
				"moves per scene": "100"
			},
			"escrow": {
				"scene limit": "100"
			},
			"fees": {
				"price": "1000"
			}
		}		
	})


	return {
		"status": "pass"
	}
	
	
	
	
#