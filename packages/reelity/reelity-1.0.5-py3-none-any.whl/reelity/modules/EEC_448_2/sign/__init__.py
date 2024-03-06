

'''
	unicode_string = json.dumps ({
		"move": "send",
		"fields": {
			"to": {
				"format": "EEC_448_1",
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

from Crypto.PublicKey import ECC
from Crypto.Signature import eddsa

import reelity.modules.EEC_448_2.modulators.hexadecimal.from_byte_string as byte_string_to_hex

def start (
	private_key_instance = None,
	unsigned_bytes = None
):
	signer = eddsa.new (private_key_instance, 'rfc8032')
	signed_bytes = signer.sign (unsigned_bytes)
		
	return {
		"signed bytes": signed_bytes,
		"signed bytes hexadecimal": byte_string_to_hex.modulate (signed_bytes)
	}
	
