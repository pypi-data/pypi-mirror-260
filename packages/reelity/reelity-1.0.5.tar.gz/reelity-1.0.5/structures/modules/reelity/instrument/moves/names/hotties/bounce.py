


'''
	{
		"name": "hotties: bounce",
		"fields": {
			"flavor": ""
		}
	}
'''



import pymongo

import reelity.instrument.climate as instrument_climate
import reelity.instrument.moon.connect as moon_connect

def perform (fields):
	moon_connection = moon_connect.start ()
	hotties = moon_connection ["pocket"] ["hotties"]
	
	proceeds = collection.delete_one ({
		"flavor": fields ["flavor"]
	})
	if proceeds.deleted_count != 1:
		return {
			"status": "fail",
			"notes": f"{ result.deleted_count } document were deleted."
		}

	return {
		"status": "pass"
	}
	
	
	
	
#
