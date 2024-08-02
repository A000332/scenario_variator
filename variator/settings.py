import numpy as np

width = [3.0, 3.5] # width of all roads

max_speed = [40] # max speed of all roads (kph)

num_lane_left = np.arange(1, 3) # number of left lanes
num_lane_right = np.arange(1, 3) # number of right lanes

start_road_grad = np.linspace(-0.1, 0.1, 3) # longitudinal gradient of start road
start_road_cant = np.linspace(-0.01, 0.01, 3) # lateral gradient of start road

is_clothoid = True # True:clothoid road  False:straight road

spiral_length = np.linspace(50, 60, 2) # length of spiral road
curv = [0.01, 0.02] # curvature of the end of spiral road (equals to the start of arc road)

third_road_height = np.linspace(0, 10, 2) # start height of third(arc) road
third_road_grad = np.linspace(-0.1, 0.1, 3) # longitudinal gradient of third(arc) road
third_road_cant = np.linspace(-0.01, 0.01, 3) # lateral gradient of third(arc) road