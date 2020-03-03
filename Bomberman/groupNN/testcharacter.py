# This is necessary to find the main code
import math
import sys
from state import State

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
        # Save world height and width (done once)
        # if self.w is None or self.h is None or self.expl_range is None:
        #     self.w = wrld.width()
        #     self.h = wrld.height()
        #     self.expl_range = wrld.expl_range
        #
        # # Find where the monsters are
        # closest_mon = self.dist_and_dir_to_closest_monster(wrld)
        # monster_dist = closest_mon[0]  # 1-4
        # monster_dir = closest_mon[1]  # 1-8
        # # Find where other characters are

        # Creation of State
        state = State(wrld, (self.x, self.y), self.name)
        print(state.as_tuple(), hash(state))

        # Commands
        dx, dy = 0, 0  # self.next_a_star_move(wrld)
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

    # def a_star(self, wrld):
    #     """
    #     Handles A* search
    #     """
    #     path, cost = self.AStarSearch((self.x, self.y), (self.exit_x - 1, self.exit_y - 1), wrld)
    #     path.append((self.exit_x, self.exit_y))
    #     cost = cost + 1
    #     return path, cost

    # def a_star_dist_to_exit(self, wrld):
    #     """
    #     Distance to exit by path
    #     """
    #     path, cost = self.a_star(wrld)
    #     return cost

