import time
import random
import calendar

class Board:
	def __init__(self, x, y, shipList):
		self.boardArray = list()
		self.width = x
		self.height = y
		self.shipList = shipList
		self.createBoard()
		self.placeShips()
		
	def createBoard (self):
		for i in range(0, self.width):
			self.boardArray.append([])
			for j in range(0, self.height):
				self.boardArray[i].append(GridSpace(0, " "))
		
	def alterGridSpace(self, x, y, gridSpace):
		self.boardArray[x][y] = gridSpace
		
		
	def placeShips (self):	
		i = 1
	
		for ship in self.shipList:
			while not self.placeOneShip(ship):
				pass
		
				
				
	def getShipNameList(self):
		nameList = []
		for i in range(0, len(self.shipList)):
			nameList.append(self.shipList[i].name)
			
		return nameList
		
		
	def placeOneShip (self, ship):
		#random.seed(calendar.timegm(time.gmtime()))
		randomX = random.randrange(0, self.width)
		randomY = random.randrange(0, self.height)
		direction = ["H", "V"][random.randrange(0, 2)]
		
		if not self.isLocationValid(randomX, randomY, direction, ship.size):
			return False
		else:
			if direction == "H":
				for i in range(randomX, randomX + ship.size):
					self.boardArray[i][randomY] = GridSpace(1, str(ship.name)[0:1], str(ship.name))
			else:
				for i in range(randomY, randomY + ship.size):
					self.boardArray[randomX][i] = GridSpace(1, str(ship.name)[0:1], str(ship.name))
					
			ship.numberCoord = randomX + 1
			ship.letterCoord = GridSpace.translateVertCoord(randomY)
			if direction == "H":
				ship.direction = "Horizontal"
			else:
				ship.direction = "Vertical"
				
			return True
		
		
	def isLocationValid(self, xCoord, yCoord, direction, size):
		if direction == "H":
			if xCoord + size > self.width or xCoord < 0:
				return False
			else:
				for i in range(xCoord, xCoord + size):
					if self.boardArray[i][yCoord].status != 0:
						return False
			
		else:
			if yCoord + size > self.height or yCoord < 0:
				return False
			else:
				for i in range(yCoord, yCoord + size):
					if self.boardArray[xCoord][i].status != 0:
						return False
						
		return True
		
		
	def getSpaceShipType (self, x, y):
		return self.boardArray[x][y].occupyingBoat
		
		
	def getSpaceStatus (self, x, y):
		return self.boardArray[x][y].getStatusString()
			
			
	def printBoard (self):
		boardString = "  "
		
		for i in range(0, self.width):
			boardString += str(i) + " " 
		boardString += "\n"
		
		for i in range(0, self.width):
			for j in range(0, self.height):
				if j == 0:
					boardString += str(i) + " " 
				boardString += self.boardArray[i][j].display + " " 
			boardString += "\n"

		print(boardString)
		
		
	def findGridsOccupiedBy (self, shipType):
		gridList = []
		for i in range(0, self.width):
			for j in range(0, self.height):
				if self.boardArray[i][j].occupyingBoat is not None and self.boardArray[i][j].occupyingBoat == shipType:
					gridList.append(self.boardArray[i][j])
					
		return gridList
		
		
class GridSpace:
	STATUS_ARRAY = ["Clear", "Occupied", "Hit", "Sunk"]

	def __init__(self, status, display, occupyingBoat = None):
		self.status = status
		self.display = display
		self.occupyingBoat = occupyingBoat
		
	def getStatusString (self):
		return self.STATUS_ARRAY [self.status]
		
	@staticmethod
	def translateVertCoord(y):
		if y == 0:
			return "A"
		elif y == 1:
			return "B"
		elif y == 2:
			return "C"
		elif y == 3:
			return "D"
		elif y == 4:
			return "E"
		elif y == 5:
			return "F"
		elif y == 6:
			return "G"
		elif y == 7:
			return "H"
		elif y == 8:
			return "I"
		elif y == 9:
			return "J"
			
		
	@staticmethod
	def translateVertCoordReverse(y):
		if y == "A":
			return 0
		elif y == "B":
			return 1
		elif y == "C":
			return 2
		elif y == "D":
			return 3
		elif y == "E":
			return 4
		elif y == "F":
			return 5
		elif y == "G":
			return 6
		elif y == "H":
			return 7
		elif y == "I":
			return 8
		elif y == "J":
			return 9
		