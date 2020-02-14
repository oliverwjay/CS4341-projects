import board
import random
import requests

#####################
# Agent definitions #
#####################



##################
# Abstract agent #
##################

class Agent(object):
    """Abstract agent class"""

    # Class constructor.
    #
    # PARAM [string] name: the name of this player
    def __init__(self, name):
        """Class constructor"""
        # Agent name
        self.name = name
        # Uninitialized player - will be set upon starting a Game
        self.player = 0

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    def go(self, brd):
        """Returns a column between 0 and (brd.w-1). The column must be free in the board."""
        raise NotImplementedError("Please implement this method")


##########################
#  Always picks 3rd col  #
##########################

class OneColumnAgent(Agent):
    """Agent to always pick the third available column"""
    def go(self, brd):
        return brd.free_cols()[min(3, len(brd.free_cols())-1)]


class OutsourcedAgent(Agent):
    """Cheats by looking up the answer"""
    def __init__(self, name, difficulty):
        """

        :param name:
        :param difficulty:
        """
        super().__init__(name)
        self.difficulty = difficulty

    def get_scores(self, brd):
        history = ''.join([str(x + 1) for x in brd.history])
        r = requests.get("http://connect4.gamesolver.org/solve", params={'pos': history}, headers={'User-Agent': 'not-python-requests'})
        scores = r.json()['score']
        # print(scores)
        scores = [(score - min(scores) + 1)*(score != 100) for score in scores]
        scores = [score**self.difficulty for score in scores]
        scores = [score / sum(scores) for score in scores]
        return scores

    def go(self, brd):
        choice = random.choices(range(7), weights=self.get_scores(brd))[0]
        # brd.print_it()
        # print(history, scores, choice)
        return choice
        # return random.choice(brd.free_cols())


##########################
# Randomly playing agent #
##########################

class RandomAgent(Agent):
    """Randomly playing agent"""

    # Pick a column at random.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    def go(self, brd):
        return random.choice(brd.free_cols())



#####################
# Interactive Agent #
#####################

class InteractiveAgent(Agent):
    """Interactive player"""

    # Ask a human to pick a column.
    #
    # PARAM [board.Board] brd: the current board state (ignored)
    # RETURN [int]: the column where the token must be added
    def go(self, brd):
        freecols = brd.free_cols()
        col = int(input("Which column? "))
        while not col in freecols:
            print("Can't place a token in column", col)
            col = int(input("Which column? "))
        return col
