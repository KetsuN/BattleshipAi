import socket
import time
from queue import Queue
from NetworkObserver import NetworkObserverSubject
import select
import xml.etree.ElementTree as ET

class Networking (NetworkObserverSubject):
	startGameRequest = '<StartGameRequest player="{0}"/>'
	
	startGameBoardOpen = '<StartGame player="{0}">'
	placeShip = '<PlaceShip name="{0}" startingNumber="{1}" startingLetter="{2}" alignment="{3}"/>'
	startGameBoardClose = '</StartGame>'
	
	sendShot = '<Turn player="{0}" type="shot"><Shot shotLocNumber="{1}" shotLocLetter="{2}"/></Turn>'
	
	sendRadarMove = '<Turn player="{0}" type="radar"><Radar shotLocNumber="{1}" shotLocLetter="{2}"/></Turn>'
	
	def __init__ (self, ip, port, name):
		super(Networking, self).__init__()
		self.ip = ip
		self.port = port
		self.playerName = name
		self.sendQueue = Queue()
		
	def sendStartGameRequest (self):
		self.sendQueue.put(self.startGameRequest.format(self.playerName))
		
		
	def sendBoard (self, shipList):
		message = self.startGameBoardOpen.format(self.playerName)
		for ship in shipList:
			message += self.placeShip.format(ship.name, ship.numberCoord, ship.letterCoord, ship.direction)
		message += self.startGameBoardClose
		
		self.sendQueue.put(message)
		
		
	def sendMove (self, numberCoord, letterCoord):
		message = self.sendShot.format(self.playerName, numberCoord, letterCoord)
		self.sendQueue.put(message)
		
		
	def sendRadar (self, numberCoord, letterCoord):
		message = self.sendRadarMove.format(self.playerName, numberCoord, letterCoord)
		self.sendQueue.put(message)
		
		
	def sendMessage (self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.setblocking(0)
		
		while True:
			data = ""
			if not self.sendQueue.empty():
				message = self.sendQueue.get()
				sock.sendto(bytes(message, "utf-8"), (self.ip, self.port))
		
			ready = select.select([sock], [], [], .1)
			if ready[0]:
				data = sock.recv(1024).decode("utf-8")
				
				#print(data)
			
				if "StartGameRequestAck" in data:
					self.notifyStartGameAck()
					
				elif "TurnRequest" in data:
					self.notifyTurnRequest()
					
				elif "TurnAck" in data and "Shot" in data:
					try:
						root = ET.fromstring("<root>" + data + "</root>")
						for element in root.find("TurnAck").findall("Shot"):
							numberCoord = int(element.attrib.get("shotLocNumber").strip())
							letterCoord = element.attrib.get("shotLocLetter").strip()
							status = element.attrib.get("status").strip()
							boat = None
							if element.attrib.get("boat") is not None:
								boat = element.attrib.get("boat").strip()
							
							self.notifyTurnAck (numberCoord, letterCoord, status, boat)
					except ET.ParseError:
						print("received bad message?")
						
				elif "TurnAck" in data and "Radar" in data:
					try:
						root = ET.fromstring("<root>" + data + "</root>")
						for element in root.find("TurnAck").findall("Radar"):
							numberCoord = int(element.attrib.get("shotLocNumber").strip())
							letterCoord = element.attrib.get("shotLocLetter").strip()
							status = element.attrib.get("status").strip()
							
							self.notifyRadarAck (numberCoord, letterCoord, status)
					except ET.ParseError:
						print("received bad message?")
						
				elif "GameOver" in data:
					try:
						root = ET.fromstring("<root>" + data + "</root>")
						for element in root.findall("GameOver"):
							winner = element.attrib.get("winner")
							loser = element.attrib.get("loser")
							
							self.notifyGameOver(winner, loser)

							break
					except ET.ParseError:
						print("received bad message?")
				
		sock.close()
		