from SudokuStarter import *
import time, os

# tempBoard = init_board('input_puzzles/easy/4_4.sudoku')
tempBoard = init_board('input_puzzles/more/9x9/9x9.12.sudoku')
tempBoard.print_board()

startTime = time.clock()
winBoard, _ = solve(tempBoard, forward_checking = True, MRV = False, Degree = False, LCV = False)
endTime = time.clock()

if winBoard:
    print endTime-startTime
    winBoard.print_board()
    print is_complete(winBoard)
else:
    print "fuck"
