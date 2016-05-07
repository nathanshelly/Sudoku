from SudokuStarter import *
import time, os

tempBoard = init_board('input_puzzles/easy/4_4.sudoku')

startTime = time.clock()
winBoard = solve(tempBoard, forward_checking = False, MRV = False, Degree = False)
endTime = time.clock()

if winBoard:
    print endTime-startTime
    winBoard.print_board()
    print is_complete(winBoard)
else:
    print "fuck"
    tempBoard.print_board()
