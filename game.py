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
        while True:
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
            
    def startGameWindow(self, layout):
        windowLayout = [[psg.Button("\t") for i in range(0, n)] for i in range(0, m)]
        # self.window.layout = windowLayout
        # self.window.close()
        self.window = psg.Window("Minesweeper", windowLayout)
    
    def gameLoop(self):
        while True:
            event, values = gameWindow.window.read()
            if(event == psg.WIN_CLOSED):
                break
        
        

gameWindow = GameWindow()
gameWindow.initiateWindow()

while True:
    event, values = gameWindow.window.read()
    if(event == psg.WIN_CLOSED):
        break
    n, m, bombs = gameWindow.readVals()

    layout = Layout(n, m, bombs)
    layout.print();

    gameWindow.startGameWindow(layout)
    gameWindow.gameLoop()









# window.close()