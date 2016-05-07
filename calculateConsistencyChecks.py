from SudokuStarter import *
import os

path = 'input_puzzles/more/9x9'
path = 'input_puzzles/easy'

totalConsistencyChecks = 0
numSuccesses = 0

for i in range(0, 10):
# for file in os.listdir(path):
    # tempBoard = init_board(path + '/' + file)
    tempBoard = init_board(path + '/' + '4_4.sudoku')
    winBoard, numConsistencyChecks = solve(tempBoard, forward_checking = True, MRV = True, Degree = False, LCV = True)
    print numConsistencyChecks

    if winBoard:
        totalConsistencyChecks += numConsistencyChecks
        numSuccesses += 1
        # print is_complete(winBoard)

print str(numSuccesses) + " boards, average number of consistency checks was: " + str(round(totalConsistencyChecks/numSuccesses, 5))
