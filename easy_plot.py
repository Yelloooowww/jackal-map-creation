import random
import datetime
import Queue
import math
import matplotlib.pyplot as plt
import Tkinter as tk
import numpy as np
from world_writer import WorldWriter
from difficulty_quant import DifficultyMetrics
from pgm_writer import PGMWriter
from yaml_writer import YamlWriter
from gen_world_ca import JackalMap

load_obstacle_map = np.load("train_env_map_bit.npy")
shape = load_obstacle_map.shape
print("map size",shape)
obstacle_map = [[0 for i in range(30)] for j in range(30)]
total_obstacle_map = [[0 for i in range(shape[1])] for j in range(shape[0])]
total_jackal_map = [[0 for i in range(shape[1])] for j in range(shape[0])]
total_closest_wall = [[0 for i in range(shape[1])] for j in range(shape[0])]
total_avg_visibility = [[0 for i in range(shape[1])] for j in range(shape[0])]
total_dispersion = [[0 for i in range(shape[1])] for j in range(shape[0])]
total_characteristic_dimension = [[0 for i in range(shape[1])] for j in range(shape[0])]


for index_i in range(0,shape[0],30):
    for index_j in range(0,shape[1],30):

        for i in range(30):
            for j in range(30):
                if index_i+i<shape[0] and index_j+j<shape[1]:
                    obstacle_map[i][j] = load_obstacle_map[index_i+i][index_j+j]
                else:
                    obstacle_map[i][j] = 1
                obstacle_map[i][j] = 1 if obstacle_map[i][j]==0 else 0

        jmap_gen = JackalMap(obstacle_map, 5)
        print(index_i,index_j)
        jackal_map = jmap_gen.get_map()
        diff = DifficultyMetrics(obstacle_map, [], disp_radius=1)
        closest_wall = diff.closest_wall()
        avg_visibility = diff.avg_visibility()
        dispersion = diff.dispersion()
        characteristic_dimension = diff.characteristic_dimension()

        for i in range(30):
            for j in range(30):
                if index_i+i<shape[0] and index_j+j<shape[1]:
                    total_obstacle_map[index_i+i][index_j+j] = obstacle_map[i][j]
                    total_jackal_map[index_i+i][index_j+j] = jackal_map[i][j]
                    total_closest_wall[index_i+i][index_j+j] = closest_wall[i][j]
                    total_avg_visibility[index_i+i][index_j+j] = avg_visibility[i][j]
                    total_dispersion[index_i+i][index_j+j] = dispersion[i][j]
                    total_characteristic_dimension[index_i+i][index_j+j] = characteristic_dimension[i][j]

str_list = ["obstacle_map",\
            "jackal_map",\
            "closest_wall",\
            "avg_visibility",\
            "dispersion",\
            "characteristic_dimension"]
cmap_list = ["binary","Greys","RdYlGn","RdYlGn","RdYlGn","Greys"]
for i,item in enumerate([total_obstacle_map,total_jackal_map,total_closest_wall,total_avg_visibility,total_dispersion,total_characteristic_dimension]):
    fig, ax = plt.subplots()
    barrr = ax.imshow(item,cmap=cmap_list[i], interpolation='nearest')
    ax.set_title(str_list[i])
    fig.colorbar(barrr, ax=ax, orientation='horizontal')
    fig.savefig("train_env_"+str_list[i]+".png")
