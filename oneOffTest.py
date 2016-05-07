from SudokuStarter import *
import time, os

tempBoard = init_board('input_puzzles/easy/9_9.sudoku')
tempBoard.print_board()

startTime = time.clock()
winBoard = solve(tempBoard, forward_checking = True, MRV = False, Degree = True, LCV = False)
endTime = time.clock()

if winBoard:
    print endTime-startTime
    winBoard.print_board()
    print is_complete(winBoard)
else:
    print "fuck"
