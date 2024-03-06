

import reelity.instrument.moon.pocket.vibes.enumerate as enumerate_vibes
	
	
def perform (fields):
	vibes = enumerate_vibes.start ()

	return {
		"status": "pass",
		"note": {
			"vibes": vibes
		}
	}