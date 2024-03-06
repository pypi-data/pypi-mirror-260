
'''
	{
		"name": "",
		"fields": {
			"name": "",
			"seed": ""
		}
	}
'''

import pymongo

import reelity.instrument.climate as instrument_climate
import reelity.instrument.moon.connect as moon_connect
import reelity.modules.EEC_448_2.keys as EEC_448_2_key_creator	

def perform (fields):
	assert (len (fields ["seed"]) == 114) 
	assert (len (fields ["name"]) >= 1)

	moon_connection = moon_connect.start ()
	vibes = moon_connection ["pocket"] ["vibes"]
	
	keys = EEC_448_2_key_creator.create (
		seed = fields ["seed"]
	)
	address = "ECC_448_2:" + keys ["public"] ["hexadecimal string"]


	'''
		Check if that vibe already exists.
	'''	
	existing_document = vibes.find_one ({
		"flavor": address
	})
	if existing_document:
		return {
			"status": "fail",
			"note": "A vibe with that address already exists"
		}
	
	vibes.insert_one ({
		"name": fields ["name"],
		"kind": "ECC_448_2",
		"flavor": "ECC_448_2:" + keys ["public"] ["hexadecimal string"],
		"showy": {
			"hexadecimal string": keys ["public"] ["hexadecimal string"]
		},
		"intimate": {
			"hexadecimal string": keys ["private"] ["hexadecimal string"]
		},
		"seed": {
			"hexadecimal string": fields ["seed"]
		}
	})

	return {
		"status": "pass"
	}