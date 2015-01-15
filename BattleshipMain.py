from Board import Board
from Ship import Ship
from Board import GridSpace
from MoveAi import MoveAi
from time import sleep
from Network import Networking
from NetworkObserver import NetworkObserver
import os
import sys
import threading
 

class BattleShip (NetworkObserver):
	def __init__(self, ip, port, name, numberOfGames):
		super(BattleShip, self).__init__()
		self.playerName = name
		self.numberOfGames = numberOfGames
		self.totalTurns = 0
		self.currentGameNumber = 0
		self.wins = 0
		self.losses = 0
		self.numberTurns = 0
		self.ai = MoveAi(10, 10)
		
		self.shipList = [Ship("Patrol"), Ship("Submarine"), Ship("Destroyer"), Ship("Battleship"), Ship("Carrier")]
		self.foundShips = []
		
		self.myBoard = Board(10, 10, self.shipList)
		self.opponentBoard = Board(10, 10, [])
		
		self.networking = Networking(ip, port, name)
		self.networking.attachObserver(self)
		self.networkThread = threading.Thread(target=self.networking.sendMessage)
		self.networkThread.start()
		
		self.startGame()
		
		
	def startGame (self):
		self.currentGameNumber += 1
		self.numberTurns = 0
		self.myBoard = Board(10, 10, self.shipList)
		self.opponentBoard = Board(10, 10, [])
		self.networking.sendStartGameRequest()
		
		
	def startGameAckResponse (self):
		self.myBoard.printBoard()
		self.networking.sendBoard(self.myBoard.shipList)
		
		
	def turnRequestResponse (self):
		if self.numberTurns == 0:
			self.networking.sendRadar(9, "I")
		else:
			moveCoords = self.ai.decideMove (self.opponentBoard, self.shipList)
			xCoord = moveCoords[0] + 1
			yCoord = GridSpace.translateVertCoord(moveCoords[1])
			self.networking.sendMove(xCoord, yCoord)
		self.numberTurns += 1
		
		
	def radarAckResponse (self, x, y, status):
		x -= 1
		y = int(GridSpace.translateVertCoordReverse(y))
		if status == "Miss":
			for i in range (x-1, x+2):
				for j in range (y-1, y+2):
					self.opponentBoard.alterGridSpace(i, j, GridSpace(1, "."))
					
		
	def turnAckResponse (self, x, y, status, shipType = None):
		x -= 1
		y = int(GridSpace.translateVertCoordReverse(y))
		
		if status == "Miss":
			self.opponentBoard.alterGridSpace(x, y, GridSpace(1, "."))
			
		elif status == "Hit":
			self.opponentBoard.alterGridSpace(x, y, GridSpace(2, "X"))
			
		elif status == "Sunk" and shipType is not None:
			self.opponentBoard.alterGridSpace(x, y, GridSpace(2, "X"))
			self.addFoundShip(shipType)
			self.opponentBoard = self.ai.markSpacesSunk(self.opponentBoard, x, y, Ship(shipType))
			return []
			
		#os.system('cls')
		self.opponentBoard.printBoard()
	
	
	def gameOverResponse (self, winner, loser):
		if winner == self.playerName:
			self.wins += 1
			print("You beat " + loser)
		else:
			self.losses += 1
			print("You lose...." + winner + " beat you")
			
		self.totalTurns += self.numberTurns
		print("{0} turns ({1} average)".format(self.numberTurns, int(self.totalTurns / self.currentGameNumber)))
		print("Current winrate: {0}% ({1}W and {2}L)".format(int(self.wins)/(int(self.wins)+int(self.losses)), self.wins, self.losses))
			
		if self.currentGameNumber < self.numberOfGames:
			self.ai.updateHeatMap(self.opponentBoard)
			sleep(3)
			self.startGame ()
		else:
			sys.exit()
		
		
	def removeFromShipList(self, shipType):
		for ship in self.shipList:
			if ship.name == shipType:
				self.shipList.remove(ship)
		
		
	def addFoundShip(self, shipType):
		self.foundShips.append(Ship(shipType))

if __name__ == "__main__":
	ip = sys.argv[1]
	port = int(sys.argv[2])
	playerName = sys.argv[3]
	numberOfGames = int(sys.argv[4])
	battleshipObj = BattleShip(ip, port, playerName, numberOfGames)