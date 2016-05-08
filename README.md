# Sudoku

Nathan Shelly and Sasha Weiss, for Northwestern University EECS 348 - Intro to AI

Implements the backtracking algorithm, with optional heuristics (described below), to solve sudoku puzzles of any size. As a performance measure, tracks the number of consistency checks made by the algorithm in solving a board.

In sudoku.py, the functions parse_file (input file parsing), is_complete (checking if a board is a solution), and init_board (initializes a puzzle) were provided. All other code is original.

input_puzzles contains a series of 4x4, 9x9, 16x16, and 25x25 puzzles of varying difficulties. The format of each is the board size and number of initial placed spots, followed by each spot as (row col value).

calculateConsistencyChecks.py is a driver which runs each board (excluding boards in the "easy" folder) and reports the number of consistency checks needed to solve, with each set of heuristics. Timeout is set at 500,000 checks.
