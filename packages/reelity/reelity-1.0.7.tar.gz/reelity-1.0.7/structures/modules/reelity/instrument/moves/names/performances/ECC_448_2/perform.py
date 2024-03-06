
'''
unicode_string = json.dumps ({
	"move": "send",
	"fields": {
		"to": {
			"kind": "EEC_448_1",
			"address": "3043300506032b6571033a00e26960a83c45c0bb86e356cd727473e96682e76c6dd01c991a6ea0a394ecca27b467554d73e2a22b05425c1926a7a92befda5c1937d6876f00"
		},
		"amount": "40324789324873"
	}
}, indent = 4)		
unsigned_bytes = unicode_string.encode ("utf-8")

import reelity.modules.EEC_448_2.sign as EEC_448_2_sign
signed = EEC_448_2_sign.start (
	private_key_instance,
	unsigned_bytes = unsigned_bytes
)

signed_bytes_hexadecimal = signed ["signed bytes hexadecimal"]
'''

'''
	{
		"name": "performances: perform",
		"fields": {
			"intimate rhythm": {
				"hexadecimal string": ""
			},
			"UTF8 string": ""
		}
	}
'''
'''

'''

import reelity.modules.EEC_448_2.sign as EEC_448_2_sign
import reelity.modules.EEC_448_2.private_key.instance as instantiate_private_key
	
import rich	
	
def story (
	fields
):
	rich.print_json (data = fields)

	private_key_DER_hexadecimal_string = fields ["intimate rhythm"] ["hexadecimal string"]
	UTF8_string = fields ["UTF8 string"]

	unsigned_bytes = UTF8_string.encode ("utf-8")

	private_key_instance = instantiate_private_key.from_DER_hexadecimal_string (
		private_key_DER_hexadecimal_string
	)
	signed = EEC_448_2_sign.start (
		private_key_instance,
		unsigned_bytes = unsigned_bytes
	)

	return {
		"status": "pass",
		"note": {
			"performance": signed ["signed bytes hexadecimal"]
		}
	}