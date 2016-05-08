#  Nathan Shelly (njs199) and Alexander (Sasha) Weiss (awq325)
# All group members were present and contributing during all work on this project

import struct, string, math, random, copy
from collections import deque

# Global check for timing out
max_consistency_checks = 500000

class SudokuBoard:
    """This will be the sudoku board game object your player will manipulate."""

    def __init__(self, size, board):
        """Constructor for the SudokuBoard"""
        self.BoardSize = size # the size of the board
        self.CurrentGameBoard = board # the current state of the game board

        self.num_in_rows = self.placed_in_rows()
        self.num_in_cols = self.placed_in_cols()
        self.num_in_ss = self.placed_in_ss()
        self.open_spots = [(i, j) for i in range(size) for j in range(size) if board[i][j] == 0]
        self.boardDomains = [[range(1, self.BoardSize+1) for x in range(size)] for x in range(size)]
        [self.remove_from_domains(i, j) for i in range(size) for j in range(size) if board[i][j] != 0]

    def remove_from_domains(self, row, col):
        """Removes value at given position from that position's neighborhoods' domains"""
        self.boardDomains[row][col] = [None]
        value = self.CurrentGameBoard[row][col]

        self.iterate_unassigned_domains(row, col, self.remove_val, value)

    def set_domain(self, r, c):
        """Sets domain at a given position by iterating that position's neighborhood"""
        self.boardDomains[r][c] = self.get_domain_dumb(r, c)

    def remove_val(self, r, c, value):
        """Removes the given value from a spot's domain if possible"""
        try:
            self.boardDomains[r][c].remove(value)
        except ValueError:
            pass

    def empty_domains(self):
        """Returns true if there are any unassigned spots on the board with no domain"""
        for (row, col) in self.open_spots:
                if not self.boardDomains[row][col]:
                    return True
        return False

    def min_domain(self):
        """Find the cell with the smallest domain"""
        dom_size = self.BoardSize + 1
        spot = (-1, -1)
        for (row, col) in self.open_spots:
                if self.boardDomains[row][col] == [None]:
                    continue
                if len(self.boardDomains[row][col]) < dom_size:
                    dom_size = len(self.boardDomains[row][col])
                    spot = (row, col)

        return spot

    def all_placed(self):
        """Checks if board is full"""
        if not self.open_spots:
            return True
        else:
            return False

    def in_domain(self, r, c, value, counter):
        """Checks if passed in value is in passed in spot's domain"""
        if value in self.get_domain_smart(r, c):
            counter[0] += 1

    def constrained_by_domain(self, row, col):
        """The number of variables a given move impacts"""
        domain = self.get_domain_smart(row, col)
        constrains = [-1]*len(domain)

        for i in range(len(domain)):
            counter_add = [0]
            counter_subtr = [0]
            self.iterate_unassigned_domains(row, col, self.in_domain, domain[i], counter_add)
            constrains[i] = counter_add[0]

        return constrains

    def check_consistency(self, row, col, value):
        """Checks if given value is a possible move for the given spot"""
        if value not in self.boardDomains[row][col]:
            return False
        return True

    ##################### Degree #####################

    def placed_in_rows(self):
        """Calculates the number of placed variables in each row"""
        num_placed = [-1]*self.BoardSize
        for i in range(self.BoardSize): # go down the rows
            num = 0
            for j in range(self.BoardSize): # go across the rows
                if self.CurrentGameBoard[i][j] != 0:
                    num += 1
            num_placed[i] = num
        return num_placed

    def placed_in_cols(self):
        """Calculates the number of placed variables in each column"""
        num_placed = [-1]*self.BoardSize
        for i in range(self.BoardSize): # go across the cols
            num = 0
            for j in range(self.BoardSize): # go down a col
                if self.CurrentGameBoard[j][i] != 0:
                    num += 1
            num_placed[i] = num
        return num_placed

    def placed_in_ss(self):
        """Calculates the number of placed variables in each spots subsquare"""
        num_placed = []
        num_ss = int(math.sqrt(self.BoardSize))
        for k in range(self.BoardSize): # for each subsquare
            num = 0
            ss_row_num = k//num_ss
            for i in range(ss_row_num*num_ss, (ss_row_num+1)*num_ss):
                ss_col_num = k % num_ss
                for j in range(ss_col_num*num_ss, (ss_col_num+1)*num_ss):
                    if self.CurrentGameBoard[i][j] != 0:
                        num += 1
            num_placed.append(num)
        return num_placed

    def increment_placed(self, row, col):
        """Increment the number of placed variables in rows, columns, and ss's"""
        self.num_in_rows[row] += 1
        self.num_in_cols[col] += 1
        self.num_in_ss[self.compute_ss_num(row, col)] += 1

    def decrement_placed(self, row, col):
        """Increment the number of placed variables in rows, columns, and ss's"""
        self.num_in_rows[row] -= 1
        self.num_in_cols[col] -= 1
        self.num_in_ss[self.compute_ss_num(row, col)] -= 1

    def getDegreeSpot(self):
        """Returns spot with greatest number of unassigned variables in its neighborhood"""
        num = -1
        spot = (-1, -1)
        for i, j in self.open_spots:
                ss_num = self.compute_ss_num(i, j)
                temp_num = sum([self.num_in_rows[i], self.num_in_cols[j], self.num_in_ss[ss_num]])
                if temp_num > num:
                    num = temp_num
                    spot = (i, j)
        return spot

    ##################### Get domains #####################

    def get_domain_smart(self, row, col):
        """Returns domain at a given spot from boardDomains data member"""
        return self.boardDomains[row][col]

    def get_domain_dumb(self, row, col):
        """Gets domain by iterating through a spot's neighborhood"""
        rowDomain = set(self.get_row_domain(row, col))
        colDomain = set(self.get_col_domain(row, col))
        subsquareDomain = set(self.get_subsquare_domain(row, col))

        return list(set.intersection(rowDomain, colDomain, subsquareDomain))

    def get_row_domain(self, row, col):
        """Returns row domain for a given row value"""
        assignedValues = [self.CurrentGameBoard[row][x] for x in range(self.BoardSize) if self.CurrentGameBoard[row][x] != 0 and x != col]
        return [val for val in range(1, self.BoardSize + 1) if val not in assignedValues]

    def get_col_domain(self, row, col):
        """Returns col domain for a given col value"""
        assignedValues = [self.CurrentGameBoard[x][col] for x in range(self.BoardSize) if self.CurrentGameBoard[x][col] != 0 and x != row]
        return [val for val in range(1, self.BoardSize + 1) if val not in assignedValues]

    def get_subsquare_domain(self, row, col):
        """Returns domain of a given spot's subsquare"""
        num_ss = int(math.sqrt(self.BoardSize))
        rowSpot = (row // num_ss) * num_ss
        colSpot = (col // num_ss) * num_ss

        assignedValues = [self.CurrentGameBoard[x][y] for x in range(rowSpot, rowSpot+num_ss) for y in range(colSpot, colSpot+num_ss) if self.CurrentGameBoard[x][y] != 0 and (x, y) != (row, col)]
        return [val for val in range(1, self.BoardSize + 1) if val not in assignedValues]

    ##################### Utilities #####################

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

    def compute_ss_num(self, row, col):
        """Calculates the subsquare number of a given spot"""
        num_ss = int(math.sqrt(self.BoardSize))
        return (col//num_ss) + (row//num_ss) * num_ss

    def iterate_unassigned_domains(self, row, col, function, *args):
        """Runs through unassigned domains in given spot's neighborhood"""
        spot_ss_num = self.compute_ss_num(row, col)
        [function(i, j, *args) for (i, j) in self.open_spots if (i, j) != (row, col) and (i == row or j == col or spot_ss_num == self.compute_ss_num(i, j))]

    def set_value(self, row, col, value):
        """Makes move, updating requisite data members"""
        self.CurrentGameBoard[row][col]=value
        self.open_spots.remove((row, col))
        self.remove_from_domains(row, col)
        self.increment_placed(row, col)

    def unset_value(self, row, col):
        """Undo move at given row, col"""
        self.CurrentGameBoard[row][col] = 0
        self.boardDomains[row][col] = self.get_domain_dumb(row, col)
        self.open_spots.append((row, col))
        self.set_domains_back(row, col)
        self.decrement_placed(row, col)

    def set_domains_back(self, row, col):
        """Iterates unassigned domains to reset their domains"""
        self.iterate_unassigned_domains(row, col, self.set_domain)

    def getSpotToPlay(self, MRV, Degree):
        """Finds our spot to play next"""
        if MRV:
            spotToPlay = self.min_domain()
        elif Degree:
            spotToPlay = self.getDegreeSpot()
        else:
            spotToPlay = random.choice(self.open_spots)

        return spotToPlay

    def getSpotToPlayDomain(self, spotToPlay, forward_checking, LCV):
        """Get's domain of our spot in correct order"""
        if forward_checking:
            domain = self.get_domain_smart(spotToPlay[0], spotToPlay[1])
        else:
            domain = range(1, self.BoardSize+1)

        if LCV:
            domainOrder = self.constrained_by_domain(spotToPlay[0], spotToPlay[1])
            domain = [value for (constraint,  value) in sorted(zip(domainOrder, domain))]

        return domain

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

def solve(initial_board, LCV = False, MRV = False, Degree = False, forward_checking = False):
    """Takes an initial SudokuBoard and solves it using back tracking, and zero
    or more of the heuristics and constraint propagation methods (determined by
    arguments). Returns the resulting board solution. """
    move_queue = deque()

    consistency_checks = [0]
    print 'Before run:', consistency_checks[0]
    board = backtrackingSearch(initial_board, forward_checking, MRV, Degree, LCV, move_queue, consistency_checks)
    print 'After run:', consistency_checks[0]

    return (board, consistency_checks[0])

def backtrackingSearch(pBoard, forward_checking, MRV, Degree, LCV, move_queue, numConsistencyChecks):
    global max_consistency_checks
    if is_complete(pBoard):
        return pBoard
    if pBoard.empty_domains():
        return False

    # Determine the spot to make our next move, and get that spot's domain in the correct order
    spotToPlay = pBoard.getSpotToPlay(MRV, Degree)
    domain = pBoard.getSpotToPlayDomain(spotToPlay, forward_checking, LCV)

    for value in domain:
        if numConsistencyChecks[0] > max_consistency_checks:
            return False
        numConsistencyChecks[0] += 1

        if not forward_checking:
            if not pBoard.check_consistency(spotToPlay[0], spotToPlay[1], value):
                continue

        # append move to our queue of all moves
        move_queue.append((spotToPlay[0], spotToPlay[1]))
        # set a value for that spot and update domains
        pBoard.set_value(spotToPlay[0], spotToPlay[1], value)
        resultingBoard = backtrackingSearch(pBoard, forward_checking, MRV, Degree, LCV, move_queue, numConsistencyChecks)

        if resultingBoard:
            return resultingBoard
        else:
            pBoard.unset_value(*move_queue.pop())

    return False
