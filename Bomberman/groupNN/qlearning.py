# This is necessary to find the main code
import math
import sys
from state import State
import numpy as np
import random

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back


class Qlearning():

    def __init__(self, total_reward):
        self.total_reward = total_reward
        self.Q = {}
        self.alpha = 0.01
        self.gamma = 0.9

    def step(self, state, eps=0.5):

        if np.random.uniform() < eps:
            act = self.sample()
        else:
            act = self.max_dict(self.Q[state])[0]

        return act

    def save_outcome(self, action, state, reward):
        """
        Saves the action
        """
        a1, max_q_s1a1 = self.max_dict(self.Q[state])
        self.Q[state][action] += self.alpha * (reward + self.gamma * max_q_s1a1 - self.Q[state][action])

    @staticmethod
    def sample():
        """
        Gets random move
        """
        connected = [(x, y) for x in range(- 1, 2) for y in range(- 1, 2) if
                     (x, y) != (0, 0)]

        move_act = random.choice(connected)

        random_bit = random.getrandbits(1)
        random_boolean = bool(random_bit)

        return move_act, random_boolean

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
