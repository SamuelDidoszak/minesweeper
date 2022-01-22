import sys
sys.path.append("../minesweeper")

import unittest
# import thread
import threading
import time
import game
from gameWindow import *
import PySimpleGUI as psg

class MyTestCase(unittest.TestCase):
   def test_1(self):
        gameWindow = GameWindow()
        thread = threading.Thread(target=game.Game(gameWindow).startGame)
        thread.start()
        time.sleep(1)
        
        gameWindow._window["-N-"].update(8)
        gameWindow._window["-M-"].update(8)
        gameWindow._window["-BOMBS-"].update(12)
        gameWindow._window["-START-"].click()
        
        time.sleep(1)
        
        layout = gameWindow._board.getLayout().getMap()
        
        count = 0
        for n in range(0, 8):
            if(count == 5):
                break
            for m in range(0, 8):
                if(layout[n][m] != -1):
                    gameWindow._board.lClick(int(n), int(m))
                    gameWindow.parseVisuals()
                else:
                    gameWindow._board.rClick(int(n), int(m))
                    gameWindow.parseVisuals()
                count += 1
                if(count == 5):
                    break
        
        
        # PySimpleGui uses gameLoop and doesn't really close in any other ways. 
        # Calling .close() method only closes the window and leaves infinite loop hanging on a separate thread
        
        gameWindow._window.close()
        time.sleep(3)
        
        gameWindow = GameWindow()
        thread2 = threading.Thread(target=game.Game(gameWindow).startGame)
        thread2.start()
        time.sleep(3)
        
        gameWindow._window["-N-"].update(8)
        gameWindow._window["-M-"].update(8)
        gameWindow._window["-BOMBS-"].update(12)
        time.sleep(2)
        gameWindow._window["-START-"].click()
        
        for n in range(0, 8):
            for m in range(0, 8):
                self.assertTrue(gameWindow._window["{} {}".format(n, m)].get_text() == " ")
        
        
        self.assertTrue(gameWindow._window["-FLAGS-"].get_text() == "0")
        
        return
        

unittest.main()