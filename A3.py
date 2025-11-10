# Program Description:
# This program is a simplified version of the classic Minesweeper game.
# It allows the user to play by revealing or flagging cells on a board, which
# contains randomly placed mines. The program also includes a bot that can
# automatically solve certain solvable boards using logical rules.

# Write your program here:
import random

# Constant variables
HIDDEN_SYMBOL = '?'
FLAG_SYMBOL = '\u2691'
EASY_PERCENT = 0.10
MEDIUM_PERCENT = 0.30
HARD_PERCENT = 0.50

def init_board(nb_rows: int, nb_cols: int, value):
    '''
    Create a 2D board with the given number of rows and columns,
    where every cell contains the specified value.

    Parameters:
        nb_rows (int): Number of rows in the board.
        nb_cols (int): Number of columns in the board.
        value (any): Value to fill each cell with.

    Returns:
        list[list]: A 2D list representing the initialized board.

    Examples:
        >>> init_board(3, 3, 0)
        [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        >>> init_board(2, 4, '?')
        [['?', '?', '?', '?'], ['?', '?', '?', '?']]
        >>> init_board(1, 3, 5)
        [[5, 5, 5]]
    '''
    board = []
    for i in range(nb_rows):
        row = []
        for j in range(nb_cols):
            row.append(value)
        board.append(row)
    return board
    
def count_total(board: list, value):
    '''
    Count how many times a given value appears in the board.

    Parameters:
        board (2D list): The 2D board to check.
        value (any): The value to count.

    Returns:
        int: The number of times the value appears in the board.

    Examples:
        >>> count_total([[1, 1], [1, 1]], 1)
        4
        >>> count_total([['?', '?'], ['?', '1']], '?')
        3
        >>> count_total([[0, 0, 0]], 1)
        0
    '''
    counter = 0
    for row in board:
        for num in row:
            if num == value:
                counter += 1
    
    return counter
        
def is_valid_position(board: list, row: int, col: int):
    '''
    Check if a position is within the bounds of the board.

    Parameters:
        board (2D list): The board to check.
        row (int): Row index.
        col (int): Column index.

    Returns:
        bool: True if the position is valid, False otherwise.

    Examples:
        >>> board = int_board([[1, 2], [3, 4], [5, 6], [7, 8]])
        >>> is_valid_position(board, 1, 1)
        True
        >>> is_valid_position(board, 1, 0)
        True
        >>> is_valid_position(board, -1, 0)
        False
    '''
    if row < 0 or col < 0:
        return False
    else: 
        return row < len(board) and col < len(board[0])

def get_neighbour_positions(board: list, row: int, col: int):
    '''
    Get a list of valid neighbouring positions around a cell.

    Parameters:
        board (2D list): The board.
        row (int): Row index of the cell.
        col (int): Column index of the cell.

    Returns:
        list[list[int]]: List of neighbouring positions as [row, col].

    Examples:
        >>> get_neighbour_positions([[1, 2], [3, 4]], 0, 0)
        [[0, 1], [1, 0], [1, 1]]
        >>> get_neighbour_positions([[1, 2, 3]], 0, 1)
        [[0, 0], [0, 2]]
        >>> get_neighbour_positions([[1, 2, 3], [4, 5, 6]], 0, 0)
        [[0, 1], [1, 0], [1,1]]
    '''
    neighbours = []
    for i in range(row - 1, row + 2):
        for j in range(col - 1, col +2):
            if is_valid_position(board, i, j) and not(i == row and j == col):
                neighbours.append([i, j]) 
    return neighbours

def count_neighbours(board: list, row: int, col: int, value):
    '''
    Count how many neighbours of a given cell have a specific value.

    Parameters:
        board (2D list): The board.
        row (int): Row index.
        col (int): Column index.
        value (any): The value to count among neighbours.

    Returns:
        int: The number of matching neighbours.

    Examples:
        >>> count_neighbours([['?', '⚑'], ['?', '?']], 0, 0, '?')
        2
        >>> count_neighbours([[1, 1], [1, 0]], 1, 1, 1)
        3
        >>> count_neighbours([['⚑', '?'], ['?', '?']], 0, 0, '?')
        3
    '''
    neighbours = get_neighbour_positions(board, row, col)
    counter = 0
    for pos in neighbours:
        r = pos[0]
        c = pos[1]
        if board[r][c] == value:
            counter += 1
    return counter

# 2: Helper board

def new_mine_position(board: list):
    '''
    Generate a random position on the board that doesn't contain a mine.

    Parameters:
        board (2D list): The helper board.

    Returns:
        tuple[int, int]: A tuple representing the (row, col) of the new mine.
    
    Examples:
        >>> random.seed(202)
        >>> new_mine_position([[0, 0], [0, 0]])
        (0, 0)
        >>> random.seed(202)
        >>> new_mine_position([[0, -1], [0, 0]])
        (1, 0)
        >>> random.seed(202)
        >>> new_mine_position([[0, 1, 1], [0, 1, -1], [0, 1, 1]])
        (1, 1)
    '''
    rows = len(board)
    cols = len(board[0])

    while True:
        int_1 = random.randint(0, rows - 1)
        int_2 = random.randint(0, cols - 1 )
        
        if board[int_1][int_2] != -1:
            return int_1, int_2

