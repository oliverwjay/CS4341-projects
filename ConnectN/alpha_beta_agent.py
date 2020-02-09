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
        self.up_bound = 10000
        self.down_bound = -10000

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        list_pos_moves = self.get_successors(brd)
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
        # Get the max_value from our tree
        moveVal = self.max_value(brd, self.down_bound, self.up_bound)
        # Return the column in which the token must be added
        return moveVal[0]

    def max_value(self, brd, alpha, beta):
        """
        Max Value Function
        :param brd: copy of game board
        :param alpha: alpha
        :param beta: beta
        :return: a utility value (v)
        """
        v = self.down_bound
        if self.terminal_test(brd):
            return [-1, self.utility_function(brd)]
        else:
            for a in self.get_successors(brd):
                v = max(v, self.min_value(a[0], alpha, beta)[1])
                print("Beta: ")
                print(v)
                if v >= beta:
                    return [a[1], v]
                alpha = max(alpha, v)
            return [a[1],v]

    def min_value(self, brd, alpha, beta):
        """
        :param brd: copy of game board
        :param alpha: alpha
        :param beta: beta
        :return: a utility value (v)
        """
        v = self.up_bound
        if self.terminal_test(brd):
            return [-1, self.utility_function(brd)]
        else:
            for a in self.get_successors(brd):
                v = min(v, self.max_value(a[0], alpha, beta)[1])
                print("Alpha: ")
                print(v)
                if v <= alpha:
                    return [a[1], v]
                beta = min(beta, v)
            return [a[1],v]

    def utility_function(self, brd):
        """
        This function will determine the value of a given board configuration
        :param brd: the board config
        :return: a utility value
        """

        # NOTE: Make Self values if needed
        win_case = 10  # Return for a win (May increase for different results)
        loss_case = -15  # Return for a loss (May decrease for different results)
        tie_case = 0  # Return for tie case (Adjust as needed)
        else_case = 0  # Return when the game is still happening (Not sure if ever reached)

        # Makes a Board Object with Initialized Parameters
        # board_obj = board.Board(brd, 7, 6, 4)

        # Gets the outcome of the board
        # Returns the winner of the game: 1 for Player 1, 2 for Player 2, and 0 for no winner
        ret = brd.get_outcome()

        if ret == 1:
            return win_case
        elif ret == 2:
            return loss_case
        else:
            if len(self.get_successors(brd)) == 0:
                return tie_case
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
            us_count = brd.is_any_line_pos(move[0], move[1], 1) + us_count
        for move in set_of_moves:
            them_count = brd.is_any_line_pos(move[0], move[1], 2) + them_count

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
                if brd[row][col] == 0:
                    ret_set.add((row, col))
                    break  # This could jump out of both loops? if issue arises

        return ret_set

    def terminal_test(self, brd):

        if brd.get_outcome() == 0:
            return False
        else:
            return True

# Testing
layout = [[1, 2, 2, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0]
        ]
ABagent = AlphaBetaAgent("TestAgent", 3)
smallBoard = board.Board(layout, 4, 4, 3)
print(ABagent.alpha_beta_pruning(smallBoard))