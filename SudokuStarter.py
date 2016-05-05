#  Nathan Shelly (njs199) and Alexander (Sasha) Weiss (awq325)
# All group members were present and contributing during all work on this project

import struct, string, math, random, copy

class SudokuBoard:
    """This will be the sudoku board game object your player will manipulate."""

    def __init__(self, size, board):
        """Constructor for the SudokuBoard"""
        self.BoardSize = size #the size of the board
        self.CurrentGameBoard = board #the current state of the game board
        self.boardDomains = [[range(1, self.BoardSize+1) for x in range(0, size)] for x in range(0, size)]

        # Set all the board's domains at first
        # print "creating new board!"
        for i in range(0, size):
          for j in range(0, size):
              if board[i][j] != 0:
                #   print 'updating domain'
                  self.updateDomains(i, j)
        # print "domains after update", self.boardDomains

    def set_value(self, row, col, value):
        """This function will create a new sudoku board object with the input
        value placed on the GameBoard row and col are both zero-indexed"""

        # add the value to the appropriate position on the board
        self.CurrentGameBoard[row][col]=value
        #return a new board of the same size with the value added
        return SudokuBoard(self.BoardSize, self.CurrentGameBoard)

    def print_board(self):
        """Prints the current game board. Leaves unassigned spots blank."""
        div = int(math.sqrt(self.BoardSize))
        dash = ""
        space = ""
        line = "+"
        sep = "|"
        for i in range(div):
            dash += "----"
            space += "    "
        for i in range(div):
            line += dash + "+"
            sep += space + "|"
        for i in range(-1, self.BoardSize):
            if i != -1:
                print "|",
                for j in range(self.BoardSize):
                    if self.CurrentGameBoard[i][j] > 9:
                        print self.CurrentGameBoard[i][j],
                    elif self.CurrentGameBoard[i][j] > 0:
                        print "", self.CurrentGameBoard[i][j],
                    else:
                        print "  ",
                    if (j+1 != self.BoardSize):
                        if ((j+1)//div != j/div):
                            print "|",
                        else:
                            print "",
                    else:
                        print "|"
            if ((i+1)//div != i/div):
                print line
            else:
                print sep

    def getRowDomain(self, row, col):
        """Returns row domain of given spot on board (list of values 1-9)"""
        domain = range(1, self.BoardSize+1)
        for i in [x for x in range(0, self.BoardSize) if x != col]:
            if self.CurrentGameBoard[row][i] == 0:
                continue
            domain.remove(self.CurrentGameBoard[row][i])
        return domain

    def getColDomain(self, row, col):
        """Returns col domain of given spot on board (list of values 1-9)"""
        domain = range(1, self.BoardSize+1)
        for i in [x for x in range(0, self.BoardSize) if x != row]:
            if self.CurrentGameBoard[i][col] == 0:
                continue
            domain.remove(self.CurrentGameBoard[i][col])
        return domain

    def getSubSquareDomain(self, row, col):
        """Returns subsquare domain of given spot on board (list of values 1-9)"""
        num_sss = int(math.sqrt(self.BoardSize)) # num_SubSquareS - lolol
        ss_row_start = row/num_sss * num_sss
        ss_col_start = (col/num_sss) * num_sss

        domain = range(1, self.BoardSize+1)
        for j in range(ss_col_start, ss_col_start+num_sss):
            for i in range(ss_row_start, ss_row_start+num_sss):
                if self.CurrentGameBoard[i][j] == 0 or (i, j) == (row, col):
                    continue
                domain.remove(self.CurrentGameBoard[i][j])
        return domain

    def get_domain(self, row, col):
        """Gets true domain for given spot from row, column and subsquare domains"""

        row_domain = self.getRowDomain(row, col)
        col_domain = self.getColDomain(row, col)
        ss_domain = self.getSubSquareDomain(row, col)

        return list(set(row_domain) & set(col_domain) & set(ss_domain))

    def get_domain_smart(self, row, col):
        return self.boardDomains[row][col]

    def generateBoardDomains(self):
        """Generates correct domains for every spot in board"""
        for i in range(0, self.BoardSize):
            for j in range(0, self.BoardSize):
                if self.CurrentGameBoard[i][j] != 0:
                    continue
                self.boardDomains[i][j] = self.get_domain(i, j)

    def openSpots(self):
        """Finds all locations on board with value 0"""
        openSpots = []
        for i in range(0, self.BoardSize):
            for j in range(0, self.BoardSize):
                if not self.CurrentGameBoard[i][j]:
                    openSpots.append((i, j))
        return openSpots

    def updateDomains(self, row, col):
        """Update domains given spot"""
        value = self.CurrentGameBoard[row][col]
        self.boardDomains[row][col] = [None] # set the current spot domain to [None]

        # print "value", value
        # print "placed spot", row, col

        # clear the row
        for i in range(0, self.BoardSize):
            if self.boardDomains[row][i] != [None]:
                try:
                    self.boardDomains[row][i].remove(value)
                    # print "spot", row, i
                    # print "rowdomain", self.boardDomains[row][i]
                except:
                    pass
        # clear the column
        for i in range(0, self.BoardSize):
            if self.boardDomains[i][col] != [None]:
                try:
                    self.boardDomains[i][col].remove(value)
                    # print "spot", i, col
                    # print "coldomain", self.boardDomains[i][col]
                except:
                    pass
        # clear the subsquare
        num_sss = int(math.sqrt(self.BoardSize))
        ss_row_start = row/num_sss * num_sss
        ss_col_start = (col/num_sss) * num_sss
        for j in range(ss_col_start, ss_col_start+num_sss):
            for i in range(ss_row_start, ss_row_start+num_sss):
                if self.CurrentGameBoard[i][j] != [None]:
                    try:
                        self.boardDomains[i][j].remove(value)
                    except:
                        pass

    def empty_domains(self):
        for i in range(0, self.BoardSize):
            for j in range(0, self.BoardSize):
                if not self.boardDomains[i][j]:
                    return True
        return False

def parse_file(filename):
    """Parses a sudoku text file into a BoardSize, and a 2d array which holds
    the value of each cell. Array elements holding a 0 are considered to be
    empty."""

    f = open(filename, 'r')
    BoardSize = int( f.readline())
    NumVals = int(f.readline())

    #initialize a blank board
    board = [ [ 0 for i in range(BoardSize) ] for j in range(BoardSize) ]

    #populate the board with initial values
    for i in range(NumVals):
        line = f.readline()
        chars = line.split()
        row = int(chars[0])
        col = int(chars[1])
        val = int(chars[2])
        board[row-1][col-1]=val

    return board

def is_complete(sudoku_board):
    """Takes in a sudoku board and tests to see if it has been filled in
    correctly."""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))

    #check each cell on the board for a 0, or if the value of the cell
    #is present elsewhere within the same row, column, or square
    for row in range(size):
        for col in range(size):
            if BoardArray[row][col]==0:
                return False
            for i in range(size):
                if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
                    return False
                if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
                    return False
            #determine which square the cell is in
            SquareRow = row // subsquare
            SquareCol = col // subsquare
            for i in range(subsquare):
                for j in range(subsquare):
                    if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]
                            == BoardArray[row][col])
                        and (SquareRow*subsquare + i != row)
                        and (SquareCol*subsquare + j != col)):
                            return False
    return True

