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
import pickle
import os


class Qlearning:

    def __init__(self, total_reward, filename="../lessons.p"):
        self.total_reward = total_reward
        self.alpha = 0.2
        self.gamma = 0.9
        self.default_reward = 0
        self.filename = filename

        if os.path.exists(filename):
            file = open(filename, 'rb')
            self.Q = pickle.load(file)
            file.close()
        else:
            self.Q = {}

    def step(self, state, eps=0.15):
        """
        Steps through one state
        """
        # if state not in self.Q:
        #     self.Q[state] = {action: self.default_reward for action in self.all_actions(state)}

        if np.random.uniform() < eps:
            act = self.sample(state)
        else:
            act = self.max_for_state(state)[0]

        print(f"State: {state} Act: {act} Score: {self.Q[state][act]}")
        opts = self.Q[state]
        return act

    def save_outcome(self, action, new_state, old_state, reward):
        """
        Saves the action
        """
        a1, max_q_s1a1 = self.max_for_state(new_state, True)
        self.Q[old_state][action] = self.alpha * (reward + self.gamma * max_q_s1a1) + (1 - self.alpha) * self.Q[old_state][action]

        file = open(self.filename, 'wb')
        pickle.dump(self.Q, file)
        file.close()

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
    def all_actions(state):
        """
        gets all possible actions
        """
        moves = [(x, y) for x in range(- 1, 2) for y in range(- 1, 2)]
        arr = []
        for move in moves:
            if not state.bomb_placed:
                arr.append((move, True))
            arr.append((move, False))
        return arr

    def max_for_state(self, state, ignore_zeros=False):
        """
        Gets the maximum dictionary
        """
        if state.result is not None:
            return ((0, 0), False), 0

        if state not in self.Q:
            self.Q[state] = {action: self.default_reward for action in self.all_actions(state)}

        d = self.Q[state]
        options = self.possible_actions(state)

        max_v = float('-inf')
        for key, val in d.items():
            if key in options and val > max_v and (not ignore_zeros or val != 0):
                max_v = val
                max_key = key

        if max_v == float('-inf'):
            return self.sample(state)

        return max_key, max_v
