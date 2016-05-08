from SudokuStarter import *
import time, os

tempBoard = init_board('input_puzzles/more/25x25/25x25.1.sudoku')
tempBoard.print_board()

startTime = time.clock()
winBoard = solve(tempBoard, forward_checking = True, MRV = True, Degree = True, LCV = True)
endTime = time.clock()

if winBoard:
    print endTime-startTime
    winBoard.print_board()
    print is_complete(winBoard)
else:
    print "fuck"
