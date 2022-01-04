import random

class Layout:
    def _boundaries(self, val, max):
        if(val < 0):
            return 0
        elif(val > max - 1):
            return max - 1
        else:
            return val
    
    def __init__(self, n, m, bombs):
        self.bombs = bombs
        self.n = n
        self.m = m
        # -2 for empty
        # -1 for bomb
        self.map = [[-2 for i in range(0, m)] for i in range(0, n)]
        # if it takes long, add a list of bombless cells
        while(bombs != 0):
            nRand = random.randint(0, n - 1)
            mRand = random.randint(0, m - 1)
            if(self.map[nRand][mRand] == -2):
                self.map[nRand][mRand] = -1
                bombs -= 1
        # count surrounding bombs
        for n in range(0, self.n):
            for m in range(0, self.m):
                if(self.map[n][m] == -2):
                    count = 0
                    for i in range(Layout._boundaries(self, n - 1, self.n), Layout._boundaries(self, n + 1, self.n) + 1):
                        for j in range(Layout._boundaries(self, m - 1, self.m), Layout._boundaries(self, m + 1, self.m) + 1):
                            count += 1 if self.map[i][j] == -1 else 0
                    self.map[n][m] = count          
                            
    def print(self):
        val = 0
        for n in range(0, self.n):
            for m in range(0, self.m):
                val = self.map[n][m]
                if(val == -1):
                    print("*", end = "\t")
                else:
                    print(val, end = "\t")
            print("\n")
            
            
class Board:    
    def __init__(self, layout):
        self.layout = layout
        self.gameOver = False
        # -4 inactive
        # -1 bomb in a cell
        # -2 marked bomb
        # -3 ?
        # 0-9 bombs nearby
        self.board = [[-4 for i in range(0, self.layout.m)] for i in range(0, self.layout.n)]
    
    def _changeCell(self, yPos, xPos):
        y = self.layout._boundaries(yPos, self.layout.n)
        x = self.layout._boundaries(xPos, self.layout.m)
        self.board[y][x] = self.layout.map[y][x]
        
    def _scan(self, m1, m2, n, stack, changeTable):
        added = False
        # uncover left corner
        if(self.layout.map[n][self.layout._boundaries(m1 - 1, self.layout.m)] != 0):
            changeTable[n][self.layout._boundaries(m1 - 1, self.layout.m)] = self.layout.map[n][self.layout._boundaries(m1 - 1, self.layout.m)]
        for m in range(m1, m2 + 1):
            if(self.layout.map[n][m] != 0):
                changeTable[n][m] = self.layout.map[n][m]
                added = False
            elif(added == False):
                stack.append([n, m])
                added = True
        # uncover right corner
        if(self.layout.map[n][self.layout._boundaries(m2 + 1, self.layout.m)] != 0):
            changeTable[n][self.layout._boundaries(m2 + 1, self.layout.m)] = self.layout.map[n][self.layout._boundaries(m2 + 1, self.layout.m)]
                    
    def showSurrounding(self, n, m):
        try:
            if(self.layout.map[n][m] != 0):
                return
            stack = []
            changeTable = [[-4 for i in range(0, self.layout.m)] for i in range(0, self.layout.n)]
            stack.append([n, m])
            while(len(stack) != 0):
                n, m = stack.pop()
                m1 = m
                m1_1Bound = self.layout._boundaries(m1 - 1, self.layout.m)
                while(self.layout.map[n][m1_1Bound] == 0 and changeTable[n][m1_1Bound] == -4):
                    changeTable[n][m1_1Bound] = 0
                    m1 = m1 - 1
                    m1_1Bound = self.layout._boundaries(m1 - 1, self.layout.m)
                    if(m1 <= 0):
                        m1 = 0
                        break
                changeTable[n][self.layout._boundaries(m1 - 1, self.layout.m)] = self.layout.map[n][self.layout._boundaries(m1 - 1, self.layout.m)]       # uncover last from left
                while(self.layout.map[n][m] == 0 and (changeTable[n][m] == -4 or (changeTable[n][m] == 0 and m == 0))):
                    changeTable[n][m] = 0
                    m = m + 1
                    if(m == self.layout.m):
                        break
                changeTable[n][self.layout._boundaries(m, self.layout.m)] = self.layout.map[n][self.layout._boundaries(m, self.layout.m)]        # uncover last from right   |   doesn't work when m = 0
                if(m == 0):
                    m += 1
                if(n + 1 <= self.layout.n - 1):
                    Board._scan(self, m1, m - 1, n + 1, stack, changeTable)
                if(n - 1 >= 0 and (changeTable[n - 1][self.layout._boundaries(m1, self.layout.m)] == -4 or changeTable[n - 1][self.layout._boundaries(m, self.layout.m)] == -4)):
                    # m1_1Bound = self.layout._boundaries(m1 - 1, self.layout.m)
                    Board._scan(self, m1, m - 1, n - 1, stack, changeTable)
        
        finally:
            for n in range(0, self.layout.n):
                for m in range(0, self.layout.m):
                    if(changeTable[n][m] != -4 and self.board[n][m] != -2 and self.board[n][m] != -3):
                        self.board[n][m] = changeTable[n][m]

    
    def lClick(self, n, m):
        if(self.board[n][m] != -4):
            return
        self.board[n][m] = self.layout.map[n][m]
        if(self.board[n][m] == -1):
            self.gameOver = True
            return
        if(self.board[n][m] == 0):
            self.board[n][m] = -4
            Board.showSurrounding(self, n, m)
    
    def rClick(self, n, m):
        if(self.board[n][m] > -2):
            return
        if(self.board[n][m] == -4):
            self.board[n][m] = -2
            # self.layout.bombs -= 1
        elif(self.board[n][m] == -2):
            self.board[n][m] = self.board[n][m] - 1
            # self.layout.bombs += 1
        elif(self.board[n][m] == -3):
            self.board[n][m] = self.board[n][m] - 1
            
    def print(self, board):
        val = 0
        for n in range(0, self.layout.n):
            for m in range(0, self.layout.m):
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
        for n in range(0, self.layout.n):
            for m in range(0, self.layout.m):
                if(self.board[n][m] == -2 and self.layout.map[n][m] == -1):
                    correctFlags += 1
        return correctFlags == self.layout.bombs
    
    def checkWinCells(self):
        cellAmount = 0
        for n in range(0, self.layout.n):
            for m in range(0, self.layout.m):
                if(self.board[n][m] == -4 or self.board[n][m] == -2 or self.board[n][m] == -3):
                    cellAmount += 1
        return cellAmount == self.layout.bombs