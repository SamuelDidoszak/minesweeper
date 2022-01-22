import sys
sys.path.append("../minesweeper")

import unittest
# import thread
import threading
import time
import game
from gameWindow import *

class MyTestCase(unittest.TestCase):
   def test_1(self):
       
        gameWindow = GameWindow()
        thread = threading.Thread(target=game.Game(gameWindow).startGame)
        thread.start()
        
        time.sleep(1)
        
        gameWindow.readVals((1, 1, 1))
        self.assertTrue(gameWindow._window["-ERRORMSG-"].get() != "")
        
        gameWindow.readVals((5, 1, 2))
        self.assertTrue(gameWindow._window["-ERRORMSG-"].get() != "")
        
        gameWindow.readVals((4, 1, 2))
        self.assertTrue(gameWindow._window["-ERRORMSG-"].get() != "")
        
        gameWindow.readVals((20, 500, 12))
        self.assertTrue(gameWindow._window["-ERRORMSG-"].get() != "")
        
        gameWindow.readVals((5, 6, -4))
        self.assertTrue(gameWindow._window["-ERRORMSG-"].get() != "")
        
        gameWindow.readVals((3, 3, 10))
        self.assertTrue(gameWindow._window["-ERRORMSG-"].get() != "")
        
        gameWindow.readVals((1, 10, 5))
        self.assertTrue(gameWindow._window["-ERRORMSG-"].get() != "")

unittest.main()