from SudokuStarter import *
import time

tempBoard = init_board('input_puzzles/easy/9_9.sudoku')
file = open("results.txt", "w")

tempBoard.print_board()
# tempBoard.generateBoardDomains()

winBoard = solve(tempBoard, forward_checking = True)
if winBoard:
    winBoard.print_board()
    print is_complete(winBoard)
    file.write(str(is_complete(winBoard)))

file.close()
