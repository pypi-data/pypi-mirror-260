
'''
	import reelity.stage.layer.utilities.generate_path_inventory as generate_path_inventory
	generate_path_inventory.start ()
'''


'''
	https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
'''

import glob
import os

def beautifully (folder):
	inventory_glob = folder + "/**/*"
	inventory = glob.glob (folder + "/**/*", recursive = True)
	
	inventory_partials = {}
	for inventory_path in inventory:
		if (os.path.isfile (inventory_path)):
			FP = open (inventory_path, "rb")
			content = FP.read () 
			FP.close ()
		
			extension = inventory_path.split ('.') [-1].lower ()
			mime = ""
			if (extension == "css"):
				mime = "text/css"
			elif (extension == "ico"):
				mime = "image/x-icon"
			elif (extension == "js"):
				mime = "text/javascript"
			elif (extension == "html"):
				mime = "text/html"
			elif (extension == "jpg"):
				mime = "image/jpg"
			elif (extension == "png"):
				mime = "image/png"
			else:
				raise Exception (f"Extension '{ extension }' was not accounted for.")
		
			inventory_partials [ inventory_path.split (folder + "/") [1] ] = {
				"path": inventory_path,
				"content": content,
				"extension": extension,
				"mime": mime
			};

	print ("path inventory size:", len (inventory))

	#for inventory_path in inventory:
	#	print ("inventory_path:", inventory_path)	
		
	return inventory_partials