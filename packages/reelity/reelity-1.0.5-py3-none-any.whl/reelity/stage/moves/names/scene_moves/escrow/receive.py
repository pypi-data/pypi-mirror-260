





import pymongo

import reelity.stage.climate as instrument_climate
import reelity.stage.moon.connect as moon_connect



'''
	
'''
def perform (fields):
	moon_connection = moon_connect.start ()
	scene_1 = moon_connection ["scenes"] ["scene-2"]

	move = "escrow: receive"
	move_number = str (scene_1.count_documents ({}) + 1)


	return {
		"status": "pass"
	}
	
	
	
	
#