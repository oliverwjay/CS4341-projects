import numpy as np
import math
import matplotlib.pyplot as plt
from testcharacter import TestCharacter


class MyModel:
    def __init__(self, world):
        self.world = world
        self.max_states = 10 ** 4
        self.gamma = .9
        self.alpha = 0.01

