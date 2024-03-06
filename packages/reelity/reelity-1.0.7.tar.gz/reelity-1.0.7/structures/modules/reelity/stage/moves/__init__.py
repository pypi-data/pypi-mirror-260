

'''
	import reelity.stage.moves as stage_moves
	effect = stage_moves.perform (
		move = {
			"name": "",
			"fields": {
				
			}
		}
	)
'''

'''
	returns {
		"status": "pass",
		"note": "",
		"fields": {
				
		}
	}
'''

'''
	returns {
		"status": "fail",
		"note": ""
	}
'''


import os
from os.path import dirname, join, normpath

import reelity.stage.moves.names.start_layer as start_layer
import reelity.stage.moves.names.is_on as is_on


#
#	scene index
#
import reelity.stage.moves.names.scene_index.establish as scene_index_establish
import reelity.stage.moves.names.scene_index.freshest as scene_index_freshest

#
#	scene 1
#
import reelity.stage.moves.names.scene_1.produce_Ehh as scene_1_produce_Ehh
import reelity.stage.moves.names.scene_1.add_splendor as scene_1_add_splendor
import reelity.stage.moves.names.scene_1.establish_rules as scene_1_establish_rules

#
#	scene insights
#
import reelity.stage.moves.names.scene_insights.moves.enumerate as scene_insights_moves_enumerate

#
#	scene moves
#
import reelity.stage.moves.names.scene_moves.escrow.send as send_escrow_move
import reelity.stage.moves.names.scene_moves.escrow.receive as receive_escrow_move


moves = {
	"layer: start": start_layer.perform,
	
	#
	#	is on
	#
	"is on": is_on.perform,
	
	
	#
	#	scene index
	#
	"scene index: establish": scene_index_establish.perform,
	"scene index: freshest": scene_index_freshest.perform,
	
	#
	#	scene 1
	#
	"scene 1: produce Ehh": scene_1_produce_Ehh.perform,
	"scene 1: add splendor": scene_1_add_splendor.perform,
	"scene 1: establish rules": scene_1_establish_rules.perform,
	
	#
	#	scene insights
	#		# insights
	#		# descriptions
	#		# impressions
	#
	"scene insights: enumerate moves": scene_insights_moves_enumerate.perform,
	
	#
	#	moves
	#
	"move: send escrow": send_escrow_move.perform,
	"move: receive escrow": receive_escrow_move.perform,
	
}

def records (record):
	print (record)

def perform (
	move = "",
	records = records
):
	if ("name" not in move):
		records (f'The "name" of the move was not given.')
		return;
	
	name = move ["name"];
	if (name in moves):
		print (f"move: { name }")
		
		try:
			return moves [ name ] (move ["fields"])
		except Exception as E:
			return {
				"status": "fail",
				"note": f'An exception occurred. { E }'
			}


	return {
		"status": "fail",
		"note": f'A move named "{ name }" was not found.'
	}
