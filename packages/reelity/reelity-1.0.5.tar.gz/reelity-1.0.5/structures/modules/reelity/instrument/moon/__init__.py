

'''
	import reelity.instrument.moon as instrument_mongo
	instrument_mongo.start (
		param = {
			"directory": "",
			"port": "27107"
		}
	)
'''

'''
	from multiprocessing import Process
	mongo = Process (
		target = instrument_mongo.start,
		args = (),
		kwargs = {
			"params": {
				"DB_directory": mongo_DB_directory,
				"port": str (mongo_port)
			}
		}
	)
	mongo.start ()
'''


'''
	mongod --dbpath ./mongo_DB --port 27018
'''
import law_dictionary

import subprocess
def start (
	params = {}
):
	law_dictionary.check (	
		allow_extra_fields = True,
		laws = {
			"DB_directory": {
				"required": True,
				"type": str
			},
			"port": {
				"required": True,
				"type": str
			}
		},
		dictionary = params
	)

	port = params ["port"]
	DB_directory = params ["DB_directory"]

	subprocess.run (
		f"mongod --dbpath '{ DB_directory }' --port '{ port }'", 
		shell = True, 
		check = True
	)
	
	#import pymongo
	#client = pymongo.MongoClient("localhost", 27017)