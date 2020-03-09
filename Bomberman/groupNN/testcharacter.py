# This is necessary to find the main code
import math
import sys
import random
from qlearning import Qlearning
from state import State

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from events import Event
from colorama import Fore, Back


class TestCharacter(CharacterEntity):
    def __init__(self, name, avatar, x, y, alpha=.005, filename="../lessons.p"):
        """
        Initialize character
        :param name: Name of character
        :param avatar: Avatar for printing
        :param x: Initial x
        :param y: Initial y
        """
        CharacterEntity.__init__(self, name, avatar, x, y)
        self.reward = 0
        self.q_learn = Qlearning(alpha, filename)
        self.est_var = None

    def do(self, wrld):
        """
        Make move, and learn result
        """
        # Estimate variant
        if self.est_var is None:
            n_mo = len(wrld.monsters)
            n_walls = sum([sum(col) for col in wrld.grid])
            self.est_var = f"_{n_mo}m_{n_walls}w"
            self.q_learn.change_file_suffix(self.est_var)

        # Creation of State
        state = State(wrld, (self.x, self.y), self.name, TestCharacter.act)

        # Find move
        act = self.q_learn.step(state)
        self.act(act)

        # Simulate move for learning
        sort_of_me = wrld.me(self)
        TestCharacter.act(sort_of_me, act)
        new_wrld, events = wrld.next()
        new_me = new_wrld.me(self)
        reward = -1  # Cost of living
        if new_me is not None:
            res_state = State(new_wrld, (new_me.x, new_me.y), self.name, TestCharacter.act)
            reward += (state.len_a_star - res_state.len_a_star)  # Reward for moving toward exit
            reward -= (max(state.dist_closest_monster, 5) - max(state.dist_closest_monster, 5))
        else:
            res_state = State(new_wrld, (self.x, self.y), self.name, TestCharacter.act)
            res_state.result = "End"

        event_scores = {Event.BOMB_HIT_CHARACTER: -1000,
                        Event.CHARACTER_KILLED_BY_MONSTER: -1000,
                        Event.CHARACTER_FOUND_EXIT: 300,
                        Event.BOMB_HIT_MONSTER: 15,
                        Event.BOMB_HIT_WALL: 5}

        # Apply event reward
        for event in events:
            if event.tpe in event_scores:
                reward += event_scores[event.tpe]

        # Learn reward
        self.q_learn.save_outcome(state, res_state, reward)

    def act(self, action):
        """
        Action: ((dx, dy), Boolean)
        The action we need to make
        """
        self.move(action[0][0], action[0][1])
        if action[1] and random.uniform(0, 1) < .9:
            self.place_bomb()


