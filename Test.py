from SudokuStarter import *

tempBoard = init_board('input_puzzles/easy/16_16.sudoku')

tempBoard.print_board()

winBoard = solve(tempBoard)
winBoard.print_board()

print is_complete(winBoard)
