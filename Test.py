from SudokuStarter import *

tempBoard = init_board('input_puzzles/easy/4_4.sudoku')

tempBoard.print_board()

print(tempBoard.getRowDomain(2, 1))
