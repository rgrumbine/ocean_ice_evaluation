'''
Integral statistics for sea ice -- area, extent, volume

edit 'base' to point to the directory above the experiments
  arguments are experiment name and 8 digit date
assumes cycle = 00
SFS assumes members 000-010
sfs.20231101/00/mem000/products/ice/netcdf/native
all hours f024 to f8784 (maxhour, step by dh), 006 to 384 for GFS

needs auxiliary file with tarea for the cells
'''

import sys
import os
import datetime
import copy

import numpy as np
from numpy import ma
import netCDF4
import matplotlib
import matplotlib.pyplot as plt

#---------------------------------------------------------------------
def parse_8digits(tag):
  """ Convert an 8 digit int to a datetime.date object """
  ftmp = int(tag)
  (yy,mm,dd) = (int(int(ftmp)/10000),int((int(ftmp)%10000)/100),int(ftmp)%100)
  tag_out = datetime.datetime(int(yy), int(mm), int(dd))
  return tag_out

# Edit these ----------------------------------------------------------
#gaea: base   = '/ncrc/home1/Robert.Grumbine/scratch6/COMROOT/'
#ursa: base   = '/home/Robert.Grumbine/scratch/COMROOT/'
#Wcoss2:
base   = sys.argv[1]
expt   = sys.argv[2]
start  = parse_8digits(sys.argv[3] )
#debug: print(base, expt, start, flush=True)
#exit(0)

maxmem = 0 #0 for GFS, 10 for SFS
#maxhour = 8784 # 366 d -- SFS
maxhour = 384  # 16 d -- GFS
dh = 6 #6 for GFS, 24 for SFS

crit_conc = 0.15 #concentration defining 'extent'

# Should not need editing below here except SFS v. GFS ----------------
def find_extent(cellarea, conc, crit):
  '''
  Find the ice extent for a given critical concentration
  '''
  total = 0.

  # very slow and requires shape info
  #nj = 320
  #ni = 360
  #for jj in range(0,nj):
  #  for ii in range(0,ni):
  #    if (conc[jj,ii] > crit):
  #      total += cellarea[jj,ii]

  # about 14x faster than above
  mask = ma.masked_array(conc > crit)
  indices = mask.nonzero()
  for k in range(0,len(indices[0])):
    jj = indices[0][k]
    ii = indices[1][k]
    total += cellarea[jj,ii]

  return total

#----------------------------------------------------------------------
matplotlib.use('Agg')
fig,ax = plt.subplots()

area   = np.zeros((int((maxhour-dh)/dh)+2 ))
extent = np.zeros((int((maxhour-dh)/dh)+2 ))
nhext  = np.zeros((int((maxhour-dh)/dh)+2 ))
shext  = np.zeros((int((maxhour-dh)/dh)+2 ))
volume = np.zeros((int((maxhour-dh)/dh)+2 ))
days   = np.zeros(len(area))

count = 0
for memno in range(0,maxmem+1):

  # SFS
  #fbase = base + '/' + expt + '/00/mem' + \
  #             f"{memno:03d}"+'/products/ice/netcdf/native/sfs.t00z.native.f'
  # GFS
  fbase =  base + expt + "/00/model/ice/history/gfs.t00z.6hr_avg.f"

  for h in range(dh,maxhour+1,dh):
    fname = fbase + f"{h:03d}" + '.nc'
    if (not os.path.exists(fname)):
        print("no such file ",fname)
        #sys.exit(1)
        continue
    model = netCDF4.Dataset(fname)
    if (count == 0):
      tlat = model.variables['TLAT'][:,:]
      #tarea *= np.cos(tlat*pi/180.)
      fhistory = fbase + f"{h:03d}" + '.nc'
      grid = netCDF4.Dataset(fhistory)
      tarea = grid.variables['tarea'][:,:]
      del grid
      tarea /= 1e12
      #debug: print("tarea ",tarea.max(), tarea.min(), flush=True )
      #debug: sys.exit(0)

      nharea = copy.deepcopy(tarea)
      nharea[tlat < 0] = 0.
      sharea = copy.deepcopy(tarea)
      sharea[tlat > 0] = 0.
      #debug: print("nh, sh area",nharea.max(), sharea.max(), nharea.shape, flush=True )
      #debug: sys.exit(0)

    hi = model.variables['hi_h'][0,:,:]
    ai = model.variables['aice_h'][0,:,:]

    i = int(h/dh+0.5)
    days[i] = h/dh

    tmp       = ai*tarea
    area[i]   = tmp.sum()
    tmp2      = hi*tmp
    volume[i] = tmp2.sum()
    #debug: sys.exit(0)

    #debug: print(days[i], area[i], volume[i], extent[i], flush=True)
    nhext[i] = find_extent(nharea, ai, crit_conc)
    shext[i] = find_extent(sharea, ai, crit_conc)
    extent[i] = nhext[i] + shext[i]
    print(memno, days[i], area[i], volume[i], extent[i], nhext[i], shext[i], flush=True )

  if (memno == 0):
    ax.plot(days[1:], area[1:], color = 'red', label = 'area')
    ax.plot(days[1:], extent[1:], color = 'blue', label = 'extent')
    ax.plot(days[1:], nhext[1:], color = 'blue', label = 'nhext')
    ax.plot(days[1:], shext[1:], color = 'orange', label = 'shext')
    ax.plot(days[2:], volume[2:], color = 'black', label = 'volume')
  else:
    ax.plot(days[1:], area[1:], color = 'red')
    ax.plot(days[1:], extent[1:], color = 'blue')
    ax.plot(days[1:], nhext[1:], color = 'blue')
    ax.plot(days[1:], shext[1:], color = 'orange')
    ax.plot(days[2:], volume[2:], color = 'black')

  count += 1

ax.set(title=expt)
ax.legend()
ax.grid()
plt.savefig("out"+expt+".png")
