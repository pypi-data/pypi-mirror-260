
'''
	python3 status.proc.py "modules/EEC_448_2/_status/status_3_sign_and_verify/status_1.py"
'''

import reelity.modules.EEC_448_2.private_key.creator as EEC_448_2_private_key_creator
import reelity.modules.EEC_448_2.private_key.etch as etch_EEC_448_private_key
import reelity.modules.EEC_448_2.private_key.scan as private_key_scan
import reelity.modules.EEC_448_2.private_key.instance as instantiate_private_key
	
import reelity.modules.EEC_448_2.public_key.creator as EEC_448_2_public_key_creator
import reelity.modules.EEC_448_2.public_key.etch as etch_EEC_448_2_public_key
import reelity.modules.EEC_448_2.public_key.scan as public_key_scan
import reelity.modules.EEC_448_2.public_key.instance as instantiate_public_key	
	
import reelity.modules.EEC_448_2.sign as EEC_448_2_sign	
import reelity.modules.EEC_448_2.verify as verify

import reelity.modules.EEC_448_2.modulators.byte_string.from_hexadecimal as hexadecimal_to_byte_string
	
import pathlib
from os.path import dirname, join, normpath
import os
import json

def erase (path):
	try:
		os.remove (path)
	except Exception as E:
		pass;

def check_1 ():
	seeds = [ 
		"4986888b11358bf3d541b41eea5daece1c6eff64130a45fc8b9ca48f3e0e02463c99c5aedc8a847686d669b7d547c18fe448fc5111ca88f4e8",
		"5986888b11358bf3d541b41eea5daece1c6eff64130a45fc8b9ca48f3e0e02463c99c5aedc8a847686d669b7d547c18fe448fc5111ca88f4e8",
		"000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",		
		"ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
		"123412341234123412341234123412341234123412341234123412341234123412341234123412341234123412341234123412341234123412",
		"0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f",	
		"135791357913579135791357913579135791357913579135791357913579135791357913579135791357913579135791357913579135791357",	
		"2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef"	
	]
	
	for seed in seeds:
		private_key_path = normpath (
			join (pathlib.Path (__file__).parent.resolve (), "EEC_448_2_private_key")
		) + ".JSON"
		public_key_path = normpath (
			join (pathlib.Path (__file__).parent.resolve (), "EEC_448_2_public_key")
		) + ".JSON"
	
		erase (private_key_path)
		erase (public_key_path)
	
		
		#
		#	create private key
		#
		private_key = EEC_448_2_private_key_creator.create (seed)
		private_key_instance = private_key ["instance"]
		private_key_DER_hexadecimal_string = private_key ["DER hexadecimal string"]
		private_key_DER_byte_string = private_key ["DER byte string"]
		
		#
		#	etch private key
		#
		etch_EEC_448_private_key.start (
			private_key_path, 
			json.dumps ({
				"private key": {
					"DER hexadecimal string": private_key ["DER hexadecimal string"]
				}
			}, indent = 4), 
			"JSON"
		)	
		
		#
		#	scan private key
		#
		assert (
			private_key_scan.start (private_key_path, "JSON") ["private key"] ["DER hexadecimal string"] ==
			private_key ["DER hexadecimal string"]
		)
		
		#
		#	instantiate private key
		#
		instantiate_private_key.from_DER_hexadecimal_string (
			private_key_scan.start (private_key_path, "JSON") ["private key"] ["DER hexadecimal string"]
		)
		
		
			
		#
		#	create public key
		#
		public_key = EEC_448_2_public_key_creator.create (
			private_key_instance
		)	
		public_key_instance = public_key ["instance"]
		
		#
		#	etch public key
		#
		etch_EEC_448_2_public_key.start (
			public_key_path,
			json.dumps ({
				"public key": {
					"DER hexadecimal string": public_key ["DER hexadecimal string"]
				}
			}, indent = 4), 
			"JSON"
		)
		
		#
		#	scan public key
		#
		assert (
			public_key_scan.start (public_key_path, "JSON") ["public key"] ["DER hexadecimal string"] ==
			public_key ["DER hexadecimal string"]
		)
		
		#
		#	instantiate public key
		#
		instantiate_public_key.from_DER_hexadecimal_string (
			public_key_scan.start (public_key_path, "JSON") ["public key"] ["DER hexadecimal string"]
		)
		
		
		#
		#	sign
		#
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
		
		signed = EEC_448_2_sign.start (
			private_key_instance,
			unsigned_bytes = unsigned_bytes
		)
		signed_bytes_hexadecimal = signed ["signed bytes hexadecimal"]
		
		print ("signed_bytes_hexadecimal:", signed_bytes_hexadecimal)
		
		#
		#	verify is legit
		#
		verification_1 = verify.start (
			public_key_instance,
			
			signed_bytes = hexadecimal_to_byte_string.modulate (signed_bytes_hexadecimal),
			unsigned_bytes = unsigned_bytes
		)
		assert (verification_1 == "yes")
		
		#
		#	verify is not legit
		#	
		verification_2 = verify.start (
			public_key_instance,
			
			signed_bytes = hexadecimal_to_byte_string.modulate (signed_bytes_hexadecimal),
			unsigned_bytes = b""
		)
		assert (verification_2 == "no")
	
		
		
		erase (private_key_path)
		erase (public_key_path)

		
checks = {
	"elliptic public and private key generation": check_1
}






#