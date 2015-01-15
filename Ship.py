class Ship:
	VALID_SHIP_NAMES = {"Patrol":2, "Destroyer":3, "Submarine":3, "Carrier":5, "Battleship":4}

	def __init__(self, name, numberCoord = None, letterCoord = None, direction = None):
		if name in self.VALID_SHIP_NAMES.keys():
			self.name = name
			self.size = self.VALID_SHIP_NAMES.get(name)
			self.numberCoord = numberCoord
			self.letterCoord = letterCoord
			self.direction = direction
		else:
			raise "Invalid Ship type specified"
			
		