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
        state = State(wrld, (self.x, self.y), self.name, TestCharacter.act)

        act = self.q_learn.step(state)
        self.act(act)

        sort_of_me = wrld.me(self)
        TestCharacter.act(sort_of_me, act)
        new_wrld, events = wrld.next()
        new_me = new_wrld.me(self)
        reward = -1  # new_wrld.scores[self.name] - wrld.scores[self.name]
        if new_me is not None:
            res_state = State(new_wrld, (new_me.x, new_me.y), self.name, TestCharacter.act)
            # reward -= 2
            reward += (state.len_a_star - res_state.len_a_star)
            reward -= (max(state.dist_closest_monster, 5) - max(state.dist_closest_monster, 5))
            # reward -= act[1] * 20
            # reward += (state.dis_to_exit() - res_state.dis_to_exit())
        else:
            res_state = State(new_wrld, (self.x, self.y), self.name, TestCharacter.act)
            res_state.result = "End"

        event_scores = {Event.BOMB_HIT_CHARACTER: -200,
                        Event.CHARACTER_KILLED_BY_MONSTER: -200,
                        Event.CHARACTER_FOUND_EXIT: 200,
                        Event.BOMB_HIT_MONSTER: 20,
                        Event.BOMB_HIT_WALL: 5}

        for event in events:
            if event.tpe in event_scores:
                reward += event_scores[event.tpe]
        # print("reward: ", reward)
        # print(state.get_scored_actions())

        self.q_learn.save_outcome(state, res_state, reward)

        pass

    def act(self, action):
        """
        Action: ((dx, dy), Boolean)
        The action we need to make
        """
        self.move(action[0][0], action[0][1])
        if action[1]:
            self.place_bomb()


