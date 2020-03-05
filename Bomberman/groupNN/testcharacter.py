# This is necessary to find the main code
import math
import sys
import random
from qlearning import Qlearning
from state import State

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back


class TestCharacter(CharacterEntity):
    def __init__(self, name, avatar, x, y):
        CharacterEntity.__init__(self, name, avatar, x, y)
        self.reward = 0
        self.q_learn = Qlearning(0)
        self.prev_act = None
        self.prev_state = None

    def do(self, wrld):
        """
        Our Code
        """
        new_reward = wrld.scores[self.name] - self.reward
        self.reward = wrld.scores[self.name]

        # Creation of State
        state = State(wrld, (self.x, self.y), self.name)

        if self.prev_act is not None:
            self.q_learn.save_outcome(self.prev_act, self.prev_state, new_reward)

        act = self.q_learn.step(state)
        self.prev_act = act
        self.prev_state = state
        self.act(act)

        pass

    def act(self, action):
        """
        Action: ((dx, dy), Boolean)
        The action we need to make
        """
        self.move(action[0][0], action[0][1])
        if action[1]:
            self.place_bomb()


