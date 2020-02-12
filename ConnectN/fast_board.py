import copy
import numpy as np
import board
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
        # Me
        self.player = slow_board.player
        # Opponent
        self.opponent = ~self.player & 3
        # Current placer
        self.cur_player = 1
        # Column heights
        self.col_heights = [-1] * self.w
        # Board data
        self.board = np.zeros((self.h, self.w), dtype=np.int16)
        for c in range(self.w):
            for r in range(self.h):
                if slow_board.board[r][c] == self.player:
                    self.col_heights[c] += 1
                    self.board[r, c] = 1
                if slow_board.board[r][c] == self.opponent:
                    self.col_heights[c] += 1
                    self.board[r, c] = -1
        # Create kernels
        self.kernels = [np.ones((self.n, 1), dtype=np.int8),
                   np.ones((1, self.n), dtype=np.int8),
                   np.identity(self.n, dtype=np.int8),
                   np.rot90(np.identity(self.n, dtype=np.int8))]

    def get_outcome_convolution(self):
        """Scores the board using convolutions"""
        score = 0  # Default score
        for k in self.kernels:  # Check kernel for each win shape
            sol = convolve2d(self.board, k, 'valid')  # Check matches with convolution
            k_score = np.sum(np.power(sol, 5))
            score += k_score
            if k_score > (self.n ** 5) // 2:
                if np.any(sol == self.n):
                    return 32767
            elif k_score < - (self.n ** 5) // 2:
                if np.any(sol == - self.n):
                    return -32767
        return score

    # Adds a token for the current player at the given column
    #
    # PARAM [int] x: The column where the token must be added; the column is assumed not full.
    #
    # NOTE: This method switches the current player.
    def add_token(self, x):
        """Adds a token for the current player at column x; the column is assumed not full"""
        # Update column height
        self.col_heights[x] += 1
        # Add token
        self.board[self.col_heights[x], x] = self.cur_player
        # Switch player
        self.cur_player *= -1

    def remove_token(self, x):
        """Adds a token for the current player at column x; the column is assumed not full"""
        # Add token
        self.board[self.col_heights[x], x] = 0
        # Update column height
        self.col_heights[x] -= 1
        # Switch player
        self.cur_player *= -1

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
                    print(self.board[y, x] % 3, end='')
            print("|")
        print("+", "-" * self.w, "+", sep='')
        print(" ", end='')
        for i in range(self.w):
            print(i, end='')
        print("")
