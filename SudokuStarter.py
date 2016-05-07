#  Nathan Shelly (njs199) and Alexander (Sasha) Weiss (awq325)
# All group members were present and contributing during all work on this project

import struct, string, math, random, copy

consistency_checks = 0
max_consistency_checks = 500000
print_timeout = True

class SudokuBoard:
    """This will be the sudoku board game object your player will manipulate."""

    def __init__(self, size, board, domains = []):
        """Constructor for the SudokuBoard"""
        self.BoardSize = size # the size of the board
        self.CurrentGameBoard = board # the current state of the game board
        if not domains:
            # print "first initialization"
            self.boardDomains = [[range(1, self.BoardSize+1) for x in range(size)] for x in range(size)]
            # Set all the board's domains at first
            for i in range(size):
              for j in range(size):
                  if board[i][j] != 0:
                      self.updateDomains(i, j)
            # self.print_board()
        else:
            self.boardDomains = domains

    def set_value(self, row, col, value):
        """This function will create a new sudoku board object with the input
        value placed on the GameBoard row and col are both zero-indexed"""

        self.CurrentGameBoard[row][col]=value
        self.updateDomains(row, col)
        #return a new board of the same size with the value added
        return SudokuBoard(self.BoardSize, self.CurrentGameBoard, domains = self.boardDomains)

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

    def get_domain_smart(self, row, col):
        return self.boardDomains[row][col]

    def generateBoardDomains(self):
        """Generates correct domains for every spot in board"""
        for i in range(self.BoardSize):
            for j in range(self.BoardSize):
                if self.CurrentGameBoard[i][j] != 0:
                    continue
                self.boardDomains[i][j] = self.get_domain(i, j)

    def openSpots(self):
        """Finds all locations on board with value 0"""
        openSpots = []
        for i in range(self.BoardSize):
            for j in range(self.BoardSize):
                if not self.CurrentGameBoard[i][j]:
                    openSpots.append((i, j))
        return openSpots

    def iterate_unassigned_domains(self, row, col, function, *args):

        for i in range(self.BoardSize):
            if self.boardDomains[row][i] != [None]:
                function(row, i, *args)

        # clear the column
        for i in range(self.BoardSize):
            if self.boardDomains[i][col] != [None]:
                function(i, col, *args)

        # clear the subsquare
        num_sss = int(math.sqrt(self.BoardSize))
        ss_row_start = row/num_sss * num_sss
        ss_col_start = (col/num_sss) * num_sss
        for j in [x for x in range(ss_col_start, ss_col_start+num_sss) if x != row]:
            for i in [x for x in range(ss_row_start, ss_row_start+num_sss) if x != col]:
                if self.CurrentGameBoard[i][j] != [None]:
                    function(i, j, *args)

    def remove_val(self, r, c, value):
        try:
            self.boardDomains[r][c].remove(value)
        except ValueError:
            pass

    def updateDomains(self, row, col):
        self.boardDomains[row][col] = [None]
        value = self.CurrentGameBoard[row][col]

        self.iterate_unassigned_domains(row, col, self.remove_val, value)

    def getDegreeSpot(self):

        inOut = [0]
        temp = -1
        spot = (-1, -1)

        for row in range(self.BoardSize):
            for col in range(self.BoardSize):
                if self.get_domain_smart(row, col) == [None]:
                    continue
                self.iterate_unassigned_domains(row, col, self.incrementUnassigned, inOut)
                if inOut[0] > temp:
                    temp = inOut[0]
                    spot = (row, col)
                inOut[0] = 0

        return spot

    def incrementUnassigned(self, row, col, inOut):
        if self.boardDomains[row][col] != [None]:
            inOut[0] += 1

    def empty_domains(self):
        for i in range(self.BoardSize):
            for j in range(self.BoardSize):
                if not self.boardDomains[i][j]:
                    return True
        return False

    def min_domain(self):
        """Find the cell with the smallest domain"""
        dom_size = self.BoardSize + 1
        spot = (-1, -1)
        for i in range(self.BoardSize):
            for j in range(self.BoardSize):
                if self.boardDomains[i][j] == [None]:
                    continue
                if len(self.boardDomains[i][j]) < dom_size:
                    dom_size = len(self.boardDomains[i][j])
                    spot = (i, j)
        return spot

    def all_placed(self):
        # is the board full
        for row in range(self.BoardSize):
            for col in range(self.BoardSize):
                if self.CurrentGameBoard[row][col] == 0:
                    return False
        return True

    def in_domain(self, r, c, value, counter):
        if value in self.get_domain_smart(r, c):
            counter[0] += 1

    def constrained_by_domain(self, row, col):
        """The number of variables a given move impacts"""
        domain = self.get_domain_smart(row, col)
        constrains = [-1]*len(domain)

        for i in range(len(domain)):
            counter = [0]
            self.iterate_unassigned_domains(row, col, self.in_domain, domain[i], counter)
            constrains[i] = counter[0]

        return constrains

    def check_consistency(self, row, col, value):
        if value not in self.boardDomains[row][col]:
            return False
        return True

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

    if not sudoku_board.all_placed():
        return False

    #check each cell on the board for a 0, or if the value of the cell
    #is present elsewhere within the same row, column, or square
    for row in range(size):
        for col in range(size):
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
    global print_timeout
    print_timeout = True

    return backtrackingSearch(initial_board, forward_checking, MRV, Degree, LCV)

def backtrackingSearch(pBoard, forward_checking, MRV, Degree, LCV):
    global consistency_checks
    global max_consistency_checks
    global print_timeout

    if is_complete(pBoard):
        return pBoard
    if pBoard.empty_domains():
        return False

    if MRV:
        spotToPlay = pBoard.min_domain()
    elif Degree:
        spotToPlay = pBoard.getDegreeSpot()
    else:
        spotToPlay = random.choice(pBoard.openSpots())

    if forward_checking:
        domain = pBoard.get_domain_smart(spotToPlay[0], spotToPlay[1])
    else:
        domain = range(1, pBoard.BoardSize+1)

    if LCV:
        domainOrder = pBoard.constrained_by_domain(spotToPlay[0], spotToPlay[1])
        domain = [value for (constraint,  value) in sorted(zip(domainOrder, domain))]

    for value in domain:
        if consistency_checks > max_consistency_checks:
            if print_timeout:
                print "timed out"
                print_timeout = False
            return False
        consistency_checks += 1

        tempBoard = copy.deepcopy(pBoard)

        if not forward_checking:
            if not tempBoard.check_consistency(spotToPlay[0], spotToPlay[1], value):
                continue

        tempBoard = tempBoard.set_value(spotToPlay[0], spotToPlay[1], value) # set a value for that spot and update domains
        result = backtrackingSearch(tempBoard, forward_checking, MRV, Degree, LCV)
        if result:
            return result

    # domain is empty or no values worked
    return False
