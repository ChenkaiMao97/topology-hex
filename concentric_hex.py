import math
import sys
import os
import meep as mp
import matplotlib.pyplot as plt
from meep import mpb

num_bands = 10
interp = 19

# honeycomb:
k_points = [mp.Vector3(2/3,1/3),
            mp.Vector3(0,0),
            mp.Vector3(0,0.5)
            ] 

k_points = mp.interpolate(interp, k_points)

# argv[1]: radius of airhole
# argv[2]: radius of center
# argv[3]: n_back
# argv[4]: n_cen
# argv[5]: resolution

resolution = int(sys.argv[6])

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!amorphous!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

r_air = 0.001*int(sys.argv[1])
r_cen1 = 0.001*int(sys.argv[2])
# r_cen1 = 1/3-r_air
r_cen2 = 0.4*r_cen1

vertices = [mp.Vecotr3(     4/3*r_air, 2/3*r_air),
            mp.Vector3(     2/3*r_air,-2/3*r_air),
            mp.Vector3(    -2/3*r_air,-4/3*r_air),
            mp.Vector3(    -4/3*r_air,-2/3*r_air),
            mp.Vector3(    -2/3*r_air, 2/3*r_air),
            mp.Vector3(     2/3*r_air, 4/3*r_air)]

vertices_cen1 = [mp.Vector3(     4/3*r_cen1, 2/3*r_cen1),
            mp.Vector3(     2/3*r_cen1,-2/3*r_cen1),
            mp.Vector3(    -2/3*r_cen1,-4/3*r_cen1),
            mp.Vector3(    -4/3*r_cen1,-2/3*r_cen1),
            mp.Vector3(    -2/3*r_cen1, 2/3*r_cen1),
            mp.Vector3(     2/3*r_cen1, 4/3*r_cen1)]

vertices_cen2 = [mp.Vector3(     4/3*r_cen2, 2/3*r_cen2),
            mp.Vector3(     2/3*r_cen2,-2/3*r_cen2),
            mp.Vector3(    -2/3*r_cen2,-4/3*r_cen2),
            mp.Vector3(    -4/3*r_cen2,-2/3*r_cen2),
            mp.Vector3(    -2/3*r_cen2, 2/3*r_cen2),
            mp.Vector3(     2/3*r_cen2, 4/3*r_cen2)]

geometry = [mp.Prism(vertices, center=mp.Vector3( 1/3, 1/3), height = mp.inf, material=mp.Medium(epsilon=1)),
            mp.Prism(vertices, center=mp.Vector3( 1/3,   0), height = mp.inf, material=mp.Medium(epsilon=1)),
            mp.Prism(vertices, center=mp.Vector3(   0,-1/3), height = mp.inf, material=mp.Medium(epsilon=1)),
            mp.Prism(vertices, center=mp.Vector3(-1/3,-1/3), height = mp.inf, material=mp.Medium(epsilon=1)),
            mp.Prism(vertices, center=mp.Vector3(-1/3,   0), height = mp.inf, material=mp.Medium(epsilon=1)),
            mp.Prism(vertices, center=mp.Vector3(   0, 1/3), height = mp.inf, material=mp.Medium(epsilon=1)),
            mp.Prism(vertices_cen1, center=mp.Vector3(   0,   0), height = mp.inf, material=mp.Medium(epsilon=(0.001*int(sys.argv[4]))**2)),
            mp.Prism(vertices_cen2, center=mp.Vector3(   0,   0), height = mp.inf, material=mp.Medium(epsilon=(0.001*int(sys.argv[5]))**2))]


# mp.Cylinder(radius = 0.001*int(sys.argv[2]), center = mp.Vector3(   0,   0), material=mp.Medium(epsilon=(0.001*int(sys.argv[4]))**2))


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

md = mpb.MPBData(rectify=True, periods=2, resolution=128)
eps = ms.get_epsilon()
converted_eps = md.convert(eps)
plt.figure()
plt.imshow(converted_eps, interpolation='spline36', cmap='binary')
plt.colorbar()

# try:
#     os.mkdir('./figures/super_cell/'+'r_air_'+str(0.001*int(sys.argv[1]))[:5]+'r_center_'+str(0.001*int(sys.argv[2]))[:5]+'n_center_'+str(0.001*int(sys.argv[4]))[:5]+'n_back_'+str(0.001*int(sys.argv[3]))[:5])
# except:
#     pass
plt.savefig('./temp_eps'+sys.argv[7]+'.png')
# plt.savefig('./figures/super_cell/'+'r_air_'+str(0.001*int(sys.argv[1]))[:5]+'r_center_'+str(0.001*int(sys.argv[2]))[:5]+'n_center_'+str(0.001*int(sys.argv[4]))[:5]+'n_back_'+str(0.001*int(sys.argv[3]))[:5]+'/eps.png')

