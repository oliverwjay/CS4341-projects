import math


class State:
    def __init__(self, world, loc, name):
        self.x, self.y = loc
        self.name = name
        self.world = world
        mo_dist, mo_dir = self.dist_and_dir_to_closest_monster()
        self.dir_closest_monster = mo_dir
        self.dist_closest_monster = min(4, mo_dist)
        self.dir_a_star = self.next_a_star_move()
        self.bomb_placed = self.have_placed_our_bomb()
        self.valid_moves = self.valid_moves((self.x, self.y))

    def have_placed_our_bomb(self):
        """
        This function checks if we have placed our bomb
        """
        arr = self.world.bombs.values()
        lis = list(arr)
        if len(lis) > 0:
            for i in range(0, len(lis)):
                if self.name == lis[i].owner.name:
                    return True
        else:
            return False

    def find_bomb_time_at_location(self, loc):
        """
        Finds a bomb at the given location
        """
        arr = self.world.bombs.values()
        lis = list(arr)
        if len(lis) > 0:
            for i in range(0, len(lis)):
                if loc[0] == lis[i].x and loc[1] == lis[i].y:
                    return lis[i].timer

    def locate_monsters(self):
        """
        This function will find where the monsters are and how many there are
        """
        count = 0
        location = []
        arr = self.world.monsters.values()
        lis = list(arr)
        if len(lis) > 0:
            for i in range(0, len(lis)):
                location.append((lis[i][i].x, lis[i][i].y))
                count = count + 1
        return location, count

    def locate_characters(self):
        """
        Locates all characters in the world and how many there are
        """
        count = 0
        location = []
        arr = self.world.characters.values()
        lis = list(arr)
        if len(lis) > 0:
            for i in range(0, len(lis)):
                location.append((lis[i][i].x, lis[i][i].y))
                count = count + 1

        return location, count

    def isBombHorOrVert(self):
        """
        Determines if a bomb is horizontal or vertical to our character with the explosion range
        value that was initialized
        """

        # Check above the player
        if (self.y - self.world.expl_range + 1) >= 0:
            for y in range(self.y, self.y - self.world.expl_range + 1):
                if self.world.bomb_at(self.x, y) is not None:
                    return True
        else:
            for y in range(0, self.y):
                if self.world.bomb_at(self.x, y) is not None:
                    return True

        # Check below the player
        if (self.y + self.world.expl_range + 1) <= self.world.height():
            for y in range(self.y, self.y + self.world.expl_range + 1):
                if self.world.bomb_at(self.x, y) is not None:
                    return True
        else:
            for y in range(self.y, self.world.height()):
                if self.world.bomb_at(self.x, y) is not None:
                    return True

        # Check to the right of the player
        if (self.x + self.world.expl_range + 1) <= self.world.width():
            for x in range(self.x, self.x + self.world.expl_range + 1):
                if self.world.bomb_at(x, self.y) is not None:
                    return True
        else:
            for x in range(self.x, self.world.width()):
                if self.world.bomb_at(x, self.y) is not None:
                    return True

        # Check to the left of the player
        if (self.x - self.world.expl_range + 1) >= 0:
            print("Not near left wall")
            for x in range(self.x - self.world.expl_range, self.x):
                if self.world.bomb_at(x, self.y) is not None:
                    return True
        else:
            for x in range(0, self.x):
                if self.world.bomb_at(x, self.y) is not None:
                    return True
        return False

    def isBombHorOrVertFromLoc(self, loc):
        """
        Determines if a bomb is horizontal or vertical to our character with the explosion range
        value that was initialized
        """

        # Check above the player
        if (loc[1] - self.world.expl_range + 1) >= 0:
            for y in range(loc[1], loc[1] - self.world.expl_range + 1):
                if self.world.bomb_at(loc[0], y) is not None:
                    return True, (loc[0], y)
        else:
            for y in range(0, loc[1]):
                if self.world.bomb_at(loc[0], y) is not None:
                    return True, (loc[0], y)

        # Check below the player
        if (loc[1] + self.world.expl_range + 1) <= self.world.height():
            for y in range(loc[1], loc[1] + self.world.expl_range + 1):
                if self.world.bomb_at(loc[0], y) is not None:
                    return True, (loc[0], y)
        else:
            for y in range(loc[1], self.world.height()):
                if self.world.bomb_at(loc[0], y) is not None:
                    return True, (loc[0], y)

        # Check to the right of the player
        if (loc[0] + self.world.expl_range + 1) <= self.world.width():
            for x in range(loc[0], loc[0] + self.world.expl_range + 1):
                if self.world.bomb_at(x, loc[1]) is not None:
                    return True, (x, loc[1])
        else:
            for x in range(loc[0], self.world.width()):
                if self.world.bomb_at(x, loc[1]) is not None:
                    return True, (x, loc[1])

        # Check to the left of the player
        if (loc[0] - self.world.expl_range + 1) >= 0:
            print("Not near left wall")
            for x in range(loc[0] - self.world.expl_range, loc[0]):
                if self.world.bomb_at(x, loc[1]) is not None:
                    return True, (x, loc[1])
        else:
            for x in range(0, loc[0]):
                if self.world.bomb_at(x, loc[1]) is not None:
                    return True, (x, loc[1])
        return False, None

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

    def get_neighbors(self, loc):
        """
        returns the legal neighbors of the point given
        :param loc: location (tuple)
        :return: all valid neighbors (List of Tuples)
        """
        connected = [(x, y) for x in range(loc[0] - 1, loc[0] + 2) for y in range(loc[1] - 1, loc[1] + 2) if
                     (x, y) != (0, 0)]
        return [neighbor for neighbor in connected if self.is_valid_loc(neighbor)]

    def is_valid_loc(self, loc):
        """
        Takes a point and checks if it is a valid location
        """
        if (0 <= loc[0] < self.world.width()) and (0 <= loc[1] < self.world.height()):
            if self.world.empty_at(loc[0], loc[1]) or self.world.exit_at(loc[0], loc[1]):
                return True
        else:
            return False

    def is_in_bounds(self, loc):
        """
        Checks if a location is in bounds
        """
        in_bounds = (0 <= loc[0] < self.world.width()) and (0 <= loc[1] < self.world.height())
        return in_bounds

    def valid_moves(self, loc):
        """
        Returns all of the valid moves our character can make
        """
        connected = [(x, y) for x in range(loc[0] - 1, loc[0] + 2) for y in range(loc[1] - 1, loc[1] + 2) if
                     (x, y) != (0, 0)]
        arr = []

        for neighbor in connected:
            if self.is_in_bounds(neighbor) and self.world.empty_at(neighbor[0], neighbor[1]):
                is_bomb, loc = self.isBombHorOrVertFromLoc(neighbor)
                # Get Bomb Time
                if loc is not None:
                    time = self.find_bomb_time_at_location(loc)
                    if is_bomb and time is not 0:
                        arr.append(neighbor)
                else:
                    arr.append(neighbor)

        return arr

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

    def AStarSearch(self, start, end):
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
            for neighbour in self.get_neighbors(current):
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

    def can_a_star_complete(self):
        """
        Checks if A star can get to goal
        """
        path, cost = self.AStarSearch((self.x, self.y), self.world.exitcell)
        return path is not None and cost is not None

    def next_a_star_move(self):
        """
        Gets the next A Star move: in a tuple of dx, dy
        """
        nxt_move = self.x, self.y
        if self.can_a_star_complete():
            path, cost = self.AStarSearch((self.x, self.y), self.world.exitcell)
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

    def dist_and_dir_to_closest_monster(self):
        # Find all the monsters in the world
        location, count = self.locate_monsters()
        smallest_dist = self.world.height() * self.world.width()
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
        elif x_diff < 0 < y_diff:
            direction = 3
        # Cell 2 is to the lower left diagonal of Cell 1
        elif y_diff < 0 < x_diff:
            direction = 6
        # Cell 2 is to the lower right diagonal of Cell 1
        elif y_diff < 0 and x_diff < 0:
            direction = 8
        # Something blew up cause this should never happen
        else:
            direction = -1
        return direction

    def as_tuple(self):
        state_hash = (
            self.dir_closest_monster,
            self.dist_closest_monster,
            self.dir_a_star,
            self.bomb_placed,
            self.valid_moves
        )
        return state_hash

    def __hash__(self):
        # TODO: Hash object
        print(str(self.as_tuple()))
        return hash(str(self.as_tuple()))
