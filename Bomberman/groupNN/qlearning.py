# This is necessary to find the main code
import math
import sys
from state import State
import numpy as np

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

class Qlearning():

    def __init__(self, state, total_reward, character, csv):
        self.state = state
        self.total_reward = total_reward
        self.character = character

    def step(self, Q, eps=0.5):

        if np.random.uniform() < eps:
            act = self.character.sample()
        else:
            act = self.max_dict()

    @staticmethod
    def max_dict(d):
        """
        Gets the maximum dictionary
        """
        max_v = float('-inf')
        for key, val in d.items():
            if val > max_v:
                max_v = val
                max_key = key
        return max_key, max_v