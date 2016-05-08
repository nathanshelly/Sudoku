from sudoku import *
import os

max_consistency_checks = 500000
resultsFile = open("results.txt", "w")
path = 'input_puzzles/more/'
typePuzzle = ['9x9', '16x16', '25x25']
backtrackingArgs =      {'forward_checking': False, 'MRV': False, 'Degree': False, 'LCV': False}
forwardCheckingArgs =   {'forward_checking': True,  'MRV': False, 'Degree': False, 'LCV': False}
MRVArgs =               {'forward_checking': True,  'MRV': True,  'Degree': False, 'LCV': False}
DegreeArgs =            {'forward_checking': True,  'MRV': False, 'Degree': True,  'LCV': False}
LCVArgs =               {'forward_checking': True,  'MRV': False, 'Degree': False, 'LCV': True}
listArgs = [backtrackingArgs, forwardCheckingArgs, MRVArgs, DegreeArgs, LCVArgs]

for pathPuzzle in typePuzzle:
    print 'Running ' + str(pathPuzzle) + ' puzzles'
    resultsFile.write('Running ' + str(pathPuzzle) + ' puzzles ' + '\n\n')
    for arguments in listArgs:
        print 'Arguments: ' + str(arguments)
        resultsFile.write('Running with arguments: ' + str(arguments) + '\n')
        numSuccesses = 0
        totalConsistencyChecks = 0
        for file in os.listdir(path+pathPuzzle):
            print 'File: ' + str(file)
            tempBoard = init_board(path + pathPuzzle + '/' + file)
            vals = arguments.values()

            # Use for solving without tracking consistency checks

            winBoard = solve(tempBoard, vals[0], vals[1], vals[2], vals[3])
            numConsistencyChecks = 0

            # Use for solving with tracking consistency checks

            # winBoard, numConsistencyChecks = solve(tempBoard, vals[0], vals[1], vals[2], vals[3])
            # print 'Number of consistency_checks = ' + str(numConsistencyChecks)

            if winBoard:
                totalConsistencyChecks += numConsistencyChecks
                numSuccesses += 1
            else:
                if numConsistencyChecks > max_consistency_checks:
                    print 'File ' + str(file) + ' timed out '

        print str(numSuccesses) + " boards succeeded, average number of consistency checks was: " + str(round(totalConsistencyChecks/numSuccesses, 5))
        resultsFile.write(str(numSuccesses) + " boards succeeded, average number of consistency checks was: " + str(round(totalConsistencyChecks/numSuccesses, 5)) + '\n\n')

resultsFile.close()
