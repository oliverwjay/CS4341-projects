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


class Qlearning:

    def __init__(self, total_reward):
        self.total_reward = total_reward
        self.Q = {}
        self.alpha = 0.01
        self.gamma = 0.9
        self.default_reward = -10

    def step(self, state, eps=0.5):
        """
        Steps through one state
        """
        if state not in self.Q:
            self.Q[state] = {action: self.default_reward for action in self.possible_actions(state)}

        if np.random.uniform() < eps:
            act = self.sample(state)
        else:
            act = self.max_dict(self.Q[state])[0]

        return act

    def save_outcome(self, action, state, reward):
        """
        Saves the action
        """
        a1, max_q_s1a1 = self.max_dict(self.Q[state])
        self.Q[state][action] += self.alpha * (reward + self.gamma * max_q_s1a1 - self.Q[state][action])

    def sample(self, state):
        """
        Gets random move
        """
        return random.choice(self.possible_actions(state))

    @staticmethod
    def possible_actions(state):
        """
        gets all possible actions
        """
        moves = state.valid_moves
        arr = []
        for move in moves:
            if not state.bomb_placed:
                arr.append((move, True))
            arr.append((move, False))
        return arr

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
