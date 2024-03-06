

'''
	import reelity.modules.EEC_448_2.modulators.hexadecimal.from_byte_string as byte_string_to_hex
	hex = byte_string_to_hex.modulate (b"")
'''


def modulate (byte_string):
	hexadecimal_string = byte_string.hex ().upper ()
	
	assert (
		bytes.fromhex (hexadecimal_string) == 
		byte_string
	)
	
	return hexadecimal_string