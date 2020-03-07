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
        self.alpha = 0.05
        self.gamma = 0.9
        self.default_reward = 0
        self.filename = filename
        self.weights = np.array([-5.1, 1, 1, 1, 1, 1, 1])

        if os.path.exists(filename):
            file = open(filename, 'rb')
            self.weights = pickle.load(file)
            file.close()

    def step(self, state, eps=0.05):
        """
        Steps through one state
        """
        # if state not in self.Q:
        #     self.Q[state] = {action: self.default_reward for action in self.all_actions(state)}

        if np.random.uniform() < eps:
            act = self.sample(state)
        else:
            act = self.best_action(state)[1]

        # print(f"State: {state} Act: {act}")
        return act

    def save_outcome(self, state, new_state, reward):
        """
        Saves the action
        """

        delta = [reward + self.gamma * self.best_action(new_state)[0]] - self.best_action(state)[0]

        self.weights += self.alpha * delta * new_state.get_f()
        print(self.weights)
        file = open(self.filename, "wb")
        pickle.dump(self.weights, file)
        file.close()

    @staticmethod
    def sample(state):
        """
        Gets random move
        """
        return random.choice(state.get_valid_actions())

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

    def best_action(self, state):
        """
        Gets the best action for approximate Q-Learning
        """
        data = state.get_scored_actions()
        return max([(np.dot(f, self.weights), a) for f, a in data])