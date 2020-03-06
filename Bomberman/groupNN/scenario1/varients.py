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

run_num = 100


#############
# VARIANT 1 #
#############

# Create the game
g1 = Game.fromfile('map.txt')

# Uncomment this if you want the test character
g1.add_character(TestCharacter("me",  # name
                               "C",  # avatar
                               0, 0  # position
                               ))

g1.go(1)

#############
# VARIANT 2 #
#############

for i in range(0, run_num):
    # Create the game
    g2 = Game.fromfile('map.txt')

    g2.add_character(TestCharacter("me",  # name
                                   "C",  # avatar
                                   0, 0  # position
                                   ))

    random.seed(time.time())
    g2 = Game.fromfile('map.txt')
    g2.add_monster(StupidMonster("stupid",  # name
                                 "S",  # avatar
                                 3, 9  # position
                                 ))

    g2.go(1)

#############
# VARIANT 3 #
#############

for i in range(0, run_num):
    # Create the game
    random.seed(time.time())
    g3 = Game.fromfile('map.txt')
    g3.add_monster(SelfPreservingMonster("selfpreserving",  # name
                                         "S",  # avatar
                                         3, 9,  # position
                                         1  # detection range
                                         ))

    g3.add_character(TestCharacter("me",  # name
                                   "C",  # avatar
                                   0, 0  # position
                                   ))

    # Run!
    g3.go(1)

#############
# VARIANT 4 #
#############

for i in range(0, run_num):
    # Create the game
    random.seed(time.time())
    g4 = Game.fromfile('map.txt')
    g4.add_monster(SelfPreservingMonster("aggressive",  # name
                                         "A",  # avatar
                                         3, 13,  # position
                                         2  # detection range
                                         ))

    g4.add_character(TestCharacter("me",  # name
                                   "C",  # avatar
                                   0, 0  # position
                                   ))

    # Run!
    g4.go(1)

#############
# VARIANT 5 #
#############

for i in range(0, run_num):
    # Create the game
    random.seed(time.time())
    g5 = Game.fromfile('map.txt')
    g5.add_monster(StupidMonster("stupid",  # name
                                 "S",  # avatar
                                 3, 5,  # position
                                 ))
    g5.add_monster(SelfPreservingMonster("aggressive",  # name
                                         "A",  # avatar
                                         3, 13,  # position
                                         2  # detection range
                                         ))

    g5.add_character(TestCharacter("me",  # name
                                   "C",  # avatar
                                   0, 0  # position
                                   ))

    # Run!
    g5.go(1)
