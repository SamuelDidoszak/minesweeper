import PySimpleGUI as psg
from minesweeper import *

class GameWindow:
    def initiateWindow(self):
        windowLayout = [
            # [psg.Text("n: \t"), psg.Input(key="-N-")],
            # [psg.Text("m: \t"), psg.Input(key="-M-")],
            # [psg.Text("Bombs: \t"), psg.Input(key="-BOMBS-")],
            [psg.Text("n: \t", text_color="#FFFFFF", background_color="#303f9f"), psg.Input(text_color="#FFFFFF", background_color="#3f51b5")],
            [psg.Text("m: \t", text_color="#FFFFFF", background_color="#303f9f"), psg.Input(text_color="#FFFFFF", background_color="#3f51b5")],
            [psg.Text("Bombs: \t", text_color="#FFFFFF", background_color="#303f9f"), psg.Input(text_color="#FFFFFF", background_color="#3f51b5")],
            [psg.Text(size=(40,1), key='-ERRORMSG-', text_color="#ff5722", background_color="#303f9f")],
            [psg.Button("Start", button_color=("#FFFFFF", "#3f51b5"))]
        ]
        self.window = psg.Window("Minesweeper", windowLayout
                                 , background_color="#303f9f")
        
    def readVals(self):
        # event, values = self.window.read()
        self.window["-ERRORMSG-"].update("")
        # check variables
        try:
            n, m, bombs = (int(values[0]), int(values[1]), int(values[2]))
        except:
            self.window["-ERRORMSG-"].update("insert all values")
            return None, None, None
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
                if(val == 0):
                    self.window["{} {}".format(i, j)].update(" ", disabled = True, button_color=("#303f9f", "#303f9f"))
                elif(val == -4):
                    self.window["{} {}".format(i, j)].update(" ")
                elif(val == -1):
                    self.window["{} {}".format(i, j)].update("*", disabled = True)
                elif(val == -2):
                    self.window["{} {}".format(i, j)].update("!")
                elif(val == -3):
                    self.window["{} {}".format(i, j)].update("?")
                else:
                    self.window["{} {}".format(i, j)].update("{}".format(val), disabled = True)
    
    def parseCell(self, i, j):
                val = self.board.board[i][j]
                if(val == 0):
                    self.window["{} {}".format(i, j)].update(" ", disabled = True, button_color=("#303f9f", "#303f9f"))
                elif(val == -4):
                    self.window["{} {}".format(i, j)].update(" ", disabled = False)
                elif(val == -1):
                    self.window["{} {}".format(i, j)].update("*", disabled = True)
                elif(val == -2):
                    self.window["{} {}".format(i, j)].update("!", disabled = True)
                    self.window["-FLAGS-"].update(int(self.window["-FLAGS-"].get()) + 1)
                elif(val == -3):
                    self.window["{} {}".format(i, j)].update("?", disabled = True)
                    self.window["-FLAGS-"].update(int(self.window["-FLAGS-"].get()) - 1)
                else:
                    self.window["{} {}".format(i, j)].update("{}".format(val), disabled = True, button_color=("#FFFFFF", "#3f51b5"))
        
            
    def startGameWindow(self, board):
        self.board = board
        windowLayout = [
            [psg.Text("0", key='-FLAGS-', text_color="#FFFFFF", background_color="#303f9f", justification="right", expand_x=True, pad=(0, 0)), 
             psg.Text("/ {}".format(self.board.layout.bombs), key='-BOMBS-', text_color="#FFFFFF", background_color="#303f9f", justification="left", pad=(0, 0))],
            [[psg.Button(-4, key="{} {}".format(i, j),
                                    # right_click_menu=["rightClick",[f" ?::{i, j}" if self.board.board[i][j] == -2 else f" !::{i, j}"]],
                                    right_click_menu=["rightClick",[f"marker::{i, j}"]],
                                    size=(2, 1), button_color=("#FFFFFF", "#3f51b5"), font="* 16 bold", disabled_button_color=("#FFFFFF", "#3f51b5")
                                    ) for j in range(0, m)] for i in range(0, n)]
        ]
        self.window = psg.Window("Minesweeper", windowLayout, finalize=True, background_color="#303f9f")
        # GameWindow.parseVisuals(self)
    
    def gameLoop(self):
        while True:
            event, values = gameWindow.window.read()
            if(event == psg.WIN_CLOSED):
                break
            # checking if the button was right clicked
            if(event.startswith("marker")):
                event = event[event.find("(")+1: len(event)-1]
                n, m = event.split(", ")
                self.board.rClick(int(n), int(m))
                GameWindow.parseCell(self, int(n), int(m))
                flagAmount = int(self.window["-FLAGS-"].get())
                if(flagAmount == self.board.layout.bombs):
                    if(self.board.checkWinFlags() == True):
                        print("YOU WON")
                continue
            n, m = event.split(" ")
            self.board.lClick(int(n), int(m))
            if(self.board.board[int(n)][int(m)] != 0):
                GameWindow.parseCell(self, int(n), int(m))
            else:
                GameWindow.parseVisuals(self)
            if(self.board.checkWinCells() == True):
                print("YOU WON")
        
        

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