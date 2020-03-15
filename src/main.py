import pandas
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from lib.env import World

def main():
    env = World(10, 10, 0.2)
    env.display()

    env.w

if __name__ == "__main__":
    main()