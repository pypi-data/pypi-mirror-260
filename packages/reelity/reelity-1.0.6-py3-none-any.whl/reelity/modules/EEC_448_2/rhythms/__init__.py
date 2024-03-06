

'''
	import reelity.modules.EEC_448_2.rhythms as EEC_448_2_rhythm_creator
	rhythms = EEC_448_2_rhythm_creator.create (
		seed = ""
	)
'''

'''
	{
		"showy": {
			"hexadecimal string": public_key_DER_hexadecimal_string,
		},
		"intimate": {
			"hexadecimal string": intimate_rhythm_DER_hexadecimal_string
		}
	}
'''

import reelity.modules.EEC_448_2.intimate_rhythm.creator as EEC_448_2_intimate_rhythm_creator
import reelity.modules.EEC_448_2.public_key.creator as EEC_448_2_public_key_creator

def create (
	seed = ""
):
	#
	#	create intimate rhythm
	#
	intimate_rhythm = EEC_448_2_intimate_rhythm_creator.create (seed)
	intimate_rhythm_instance = intimate_rhythm ["instance"]
	intimate_rhythm_DER_hexadecimal_string = intimate_rhythm ["DER hexadecimal string"]
	
	#
	#	create showy rhythm
	#
	public_key = EEC_448_2_public_key_creator.create (
		intimate_rhythm_instance
	)
	public_key_instance = public_key ["instance"]
	public_key_DER_hexadecimal_string = public_key ["DER hexadecimal string"]
	
	return {
		"showy": {
			"hexadecimal string": public_key_DER_hexadecimal_string,
		},
		"intimate": {
			"hexadecimal string": intimate_rhythm_DER_hexadecimal_string
		}
	}