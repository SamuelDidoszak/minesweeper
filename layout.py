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