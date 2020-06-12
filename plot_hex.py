import matplotlib.pyplot as plt
import sys


f_te = open("bandte.dat")
# f_tm = open("bandtm.dat")

te_bands = []
f_te.readline()
for x in f_te:
	x =x[:-1] # get rid of \n
	te_bands.append([float(i) for i in x.split(",")[6:]])
# print(te_bands) 
plt.figure()
plt.plot(te_bands,'r')

plt.savefig('./temp_te'+sys.argv[6]+'.png')
# plt.savefig('./figures/super_cell/'+'r_air_'+str(0.001*int(sys.argv[1]))[:5]+'r_center_'+str(0.001*int(sys.argv[2]))[:5]+'n_center_'+str(0.001*int(sys.argv[4]))[:5]+'n_back_'+str(0.001*int(sys.argv[3]))[:5]+'/te.png',dpi=300)
