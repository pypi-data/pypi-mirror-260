

'''
	import reelity.modules.EEC_448_2.modulators.byte_string.from_hexadecimal as hexadecimal_to_byte_string
	byte_string = hexadecimal_to_byte_string.modulate ("0123456789ABCDEF")
'''

def modulate (hexadecimal_string):
	byte_string = bytes.fromhex (hexadecimal_string);

	assert (
		byte_string.hex ().upper () == 
		hexadecimal_string.upper ()
	)
	
	return byte_string