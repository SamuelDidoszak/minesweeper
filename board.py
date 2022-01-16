import layout

class Board:
    """
    Class for the board that player sees. Contains methods that operate on that board
    
    Attributes:
        _layout(Layout): a layout of the game
        _board(int[][]): board that player sees
        
    """
    def __init__(self, layout):
        """
        The constructor for Board class.
        Creates the _board
        
        Attributes:
            _layout(Layout): a layout of the game
            
        """
        self._layout = layout
        # -4 inactive
        # -1 bomb in a cell
        # -2 marked bomb
        # -3 ?
        # 0-9 bombs nearby
        self._board = [[-4 for i in range(0, Board.getM(self))] for i in range(0, Board.getN(self))]
    
    def _changeCell(self, yPos, xPos):
        """
        Changes the value of _board into the corresponding value from the layout _map
        
        Attributes:
            yPos(int): y dimension number (n)
            xPos(int): x dimension number (m)
        """
        y = self._layout._boundaries(yPos, Board.getN(self))
        x = self._layout._boundaries(xPos, Board.getM(self))
        self._board[y][x] = self._layout.getMap()[y][x]
        
    def _scan(self, m1, m2, n, stack, changeTable):
        """
        Scans the map for cells without any surrounding bombs. Adds them to the stack
        
        Parameters:
            m1(int): lefthand value on which the searching starts
            m2(int): righthand value on which the searching ends
            n(int): y dimension value on which the searching occurs
            stack([int[][]]): stack containing the x, y values of points where scanning should start
            changeTable([int[][]]): list containing x, y dimension numbers of cells to uncover
        """
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
        """
        Uncovering algorithm. Used scanline flood algorithm.
        Finds every cell without surrounding bombs and uncovers them
        
        Parameters:
            n(int): y dimension index of the cell where algorithm should start
            m(int): x dimension index of the cell where algorithm should start
        """
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
        """
        Handles left click. Uncovers n, m cell if necessary
        
        Parameters:
            n(int): y dimension index of the cell which was clicked
            m(int): x dimension index of the cell which was clicked
        """
        if(self._board[n][m] != -4):
            return
        self._board[n][m] = self._layout.getMap()[n][m]
        if(self._board[n][m] == 0):
            self._board[n][m] = -4
            Board.showSurrounding(self, n, m)
    
    def rClick(self, n, m):
        """
        Handles right click. Adds the flag, ? or returns the n, m cell to the covered state
        
        Parameters:
            n(int): y dimension index of the cell which was clicked
            m(int): x dimension index of the cell which was clicked
        """
        if(self._board[n][m] > -2):
            return
        if(self._board[n][m] == -4):
            self._board[n][m] = -2
        elif(self._board[n][m] == -2):
            self._board[n][m] = self._board[n][m] - 1
        elif(self._board[n][m] == -3):
            self._board[n][m] = self._board[n][m] - 1
            
    def print(self, board):
        """
        Prints board to the console
        Useful for debugging purposes
        """
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
        """
        Checks if flags are placed exactly on the bombs.
        Player doesn't have to uncover every cell in order to win
        
        Returns:
            True or False
        """
        correctFlags = 0
        for n in range(0, Board.getN(self)):
            for m in range(0, Board.getM(self)):
                if(self._board[n][m] == -2 and self._layout.getMap()[n][m] == -1):
                    correctFlags += 1
        return correctFlags == self._layout.getBombs()
    
    def checkWinCells(self):
        """
        Checks if all of the cells not containing bombs were uncovered.
        
        Returns:
            True or False
        """
        cellAmount = 0
        for n in range(0, Board.getN(self)):
            for m in range(0, Board.getM(self)):
                if(self._board[n][m] == -4 or self._board[n][m] == -2 or self._board[n][m] == -3):
                    cellAmount += 1
        return cellAmount == self._layout.getBombs()
    
    
    # getters
    
    def getN(self):
        """
        Returns:
            (int): the maximum y dimension number n
        """
        return self._layout._n
    
    def getM(self):
        """
        Returns:
            (int): the maximum x dimension number m
        """
        return self._layout._m
    
    def getLayout(self):
        """
        Returns:
            (Layout): the Layout class used by this Board
        """
        return self._layout
    
    def getBoard(self):
        """
        Returns:
            (int[][]): the _board attribute. This is the map that's shown to the player

        Meaning of the values:
            -4: inactive
            -1: bomb in a cell
            -2: marked bomb
            -3: ?
            0-9: bombs nearby
        """
        return self._board