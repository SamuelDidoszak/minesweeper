import layout

class Board:    
    def __init__(self, layout):
        self._layout = layout
        self._gameOver = False
        # -4 inactive
        # -1 bomb in a cell
        # -2 marked bomb
        # -3 ?
        # 0-9 bombs nearby
        self._board = [[-4 for i in range(0, Board.getM(self))] for i in range(0, Board.getN(self))]
    
    def _changeCell(self, yPos, xPos):
        y = self._layout._boundaries(yPos, Board.getN(self))
        x = self._layout._boundaries(xPos, Board.getM(self))
        self._board[y][x] = self._layout.getMap()[y][x]
        
    def _scan(self, m1, m2, n, stack, changeTable):
        added = False
        # uncover left corner
        m1_1LBound = self._layout._boundaries(m1 - 1, Board.getM(self))
        if(self._layout.getMap()[n][m1_1LBound] != 0):
            changeTable[n][m1_1LBound] = self._layout.getMap()[n][m1_1LBound]
        elif(m1 != 0 and self._layout.getMap()[n][m1] != 0):
            stack.append([n, m1_1LBound])
        for m in range(m1, m2 + 1):
            if(self._layout.getMap()[n][m] != 0):
                changeTable[n][m] = self._layout.getMap()[n][m]
                added = False
            elif(added == False):
                stack.append([n, m])
                added = True
        # uncover right corner
        m1_1RBound = self._layout._boundaries(m2 + 1, Board.getM(self))
        if(self._layout.getMap()[n][m1_1RBound] != 0):
            changeTable[n][m1_1RBound] = self._layout.getMap()[n][m1_1RBound]
        elif(m2 != Board.getM(self)-1 and self._layout.getMap()[n][m2] != 0):
            stack.append([n, m1_1RBound])
                    
    def showSurrounding(self, n, m):
        try:
            if(self._layout.getMap()[n][m] != 0):
                return
            stack = []
            changeTable = [[-4 for i in range(0, Board.getM(self))] for i in range(0, Board.getN(self))]
            stack.append([n, m])
            while(len(stack) != 0):
                n, m = stack.pop()
                m1 = m
                m1_1Bound = self._layout._boundaries(m1 - 1, Board.getM(self))
                while(self._layout.getMap()[n][m1_1Bound] == 0 and changeTable[n][m1_1Bound] == -4):
                    changeTable[n][m1_1Bound] = 0
                    m1 = m1 - 1
                    m1_1Bound = self._layout._boundaries(m1 - 1, Board.getM(self))
                    if(m1 <= 0):
                        m1 = 0
                        break
                changeTable[n][self._layout._boundaries(m1 - 1, Board.getM(self))] = self._layout.getMap()[n][self._layout._boundaries(m1 - 1, Board.getM(self))]       # uncover last from left
                while(self._layout.getMap()[n][m] == 0 and (changeTable[n][m] == -4 or (changeTable[n][m] == 0 and m == 0))):
                    changeTable[n][m] = 0
                    m = m + 1
                    if(m == Board.getM(self)):
                        break
                changeTable[n][self._layout._boundaries(m, Board.getM(self))] = self._layout.getMap()[n][self._layout._boundaries(m, Board.getM(self))]        # uncover last from right   |   doesn't work when m = 0
                if(m == 0):
                    m += 1
                if(n + 1 <= Board.getN(self) - 1):
                    Board._scan(self, m1, m - 1, n + 1, stack, changeTable)
                if(n - 1 >= 0 and (changeTable[n - 1][self._layout._boundaries(m1, Board.getM(self))] == -4 or changeTable[n - 1][self._layout._boundaries(m1 - 1, Board.getM(self))] == -4 or changeTable[n - 1][self._layout._boundaries(m, Board.getM(self))] == -4)):
                    Board._scan(self, m1, m - 1, n - 1, stack, changeTable)
        
        finally:
            for n in range(0, Board.getN(self)):
                for m in range(0, Board.getM(self)):
                    if(changeTable[n][m] != -4 and self._board[n][m] != -2 and self._board[n][m] != -3):
                        self._board[n][m] = changeTable[n][m]

    
    def lClick(self, n, m):
        if(self._board[n][m] != -4):
            return
        self._board[n][m] = self._layout.getMap()[n][m]
        if(self._board[n][m] == -1):
            self._gameOver = True
            return
        if(self._board[n][m] == 0):
            self._board[n][m] = -4
            Board.showSurrounding(self, n, m)
    
    def rClick(self, n, m):
        if(self._board[n][m] > -2):
            return
        if(self._board[n][m] == -4):
            self._board[n][m] = -2
        elif(self._board[n][m] == -2):
            self._board[n][m] = self._board[n][m] - 1
        elif(self._board[n][m] == -3):
            self._board[n][m] = self._board[n][m] - 1
            
    def print(self, board):
        val = 0
        for n in range(0, Board.getN(self)):
            for m in range(0, Board.getM(self)):
                val = board[n][m]
                if(val == -4):
                    print(" ", end = "\t")
                elif(val == -1):
                    print("*", end = "\t")
                elif(val == -2):
                    print("!", end = "\t")
                elif(val == -3):
                    print("?", end = "\t")
                else:
                    print(val, end = "\t")
            print("\n")
            
    def checkWinFlags(self):
        correctFlags = 0
        for n in range(0, Board.getN(self)):
            for m in range(0, Board.getM(self)):
                if(self._board[n][m] == -2 and self._layout.getMap()[n][m] == -1):
                    correctFlags += 1
        return correctFlags == self._layout.getBombs()
    
    def checkWinCells(self):
        cellAmount = 0
        for n in range(0, Board.getN(self)):
            for m in range(0, Board.getM(self)):
                if(self._board[n][m] == -4 or self._board[n][m] == -2 or self._board[n][m] == -3):
                    cellAmount += 1
        return cellAmount == self._layout.getBombs()
    
    
    # getters
    
    def getN(self):
        return self._layout._n
    
    def getM(self):
        return self._layout._m
    
    def getLayout(self):
        return self._layout
    
    def getGameOver(self):
        return self._gameOver
    
    def getBoard(self):
        return self._board