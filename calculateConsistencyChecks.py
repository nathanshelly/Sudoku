from SudokuStarter import *
import os


path = 'input_puzzles/more/'
# path = 'input_puzzles/easy'
totalConsistencyChecks = 0
numSuccesses = 0
typePuzzle = ['9x9', '16x16', '25x25']
backtrackingArgs =      {'forward_checking': False, 'MRV': False, 'Degree': False, 'LCV': False}
forwardCheckingArgs =   {'forward_checking': True,  'MRV': False, 'Degree': False, 'LCV': False}
MRVArgs =               {'forward_checking': True,  'MRV': True,  'Degree': False, 'LCV': False}
DegreeArgs =            {'forward_checking': True,  'MRV': False, 'Degree': True,  'LCV': False}
LCVArgs =               {'forward_checking': True,  'MRV': False, 'Degree': False, 'LCV': True}
listArgs = [backtrackingArgs, forwardCheckingArgs, MRVArgs, DegreeArgs, LCVArgs]

for pathPuzzle in typePuzzle:
    print pathPuzzle
    for arguments in listArgs:
        print arguments
        # for i in range(0, 25):
        for file in os.listdir(path+pathPuzzle):
            print file
            tempBoard = init_board(path + pathPuzzle + '/' + file)
            # tempBoard = init_board(path + '/' + '4_4.sudoku')
            winBoard, numConsistencyChecks = solve(tempBoard, forward_checking = True, MRV = False, Degree = False, LCV = True)
            print numConsistencyChecks

            if winBoard:
                totalConsistencyChecks += numConsistencyChecks
                numSuccesses += 1
                # print is_complete(winBoard)
        print str(numSuccesses) + " boards, average number of consistency checks was: " + str(round(totalConsistencyChecks/numSuccesses, 5))
