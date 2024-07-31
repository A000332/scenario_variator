import numpy as np

# width = [2.5, 3.0, 3.5]
width = np.linspace(2.5, 3.5, 3)
# width = np.arange(2.5, 3.6, 0.5)

num_lane_left = np.arange(1, 4)
num_lane_right = np.arange(1, 4)

start_road_grad = np.linspace(-0.1, 0.1, 3)
start_road_cant = np.linspace(-0.01, 0.01, 3)

is_clothoid = True

mig_interval = np.linspace(40, 60, 3)
curv = np.linspace(0.01, 0.03, 3)
