

'''
	import reelity.modules.EEC_448_2.keys as EEC_448_2_key_creator
	keys = EEC_448_2_key_creator.create (
		seed = ""
	)
'''

'''
	{
		"public": {
			"hexadecimal string": public_key_DER_hexadecimal_string,
		},
		"private": {
			"hexadecimal string": private_key_DER_hexadecimal_string
		}
	}
'''

import reelity.modules.EEC_448_2.private_key.creator as EEC_448_2_private_key_creator
import reelity.modules.EEC_448_2.public_key.creator as EEC_448_2_public_key_creator

def create (
	seed = ""
):
	#
	#	create private key
	#
	private_key = EEC_448_2_private_key_creator.create (seed)
	private_key_instance = private_key ["instance"]
	private_key_DER_hexadecimal_string = private_key ["DER hexadecimal string"]
	
	#
	#	create public key
	#
	public_key = EEC_448_2_public_key_creator.create (
		private_key_instance
	)
	public_key_instance = public_key ["instance"]
	public_key_DER_hexadecimal_string = public_key ["DER hexadecimal string"]
	
	return {
		"public": {
			"hexadecimal string": public_key_DER_hexadecimal_string,
		},
		"private": {
			"hexadecimal string": private_key_DER_hexadecimal_string
		}
	}