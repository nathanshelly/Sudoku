from SudokuStarter import *
import time, os

resultsFile = open("results.txt", "w")
path = 'input_puzzles/more/9x9'

# counter = 1
# numberOfFails = 0
#
# for file in os.listdir(path):
#         tempBoard = init_board(path + '/' + file)
#         print "Board #" + str(counter) + ": "
#         # tempBoard.print_board()
#
#         startTime = time.clock()
#         winBoard = solve(tempBoard, forward_checking = True, MRV = True)
#         endTime = time.clock()
#
#         if winBoard:
#             totalTime = endTime - startTime
#             print "Board #" + str(counter) + " took " + str(round(totalTime, 3)) + " seconds to complete"
#             # winBoard.print_board()
#             print is_complete(winBoard)
#             resultsFile.write(str(is_complete(winBoard)))
#         else:
#             numberOfFails += 1
#
#         counter += 1
#
# print "Number of fails:", numberOfFails


resultsFile = open("results.txt", "w")
reps = 100
totalConsistencyChecks = 0

for i in range(reps):
    tempBoard = init_board('input_puzzles/easy/4_4.sudoku')

    winBoard, numConsistencyChecks = solve(tempBoard, forward_checking = True, MRV = False, Degree = False, LCV = True)

    if winBoard:
        totalConsistencyChecks += numConsistencyChecks
        print "Board " + str(i) + " took " + str(numConsistencyChecks) + " checks to complete"

resultsFile.close()
print totalConsistencyChecks
print str(reps) + " boards, average checks was: " + str(round(totalConsistencyChecks/float(reps), 5))
