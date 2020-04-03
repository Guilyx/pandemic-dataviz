import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')  # Change backend ( segfault issue )
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import sys
from os import system
import time
import random
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from lib.state import State
from lib.pandemic import Pandemic
from lib.env import World

class DataViz():
    def __init__(self, Pandemic):
        self.pandemic = Pandemic
    
    def plotStackChart(self):
        pass

    def plotLines(self):
        pass

    def plotPieChart(self):
        pass
