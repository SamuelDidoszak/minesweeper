import random

class Layout:
    """
    Class for the layout of the game.
    Holds the map with cell values.
    
    Attributes:
        _n(int): x dimension value
        _m(int): y dimension value
        _bombs(int): amount of bombs
        _map(int[][]): map of the game. It's values are -1 if the cell contains a bomb, or numbers 0-8 that represent the amount of surrounding bombs
    """
    def _boundaries(self, val, max):
        """
        Checks if val is within bounds of map
        
        Parameters:
            val(int): value to check
            max(int): maximum bound value. Pass n or m
            
        Returns:
            either val, 0 if val < 0 or max if val > max - 1
        """
        if(val < 0):
            return 0
        elif(val > max - 1):
            return max - 1
        else:
            return val
    
    def __init__(self, n, m, bombs):
        """
        The constructor for Layout class.
        Initializes the map and counts surrounding bombs for every cell
        
        Attributes:
            n(int): x length value
            m(int): y length value
            bombs(int): amount of bombs
        """
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
        """
        Prints map to the console
        Useful for debugging purposes
        """
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
        """
        Returns:
            int[][]: the _map attribute
            It's values are -1 if the cell contains a bomb, or numbers 0-8 that represent the amount of surrounding bombs
        """
        return self._map
    
    def getBombs(self):
        """
        Returns:
            int: the amount of bombs
        """
        return self._bombs