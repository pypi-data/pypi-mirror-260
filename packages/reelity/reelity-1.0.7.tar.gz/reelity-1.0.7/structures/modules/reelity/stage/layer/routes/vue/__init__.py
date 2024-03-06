



#
#
import json
from os.path import exists, dirname, normpath, join
#
#


#
#
from flask import Flask, request, send_file, request, make_response, send_from_directory, Response
#from flask_cors import CORS
#from flask_limiter import Limiter
#from flask_limiter.util import get_remote_address
#from flask_socketio import SocketIO, emit
#



def route (
	app = {},
	vue_dist_inventory = None
):
	assert (type (vue_dist_inventory) == dict), type (vue_dist_inventory)

	@app.route ('/', methods = [ 'GET' ])
	def home ():	
		return Response (
			vue_dist_inventory ["index.html"] ["content"], 
			mimetype = vue_dist_inventory [ "index.html" ] ["mime"],
			headers = {}
		)	
				
	@app.route ('/<path:route_path>', methods = [ 'GET' ])
	def send_report (route_path):		
		print ("route:", route_path)
	
		try:
			if (route_path in vue_dist_inventory):
				print ('route is in inventory')
			
				content = vue_dist_inventory [ route_path ] ["content"]
				mimetype = vue_dist_inventory [ route_path ] ["mime"]
				
				headers = {}
				
				return Response (
					content, 
					mimetype = mimetype,
					headers = headers
				)	
					
			else:
				print ("doesn't exist")

		except Exception as E:
			print ("exception:", E)
			pass
			
		return Response (
			vue_dist_inventory ["index.html"] ["content"], 
			mimetype = vue_dist_inventory [ "index.html" ] ["mime"],
			status = 600
		)