def init_board(file_name):
    """Creates a SudokuBoard object initialized with values from a text file"""
    board = parse_file(file_name)
    return SudokuBoard(len(board), board)

def solve(initial_board, forward_checking = False, MRV = False, Degree = False,
    LCV = False):
    """Takes an initial SudokuBoard and solves it using back tracking, and zero
    or more of the heuristics and constraint propagation methods (determined by
    arguments). Returns the resulting board solution. """
    return backtrackingSearch(initial_board, forward_checking)

def backtrackingSearch(pBoard, forward_checking = False):
    if is_complete(pBoard):
        return pBoard

    # if any cells have no possible spots, short circuit. Could put this check in updateDomains, but the flag would be ugly to pass.
    if forward_checking:
        if pBoard.empty_domains():
            # print "short-circuit!"
            return False

    spotToPlay = random.choice(pBoard.openSpots())
    # domain = pBoard.get_domain(spotToPlay[0], spotToPlay[1])
    domain = pBoard.get_domain_smart(spotToPlay[0], spotToPlay[1])

    for value in domain:
        tempBoard = copy.deepcopy(pBoard)
        tempBoard = tempBoard.set_value(spotToPlay[0], spotToPlay[1], value) # set a value for that spot
        # tempBoard.updateDomains(spotToPlay[0], spotToPlay[1])
        result = backtrackingSearch(tempBoard, forward_checking)
        if result:
            return result

    # domain is empty or no values worked
    return False
