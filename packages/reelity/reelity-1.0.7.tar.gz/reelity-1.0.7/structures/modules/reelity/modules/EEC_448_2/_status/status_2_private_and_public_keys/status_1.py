
'''
	python3 status.proc.py "modules/EEC_448_2/_status/status_2_private_and_public_keys/status_1.py"
'''

import reelity.modules.EEC_448_2.private_key.creator as EEC_448_2_private_key_creator
import reelity.modules.EEC_448_2.private_key.etch as etch_EEC_448_private_key
import reelity.modules.EEC_448_2.private_key.scan as private_key_scan

import reelity.modules.EEC_448_2.public_key.creator as EEC_448_2_public_key_creator
import reelity.modules.EEC_448_2.public_key.etch as etch_EEC_448_2_public_key
import reelity.modules.EEC_448_2.public_key.scan as public_key_scan
		
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
		#	create public key
		#
		public_key = EEC_448_2_public_key_creator.create (
			private_key_instance
		)	
		
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
		
		erase (private_key_path)
		erase (public_key_path)

		
checks = {
	"elliptic public and private key generation": check_1
}






#