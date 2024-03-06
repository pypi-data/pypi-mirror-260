

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
		"note": ""
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

import reelity.instrument.moves.names.make as make
import reelity.instrument.moves.names.start_layer as start_layer
import reelity.instrument.moves.names.is_on as is_on

#
#	vibes
#
import reelity.instrument.moves.names.vibes.make_ECC_448_2 as make_ECC_448_2_vibe
import reelity.instrument.moves.names.vibes.enumerate as enumerate_vibes


#
#	performances
#		# plurformance
#
import reelity.instrument.moves.names.performances.ECC_448_2.perform as perform

#
#	feelings
#
import reelity.instrument.moves.names.feelings.ECC_448_2.feel as feel

#
#	hotties
#
import reelity.instrument.moves.names.hotties.add as add_hottie
import reelity.instrument.moves.names.hotties.show as show_hotties
import reelity.instrument.moves.names.hotties.bounce as bounce_hottie

moves = {
	"layer: start": start_layer.perform,
	
	#
	#	is on
	#
	"is on": is_on.perform,
	
	#
	#	vibes
	#
	"vibes: make ECC 448 2": make_ECC_448_2_vibe.perform,
	"vibes: enumerate": enumerate_vibes.perform,
	
	#
	#	performances
	#
	"performances ECC 448 2: perform": perform.story,
	
	
	#
	#	feelings
	#
	"feelings ECC 448 2: feel": feel.performance,
	
	#
	#	hotties
	#	
	"hotties: add": add_hottie.perform,
	"hotties: show": show_hotties.perform,
	"hotties: bounce": bounce_hottie.perform
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
	
		return moves [ name ] (move ["fields"])

	return {
		"status": "fail",
		"note": f'A move named "{ name }" was not found.'
	}
