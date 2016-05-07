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

acc = 0
for i in range(0, 10):
    tempBoard = init_board('input_puzzles/easy/9_9.sudoku')
    startTime = time.clock()
    winBoard = solve(tempBoard, forward_checking = False, MRV = False, Degree = False, LCV = True)
    endTime = time.clock()

    if winBoard:
        totalTime = endTime - startTime
        acc += totalTime
        print "Board " + str(i) + " took " + str(round(totalTime, 3)) + " seconds to complete"
        # winBoard.print_board()
        print is_complete(winBoard)
        resultsFile.write(str(is_complete(winBoard)))

resultsFile.close()
print "Ten boards, average time was: " + str(round(acc/10.0, 5))
