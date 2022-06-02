import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt

pc = o3d.io.read_point_cloud('train_env.ply')
points_array = np.asarray((pc.points))

map_height, map_width = 120, 120
map = np.zeros((map_height, map_width))
origin_x, origin_y = -25, -25
resolution = 0.6
for i in range(len(points_array)):
    if points_array[i][2] < 0.2 : continue
    # if points_array[i][2] > 0.6   : continue

    c = int((points_array[i][0] - origin_x)/resolution)
    r = int((points_array[i][1] - origin_y)/resolution)

    if c >= map_height or c < 0 : continue
    if r >= map_width or r < 0 : continue

    map[r][c] += 1

# print(map)
map_bit = map
for c in range(map_height):
    for r in range(map_width):
        map_bit[r][c] = 0 if map[r][c] > 25 else 1

print(map_bit)
np.save('train_env_map_bit.npy', map_bit)
plt.imshow(map_bit)
plt.colorbar()
plt.show()
