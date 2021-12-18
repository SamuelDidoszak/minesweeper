import PySimpleGUI as psg
from minesweeper import *

class GameWindow:
    def initiateWindow(self):
        windowLayout = [
            # [psg.Text("n: \t"), psg.Input(key="-N-")],
            # [psg.Text("m: \t"), psg.Input(key="-M-")],
            # [psg.Text("Bombs: \t"), psg.Input(key="-BOMBS-")],
            [psg.Text("n: \t"), psg.Input()],
            [psg.Text("m: \t"), psg.Input()],
            [psg.Text("Bombs: \t"), psg.Input()],
            [psg.Text(size=(40,1), key='-ERRORMSG-')],
            [psg.Button("Start")]
        ]
        self.window = psg.Window("Minesweeper", windowLayout)
        
    def readVals(self):
        # event, values = self.window.read()
        self.window["-ERRORMSG-"].update("")
        # check variables
        n, m, bombs = (int(values[0]), int(values[1]), int(values[2]))
        if(n < 2 or n > 15):
            self.window["-ERRORMSG-"].update("n value is out of bounds")
            # window["-N-"].update("")
        if(m < 2 or m > 15):
            self.window["-ERRORMSG-"].update("m value is out of bounds")
            # window["-M-"].update("")
        if(bombs < 1 or bombs > (n * m)):
            self.window["-ERRORMSG-"].update("bomb value is out of bounds")
            # window["-BOMBS-"].update("")
            
        if(self.window["-ERRORMSG-"].get() == ""):
            self.window.close()
            return n, m, bombs
        
        return None, None, None

    def parseVisuals(self):
        for i in range(0, n):
            for j in range(0, m):
                val = self.board.board[i][j]
                if(val == -4):
                    self.window["{} {}".format(i, j)].update("   ")
                elif(val == -1):
                    self.window["{} {}".format(i, j)].update(" * ")
                elif(val == -2):
                    self.window["{} {}".format(i, j)].update(" ! ")
                elif(val == -3):
                    self.window["{} {}".format(i, j)].update(" ? ")
                else:
                    self.window["{} {}".format(i, j)].update(" {} ".format(val))
    
    def parseCell(self, i, j):
                val = self.board.board[i][j]
                if(val == -4):
                    self.window["{} {}".format(i, j)].update("   ")
                elif(val == -1):
                    self.window["{} {}".format(i, j)].update(" * ")
                elif(val == -2):
                    self.window["{} {}".format(i, j)].update(" ! ")
                elif(val == -3):
                    self.window["{} {}".format(i, j)].update(" ? ")
                else:
                    self.window["{} {}".format(i, j)].update(" {} ".format(val))
        
            
    def startGameWindow(self, board):
        self.board = board
        windowLayout = [[psg.Button(-4, key="{} {}".format(i, j)) for i in range(0, m)] for j in range(0, n)]
        self.window = psg.Window("Minesweeper", windowLayout, finalize=True)
        # GameWindow.parseVisuals(self)
    
    def gameLoop(self):
        while True:
            event, values = gameWindow.window.read()
            if(event == psg.WIN_CLOSED):
                break
            print("event: ", event)
            n, m = event.split(" ")
            self.board.lClick(int(n), int(m))
            GameWindow.parseCell(self, int(n), int(m))
        
        

gameWindow = GameWindow()
gameWindow.initiateWindow()

while True:
    while True:
        event, values = gameWindow.window.read()
        if(event == psg.WIN_CLOSED):
            break
        n, m, bombs = gameWindow.readVals()
        if(n != None):
            break

    layout = Layout(n, m, bombs)
    board = Board(layout)
    # layout.print();

    gameWindow.startGameWindow(board)
    gameWindow.parseVisuals()
    gameWindow.gameLoop()
    break









# window.close()