import pygame
import sys
import time
import random
import math
import gym
import numpy as np
import tflearn.layers.core import input_layer, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean, median
from collections import Counter

LR = 1e-3
goal_steps = 300
score_requirement = 50
initial_games = 5000
