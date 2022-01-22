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
        
        gameWindow._window["-N-"].update(8)
        gameWindow._window["-M-"].update(8)
        gameWindow._window["-BOMBS-"].update(12)
        gameWindow._window["-START-"].click()
        
        gameWindow
        time.sleep(1)
        
        layout = gameWindow._board.getLayout().getMap()
        
        for n in range(0, 8):
            for m in range(0, 8):
                if(layout[n][m] == -1):
                    gameWindow._board.lClick(int(n), int(m))
                    gameWindow.parseCell(int(n), int(m))
                    self.assertTrue(gameWindow._window["{} {}".format(n, m)].get_text() == "*")
                    return
        

unittest.main()