# This is necessary to find the main code
import sys
import random
import time

sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game
from monsters.stupid_monster import StupidMonster
from monsters.selfpreserving_monster import SelfPreservingMonster

# This is your code!
sys.path.insert(1, '../groupNN')

# Uncomment this if you want the empty test character
from testcharacter import TestCharacter


def run_variant(variant, scenario=1, t=1):
    # Find map
    scene = 'map.txt'
    if scenario == 2:
        scene = '../scenario2/map.txt'

    # Build game
    g = Game.fromfile(scene)

    # Randomize seed
    random.seed(time.time())

    # Randomize character
    g.add_character(TestCharacter("me",  # name
                                   "C",  # avatar
                                   0, 0  # position
                                   ))

    # Add monsters
    if variant == 2 or variant == 5:
        g.add_monster(StupidMonster("stupid",  # name
                                     "S",  # avatar
                                     3, 9  # position
                                     ))
    elif variant == 3:
        g.add_monster(SelfPreservingMonster("selfpreserving",  # name
                                             "S",  # avatar
                                             3, 9,  # position
                                             1  # detection range
                                             ))
    if variant >= 4:
        g.add_monster(SelfPreservingMonster("aggressive",  # name
                                         "A",  # avatar
                                         3, 13,  # position
                                         2  # detection range
                                         ))
    g.go(t)
    return g.world.scores['me']


n_runs = 5
enabled_variants = [4]
enabled_scenarios = [1]
scores = []
for i in range(n_runs):
    for variant in enabled_variants:
        for scenario in enabled_scenarios:
            scores.append(run_variant(variant, scenario))
print(scores)
