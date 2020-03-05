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
    def __init__(self, name, avatar, x, y):
        CharacterEntity.__init__(self, name, avatar, x, y)
        self.reward = 0
        self.q_learn = Qlearning(0)

    def do(self, wrld):
        """
        Our Code
        """

        # Creation of State
        state = State(wrld, (self.x, self.y), self.name)

        act = self.q_learn.step(state)
        self.act(act)

        sort_of_me = wrld.me(self)
        TestCharacter.act(sort_of_me, act)
        new_wrld, events = wrld.next()
        new_me = new_wrld.me(self)
        reward = -3  # new_wrld.scores[self.name] - wrld.scores[self.name]
        if new_me is not None:
            res_state = State(new_wrld, (new_me.x, new_me.y), self.name)
            event_scores = {Event.BOMB_HIT_CHARACTER: -100,
                            Event.CHARACTER_KILLED_BY_MONSTER: -100,
                            Event.CHARACTER_FOUND_EXIT: 100,
                            Event.BOMB_HIT_MONSTER: 10,
                            Event.BOMB_HIT_WALL: 10}

            for event in events:
                if event in event_scores:
                    reward += event_scores[event]

            reward += (state.len_a_star - res_state.len_a_star) * 4
            reward += (state.dis_to_exit() - res_state.dis_to_exit()) * 4
        else:
            res_state = state
        print("reward: ", reward)

        self.q_learn.save_outcome(act, res_state, state, reward)

        pass

    def act(self, action):
        """
        Action: ((dx, dy), Boolean)
        The action we need to make
        """
        self.move(action[0][0], action[0][1])
        if action[1]:
            self.place_bomb()


