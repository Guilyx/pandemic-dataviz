# -*- coding: utf-8 -*-

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from lib.env import World
from lib.node import Node, State

def test_uniqueness():
    env = World(10, 10, 0.2)
    free_tiles = env.list_available_tiles()
    nodes = [Node(State.HEALTHY, i) for i in free_tiles]

    # list of positions
    pos = []
    for elem in nodes:
        pos.append(elem.position)

    # check uniqueness
    seen = set()
    uniqueness = not any(k in seen or seen.add(k) for k in pos)

    assert(uniqueness == True)

def test_outofbounds():
    env = World(10, 10, 0.2)
    free_tiles = env.list_available_tiles()
    new_node = [Node(State.HEALTHY, i) for i in free_tiles]

    for elem in new_node:
        assert(elem.position >= 0 and elem.position <= (env.L*env.H))

def test_availability():
    env = World(10, 10, 0.2)
    free_tiles = env.list_available_tiles()

    new_node = [Node(State.HEALTHY, i) for i in free_tiles]

    for elem in new_node:
        assert(env.w[elem.position] != State.WALL)