from SudokuStarter import *


tempBoard = init_board('input_puzzles/easy/16_16.sudoku')
file = open("results.txt", "w")

tempBoard.print_board()
tempBoard.generateBoardDomains()

winBoard = solve(tempBoard)
winBoard.print_board()

print is_complete(winBoard)

file.write(str(is_complete(winBoard)))
file.close()
