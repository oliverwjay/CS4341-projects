import math
import random
import time
import agent
from . import fast_board


###########################
# Alpha-Beta Search Agent #
###########################


class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth, time_limit=15, est_prune=0, debug=False, auto_depth=False):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth
        self.up_bound = 10000
        self.down_bound = -10000

        self.win_case = 100000  # Return for a win (May increase for different results)
        self.loss_case = -1500  # Return for a loss (May decrease for different results)
        self.tie_case = 0  # Return for tie case (Adjust as needed)

        self.time_limit = time_limit  # How long to restrict to
        self.est_prune = est_prune  # Fractions of nodes estimated to be pruned
        self.nodes_per_second = None  # Estimated number of nodes that can be evaluated per second
        self.nodes_visited = 0  # Number of nodes visited
        self.time_cutoff = .875  # Fraction of time before skipping nodes
        self.forced_cutoff = False  # If the program has had to end early

        self.start_time = time.time()  # Time of evaluation start

        self.debug = debug  # Whether to print output

        self.auto_depth = auto_depth  # Automatically run at higher depth if there is time

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Start timer
        self.start_time = time.time()
        self.nodes_visited = 0
        self.forced_cutoff = False

        # Build faster board
        brd = fast_board.FastBoard(brd)

        # Run CPU test
        if self.nodes_per_second is None and sum(brd.col_heights) <= 1 - brd.w:
            if self.debug:
                print("First turn")

        # Calculate move
        depth = self.max_depth
        score, move = self.alpha_beta_pruning(brd, depth)

        while self.auto_depth and self.get_time() < .5 and self.down_bound < score < self.up_bound and score:
            depth += 2
            score2, move2 = self.alpha_beta_pruning(brd, depth)
            if not self.forced_cutoff:
                if self.debug:
                    print(f"Improved depth! old:{(score, move)} new:{(score2, move2)}")
                move = move2
                score = score2

        # Print results
        if self.debug:
            print(f"Evaluated {self.nodes_visited} in {self.get_time(False)}")

        return move

    def get_time(self, proportional=True):
        """
        Returns the time elapsed
        :param proportional: True returns time from 0-1, False returns 0 - time limit
        :return: Time elapsed
        """
        # Calculate time
        cur_time = time.time() - self.start_time
        if proportional:
            return cur_time / self.time_limit
        else:
            return cur_time

    def alpha_beta_pruning(self, brd, depth):
        """
        Alpha Beta Pruning Function
        :param brd: brd
        :return: An Action
        """
        # Get the max_value from our tree
        moveVal = self.max_value(brd, self.down_bound, self.up_bound, depth)
        # Return the column in which the token must be added
        return moveVal

    def get_sorted_options(self, brd):
        """
        Finds the options
        :param brd: Game board
        :return: Max sorted list of tuples in form (heuristic, move)
        """
        # Increment node visit count
        self.nodes_visited += 1

        # Find options
        opts = brd.free_cols()

        # Find heuristics
        scored_opts = []
        for opt in opts:
            # Add token
            brd.add_token(opt)
            # Score
            scored_opts.append((brd.get_outcome_convolution(), opt))
            # Remove token
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

        # Check clock
        time_pressure = self.get_time()
        # Check for tie
        if not scored_opts:
            return 0, -1

        # If end of recursion, pick the best heuristic
        if depth_lim <= 0 or (depth_lim == 2 and time_pressure > self.time_cutoff) or time_pressure > .95:
            if depth_lim > 0:
                self.forced_cutoff = True
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

        # Check clock
        time_pressure = self.get_time()

        # Check for tie
        if not scored_opts:
            return 0, -1

        # If end of recursion, pick the best heuristic
        if depth_lim <= 0 or (depth_lim == 2 and time_pressure > self.time_cutoff):
            return scored_opts[0]

        # Set default v
        v = self.up_bound + 1
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
            beta = min(beta, v)
        return v, best_opt


# 7x6 Agent
# THE_AGENT = AlphaBetaAgent("Group26", 6, auto_depth=True)

# 10x8 Agent
THE_AGENT = AlphaBetaAgent("Group26", 5, auto_depth=True)
