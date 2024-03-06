




'''
	{
		"name": "hotties: add",
		"fields": {
			"name": "",
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
	
	existing_document = hotties.find_one ({
		"flavor": flavor
	})
	if existing_document:
		return {
			"status": "fail",
			"note": "That flavor of hottie is already added."
		}
		
	vibes.insert_one ({
		"name": fields ["name"],
		"flavor": flavor
	})

	return {
		"status": "pass"
	}
	
	
	
	
#