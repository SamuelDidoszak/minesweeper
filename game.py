from gameWindow import *
from layout import *
from board import *

def gameEnded(won, gameWindow):
        returnValue = gameWindow.createPopup(won)
        global exitGame
        if(returnValue == "Exit"):
            exitGame = True
        else:
            exitGame = False
            return


gameWindow = GameWindow()

while True:
    gameWindow.initiateWindow()
    exitGame = True
    while True:
        event, values = gameWindow.window.read()
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
        event, values = gameWindow.window.read()
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
            gameWindow.board.rClick(int(n), int(m))
            gameWindow.parseCell(int(n), int(m))
            flagAmount = int(gameWindow.window["-FLAGS-"].get())
            if(flagAmount == gameWindow.board.layout.bombs):
                if(gameWindow.board.checkWinFlags() == True):
                    gameEnded(True, gameWindow)
                    break
            continue
        n, m = event.split(" ")
        gameWindow.board.lClick(int(n), int(m))
        if(gameWindow.board.board[int(n)][int(m)] != 0):
            gameWindow.parseCell(int(n), int(m))
            if(gameWindow.board.board[int(n)][int(m)] == -1):
                gameEnded(False, gameWindow)
                break
        else:
            gameWindow.parseVisuals()
        if(gameWindow.board.checkWinCells() == True):
            gameEnded(True, gameWindow)
            break
    
    gameWindow.window.close()
    if(exitGame == True):
        break