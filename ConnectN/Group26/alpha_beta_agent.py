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
        print(moveVal, self.get_sorted_options(brd))
        return moveVal[1]

    @staticmethod
    def get_sorted_options(brd):
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

