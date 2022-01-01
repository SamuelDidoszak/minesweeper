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
        
    # def showSurrounding(self, n, m):
    #     print("lookin for bombs hmmmm")
    #     i = n
    #     stops = []
    #     updown = 1
    #     try:
    #         while(i >= 0 and i < self.layout.n):
    #             j = m
    #             while(True):
    #                 j += 1
    #                 print("bruh")
    #                 if(j < self.layout.m):
    #                     print("[{}][{}]".format(i, j))
    #                     if(self.layout.map[i][j] != 0):
    #                         self.board[i][j] = self.layout.map[i][j]
    #                         break
    #                 else:
    #                     j -= 1
    #                     print("????????????????????")
    #                     break
    #             for j in range(j, -1, -1):
    #                 print("i, j: {} {}".format(i, j))
    #                 if(j != m or i != n):
    #                     print("\tok")
    #                     self.board[i][j] = self.layout.map[i][j]
    #                 if(self.layout.map[i][j] != 0):
    #                     break
    #             print("addin i")
    #             i -= 1
                
    #     finally:
    #         self.layout.print()
    #         print("\n")
    #         Board.print(self, self.board)
    
    def _changeCell(self, yPos, xPos):
        print("YOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO \t", yPos, xPos)
        y = self.layout._boundaries(yPos, self.layout.n)
        x = self.layout._boundaries(xPos, self.layout.m)
        self.board[y][x] = self.layout.map[y][x]
        print(self.layout.map[y][x], self.board[y][x])
                    
    def showSurrounding(self, n, m):
        print("lookin for bombs hmmmm")
        try:
            yPos = n
            xPos = m
            maxPos = 0
            # alghoritm written for bottom right corner
            while(True):
                maxPosTemp = 0
                while(self.layout.map[yPos][xPos] == 0):
                    print("uncovering and stuff")
                    # uncover surrounding cells
                    [Board._changeCell(self, y, x) for x in range(xPos - 1, xPos + 2) for y in range(yPos - 1, yPos + 2)]
                    xPos += 1
                    maxPosTemp += 1
                    if(xPos == self.layout.m or xPos == 0):
                        break
                if(maxPosTemp > maxPos):
                    maxPos = maxPosTemp
                xPos = m
                yPos += 1
                
                if(yPos == 0 or yPos == self.layout.n):
                    break
                
                if(self.layout.map[yPos][xPos] != 0):
                    while(True):
                        uncovered = 0
                        if(not(self.layout.map[yPos][xPos] == 0 or maxPosTemp < maxPos)):
                            break;
                        if(self.layout.map[yPos][xPos] == 0):
                            if(self.layout.map[yPos][xPos - 1] != 0):
                                newStart = xPos - 1
                                m = newStart                            # keep in mind
                            # uncover surrounding cells
                            [Board._changeCell(self, y, x) for x in range(xPos - 1, xPos + 2) for y in range(yPos - 1, yPos + 2)]
                            uncovered += 1
                        xPos += 1
                        if(xPos == 0 or xPos == self.layout.m):
                            break
                    yPos -= 1
                    if(uncovered == 0):
                        break
        
        finally:
            self.layout.print()
            print("\n")
            Board.print(self, self.board)
                    
    
    def lClick(self, n, m):
        if(self.board[n][m] != -4):
            return
        self.board[n][m] = self.layout.map[n][m]
        if(self.board[n][m] == -1):
            self.gameOver = True
            return
        if(self.board[n][m] == 0):
            Board.showSurrounding(self, n, m)
    
    def rClick(self, n, m):
        if(self.board[n][m] > -2):
            return
        if(self.board[n][m] == -4):
            self.board[n][m] = -2
            self.layout.bombs -= 1
        elif(self.board[n][m] == -2):
            self.board[n][m] = self.board[n][m] - 1
            self.layout.bombs += 1
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