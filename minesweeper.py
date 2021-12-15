import random

class Layout:
    def __init__(self, n, m, bombs):
        self.bombs = bombs
        self.n = n
        self.m = m
        self.map = [[False for i in range(0, m)] for i in range(0, n)]
        # if it takes long, add a list of bombless cells
        while(bombs != 0):
            nRand = random.randint(0, n - 1)
            mRand = random.randint(0, m - 1)
            if(self.map[nRand][mRand] == False):
                self.map[nRand][mRand] = True
                bombs -= 1
                
    def _boundaries(self, val, max):
        if(val < 0):
            return 0
        elif(val > max - 1):
            return max - 1
        else:
            return val
               
    def countSurrounding(self):
        for n in range(0, self.n):
            for m in range(0, self.m):
                if(self.map[n][m] == False):
                    count = 0
                    for i in range(Layout._boundaries(self, n - 1, self.n), Layout._boundaries(self, n + 1, self.n) + 1):
                        for j in range(Layout._boundaries(self, m - 1, self.m), Layout._boundaries(self, m + 1, self.m) + 1):
                            count += 1 if self.map[i][j] == True and isinstance(self.map[i][j], (bool)) else 0
                    self.map[n][m] = count              
                            
    def print(self):
        for n in range(0, len(self.map)):
            for m in range(0, len(self.map[0])):
                print(self.map[n][m], end = "\t")
            print("\n")
    


layout = Layout(3, 8, 10)
layout.countSurrounding()
layout.print();