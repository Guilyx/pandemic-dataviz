# -*- coding: utf-8 -*-

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from lib.env import World
from lib.node import Node, State
import random

def test_position_validity():
    for i in range(1000):
        rdn = random.random()
        if rdn > 0.5:
            pos = -1*(random.randint(1, 1000))
            node = Node(State.DEAD, pos)
            assert(node.valid_node == False)
        else:
            pos = random.randint(1, 1000)
            node = Node(State.DEAD, pos)
            assert(node.valid_node == True)

def test_state_validity():
    for i in range(1000):
        rdn = random.random()
        if rdn > 0.5:
            state = random.choice(State.ALLOWED_)
            node = Node(state, 0)
            assert(node.valid_node == True)
        else:
            state = random.randint(-1000, 1000)
            if state in State.ALLOWED_:
                pass
            else:
                node = Node(state, 0)
                assert(node.valid_node == False)