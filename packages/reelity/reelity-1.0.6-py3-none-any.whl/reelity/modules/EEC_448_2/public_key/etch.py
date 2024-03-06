



'''
	import reelity.modules.EEC_448_2.public_key.write as write_EEC_448_2_public_key
	write_EEC_448_2_public_key.start (
		path,
		public_key_string,
		format
	)
'''

import os

def start (
	path, 
	public_key_string, 
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
	
	f.write (public_key_string)
	f.close ()
	
	return True
	
