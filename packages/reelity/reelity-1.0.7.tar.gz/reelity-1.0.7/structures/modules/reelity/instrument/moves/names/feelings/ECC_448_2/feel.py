
'''
	JavaScript UTF8?
		https://stackoverflow.com/questions/13356493/decode-utf-8-with-javascript
		https://stackoverflow.com/questions/37596748/how-do-i-encode-a-javascript-string-in-utf-16
'''

'''
{
	name: "feelings ECC 448 2: feel",
	fields:  {
		"showy rhythm": {
			"hexadecimal string": showy_rhythm
		},
		"UTF8 story": story,
		"UTF8 performance": performance
	}
}

'''

	
import rich	

import reelity.modules.EEC_448_2.verify as verify

import reelity.modules.EEC_448_2.modulators.byte_string.from_UTF8 as UTF8_to_byte_string
import reelity.modules.EEC_448_2.modulators.byte_string.from_hexadecimal as hexadecimal_to_byte_string

import reelity.modules.EEC_448_2.public_key.instance as instantiate_public_key
	

def performance (
	fields
):
	rich.print_json (data = fields)

	public_key_string = fields ["showy rhythm"] ["hexadecimal string"]
	UTF8_story = fields ["UTF8 story"]
	UTF8_performance = fields ["UTF8 performance"]

	public_key_instance = instantiate_public_key.from_DER_hexadecimal_string (
		public_key_string
	)
	
	print (UTF8_to_byte_string.modulate (UTF8_story))
	print (UTF8_to_byte_string.modulate (UTF8_performance))
	
	#
	#	hexadecimal_to_byte_string.modulate (
	#	UTF8_to_byte_string.module (
	#

	verified = verify.start (
		public_key_instance,
		
		signed_bytes = hexadecimal_to_byte_string.modulate (UTF8_performance),
		unsigned_bytes = UTF8_to_byte_string.modulate (UTF8_story)
	)
	if (verified == "yes"):
		feeling = "euphoria"
	else:
		feeling = "obscure"

	return {
		"status": "pass",
		"note": {
			"feeling": feeling
		}
	}