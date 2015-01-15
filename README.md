Application written by Tim "KetsuN" Butler

# BattleshipAi
Statistical Battleship client AI.  This client should be connect with a central server to play against another client.
The AI uses statistical analysis at each turn.  The next move space is decided by the "most likely" location that a ship may reside
given the number of remaining ships to be found.  In the case that hits are found, but they are not included in the "sunken" ships, 
probabilistic priority will be given to ships surrounding the hit grid spaces.

This application should be executed through the main BattleshipAi.py file.  

##  NOTE  ##
This application will not work as intended unless it is able to communicate with the expected battleship server.
Unfortunately, I am not the owner of the server and, as such, the code for the server is not included with this repo, nor other repos under my name.
I plan on creating a duplicate server of my own for this application in the future

File Description:
* BattleshipAi.py		- Main battleship executable file.
* Board.py			- Board objects representing game play fields.
* Ship.py				- For ship objects.
* Network				- For communication with the battleship server.
* NetworkObserver.py	- Contains observer pattern classes so that the network objects can communicate with observers without exiting the communication loop.
* MoveAi.py			- Main AI processing class.  Used to weight each grid space on the board and choose the best moves.
