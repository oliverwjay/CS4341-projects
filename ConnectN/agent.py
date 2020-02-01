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
        return brd.free_cols()[3]


class OutsourcedAgent(Agent):
    """Cheats by looking up the answer"""
    def go(self, brd):
        history = ''.join([str(x + 1) for x in brd.history])
        r = requests.get("http://connect4.gamesolver.org/solve", params={'pos': history}, headers={'User-Agent': 'not-python-requests'})
        scores = r.json()['score']
        scores = [x-((x == 100) * 200) for x in scores]
        choice = scores.index(max(scores))
        brd.print_it()
        print(history, scores, choice)
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
