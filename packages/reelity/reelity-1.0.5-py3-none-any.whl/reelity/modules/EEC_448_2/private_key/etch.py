
'''
	import reelity.modules.EEC_448_2.private_key.etch as etch_EEC_448_private_key
	etch_EEC_448_private_key.start (path, private_key_string, "JSON")
'''

'''
	{ form, save, write, compose, produce, etch }
'''

import os

def start (
	path, 
	private_key_string, 
	format
):
	if (os.path.exists (path)):
		raise Exception (f"The path for the private_key is not available. '{ path }'");
	
	if (format == "DER"):
		f = open (path, 'wb')
		
	elif (format in [ "PEM", "hexadecimal", "JSON" ]):
		f = open (path, 'w')
		
	else:
		raise Exception (f"format '{ format }' was not accounted for.")
	
	f.write (private_key_string)
	f.close ()
	
	return True