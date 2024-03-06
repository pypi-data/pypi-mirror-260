


'''
	import reelity.modules.EEC_448_2.public_key.scan as public_key_scan
	public_key_scan.start (public_key_path, "JSON") ["public key"] ["DER hexadecimal string"]
'''


#
#	https://pycryptodome.readthedocs.io/en/latest/src/public_key/ecc.html#Crypto.PublicKey.ECC.import_key
#

from Crypto.PublicKey import ECC

import json

def start (path, format):
	if (format == "JSON"):
		with open (path, mode = 'r') as file:
			JSON_string = file.read ()
			
			return json.loads (JSON_string)

	if (format == "DER"):
		with open (path, mode = 'rb') as file:
			public_key_bytes = file.read ()
			
			public_key = ECC.import_key (
				public_key_bytes,
				curve_name = "Ed448"
			)
			
			public_key_string = public_key_bytes.hex ()

			return [ 
				public_key, 
				public_key_bytes, 
				public_key_string 
			];
		
	raise Exception ("")

