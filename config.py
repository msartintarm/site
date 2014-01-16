import re

# CONFIGURATION : Structure of audio
# Origin URL, destination node, loop[, loop offset, loop time])
#  These are at 120 BPM: 1 sec = 2 beats
# 0. Low-pass input detects movement, occuring on the half-beat; slightly below 0.25s
# 1. Non-looping sound, which will be triggered by the above sample
# 2. Non-looping sound, which will be triggered by the above sample
# 3. Rest of the song.
# CONFIGURATION : Structure of pieces
# Syntax: name, texture, array of x-y coordinate strings
#  String values can either be absolute, or relative to prev. strings
#  Can also specify loops of continuous increments
 
level = {
	"grid-size": 50,
	"textures": ["brick-texture", "heaven-texture", "rug-texture"],
	    "audio": [["music/beats.mp3", "audio-low-pass", "loop", "1", "8"],
	              ["music/move.wav", "audio-output"],
	              ["music/jump1.wav", "audio-output"],
	              ["music/jump2.wav", "audio-output"],
	              ["music/jump3.wav", "audio-output"],
	              ["music/jump4.wav", "audio-output"],
	              ["music/background.wav", "audio-delay", "loop", "0", "8"]],
	    "pieces": [
	    	["floor", "rug-texture", "1", "3", ["-11,-1", "20*(+1,+0)"]],
	    	["wall", "brick-texture", "1", "1", [
	        	"6,3", "+1,+1", "+1,+1", "+1,+1", "12*(+1,+0)",
	            "+4,-2", "4*(+2,+0)",
	            "-4,+2", "4*(-2,+0)",
	            "+4,-2", "4*(+2,+0)",
	            "-4,+2", "4*(-2,+0)",
	            "+2,-3", "20*(+1,+0)"]]],
	"start-position": ["0", "300", "750"]
}

regex = re.compile(r"(?:([0-9]+)\*\()?([-+])*([0-9]+)\,([-+])*([0-9]+)\)?")

class GameConfig():

	def __init__(self):

		self.squares = {}
		self.pieces = []
		self.audio = level["audio"]
		self.start = level["start-position"]

		# Either op doesn't exist (val), is a '-' (= dec old), or is  a '+' (= inc old)
		def newCoordVal(old, op, val):
			if op == None:
				return int(val)
			if op == "-":
				 return old - int(val)
			if op == "+":
				return old + int(val)
			return -1

		for i, piece in enumerate(level["pieces"]):

			# Parse coordinates into map. Can be specified as absolute, 
			#  or in [loops of] offsets. Will be enumerated over in rendering.
			x = 0
			y = 0
			squares = {}
			for coord in piece[4]:

				result = regex.search(coord)

                # Index 1: loop count (opt); 2, 4: inc sign (opt); 3, 5: value (non-opt)
				loop = 1
				if result.group(1):
					loop = int(result.group(1))
				j = 0
				while j < loop:

					x = newCoordVal(x, result.group(2), result.group(3))
					y = newCoordVal(y, result.group(4), result.group(5))

					if not y in squares:
						squares[y] = {};
					squares[y][x] = i
					j += 1


        	# Use info to construct config object
			self.pieces.append({
				"name": piece[0],
				"squares": squares.copy()
			});

		print(self.pieces)


