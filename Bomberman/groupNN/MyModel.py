import numpy as np
import matplotlib.pyplot as plt
from testcharacter import TestCharacter


class MyModel:
    def __init__(self, world):
        self.world = world
        self.max_states = 10**4
        self.gamma = .9
        self.alpha = 0.01

    @staticmethod
    def max_dict(d):
        """
        Gets the maximum from a dictionary
        """
        max_v = float('-inf')
        for key, val in d.items():
            if val > max_v:
                max_v = val
                max_key = key
        return max_key, max_v

    def create_bins(self):
        """
        creates bounds on the input space
        """

    def assign_bins(self, obs, bins, world):
        """
        Assigns the observations to the bins
        """

    @staticmethod
    def get_state_as_string(state):
        """
        Gets the state as a string
        """
        string_state = ''.join(str(int(e)) for e in state)
        return string_state

    def play_one_game(self, bins, Q, eps=0.5):
        observation = 0  # env.reset()
        done = False
        cnt = 0  # Num moves in an episode
        state = 0  # get_state_as_string(assign_bins(observation, bins))
        total_reward = 0

        while not done:
            cnt += 1
            if np.random.uniform() < eps:
                act = env.action_space.sample()  # epsilon greedy
            else:
                act = self.max_dict(Q[state])[0]

            observation, reward, done, _ = env.step(act)

            total_reward += reward

            if done and cnt < 200:
                reward = -300

            state_new = get_state_as_string(self.assign_bins(observation, bins))

            a1, max_q_s1a1 = self.max_dict(Q[state_new])
            Q[state][act] += self.alpha * (reward + self.gamma * max_q_s1a1 - Q[state][act])
            state, act = state_new, a1

        return total_reward, cnt


