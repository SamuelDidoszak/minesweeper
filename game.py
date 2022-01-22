from gameWindow import *
from layout import *
from board import *

class Game:
    """
    The class containing two methods necessarry for the game function
    """
    def __init__(self, gameWindow):
        self.gameWindow = gameWindow
    
    def gameEnded(self, won):
        """
        Creates a popup presenting a decision to the player whether he wants to continue the game or exit it.
        Value of the popup changes with the won value
        
        Parameters:
            won(Bool): a boolean meaning if the game was won.
        """
        returnValue = self.gameWindow.createPopup(won)
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
            self.gameWindow.initiateWindow()
            self._exitGame = True
            while True:
                event, values = self.gameWindow._window.read()
                if(event == psg.WIN_CLOSED):
                    break
                n, m, bombs = self.gameWindow.readVals(list(values.values()))
                if(n != None):
                    break
            if(values == None):
                break
            
            layout = Layout(n, m, bombs)
            board = Board(layout)

            self.gameWindow.startGameWindow(board)
            self.gameWindow.parseVisuals()
            
            while True:
                event, values = self.gameWindow._window.read()
                if(event == psg.WIN_CLOSED):
                    break
                # checking if the event is a keyboard input
                if(len(event) == 1):
                    self.gameWindow.parseXyzzy(event)
                    continue
                # checking if the button was right clicked
                if(event.startswith("marker")):
                    event = event[event.find("(")+1: len(event)-1]
                    n, m = event.split(", ")
                    self.gameWindow._board.rClick(int(n), int(m))
                    self.gameWindow.parseCell(int(n), int(m))
                    flagAmount = int(self.gameWindow._window["-FLAGS-"].get())
                    if(flagAmount == self.gameWindow._board.getLayout().getBombs()):
                        if(self.gameWindow._board.checkWinFlags() == True):
                            Game.gameEnded(self, True)
                            break
                    continue
                n, m = event.split(" ")
                self.gameWindow._board.lClick(int(n), int(m))
                if(self.gameWindow._board.getBoard()[int(n)][int(m)] != 0):
                    self.gameWindow.parseCell(int(n), int(m))
                    if(self.gameWindow._board.getBoard()[int(n)][int(m)] == -1):
                        Game.gameEnded(self, False)
                        break
                else:
                    self.gameWindow.parseVisuals()
                if(self.gameWindow._board.checkWinCells() == True):
                    Game.gameEnded(self, True)
                    break
            
            self.gameWindow._window.close()
            if(self._exitGame == True):
                break
            
    def getGameWindow(self):
        return self.gameWindow

if __name__ == "__main__":
    gameWindow = GameWindow()
    Game(gameWindow).startGame()
    
def getGameWindow():
        return gameWindow
# else:
#     def japierdole(gameWindowOuter):
#         gameWindow = gameWindowOuter

