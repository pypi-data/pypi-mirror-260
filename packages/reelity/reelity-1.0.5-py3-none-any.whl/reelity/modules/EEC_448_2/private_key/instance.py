


'''
	import reelity.modules.EEC_448_2.private_key.instance as instantiate_private_key
	private_key_instance = instantiate_private_key.from_DER_hexadecimal_string (DER_hexadecimal_string)
'''

'''
	DER_key_string = private_key_instance.export_key (
		format = "DER"
	)	
	PEM_key_string = private_key_instance.export_key (
		format = "PEM"
	)
'''

import reelity.modules.EEC_448_2.modulators.byte_string.from_hexadecimal as hexadecimal_to_byte_string

from Crypto.PublicKey import ECC

def from_DER_hexadecimal_string (DER_hexadecimal_string):
	instance = ECC.import_key (
		hexadecimal_to_byte_string.modulate (DER_hexadecimal_string),
		curve_name = "Ed448"
	)
	
	'''
		assertions
	'''
	DER_key_string = instance.export_key (
		format = "DER"
	)
	hexadecimal_string = DER_key_string.hex ().upper ()
	assert (len (hexadecimal_string) == 146), len (hexadecimal_string)
	assert (bytes.fromhex (hexadecimal_string) == DER_key_string)
	
	
	return instance;