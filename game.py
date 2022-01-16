from gameWindow import *
from layout import *
from board import *

class Game:
    """
    The class containing two methods necessarry for the game function
    """
    def gameEnded(self, won):
        """
        Creates a popup presenting a decision to the player whether he wants to continue the game or exit it.
        Value of the popup changes with the won value
        
        Parameters:
            won(Bool): a boolean meaning if the game was won.
        """
        returnValue = gameWindow.createPopup(won)
        if(returnValue == "Exit"):
            self._exitGame = True
        else:
            self._exitGame = False
            return

    def startGame(self):
        """
        Called only once. Contains the game loop and all of the logic necessary for the game function
        """
        while True:
            gameWindow.initiateWindow()
            self._exitGame = True
            while True:
                event, values = gameWindow._window.read()
                if(event == psg.WIN_CLOSED):
                    break
                n, m, bombs = gameWindow.readVals(list(values.values()))
                if(n != None):
                    break
            if(values == None):
                break
            
            layout = Layout(n, m, bombs)
            board = Board(layout)

            gameWindow.startGameWindow(board)
            gameWindow.parseVisuals()
            
            while True:
                event, values = gameWindow._window.read()
                if(event == psg.WIN_CLOSED):
                    break
                # checking if the event is a keyboard input
                if(len(event) == 1):
                    gameWindow.parseXyzzy(event)
                    continue
                # checking if the button was right clicked
                if(event.startswith("marker")):
                    event = event[event.find("(")+1: len(event)-1]
                    n, m = event.split(", ")
                    gameWindow._board.rClick(int(n), int(m))
                    gameWindow.parseCell(int(n), int(m))
                    flagAmount = int(gameWindow._window["-FLAGS-"].get())
                    if(flagAmount == gameWindow._board.getLayout().getBombs()):
                        if(gameWindow._board.checkWinFlags() == True):
                            Game.gameEnded(self, True)
                            break
                    continue
                n, m = event.split(" ")
                gameWindow._board.lClick(int(n), int(m))
                if(gameWindow._board.getBoard()[int(n)][int(m)] != 0):
                    gameWindow.parseCell(int(n), int(m))
                    if(gameWindow._board.getBoard()[int(n)][int(m)] == -1):
                        Game.gameEnded(self, False)
                        break
                else:
                    gameWindow.parseVisuals()
                if(gameWindow._board.checkWinCells() == True):
                    Game.gameEnded(self, True)
                    break
            
            gameWindow._window.close()
            if(self._exitGame == True):
                break
    
    
    
gameWindow = GameWindow()
Game().startGame()
