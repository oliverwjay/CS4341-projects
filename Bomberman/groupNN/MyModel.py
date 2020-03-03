import numpy as np
import math
import matplotlib.pyplot as plt


class MyModel:
    def __init__(self, agent, world):
        self.world = world
        self.max_states = 10 ** 4
        self.gamma = .9
        self.alpha = 0.01
        self.agent = agent

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
        bins = np.zeros((9, 10))
        diagonal = math.sqrt((math.pow(self.world.height(), 2) + math.pow(self.world.width(), 2)))
        bins[0] = np.linspace(0, diagonal)  # Bin for monster 1
        bins[1] = np.linspace(0, diagonal)  # Bin for monster 2
        bins[2] = np.linspace(0, diagonal)  # Bin for Enemy Character 1
        bins[3] = np.linspace(0, diagonal)  # Bin for Enemy Character 2
        bins[4] = np.linspace(0, diagonal)  # Bin for Enemy Character 3
        bins[5] = np.linspace(0, diagonal)  # Bin for Enemy Character 4
        bins[6] = np.linspace(0, 1)  # Bin for Bomb (Before Explosion)
        bins[7] = np.linspace(0, (self.world.height() * self.world.width()))  # Bin for Exit
        bins[8] = np.linspace(0,8)  # Bin for Fire Location
        # TODO: Need to check if Bin for Fire Location is correct

    def assign_bins(self, obs, bins, world):
        """
        Assigns the observations to the bins
        """
        state = np.zeros(9)
        char_loc = (self.agent.x, self.agent.y)
        state[0] = world.monsters_at()[0]
        return state
