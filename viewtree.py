from mpl_toolkits.mplot3d import Axes3D

import re
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# change the path if the coords file is not in the same directory
coordfilename = "coords.txt"

fin = open(coordfilename, 'r')
coords_raw = fin.readlines()

coords_bits = [i.split(",") for i in coords_raw]

coords = []

for slab in coords_bits:
    new_coord = []
    for i in slab:
        new_coord.append(int(re.sub(r'[^-\d]', '', i)))
    coords.append(new_coord)

for triplet in coords:
    ax.scatter(triplet[0], triplet[1], triplet[2], marker='^')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()
