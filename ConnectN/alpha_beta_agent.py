import math
import agent
import board

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

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        list_pos_moves = self.get_successors(brd)

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
        :return: Action
        """

    def max_value(self, brd, alpha, beta):
        """
        Max Value Function
        :param brd: brd
        :param alpha: alpha
        :param beta: beta
        :return: a utility value (v)
        """

    def min_value(self, brd, alpha, beta):
        """

        :param brd:
        :param alpha:
        :param beta:
        :return:
        """

        # MiniMax pseudo code
        """function minimax(node, depth, maximizingPlayer)
            if depth = 0 or node is a terminal node
                   return the utility of the node

            if maximizingPlayer
                   bestValue := ??
            for each child of node
                   v := minimax(child, depth ? 1, FALSE)
                   bestValue := max(bestValue, v)
            return bestValue  

            else (* minimizing player *)
                   bestValue := +?
                   for each child of node
                          v := minimax(child, depth ? 1, TRUE)
                          bestValue := min(bestValue, v)
                   return bestValue
        """

        # Alpha Beta Prunning Psuedo code
        """
        evaluate (node, alpha, beta)
            if node is a leaf (NEEDS A FUNCTION)
                return the utility value of node (IS A FUNCTION)
            if node is a minimizing  (NEEDS A FUNCTION)
                for each child of node
                    beta = min (beta, evaluate (child, alpha, beta))
                    if beta &lt;= alpha
                    return beta
                return beta
            if node is a maximizing node
                for each child of node
                alpha = max (alpha, evaluate (child, alpha, beta))
                if beta &lt;= alpha
                    return alpha
                return alpha
        """

    def utility_function(self, brd):
        """
        This function will determine the value of a given board configuration
        :param brd: the board config
        :return: a utility value
        """

        # NOTE: Make Self values if needed
        win_case = 1  # Return for a win (May increase for different results)
        loss_case = -1  # Return for a loss (May decrease for different results)
        tie_case = 0  # Return for tie case (Adjust as needed)
        else_case = 0  # Return when the game is still happening (Not sure if ever reached)

        # Makes a Board Object with Initialized Parameters
        board_obj = board.Board(brd, 7, 6, 4)

        # Gets the outcome of the board
        # Returns the winner of the game: 1 for Player 1, 2 for Player 2, and 0 for no winner
        ret = board_obj.get_outcome()

        if ret == 1:
            return win_case
        elif ret == 2:
            return loss_case
        else:
            if len(self.get_successors(brd)) == 0:
                return tie_case
            else:
                return else_case
