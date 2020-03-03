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
        # Save world height and width (done once)
        if self.w is None or self.h is None or self.expl_range is None:
            self.w = wrld.width()
            self.h = wrld.height()
            self.expl_range = wrld.expl_range

        # Find Exit location (done once)
        if self.exit_x is None or self.exit_y is None:
            self.find_exit(wrld)

        # Find where the monsters are
        closest_mon = self.dist_and_dir_to_closest_monster(wrld)
        monster_dist = closest_mon[0]  # 1-4
        monster_dir = closest_mon[1]  # 1-8
        # Find where other characters are

        # Run A Star

        #

        # print(self.a_star(wrld))
        # print(self.locate_characters(wrld))

        # Commands
        dx, dy = self.next_a_star_move(wrld)
        bomb = False
        # Handle input
        # for c in input("How would you like to move (w=up,a=left,s=down,d=right,b=bomb)? "):
        #     if 'w' == c:
        #         dy -= 1
        #     if 'a' == c:
        #         dx -= 1
        #     if 's' == c:
        #         dy += 1
        #     if 'd' == c:
        #         dx += 1
        #     if 'b' == c:
        #         bomb = True
        # Execute commands
        self.move(dx, dy)
        if bomb:
            self.place_bomb()

        pass

    def have_placed_our_bomb(self, wrld):
        """
        This function checks if we have placed our bomb
        """
        arr = wrld.bombs.values()
        lis = list(arr)
        if len(lis) > 0:
            for i in range(0, len(lis)):
                if self.name == lis[i].owner.name:
                    return True
        else:
            return False

    def locate_monsters(self, wrld):
        """
        This function will find where the monsters are and how many there are
        """
        count = 0
        location = []
        arr = wrld.monsters.values()
        lis = list(arr)
        if len(lis) > 0:
            for i in range(0, len(lis)):
                location.append((lis[i][i].x, lis[i][i].y))
                count = count + 1

        return location, count

    def locate_characters(self, wrld):
        """
        Locates all characters in the world and how many there are
        """
        count = 0
        location = []
        arr = wrld.characters.values()
        lis = list(arr)
        if len(lis) > 0:
            for i in range(0, len(lis)):
                location.append((lis[i][i].x, lis[i][i].y))
                count = count + 1

        return location, count

    def find_exit(self, wrld):
        """
        This function will find where the exit is on the board and store it
        """
        arr = wrld.exitcell
        self.exit_x = arr[0]
        self.exit_y = arr[1]

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

    def get_neighbors(self, loc, wrld):
        """
        returns the legal neighbors of the point given
        :param loc: location (tuple)
        :param wrld: the world
        :return: all valid neighbors (List of Tuples)
        """
        #  tl t tr
        #  l  X  r
        #  bl b br

        # Get all neighbors
        top_left = (loc[0] - 1, loc[1] - 1)
        top = (loc[0], loc[1] - 1)
        top_right = (loc[0] + 1, loc[1] - 1)
        left = (loc[0] - 1, loc[1])
        right = (loc[0] + 1, loc[1])
        bottom_left = (loc[0] - 1, loc[1] + 1)
        bottom = (loc[0], loc[1] + 1)
        bottom_right = (loc[0] + 1, loc[1] + 1)

        ans = list()

        if self.is_valid_loc(top_left, wrld):
            ans.append(top_left)
        if self.is_valid_loc(top, wrld):
            ans.append(top)
        if self.is_valid_loc(top_right, wrld):
            ans.append(top_right)
        if self.is_valid_loc(left, wrld):
            ans.append(left)
        if self.is_valid_loc(right, wrld):
            ans.append(right)
        if self.is_valid_loc(bottom_left, wrld):
            ans.append(bottom_left)
        if self.is_valid_loc(bottom, wrld):
            ans.append(bottom)
        if self.is_valid_loc(bottom_right, wrld):
            ans.append(bottom_right)

        return ans

    def is_valid_loc(self, loc, wrld):
        """
        Takes a point and checks if it is a valid location
        """
        if (0 <= loc[0] < self.w) and (0 <= loc[1] < self.h):
            if wrld.empty_at(loc[0], loc[1]) or wrld.exit_at(loc[0], loc[1]):
                return True
        else:
            return False

    @staticmethod
    def euclidean_heuristic(point1, point2):
        """
        calculate the dist between two points
        :param point1: tuple of location
        :param point2: tuple of location
        :return: dist between two points
        """
        # Distance Formula
        euclid = math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

        # return value
        return euclid

    @staticmethod
    def move_cost(current, next_point):
        """
        calculate the dist between two points
        :param current: tuple of location
        :param next_point: tuple of location
        :return: dist between two points
        """
        # parse x and y positions from the tuples
        current_x = current[0]
        current_y = current[1]
        next_x = next_point[0]
        next_y = next_point[1]

        # calculate the distance between point in x and y direction
        x_dist = abs(next_x - current_x)
        y_dist = abs(next_y - current_y)

        # add the differences in x and y for the total cost
        move_cost = x_dist + y_dist

        # return move cost
        return move_cost

    def AStarSearch(self, start, end, wrld):
        """
        https://rosettacode.org/wiki/A*_search_algorithm#Python
        """
        G = {}  # Actual movement cost to each position from the start position
        F = {}  # Estimated movement cost of start to end going via this position

        # Initialize starting values
        G[start] = 0
        F[start] = self.euclidean_heuristic(start, end)

        closedVertices = set()
        openVertices = set([start])
        cameFrom = {}

        while len(openVertices) > 0:
            # Get the vertex in the open list with the lowest F score
            current = None
            currentFscore = None
            for pos in openVertices:
                if current is None or F[pos] < currentFscore:
                    currentFscore = F[pos]
                    current = pos

            # Check if we have reached the goal
            if current == end:
                # Retrace our route backward
                path = [current]
                while current in cameFrom:
                    current = cameFrom[current]
                    path.append(current)
                path.reverse()
                return path, F[end]  # Done!

            # Mark the current vertex as closed
            openVertices.remove(current)
            closedVertices.add(current)

            # Update scores for vertices near the current position
            for neighbour in self.get_neighbors(current, wrld):
                if neighbour in closedVertices:
                    continue  # We have already processed this node exhaustively
                candidateG = G[current] + self.move_cost(current, neighbour)

                if neighbour not in openVertices:
                    openVertices.add(neighbour)  # Discovered a new vertex
                elif candidateG >= G[neighbour]:
                    continue  # This G score is worse than previously found

                # Adopt this G score
                cameFrom[neighbour] = current
                G[neighbour] = candidateG
                H = self.euclidean_heuristic(neighbour, end)
                F[neighbour] = G[neighbour] + H

        return None, None

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

    def can_a_star_complete(self, wrld):
        """
        Checks if A star can get to goal
        """
        path, cost = self.AStarSearch((self.x, self.y), (self.exit_x, self.exit_y), wrld)
        return path is not None and cost is not None

    def next_a_star_move(self, wrld):
        """
        Gets the next A Star move: in a tuple of dx, dy
        """
        nxt_move = self.x, self.y
        if self.can_a_star_complete(wrld):
            path, cost = self.AStarSearch((self.x, self.y), (self.exit_x, self.exit_y), wrld)
            nxt_move = path[1]

        dx = nxt_move[0] - self.x
        dy = nxt_move[1] - self.y

        return dx, dy

    def normalize_dist(self, value, wrld):
        height = wrld.height()
        width = wrld.width()
        max_dist = math.sqrt(math.pow(height, 2) + math.pow(width, 2))
        # normalized = (values - min(values)) / (max(values) - min(values))
        normalized = value / max_dist
        return normalized

    def layer_dist(self, x1, y1, x2, y2):
        """
        Gets the distance between to points in a propagating wave away from the first point
        :param x1:
        :param y1:
        :param x2:
        :param y2:
        :return:
        """
        # e_dist = self.euclidean_distance(x1, y1, x2, y2)
        # layer_dist = math.floor(e_dist)
        x_dist = abs(x1 - x2)
        y_dist = abs(y1 - y2)
        layer_dist = 0
        if y_dist > x_dist:
            layer_dist = y_dist
        elif x_dist > y_dist:
            layer_dist = x_dist
        elif x_dist == y_dist:
            layer_dist = y_dist
        return layer_dist

    def dist_and_dir_to_closest_monster(self, wrld):
        # Find all the monsters in the world
        location, count = self.locate_monsters(wrld)
        smallest_dist = self.h * self.w
        direction = -1
        for monster_loc in location:
            dist_to_mon = self.layer_dist(self.x, self.y, monster_loc[0], monster_loc[1])
            if dist_to_mon < smallest_dist:
                smallest_dist = dist_to_mon
                direction = self.dir_between_cells(self.x, self.y, monster_loc[0], monster_loc[1])
        if smallest_dist > 4:
            smallest_dist = 4  # If the monster is too far away, consider the distance as the character's max vision
        print(smallest_dist)
        print(direction)
        return smallest_dist, direction

    @staticmethod
    def dir_between_cells(x1, y1, x2, y2):
        x_diff = x1 - x2
        y_diff = y1 - y2
        direction = -1
        # Cells are in the same column
        if x_diff == 0:
            if y_diff > 0:
                direction = 2  # Cell 2 is above Cell 1
            elif y_diff < 0:
                direction = 7  # Cell 2 is below Cell 1
            else:
                direction = 0  # Cells are on top of each other
        #  Cells are in the same row
        elif y_diff == 0:
            if x_diff > 0:
                direction = 4  # Cell 2 is to the left of Cell 1
            elif x_diff < 0:
                direction = 5  # Cell 2 is to the right of Cell 1
            else:
                direction = 0  # Cells are on top of each other
        #  Cell 2 is to the upper left diagonal of Cell 1
        elif y_diff > 0 and x_diff > 0:
            direction = 1
        #  Cell 2 is to the upper right diagonal of Cell 1
        elif x_diff < 0 and y_diff > 0:
            direction = 3
        # Cell 2 is to the lower left diagonal of Cell 1
        elif y_diff < 0 and x_diff > 0:
            direction = 6
        # Cell 2 is to the lower right diagonal of Cell 1
        elif y_diff < 0 and x_diff < 0:
            direction = 8
        # Something blew up cause this should never happen
        else:
            direction = -1
        return direction