def new_mine(board: list):
    '''
    Add a mine to a random valid position and increment nearby cell counts.

    Parameters:
        board (2D list): The helper board.

    Returns:
        None
    
    Examples:
        >>> random.seed(202)
        >>> board = init_board(3, 3, 0)
        >>> new_mine(board)
        >>> board
        [[0, 1, 1], [0, 1, -1], [0, 1, 1]]

        >>> random.seed(202)
        >>> board = init_board(3, 3, 0)
        >>> new_mine(board)
        >>> new_mine(board)
        >>> board
        [[1, 2, 2], [1, -1, -1], [1, 2, 2]]

        >>> random.seed(202)
        >>> board = init_board(4, 4, 0)
        >>> new_mine(board)
        >>> new_mine(board)
        >>> new_mine(board)
        >>> board
        [[1, 1, 1, 0], [1, -1, 2, 1], [0, 1, -1, 1], [0, 1, 1, 1]]
    '''
    pos = new_mine_position(board)
    row = pos[0]
    col = pos[1]
    board[row][col] = -1

    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
            if 0 <= i < len(board) and 0 <= j < len(board[0]):
                if board[i][j] != -1:
                    board[i][j] += 1
    
def generate_helper_board(nb_rows :int, nb_cols: int, nb_mines: int):
    '''
    Create a helper board with mine positions and adjacent mine counts.

    Parameters:
        nb_rows (int): Number of rows.
        nb_cols (int): Number of columns.
        nb_mines (int): Number of mines.

    Returns:
        2D list of integers: A helper board containing 
        minevvalues (-1) and numbers.
    
    Examples:
        >>> random.seed(202)
        >>> generate_helper_board(3, 3, 2)
        [[0, 1, -1], [0, 1, 1], [-1, 1, 0]]

        >>> random.seed(202)
        >>> generate_helper_board(4, 4, 3)
        [[0, 1, 1, 1], [0, 1, -1, 1], [0, 1, 1, 1], [0, 0, 0, 0]]

        >>> random.seed(202)
        >>> generate_helper_board(2, 5, 2)
        [[0, 1, -1, 1, 0], [0, 1, 1, 1, 0]]
    '''
    board = init_board(nb_rows, nb_cols, 0)
    counter = 0
    while counter < nb_mines:
        new_mine(board)
        counter = 0
        for row in board:
            for i in row:
                if i == -1:
                    counter += 1
    return board

# 3: The Game Board

def flag(board: list, row: int, col: int):
    '''
    Toggle a flag on a given cell.

    Parameters:
        board (list[list[str]]): The game board.
        row (int): Row index.
        col (int): Column index.

    Returns:
        None
    
    Examples:
        >>> board = [['?', '?'], ['?', '?']]
        >>> flag(board, 0, 0)
        >>> board
        [['⚑', '?'], ['?', '?']]

        >>> board = [['?', '⚑'], ['?', '?']]
        >>> flag(board, 0, 1)
        >>> board
        [['?', '?'], ['?', '?']]

        >>> board = [['?', '?'], ['?', '?']]
        >>> flag(board, 1, 0)
        >>> board
        [['?', '?'], ['⚑', '?']]
    '''
    if board[row][col] == HIDDEN_SYMBOL:
        board[row][col] = FLAG_SYMBOL
    elif board[row][col] == FLAG_SYMBOL:
        board[row][col] = HIDDEN_SYMBOL


def reveal(helper_board: list, game_board: list, row: int, col: int):
    '''
    Reveal a cell based on the helper board.

    If the revealed cell contains a mine, an AssertionError is raised.

    Parameters:
        helper_board (2D list): Board with mine data.
        game_board (2D list): Player's visible board.
        row (int): Row index.
        col (int): Column index.

    Returns:
        None

    Examples:
        >>> helper_board = [[0, 1], [-1, 1]]
        >>> game_board = [['?', '?'], ['?', '?']]
        >>> reveal(helper_board, game_board, 0, 1)
        >>> game_board
        [['?', '1'], ['?', '?']]

        >>> helper_board = [[2, -1], [1, 1]]
        >>> game_board = [['?', '?'], ['?', '?']]
        >>> reveal(helper_board, game_board, 1, 0)
        >>> game_board
        [['?', '?'], ['1', '?']]

        >>> helper_board = [[0, -1], [1, 0]]
        >>> game_board = [['?', '?'], ['?', '?']]
        >>> reveal(helper_board, game_board, 0, 1)
        Traceback (most recent call last):
        AssertionError: BOOM! You lost.
    '''
    value = helper_board[row][col]
    if value == -1:
        raise AssertionError("BOOM! You lost.")
    else:
        game_board[row][col] = str(value)


