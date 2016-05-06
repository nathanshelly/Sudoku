from SudokuStarter import *
import time, os

tempBoard = init_board('input_puzzles/easy/16_16.sudoku')

winBoard = solve(tempBoard, forward_checking = True, MRV = False)

if winBoard:
    winBoard.print_board()
    print is_complete(winBoard)
