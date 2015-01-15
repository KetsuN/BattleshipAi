class NetworkObserverSubject ():
	def __init__(self):
		self.observers = []
	
	def attachObserver(self, observer):
		self.observers.append(observer)
		
	def notifyStartGameAck (self):
		for observer in self.observers:
			observer.startGameAckResponse()
		
	def notifyTurnRequest (self):
		for observer in self.observers:
			observer.turnRequestResponse()
		
	def notifyTurnAck (self, numberCoord, letterCoord, status, boat):
		for observer in self.observers:
			observer.turnAckResponse(numberCoord, letterCoord, status, boat)
		
	def notifyRadarAck (self, numberCoord, letterCoord, status):
		for observer in self.observers:
			observer.radarAckResponse(numberCoord, letterCoord, status)
			
	def notifyGameOver (self, winner, loser):
		for observer in self.observers:
			observer.gameOverResponse(winner, loser)
		
		
class NetworkObserver ():
	def __init__(self):
		pass
		
	def startGameAckResponse (self):
		pass
		
	def turnRequestResponse (self):
		pass
		
	def turnAckResponse (self, numberCoord, letterCoord, status, boat):
		pass
		
	def radarAckResponse (self, numberCoord, letterCoord, status):
		pass
		
	def gameOverResponse (self, winner, loser):
		pass