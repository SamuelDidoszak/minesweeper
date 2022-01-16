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
        self._bombs = bombs
        self._n = n
        self._m = m
        # -2 for empty
        # -1 for bomb
        self._map = [[-2 for i in range(0, m)] for i in range(0, n)]
        # if it takes long, add a list of bombless cells
        while(bombs != 0):
            nRand = random.randint(0, n - 1)
            mRand = random.randint(0, m - 1)
            if(self._map[nRand][mRand] == -2):
                self._map[nRand][mRand] = -1
                bombs -= 1
        # count surrounding bombs
        for n in range(0, self._n):
            for m in range(0, self._m):
                if(self._map[n][m] == -2):
                    count = 0
                    for i in range(Layout._boundaries(self, n - 1, self._n), Layout._boundaries(self, n + 1, self._n) + 1):
                        for j in range(Layout._boundaries(self, m - 1, self._m), Layout._boundaries(self, m + 1, self._m) + 1):
                            count += 1 if self._map[i][j] == -1 else 0
                    self._map[n][m] = count          
                            
    def print(self):
        val = 0
        for n in range(0, self._n):
            for m in range(0, self._m):
                val = self._map[n][m]
                if(val == -1):
                    print("*", end = "\t")
                else:
                    print(val, end = "\t")
            print("\n")
            
    def getMap(self):
        return self._map
    
    def getBombs(self):
        return self._bombs