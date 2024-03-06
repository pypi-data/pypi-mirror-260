
'''
	#
	#	write public key to path
	#
	import reelity.modules.EEC_448_2.public_key.creator as EEC_448_2_public_key_creator
	public_key = EEC_448_2_public_key_creator.create (
		private_key_instance
	)
	public_key_instance = public_key ["instance"]
	public_key_DER_hexadecimal_string = public_key ["DER hexadecimal string"]
		
'''

'''
	format:
		DER
		PEM
'''
import os

from Crypto.PublicKey.ECC import EccKey
from Crypto.PublicKey import ECC

import reelity.modules.EEC_448_2.private_key.scan as private_scan


def create_DER_hexadecimal_string (public_key_DER_byte_string):
	public_key_DER_hexadecimal_string = public_key_DER_byte_string.hex ()
	assert (len (public_key_DER_hexadecimal_string) == 138)
	assert (
		bytes.fromhex (public_key_DER_hexadecimal_string) == 
		public_key_DER_byte_string
	)
	
	return public_key_DER_hexadecimal_string

def create (
	private_key_instance = None
):	
	public_key_instance = private_key_instance.public_key ()
	public_key_DER_byte_string = public_key_instance.export_key (
		format = "DER"
	)
	public_key_PEM_string = public_key_instance.export_key (
		format = "PEM"
	)
	
	public_key_DER_hexadecimal_string = create_DER_hexadecimal_string (
		public_key_DER_byte_string
	)

	return {		
		"instance": public_key_instance, 
		
		"DER byte string": public_key_DER_byte_string,
		"DER hexadecimal string": public_key_DER_hexadecimal_string,
		
		"PEM string": public_key_PEM_string
	}
