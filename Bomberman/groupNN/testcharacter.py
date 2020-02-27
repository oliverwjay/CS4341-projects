# This is necessary to find the main code
import math
import sys

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back


class TestCharacter(CharacterEntity):
    def __init__(self, name, avatar, x, y):
        CharacterEntity.__init__(self, name, avatar, x, y)
        self.exit_x = None
        self.exit_y = None
        self.w = None
        self.h = None
        self.expl_range = None

    def do(self, wrld):
        """
        Our Code
        """
        # Save world height and width
        if self.w is None or self.h is None or self.expl_range is None:
            self.w = wrld.width()
            self.h = wrld.height()
            self.expl_range = wrld.expl_range

        # Find Exit location
        if self.exit_x is None or self.exit_y is None:
            self.find_exit(wrld)

        # print(self.x, self.y)
        # print(self.euclidean_distance(self.exit_x, self.exit_y, self.x, self.y))
        # print(self.manhattan_distance(self.exit_x, self.exit_y, self.x, self.y))
        print("WE ARE HERE:")
        print(self.x, self.y)
        print("Is there a bomb above or below us:")
        print(self.isBombHorOrVert(wrld))
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

    def find_exit(self, wrld):
        """
        This function will find where the exit is on the board and store it
        """
        for x in range(0, self.w):
            for y in range(0, self.h):
                if wrld.exit_at(x, y):
                    self.exit_x = x
                    self.exit_y = y
                    print("Found Exit at")
                    print(x, y)

    def isBombHorOrVert(self, wrld):
        """
        Determines if a bomb is horizontal or vertical to our character with the explosion range
        value that was initialized
        """

        # Check above the player
        if (self.y - self.expl_range + 1) >= 0:
            for y in range(self.y, self.y - self.expl_range + 1):
                if wrld.bomb_at(self.x, y) is not None:
                    return True
        else:
            for y in range(0, self.y):
                if wrld.bomb_at(self.x, y) is not None:
                    return True

        # Check below the player
        if (self.y + self.expl_range + 1) <= self.h:
            for y in range(self.y, self.y + self.expl_range + 1):
                if wrld.bomb_at(self.x, y) is not None:
                    return True
        else:
            for y in range(self.y, self.h):
                if wrld.bomb_at(self.x, y) is not None:
                    return True

        # Check to the right of the player
        if (self.x + self.expl_range + 1) <= self.w:
            for x in range(self.x, self.x + self.expl_range + 1):
                if wrld.bomb_at(x, self.y) is not None:
                    return True
        else:
            for x in range(self.x, self.w):
                if wrld.bomb_at(x, self.y) is not None:
                    return True

        # Check to the left of the player
        if (self.x - self.expl_range + 1) >= 0:
            print("Not near left wall")
            for x in range(self.x - self.expl_range, self.x):
                if wrld.bomb_at(x, self.y) is not None:
                    return True
        else:
            for x in range(0, self.x):
                if wrld.bomb_at(x, self.y) is not None:
                    return True
        return False

    @staticmethod
    def euclidean_distance(x1, y1, x2, y2):
        """
        Calculates the euclidean distance between two points
        """
        dist = math.sqrt(math.pow(x2 - x1, 2) + (math.pow(y2 - y1, 2)))
        return dist

    @staticmethod
    def manhattan_distance(x1, y1, x2, y2):
        """
        Calculates manhattan distance between two points
        """
        dist = abs((x2 - x1) + (y2 - y1))
        return dist
