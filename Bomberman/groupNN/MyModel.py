import numpy as np
import matplotlib.pyplot as plt


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




