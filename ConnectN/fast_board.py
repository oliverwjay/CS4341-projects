import copy
import numpy as np
from . import board
from scipy.signal import convolve2d, fftconvolve, correlate2d, oaconvolve


##############
# Game Board #
##############

class FastBoard(object):

    # Class constructor.
    #
    # PARAM [2D list of int] board: the board configuration, row-major
    # PARAM [int]            w:     the board width
    # PARAM [int]            h:     the board height
    # PARAM [int]            n:     the number of tokens to line up to win
    def __init__(self, slow_board):
        """Class constructor"""
        # Board width
        self.w = slow_board.w
        # Board height
        self.h = slow_board.h
        # How many tokens in a row to win
        self.n = slow_board.n
        # Current player
        self.player = 1
        # Current player
        self.opponent = 2
        # Board data
        self.board = np.zeros((self.h, self.w), dtype=np.int8)
        for c in range(self.w):
            for r in range(self.h):
                if slow_board.board[r][c] == self.player:
                    self.board[r, c] = 1
                if slow_board.board[r][c] == self.opponent:
                    self.board[r, c] = -1
        # Create kernels
        self.kernels = [np.ones((self.n, 1), dtype=np.int8),
                   np.ones((1, self.n), dtype=np.int8),
                   np.identity(self.n, dtype=np.int8),
                   np.rot90(np.identity(self.n, dtype=np.int8))]

    # Check if a line of identical tokens exists starting at (x,y) in direction (dx,dy)
    #
    # PARAM [int] x:  the x coordinate of the starting cell
    # PARAM [int] y:  the y coordinate of the starting cell
    # PARAM [int] dx: the step in the x direction
    # PARAM [int] dy: the step in the y direction
    # RETURN [Bool]: True if n tokens of the same type have been found, False otherwise
    def is_line_at(self, x, y, dx, dy):
        """Return True if a line of identical tokens exists starting at (x,y) in direction (dx,dy)"""
        # Avoid out-of-bounds errors
        if ((x + (self.n - 1) * dx >= self.w) or
                (y + (self.n - 1) * dy < 0) or (y + (self.n - 1) * dy >= self.h)):
            return False
        # Get token at (x,y)
        t = self.board[y, x]
        # Go through elements
        for i in range(1, self.n):
            if self.board[y + i * dy, x + i * dx] != t:
                return False
        return True

    # Check if a line of identical tokens exists starting at (x,y) in any direction
    #
    # PARAM [int] x:  the x coordinate of the starting cell
    # PARAM [int] y:  the y coordinate of the starting cell
    # RETURN [Bool]: True if n tokens of the same type have been found, False otherwise
    def is_any_line_at(self, x, y):
        """Return True if a line of identical tokens exists starting at (x,y) in any direction"""
        return (self.is_line_at(x, y, 1, 0) or  # Horizontal
                self.is_line_at(x, y, 0, 1) or  # Vertical
                self.is_line_at(x, y, 1, 1) or  # Diagonal up
                self.is_line_at(x, y, 1, -1))  # Diagonal down

    # Calculate the game outcome.
    #
    # RETURN [int]: 1 for Player 1, 2 for Player 2, and 0 for no winner
    def get_outcome(self):
        """Returns the winner of the game: 1 for Player 1, 2 for Player 2, and 0 for no winner"""
        for y in range(self.h):
            for x in range(self.w):
                if (self.board[y][x] != 0) and self.is_any_line_at(x, y):
                    return self.board[y][x]
        return 0

    def get_outcome_convolution(self):
        """Scores the board using convolutions"""
        score = 0  # Default score
        for k in self.kernels:  # Check kernel for each win shape
            sol = convolve2d(self.board, k, 'valid')  # Check matches with convolution
            score += np.sum(np.power(sol, 3))
        return score

    # Adds a token for the current player at the given column
    #
    # PARAM [int] x: The column where the token must be added; the column is assumed not full.
    #
    # NOTE: This method switches the current player.
    def add_token(self, x):
        """Adds a token for the current player at column x; the column is assumed not full"""
        # Find empty slot for token
        y = 0
        while self.board[y, x] != 0:
            y = y + 1
        self.board[y, x] = self.player
        # Switch player
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    # Returns a list of the columns with at least one free slot.
    #
    # RETURN [list of int]: the columns with at least one free slot
    def free_cols(self):
        """Returns a list of the columns with at least one free slot"""
        return [x for x in range(self.w) if self.board[-1, x] == 0]

    # Prints the current board state.
    def print_it(self):
        print("+", "-" * self.w, "+", sep='')
        for y in range(self.h - 1, -1, -1):
            print("|", sep='', end='')
            for x in range(self.w):
                if self.board[y, x] == 0:
                    print(" ", end='')
                else:
                    print(2-self.board[y, x], end='')
            print("|")
        print("+", "-" * self.w, "+", sep='')
        print(" ", end='')
        for i in range(self.w):
            print(i, end='')
        print("")
