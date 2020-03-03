class State:
    def __init__(self, world):
        # TODO: Compute these
        self.dir_closest_monster = None
        self.dir_a_star = None
        self.bomb_placed = None
        self.valid_moves = None
        self.path_blocked = None

    def __hash__(self):
        # TODO: Hash object
        return ""
