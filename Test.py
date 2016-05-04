from SudokuStarter import *

tempBoard = init_board('input_puzzles/easy/9_9.sudoku')

tempBoard.print_board()

print(tempBoard.getSubSquareDomain(2, 0))
print(tempBoard.getRowDomain(2, 0))
print(tempBoard.getColDomain(2,0))
