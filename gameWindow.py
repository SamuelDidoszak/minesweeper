import PySimpleGUI as psg
from layout import *
from board import *
from exceptions import *

class GameWindow:
    """
    Class containing all of the methods necessary for displaying GUI to the user.
    
    Attributes:
        _window(PySimpleGUI Window): current window that is shown to the player
        _board(Board): board of the game
        _keyInputs(str[]): list containing the keystrokes input by the user. Clears every time user hits 'x' key
    """
    def initiateWindow(self):
        """
        The first method to be called. Creates the window which prompts user to input n, m and bomb values
        """
        windowLayout = [
            [psg.Text("n: \t", text_color="#FFFFFF", background_color="#303f9f"), psg.Input(key="-N-", text_color="#FFFFFF", background_color="#3f51b5")],
            [psg.Text("m: \t", text_color="#FFFFFF", background_color="#303f9f"), psg.Input(key="-M-", text_color="#FFFFFF", background_color="#3f51b5")],
            [psg.Text("Bombs: \t", text_color="#FFFFFF", background_color="#303f9f"), psg.Input(key="-BOMBS-", text_color="#FFFFFF", background_color="#3f51b5")],
            [psg.Text(size=(40,1), key='-ERRORMSG-', text_color="#ff5722", background_color="#303f9f")],
            [psg.Button("Start", button_color=("#FFFFFF", "#3f51b5"))]
        ]
        self._window = psg.Window("Minesweeper", windowLayout, finalize=True
                                 , background_color="#303f9f")
    
    def readVals(self, values):
        """
        Parses values input by the user.
        
        Params:
            values: values that user inserted into according psg.Input elements
            
        Returns:
            n(int): y dimension size of the game
            m(int): x dimension size of the game
            bombs(int): bomb number
            null, null, null if parsing threw errors
        """
        self._window["-ERRORMSG-"].update("")
        # check variables
        try:
            n, m, bombs = (int(values[0]), int(values[1]), int(values[2]))
        except:
            self._window["-ERRORMSG-"].update(EmptyValuesException())
            return None, None, None
        try:
            if(n < 2 or n > 15):
                raise ValuesOutOfBoundsException("n")
            if(m < 2 or m > 15):
                raise ValuesOutOfBoundsException("m")
            if(bombs < 1 or bombs > (n * m)):
                raise ValuesOutOfBoundsException("bombs")
        except ValuesOutOfBoundsException as e:
            self._window["-ERRORMSG-"].update(e)
            self._window["-{}-".format(str(e.val).upper())].update("")
            
        if(self._window["-ERRORMSG-"].get() == ""):
            self._window.close()
            return n, m, bombs
        
        return None, None, None   

    def parseVisuals(self):
        """
        Parses the graphical board of the whole game.
        Changes int values of the board into characters shown to the user and disables necessary cells
        """
        for i in range(0, self._board.getN()):
            for j in range(0, self._board.getM()):
                val = self._board.getBoard()[i][j]
                if(val == 0):
                    self._window["{} {}".format(i, j)].update(" ", disabled = True, button_color=("#303f9f", "#303f9f"))
                elif(val == -4):
                    self._window["{} {}".format(i, j)].update(" ")
                elif(val == -1):
                    self._window["{} {}".format(i, j)].update("*", disabled = True)
                elif(val == -2):
                    self._window["{} {}".format(i, j)].update("!")
                elif(val == -3):
                    self._window["{} {}".format(i, j)].update("?")
                else:
                    self._window["{} {}".format(i, j)].update("{}".format(val), disabled = True)
    
    def parseCell(self, i, j):
        """
        Parses the graphical board of the i, j cell
        Changes int value of the board into character shown to the user and disables necessary cells
        
        Parameters:
            i(int): y dimension number n of the board to be parsed
            j(int): x dimension number m of the board to be parsed
        """
        val = self._board.getBoard()[i][j]
        if(val == 0):
            self._window["{} {}".format(i, j)].update(" ", disabled = True, button_color=("#303f9f", "#303f9f"))
        elif(val == -4):
            self._window["{} {}".format(i, j)].update(" ", disabled = False)
        elif(val == -1):
            self._window["{} {}".format(i, j)].update("*", disabled = True)
        elif(val == -2):
            self._window["{} {}".format(i, j)].update("!", disabled = True)
            self._window["-FLAGS-"].update(int(self._window["-FLAGS-"].get()) + 1)
        elif(val == -3):
            self._window["{} {}".format(i, j)].update("?", disabled = True)
            self._window["-FLAGS-"].update(int(self._window["-FLAGS-"].get()) - 1)
        else:
            self._window["{} {}".format(i, j)].update("{}".format(val), disabled = True, button_color=("#FFFFFF", "#3f51b5"))
                    
    def parseXyzzy(self, key):
        """
        Handles the keystrokes sent by the user.
        If the player inputs 'xyzzy', all the buttons under which bombs reside change their color to yellow
        """
        if(key == "x"):
            self._keyInputs = ["x"]
        else:
            self._keyInputs.append(key)
        if("".join(self._keyInputs[-5 : len(self._keyInputs)+1]) == "xyzzy"):
            for n in range(0, self._board.getN()):
                for m in range(0, self._board.getM()):
                    if(self._board.getLayout().getMap()[n][m] == -1):
                        self._window["{} {}".format(n, m)].update(button_color=("#ff5722", "#ff5722"))
                          
    def startGameWindow(self, board):
        """
        Starts the window containing the whole game GUI and its layout
        
        Parameters:
            board(Board): the board which is initiated into _board attribute
        """
        self._board = board
        windowLayout = [
            [psg.Text("0", key='-FLAGS-', text_color="#FFFFFF", background_color="#303f9f", justification="right", expand_x=True, pad=(0, 0)), 
             psg.Text("/ {}".format(self._board.getLayout().getBombs()), key='-BOMBS-', text_color="#FFFFFF", background_color="#303f9f", justification="left", pad=(0, 0))],
            [[psg.Button("", key="{} {}".format(i, j),
                                    right_click_menu=["rightClick",[f"marker::{i, j}"]],
                                    size=(2, 1), button_color=("#FFFFFF", "#3f51b5"), font="* 16 bold", disabled_button_color=("#FFFFFF", "#3f51b5")
                                    ) for j in range(0, self._board.getM())] for i in range(0, self._board.getN())]
        ]
        self._window = psg.Window("Minesweeper", windowLayout, finalize=True, return_keyboard_events=True, background_color="#303f9f")
        self._keyInputs = []
    
    def createPopup(self, won):
        """
        Creates a popup presenting a decision to the player whether he wants to continue the game or exit it.
        Value of the popup changes with the won value 
            
        Parameters:
            won(Bool): a boolean meaning if the game was won.
        """
        prompt = "You have won! \nStart a new game?" if won == True else "You lost. \nStart a new game?"
        returnValue = psg.popup(prompt, background_color="#303f9f", button_color=("#FFFFFF", "#3f51b5"), custom_text=("New game", "Exit"), grab_anywhere=True)
        return returnValue