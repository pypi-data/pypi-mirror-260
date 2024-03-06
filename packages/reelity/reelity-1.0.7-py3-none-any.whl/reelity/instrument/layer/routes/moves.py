
from flask import Flask, request
import rich

import reelity.instrument.moves as moves

import json
import traceback

def route (app):
	records = 1;

	@app.route ("/", methods = [ 'PATCH' ])
	def route ():
		data = ""
		
		print ("A patch request was received.")
		
		try:
			data = request.get_data ();
			
			UTF8 = data.decode ('utf-8')
			if (records >= 1): print ("UTF8 ::", UTF8)
			
			JSON = json.loads (UTF8)
			if (records >= 1): print ("JSON ::", json.dumps (UTF8))
			
			data = moves.perform (move = JSON)
			if (records >= 1): rich.print_json (data = data)
			
			response = app.response_class (
				response = json.dumps (data),
				status = 200,
				mimetype = 'application/json'
			)

			return response
			
		except Exception as E:
			print ("exception:", traceback.format_exc ())
	
		return json.dumps ({
			"obstacle": ""
		})