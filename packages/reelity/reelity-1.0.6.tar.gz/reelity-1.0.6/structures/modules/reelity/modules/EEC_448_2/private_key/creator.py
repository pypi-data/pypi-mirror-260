

'''
	seed = "4986888b11358bf3d541b41eea5daece1c6eff64130a45fc8b9ca48f3e0e02463c99c5aedc8a847686d669b7d547c18fe448fc5111ca88f4e8"

	import reelity.modules.EEC_448_2.private_key.creator as EEC_448_2_private_key_creator
	EEC_448_2_private_key_creator.create (
		seed
	)
	
	private_key_instance = private_key ["instance"]
	private_key_hexadecimal = private_key ["hexadecimal string"]
'''


'''
	options:
		seed:
			4986888b11358bf3d541b41eea5daece1c6eff64130a45fc8b9ca48f3e0e02463c99c5aedc8a847686d669b7d547c18fe448fc5111ca88f4e8
			5986888b11358bf3d541b41eea5daece1c6eff64130a45fc8b9ca48f3e0e02463c99c5aedc8a847686d669b7d547c18fe448fc5111ca88f4e8
			4986888B11358BF3D541B41EEA5DAECE1C6EFF64130A45FC8B9CA48F3E0E02463C99C5AEDC8A847686D669B7D547C18FE448FC5111CA88F4E8
			
		format:
			DER
			PEM
'''

'''
	https://pycryptodome.readthedocs.io/en/latest/src/public_key/ecc.html
'''
from Crypto.PublicKey.ECC import EccKey
import os.path

def create (seed):	
	assert (len (seed) == 114)

	instance = EccKey (
		curve = "Ed448", 
		seed = bytes.fromhex (seed)
	)
	DER_key_string = instance.export_key (
		format = "DER"
	)	
	PEM_key_string = instance.export_key (
		format = "PEM"
	)
	
	#
	#	https://stackoverflow.com/questions/6624453/whats-the-correct-way-to-convert-bytes-to-a-hex-string-in-python-3
	#
	#
	#	138 characters
	#
	hexadecimal_string = DER_key_string.hex ().upper ()
	assert (len (hexadecimal_string) == 146), len (hexadecimal_string)
	assert (bytes.fromhex (hexadecimal_string) == DER_key_string)
		
	return {		
		"instance": instance, 
		
		"DER byte string": DER_key_string,
		"DER hexadecimal string": hexadecimal_string,
		
		"PEM string": PEM_key_string
	}