def print_board(board: list):
    '''
    Print the board neatly row by row.

    Parameters:
        board (2d list): The board to print.

    Returns:
        None

    Examples:
        >>> board1 = [['?', '?'], ['?', '?']]
        >>> print_board(board1)
        ? ?
        ? ?

        >>> board2 = [['1', '⚑'], ['?', '2']]
        >>> print_board(board2)
        1 ⚑
        ? 2

        >>> board3 = [['0', '1', '⚑'], ['1', '2', '1'], ['⚑', '1', '0']]
        >>> print_board(board3)
        0 1 ⚑
        1 2 1
        ⚑ 1 0
    '''
    for row in board:
        print(" ".join(row))

# 4: Playing The Game

def count_unrevealed_non_mines(helper_board: list, game_board: list):
    '''
    Count the number of unrevealed cells that are not mines.

    Parameters:
        helper_board (2D list): Helper board with mine info.
        game_board (2D list): Visible board with player moves.

    Returns:
        int: Number of unrevealed non-mine cells remaining.
    
    Examples:
        >>> helper_board = [[0, -1], [1, 0]]
        >>> game_board = [['?', '?'], ['?', '?']]
        >>> count_unrevealed_non_mines(helper_board, game_board)
        3

        >>> helper = [[-1, -1], [1, 0]]
        >>> game_board = [['?', '?'], ['1', '?']]
        >>> count_unrevealed_non_mines(helper_board, game_board)
        1

        >>> helper_board = [[0, 1, -1], [1, 2, 1], [-1, 1, 0]]
        >>> game_board = [['0', '1', '?'], ['?', '?', '1'], ['?', '1', '0']]
        >>> count_unrevealed_non_mines(helper_board, game_board)
        3
    '''
    count = 0
    rows = len(helper_board)
    cols = len(helper_board[0])
    for r in range(rows):
        for c in range(cols):
            if helper_board[r][c] != -1 and game_board[r][c] == HIDDEN_SYMBOL:
                count += 1
    return count


def play():
    '''
    Main game loop for playing Minesweeper interactively.
    Prompts the user for difficulty, grid dimensions, and moves until all
    non-mine cells are revealed or the player hits a mine.
    '''
    rows = int(input("Enter number of rows for the board: "))
    cols = int(input("Enter number of columns for the board: "))
    difficulty = input("Choose a difficulty from [EASY, MEDIUM, HARD]: ")

    if difficulty == "EASY":
        mines = int(EASY_PERCENT * (rows * cols))
    elif difficulty == "MEDIUM":
        mines = int(MEDIUM_PERCENT * (rows * cols))
    elif difficulty == "HARD":
        mines = int(HARD_PERCENT * (rows * cols))
    
    helper_board = generate_helper_board(rows, cols, mines)
    game_board = init_board(rows, cols, HIDDEN_SYMBOL)
    flag_count = 0

    while count_unrevealed_non_mines(helper_board, game_board) > 0:
        # Calculate remaining mines based on flags placed
        mines_remaining = mines - flag_count
        print("Current Board: (" + str(mines_remaining) + " mines remaining)")
        print_board(game_board)

        # Ask player whether to reveal a cell or place/remove a flag
        flag_state = int(input("Choose 0 to reveal or 1 to flag: "))
        row = int(input("Which row? "))
        col = int(input("Which col? "))

        if flag_state == 0:
        # Reveal the chosen cell
            reveal(helper_board, game_board, row, col)
        elif flag_state == 1:
        # Toggle a flag on the chosen cell
            flag(game_board, row, col)
            flag_count += 1

    print("Congratulations! You won!")
    for r in range(len(helper_board)):
        for c in range(len(helper_board[0])):
            if game_board[r][c] == HIDDEN_SYMBOL:
                game_board[r][c] = FLAG_SYMBOL
    print("Final Board: ")
    print_board(game_board)

# 5: Bot

def solve_cell(board: list, row: int, col: int, left_click, right_click):
    '''
    Analyze a cell and take action based on surrounding clues.
    If the number of flagged neighbours equals the cell number,
    it reveals all remaining hidden neighbours.
    If the number of hidden neighbours equals remaining mines, 
    it flags those cells.
    '''
    cell = board[row][col]

    # Check if cell is a number (string form)
    if cell == HIDDEN_SYMBOL or cell == FLAG_SYMBOL:
        return
    
    # Convert string to integer
    num = int(cell)
    
    # Get neighbours
    neighbours = get_neighbour_positions(board, row, col)

    # Count flagged and hidden neighbors
    flagged_count = count_neighbours(board, row, col, FLAG_SYMBOL)
    hidden_count = count_neighbours(board, row, col, HIDDEN_SYMBOL)

    if flagged_count == num:
        for pos in neighbours:
            r, c = pos
            if board[r][c] == HIDDEN_SYMBOL:
                left_click(r, c)
                
    if hidden_count == num - flagged_count:
        for pos in neighbours:
            r, c = pos
            if board[r][c] == HIDDEN_SYMBOL:
                right_click(r, c)
    
def solve(board: list, left_click, right_click):
    '''
    Run the bot to repeatedly call solve_cell until the game is solved.
    The bot continues making deductions until no hidden cells remain.
    '''
    while count_total(board, HIDDEN_SYMBOL) > 0:
        for r in range(len(board)):
            for c in range(len(board[0])):
                solve_cell(board, r, c, left_click, right_click)