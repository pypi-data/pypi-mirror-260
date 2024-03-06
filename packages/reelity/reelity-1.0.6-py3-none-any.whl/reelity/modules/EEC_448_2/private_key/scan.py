


'''
	import reelity.modules.EEC_448_2.private_key.scan as private_key_scan
	private_key_scan = private_key_scan.start (path) ["hexadecimal string"]
'''

from Crypto.PublicKey import ECC
from fractions import Fraction

import json

def start (path, format):

	if (format == "JSON"):
		with open (path, mode = 'r') as file:
			JSON_string = file.read ()
			
			return json.loads (JSON_string)
		

	if (format == "DER"):
		with open (path, mode = 'rb') as file:
			byte_string = file.read ()
			instance = ECC.import_key (
				byte_string,
				curve_name = "Ed448"
			)
			hexadecimal_string = byte_string.hex ().upper ()

			class private_key:
				def __init__ (this, instance):
					this.instance = instance
				
			return {
				"DER hexadecimal string": hexadecimal_string,
				"DER byte string": byte_string,
				"instance": instance,
			}
			
	raise Exception ("...")

