import math
import sys
import os
import meep as mp
import matplotlib.pyplot as plt
from meep import mpb

num_bands = 10
interp = 19

# honeycomb:
k_points = [
            mp.Vector3(0,0)
            ] 

k_points = mp.interpolate(interp, k_points)

# argv[1]: radius of airhole
# argv[2]: radius of center
# argv[3]: n_back
# argv[4]: n_cen
# argv[5]: resolution

resolution = int(sys.argv[5])

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!amorphous!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

r_air = 0.001*int(sys.argv[1])
r_cen = 0.001*int(sys.argv[2])

vertices = [mp.Vector3(     4/3*r_air, 2/3*r_air),
            mp.Vector3(     2/3*r_air,-2/3*r_air),
            mp.Vector3(    -2/3*r_air,-4/3*r_air),
            mp.Vector3(    -4/3*r_air,-2/3*r_air),
            mp.Vector3(    -2/3*r_air, 2/3*r_air),
            mp.Vector3(     2/3*r_air, 4/3*r_air)]

vertices_cen = [mp.Vector3(     4/3*r_air, 2/3*r_air),
            mp.Vector3(     2/3*r_air,-2/3*r_air),
            mp.Vector3(    -2/3*r_air,-4/3*r_air),
            mp.Vector3(    -4/3*r_air,-2/3*r_air),
            mp.Vector3(    -2/3*r_air, 2/3*r_air),
            mp.Vector3(     2/3*r_air, 4/3*r_air)]

geometry = [mp.Prism(vertices, center=mp.Vector3( 1/3, 1/3), height = mp.inf, material=mp.Medium(epsilon=1)),
            mp.Prism(vertices, center=mp.Vector3( 1/3,   0), height = mp.inf, material=mp.Medium(epsilon=1)),
            mp.Prism(vertices, center=mp.Vector3(   0,-1/3), height = mp.inf, material=mp.Medium(epsilon=1)),
            mp.Prism(vertices, center=mp.Vector3(-1/3,-1/3), height = mp.inf, material=mp.Medium(epsilon=1)),
            mp.Prism(vertices, center=mp.Vector3(-1/3,   0), height = mp.inf, material=mp.Medium(epsilon=1)),
            mp.Prism(vertices, center=mp.Vector3(   0, 1/3), height = mp.inf, material=mp.Medium(epsilon=1)),
            mp.Cylinder(radius = 0.001*int(sys.argv[2]), center = mp.Vector3(   0,   0), material=mp.Medium(epsilon=(0.001*int(sys.argv[4]))**2))]


# geometry = [mp.Cylinder(, center = mp.Vector3( 1/3, 1/3), material=mp.Medium(epsilon=1)),
# 			mp.Cylinder(radius = 0.001*int(sys.argv[1]), center = mp.Vector3( 1/3,   0), material=mp.Medium(epsilon=1)),
#             mp.Cylinder(radius = 0.001*int(sys.argv[1]), center = mp.Vector3(   0,-1/3), material=mp.Medium(epsilon=1)),
#             mp.Cylinder(radius = 0.001*int(sys.argv[1]), center = mp.Vector3(-1/3,-1/3), material=mp.Medium(epsilon=1)),
#             mp.Cylinder(radius = 0.001*int(sys.argv[1]), center = mp.Vector3(-1/3,   0), material=mp.Medium(epsilon=1)),
#             mp.Cylinder(radius = 0.001*int(sys.argv[1]), center = mp.Vector3(   0, 1/3), material=mp.Medium(epsilon=1)),
#             mp.Cylinder(radius = 0.001*int(sys.argv[2]), center = mp.Vector3(   0,   0), material=mp.Medium(epsilon=(0.001*int(sys.argv[4]))**2))]

geometry_lattice = mp.Lattice(size=mp.Vector3(1, 1),
                                 basis1=mp.Vector3(0.5,3**0.5 / 2),
                                 basis2=mp.Vector3(0.5,-3**0.5 / 2))

ms = mpb.ModeSolver(num_bands=num_bands,
                    k_points=k_points,
                    geometry_lattice = geometry_lattice,
                    geometry=geometry,
                    resolution=resolution,
                    default_material = mp.Medium(epsilon=(0.001*int(sys.argv[3]))**2))

ms.run_te()

print(ms.freqs)
