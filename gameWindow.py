import PySimpleGUI as psg
from layout import *
from board import *
from exceptions import *

class GameWindow:
    def initiateWindow(self):
        windowLayout = [
            [psg.Text("n: \t", text_color="#FFFFFF", background_color="#303f9f"), psg.Input(key="-N-", text_color="#FFFFFF", background_color="#3f51b5")],
            [psg.Text("m: \t", text_color="#FFFFFF", background_color="#303f9f"), psg.Input(key="-M-", text_color="#FFFFFF", background_color="#3f51b5")],
            [psg.Text("Bombs: \t", text_color="#FFFFFF", background_color="#303f9f"), psg.Input(key="-BOMBS-", text_color="#FFFFFF", background_color="#3f51b5")],
            [psg.Text(size=(40,1), key='-ERRORMSG-', text_color="#ff5722", background_color="#303f9f")],
            [psg.Button("Start", button_color=("#FFFFFF", "#3f51b5"))]
        ]
        self.window = psg.Window("Minesweeper", windowLayout, finalize=True
                                 , background_color="#303f9f")
    
    def readVals(self, values):
        self.window["-ERRORMSG-"].update("")
        # check variables
        try:
            n, m, bombs = (int(values[0]), int(values[1]), int(values[2]))
        except:
            self.window["-ERRORMSG-"].update(EmptyValuesException())
            return None, None, None
        try:
            if(n < 2 or n > 15):
                raise ValuesOutOfBoundsException("n")
            if(m < 2 or m > 15):
                raise ValuesOutOfBoundsException("m")
            if(bombs < 1 or bombs > (n * m)):
                raise ValuesOutOfBoundsException("bombs")
        except ValuesOutOfBoundsException as e:
            self.window["-ERRORMSG-"].update(e)
            self.window["-{}-".format(str(e.val).upper())].update("")
            
        if(self.window["-ERRORMSG-"].get() == ""):
            self.window.close()
            return n, m, bombs
        
        return None, None, None   

    def parseVisuals(self):
        for i in range(0, self.board.layout.n):
            for j in range(0, self.board.layout.m):
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
                    
    def parseXyzzy(self, key):
        if(key == "x"):
            self.keyInputs = ["x"]
        else:
            self.keyInputs.append(key)
        if("".join(self.keyInputs[-5 : len(self.keyInputs)+1]) == "xyzzy"):
            for n in range(0, self.board.layout.n):
                for m in range(0, self.board.layout.m):
                    if(self.board.layout.map[n][m] == -1):
                        self.window["{} {}".format(n, m)].update(button_color=("#ff5722", "#ff5722"))
                          
    def startGameWindow(self, board):
        self.board = board
        windowLayout = [
            [psg.Text("0", key='-FLAGS-', text_color="#FFFFFF", background_color="#303f9f", justification="right", expand_x=True, pad=(0, 0)), 
             psg.Text("/ {}".format(self.board.layout.bombs), key='-BOMBS-', text_color="#FFFFFF", background_color="#303f9f", justification="left", pad=(0, 0))],
            [[psg.Button("", key="{} {}".format(i, j),
                                    right_click_menu=["rightClick",[f"marker::{i, j}"]],
                                    size=(2, 1), button_color=("#FFFFFF", "#3f51b5"), font="* 16 bold", disabled_button_color=("#FFFFFF", "#3f51b5")
                                    ) for j in range(0, self.board.layout.m)] for i in range(0, self.board.layout.n)]
        ]
        self.window = psg.Window("Minesweeper", windowLayout, finalize=True, return_keyboard_events=True, background_color="#303f9f")
        self.keyInputs = []
    
    def createPopup(self, won):
        prompt = "You have won! \nStart a new game?" if won == True else "You lost. \nStart a new game?"
        returnValue = psg.popup(prompt, background_color="#303f9f", button_color=("#FFFFFF", "#3f51b5"), custom_text=("New game", "Exit"), grab_anywhere=True)
        return returnValue
