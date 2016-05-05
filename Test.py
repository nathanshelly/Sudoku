from SudokuStarter import *

tempBoard = init_board('input_puzzles/easy/4_4.sudoku')

tempBoard.print_board()
tempBoard.set_value(0, 0, 1)
tempBoard.set_value(0, 1, 2)
tempBoard.set_value(0, 3, 4)
tempBoard.set_value(1, 3, 3)
tempBoard.generateBoardDomains()

print tempBoard.boardDomains
print empty_domains(tempBoard)
