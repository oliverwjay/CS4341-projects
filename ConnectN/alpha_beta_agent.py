import math
import random

import agent
import board
import fast_board

###########################
# Alpha-Beta Search Agent #
###########################


class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth
        self.up_bound = 10000
        self.down_bound = -10000

        self.win_case = 100000  # Return for a win (May increase for different results)
        self.loss_case = -1500  # Return for a loss (May decrease for different results)
        self.tie_case = 0  # Return for tie case (Adjust as needed)

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        brd = fast_board.FastBoard(brd)
        return self.alpha_beta_pruning(brd)

    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple"""
        """"(new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb, col))
        return succ

    def alpha_beta_pruning(self, brd):
        """
        Alpha Beta Pruning Function
        :param brd: brd
        :return: An Action
        """
        brd.print_it()
        print("Evaluating:")
        # Get the max_value from our tree
        moveVal = self.max_value(brd, self.down_bound, self.up_bound, self.max_depth)
        # Return the column in which the token must be added
        print(moveVal)
        moves = brd.free_cols()
        for col in moves:
            brd.add_token(col)
            print(brd.get_outcome_convolution())
            brd.remove_token(col)
            # if self.utility_function(brd) == moveVal:
            #     print(col)
            #     brd.remove_token(col)
            #     return col
        if moves.__len__() == 0:
            return -1
        return moveVal[1]

    def get_sorted_options(self, brd):
        """
        Finds the options
        :param brd: Game board
        :return: Max sorted list of tuples in form (heuristic, move)
        """
        # Find options
        opts = brd.free_cols()

        # Find heuristics
        scored_opts = []
        for opt in opts:
            brd.add_token(opt)
            scored_opts.append((brd.get_outcome_convolution(), opt))
            brd.remove_token(opt)

        # Sore options by heuristic
        scored_opts.sort()

        # Return sorted list
        return scored_opts

    def max_value(self, brd, alpha, beta, depth_lim):
        """
        Max Value Function
        :param brd: copy of game board
        :param alpha: alpha
        :param beta: beta
        :param depth_lim: how many layers deep to try
        :return: a utility value (v), the best move
        """
        # Get options sorted by heuristic
        scored_opts = self.get_sorted_options(brd)[::-1]

        # Check for tie
        if not scored_opts:
            return 0, -1

        # If end of recursion, pick the best heuristic
        if depth_lim <= 0:
            return scored_opts[0]

        # Set default v
        v = self.down_bound - 1
        best_opt = scored_opts[0][1]

        # Evaluate each
        for score, opt in scored_opts:
            if score > self.up_bound:
                return self.up_bound, opt
            brd.add_token(opt)
            full_score = self.min_value(brd, alpha, beta, depth_lim - 1)[0]
            brd.remove_token(opt)
            if full_score > v:
                v = full_score
                best_opt = opt
                if v >= beta:
                    break
            alpha = max(alpha, v)
        return v, best_opt

    def min_value(self, brd, alpha, beta, depth_lim):
        """
        Max Value Function
        :param brd: copy of game board
        :param alpha: alpha
        :param beta: beta
        :param depth_lim: how many layers deep to try
        :return: a utility value (v), the best move
        """
        # Get options sorted by heuristic
        scored_opts = self.get_sorted_options(brd)

        # Check for tie
        if not scored_opts:
            return 0, -1

        # If end of recursion, pick the best heuristic
        if depth_lim <= 0:
            return scored_opts[0]

        # Set default v
        v = self.up_bound - 1
        best_opt = scored_opts[0][1]

        # Evaluate each
        for score, opt in scored_opts:
            if score < self.down_bound:
                return self.down_bound, opt
            brd.add_token(opt)
            full_score = self.max_value(brd, alpha, beta, depth_lim - 1)[0]
            brd.remove_token(opt)
            if full_score < v:
                v = full_score
                best_opt = opt
                if v <= alpha:
                    break
            beta = max(beta, v)
        return v, best_opt

    def utility_function(self, brd):
        """
        This function will determine the value of a given board configuration
        :param brd: the board config
        :return: a utility value
        """

        # Gets the outcome of the board
        # Returns the winner of the game: 1 for Player 1, 2 for Player 2, and 0 for no winner
        ret = brd.get_outcome()

        if ret == 1:
            return self.win_case
        elif ret == 2:
            return self.loss_case
        else:
            if len(self.get_successors(brd)) == 0:
                return self.tie_case
            else:
                return self.evaluate(brd)

    def evaluate(self, brd):
        """
        Evaluates the current board state if it had no win or loss and is not a tie
        :param brd: the board
        :return: the value of this board
        """

        us_count = 0
        them_count = 0
        # This is temporary and will be modified at a later date

        # Get the set of all cords in the board
        set_of_moves = self.get_open_spaces(brd)

        # Check if these blank spaces connect to n-1 of a certain x or o
        for move in set_of_moves:
            us_count = brd.is_any_line_poss(move[0], move[1], 1) + us_count
        for move in set_of_moves:
            them_count = brd.is_any_line_poss(move[0], move[1], 2) + them_count

        return us_count - them_count

    def get_open_spaces(self, brd):
        """
        gets the open spaces (x, y) cords
        :param brd: the board
        :return: set of open spaces
        """
        # Get possible actions (returns array of cols)
        freecols = brd.free_cols()
        ret_set = set()

        # Get a set of the next possible moves
        for col in freecols:
            for row in range(0, brd.h):
                if brd.board[row][col] == 0:
                    ret_set.add((col, row))
                    break  # This could jump out of both loops? if issue arises

        return ret_set

    def terminal_test(self, brd):
        """
        Tests if this is a final board position
        :param brd: the board state
        :return: returns a boolean on if it is a terminal state
        """
        freecols = brd.free_cols()
        if brd.get_outcome() == 0 and len(freecols) > 0:
            return False
        else:
            return True