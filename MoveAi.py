from Board import Board
from Ship import Ship
from Board import GridSpace
from math import sqrt
from time import sleep

class MoveAi:	
	def __init__ (self, gameWidth, gameHeight):
		self.heatMap = [[]]
		self.width = gameWidth
		self.height = gameHeight
		
		self.initializeHeatMap()
		
	def initializeHeatMap (self):
		for i in range(0, self.width):
			self.heatMap.append([])
			for j in range(0, self.height):
				self.heatMap[i].append(1)
				
				
	def updateHeatMap (self, gameBoard):
		for i in range(0, self.width):
			for j in range(0, self.height):
				if gameBoard.getSpaceStatus(i, j) == "Sunk":
					self.heatMap[i][j] += 1
					
					
		boardString = "  "
		
		for i in range(0, self.width):
			boardString += str(i) + " " 
		boardString += "\n"
		
		for i in range(0, self.width):
			for j in range(0, self.height):
				if j == 0:
					boardString += str(i) + " " 
				boardString += str(self.heatMap[i][j]) + " " 
			boardString += "\n"
			
		print(boardString)
		
			
			
	def decideMove(self, gameBoard, shipList):
		decisionArray = self.createCleanDecisionArray(gameBoard)
	
		for i in range(0, self.width):
			decisionArray.append([])
			for j in range(0, self.height):
				decisionArray[i].append(1)

		for i in range (0, self.width):
			for j in range(0, self.height):
				hitMultipler = 0
				
				for ship in shipList:
					if ship.name not in gameBoard.getShipNameList():
						for k in range(0, ship.size):
							if gameBoard.isLocationValid(i-k, j, "H", ship.size):
								decisionArray[i][j] += 2 
								
							if gameBoard.isLocationValid(i, j-k, "V", ship.size):
								decisionArray[i][j] += 2 
								
				#if self.useHeatMap():
				#	decisionArray[i][j] += self.heatMap[i][j]
								
				if gameBoard.getSpaceStatus(i, j) == "Clear":	
					hitMultipler += self.getHitMultiplier(gameBoard, i, j, ship.size)					
							
				decisionArray[i][j] = (decisionArray[i][j] + 1) * hitMultipler
				
		self.displayDesicionTable(gameBoard, decisionArray)
				
		nextMove = self.findMaxDecision (gameBoard, decisionArray)
		return nextMove
		
		
	def useHeatMap (self):
		lst = []
		variance = 0
		sum = 0
		
		for i in range(0, self.width):
			for j in range(0, self.height):
				lst.append(self.heatMap[i][j])
				
		for i in range(len(lst)):
			sum += lst[i]
		mn = (sum / len(lst))
		
		for e in lst:
			variance += (e-mn)**2
		variance /= len(lst)

		stdev = sqrt(variance)
		#print ("STDEV: {0}".format(stdev))
		
		if stdev > (mn * (len(lst)/2)):
			return True
		else:	
			return False
		
		
	def getHitMultiplier (self, gameBoard, x, y, shipSize):
		counter = 1
		# Left direction
		for i in range(1, shipSize):
			if x - i >= 0 and gameBoard.getSpaceStatus(x - i, y) == "Hit":
				counter += 10
			else:
				break
	
		# Right direction
		for i in range(1, shipSize):
			if x + i < self.width and gameBoard.getSpaceStatus(x + i, y) == "Hit":
				counter += 10
			else:
				break
	
		# Up direction
		for i in range(1, shipSize):
			if y - i >= 0 and gameBoard.getSpaceStatus(x, y - i) == "Hit":
				counter += 10
			else:
				break
				
		# Down direction
		for i in range(1, shipSize):
			if y + i < self.height and (gameBoard.getSpaceStatus(x, y + i) == "Hit"):
				counter += 10
			else:
				break
				
		return counter
			
		
	def findMaxDecision (self, gameBoard, decisionArray):
		maxStat = 0
		coords = []
		for i in range (0, self.width):
			for j in range(0, self.height):
				if decisionArray[i][j] > maxStat:
					maxStat = decisionArray[i][j]
					coords = [i, j]
		return coords
		
		
	def createCleanDecisionArray (self, gameBoard):
		decisionArray = [[]]
	
		for i in range(0, self.width):
			decisionArray.append([])
			for j in range(0, self.height):
				decisionArray[i].append(0)
				
		return decisionArray
		
		
	def displayDesicionTable(self, gameBoard, decisionArray):
		boardString = "  "
		
		for i in range(0, self.width):
			boardString += str(i) + " " 
		boardString += "\n"
		
		for i in range(0, self.width):
			for j in range(0, self.height):
				if j == 0:
					boardString += str(i) + " " 
				boardString += str(decisionArray[i][j]) + " " 
			boardString += "\n"
			
		print(boardString)
		
		
	def markSpacesSunk(self, gameBoard, startX, startY, ship):
		symbol = ship.name[0:1]
		shipSize = ship.size
		
		sunkArray = [[startX, startY]]
		for i in range(1, shipSize):
			if startX - i > 0 and gameBoard.getSpaceStatus(startX - i, startY) == "Hit":
				sunkArray.append([startX-i, startY])
			else:
				break
				
			for coords in sunkArray:
				gameBoard.boardArray[coords[0]][coords[1]].status = 3
				gameBoard.boardArray[coords[0]][coords[1]].display = symbol
				
		
		sunkArray = [[startX, startY]]
		for i in range(1, shipSize):
			if startX + i < self.width and gameBoard.getSpaceStatus(startX + i, startY) == "Hit":
				sunkArray.append([startX+i, startY])
			else:
				break
				
			for coords in sunkArray:
				gameBoard.boardArray[coords[0]][coords[1]].status = 3
				gameBoard.boardArray[coords[0]][coords[1]].display = symbol
				
		
		sunkArray = [[startX, startY]]
		for i in range(1, shipSize):
			if startY - i > 0 and gameBoard.getSpaceStatus(startX, startY - i) == "Hit":
				sunkArray.append([startX, startY - i])
			else:
				break
				
			for coords in sunkArray:
				gameBoard.boardArray[coords[0]][coords[1]].status = 3
				gameBoard.boardArray[coords[0]][coords[1]].display = symbol
				
		
		sunkArray = [[startX, startY]]
		for i in range(1, shipSize):
			if startY + i < self.height and gameBoard.getSpaceStatus(startX, startY + i) == "Hit":
				sunkArray.append([startX, startY + i])
			else:
				break
				
			for coords in sunkArray:
				gameBoard.boardArray[coords[0]][coords[1]].status = 3
				gameBoard.boardArray[coords[0]][coords[1]].display = symbol
				
		return gameBoard
			
			
	