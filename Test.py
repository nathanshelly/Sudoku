from SudokuStarter import *

tempBoard = init_board('input_puzzles/easy/4_4.sudoku')

tempBoard.print_board()

winBoard = solve(tempBoard)
winBoard.print_board()

# print openSpots(tempBoard)
# print(tempBoard.getSubSquareDomain(2, 0))
# print(tempBoard.getRowDomain(2, 0))
# print(tempBoard.getColDomain(2,0))
