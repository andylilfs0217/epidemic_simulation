from enum import Enum


class SystemMode(Enum):
    CONSOLE = 0
    FILE = 1
    BOTH = 2


# Set random behavior
IS_FIX_RAND = True
# IS_FIX_RAND = False
RAND_SEED = 871264823

# Set output mode
# PRINT_MODE = SystemMode.CONSOLE
PRINT_MODE = SystemMode.FILE
# PRINT_MODE = SystemMode.BOTH

SHOW_DETAIL_LOG = True
# SHOW_DETAIL_LOG = False

# Set attribute of different parameters
# Meaning for simulating different times with different params
# [
# Initial setup,
# Double infection prop,
# x3 infection prop,
# half infection prop
# lengthen inf period
# shorten inf period
# lengthen rec period
# shorten rec period
# increase init inf
# much increase init inf
# ]
# The infection probability of each node in range[0,1]
INFECTION_PROP = [0.05, 0.025, 0.075, 0.05, 0.05, 0.05, 0.05]
# The period of infectious of each node in range[1,TURNS]
INFECTIOUS_PERIOD = [3, 3, 3, 1, 5, 3, 3]
# The recovery period of each node in range[1,TURNS]
RECOVERY_PERIOD = [7, 7, 7, 7, 7, 3, 10]
# The initial number of infected nodes in range[1,#nodes]
INIT_INFECTED = [1, 1, 1, 1, 1, 1, 1]
# Number of steps for each epoch running a model once in range[1,infinity]
STEPS = [300, 300, 300, 300, 300, 300, 300]
# Number of times running a model in range[1,infinity]
EPOCHS = [10, 10, 10, 10, 10, 10, 10]

# # The infection probability of each node in range[0,1]
# INFECTION_PROP = [0.05]
# # The period of infectious of each node in range[1,TURNS]
# INFECTIOUS_PERIOD = [3]
# # The recovery period of each node in range[1,TURNS]
# RECOVERY_PERIOD = [7]
# # The initial number of infected nodes in range[1,#nodes]
# INIT_INFECTED = [1]
# # Number of steps for each epoch running a model once in range[1,infinity]
# STEPS = [300]
# # Number of times running a model in range[1,infinity]
# EPOCHS = [10]
