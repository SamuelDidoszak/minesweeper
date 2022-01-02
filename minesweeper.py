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
        # print("uncovering\t", yPos, xPos)
        y = self.layout._boundaries(yPos, self.layout.n)
        x = self.layout._boundaries(xPos, self.layout.m)
        self.board[y][x] = self.layout.map[y][x]
                    
    def showSurrounding(self, n, m):
        try:
            maxPos = 0
            xDirection = -1     # changes to 1 instantly
            yDirection = 1
            # alghoritm written for bottom right corner
            for side in range(1, 5):
                if(side % 2 == 1):
                    xDirection *= -1
                if(side % 3 == 0):
                    yDirection *= -1
                
                yPos = n
                xPos = m
                print("\n\ncurrent iteration: {}\n\n".format(side))
                print(xDirection, yDirection, "\n\n")
                
                while(True):
                    maxPosTemp = 0
                    newMax = False
                    while(self.layout.map[yPos][xPos] == 0):
                        # uncover surrounding cells
                        [Board._changeCell(self, y, x) for x in range(xPos - 1, xPos + 2) for y in range(yPos - 1, yPos + 2)]
                        xPos += 1 * xDirection
                        maxPosTemp += 1
                        if(xPos < 0 or xPos >= self.layout.m):
                            break
                    if(maxPosTemp > maxPos):
                        newMax = True if maxPos != 0 else False
                        maxPos = maxPosTemp
                    maxPosTemp = 0
                    xPos = m
                    yPos += 1 * yDirection
                    
                    if(yPos < 0 or yPos >= self.layout.n):
                        break
                    
                    debugIteration = 0
                    if(self.layout.map[yPos][xPos] != 0 or newMax == True):
                        print("got to alternative: ", yPos, ":", xPos)
                        while(True):
                            if(debugIteration == 30):
                                print("debug timee")
                            print("iteration")
                            uncovered = 0
                            if(not(self.layout.map[yPos][xPos] == 0 or maxPosTemp < maxPos)):
                                print("broken")
                                break;
                            maxPosTemp = 0
                            if(self.layout.map[yPos][xPos] == 0):
                                if(self.layout.map[yPos][self.layout._boundaries(xPos - 1 * xDirection, self.layout.m)] != 0):
                                    print("gave newStart")
                                    newStart = xPos - 1 * xDirection
                                    m = newStart                            # keep in mind
                                    # Board.showSurrounding(self, yPos, newStart)
                                # uncover surrounding cells
                                print("uncovering from alternative: ", yPos, ":", xPos, "->")
                                [Board._changeCell(self, y, x) for x in range(xPos - 1, xPos + 2) for y in range(yPos - 1, yPos + 2)]
                                uncovered += 1
                            xPos += 1 * xDirection
                            maxPosTemp += 1
                            if(xPos < 0 or xPos >= self.layout.m):
                                xPos = m
                                break
                            debugIteration += 1
                        yPos += 1 * yDirection
                        if(yPos < 0 or yPos >= self.layout.n):
                            break
                        if(uncovered == 0):
                            print("no uncovered, end of the algorithm")
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