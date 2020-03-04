# This is necessary to find the main code
import math
import sys
from state import State
import random

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back



class TestCharacter(CharacterEntity):
    def __init__(self, name, avatar, x, y):
        CharacterEntity.__init__(self, name, avatar, x, y)

    def do(self, wrld):
        """
        Our Code
        """

        # Creation of State
        state = State(wrld, (self.x, self.y), self.name)
        print(state.as_tuple(), hash(state))

        # Commands
        dx, dy = 0, 0
        bomb = False
        # Handle input
        for c in input("How would you like to move (w=up,a=left,s=down,d=right,b=bomb)? "):
            if 'w' == c:
                dy -= 1
            if 'a' == c:
                dx -= 1
            if 's' == c:
                dy += 1
            if 'd' == c:
                dx += 1
            if 'b' == c:
                bomb = True
        # Execute commands
        self.move(dx, dy)
        if bomb:
            self.place_bomb()

        pass

    def sample(self):
        """
        Gets random move
        """
        connected = [(x, y) for x in range(- 1, 2) for y in range(- 1, 2) if
                     (x, y) != (0, 0)]

        move_act = random.choice(connected)

        random_bit = random.getrandbits(1)
        random_boolean = bool(random_bit)

        return move_act, random_boolean

    def act(self, action, world):
        """
        Action: ((dx, dy), Boolean)
        The action we need to make
        """
        self.move(action[0][0], action[0][1])
        if action[1]:
            self.place_bomb()

        return world.scores[self.name], State(world, (self.x, self.y), self.name)
