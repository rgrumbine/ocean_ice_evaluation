'''
Plot the NSIDC extents against the UFS modelled extents
Robert Grumbine
22 Apr 2026
'''

import sys
import datetime

import numpy as np
import matplotlib
import matplotlib.pyplot as plt


#------------------------------------------------------------------------
def nsidc_readin(fname):
  ''' nsidc_readin(fname) -- read in the nsidc extent file '''
  ext = []
  missing = []
  tag = []
  with open(fname,"r",encoding="utf-8") as fnorth:
    line = fnorth.readline()
    line = fnorth.readline()
    for line in fnorth:
      words=line.split(',')
      yy = int(words[0])
      mm = int(words[1])
      dd = int(words[2])
      fttag = datetime.datetime(yy,mm,dd)
      ext.append(float(words[3]))
      missing.append(float(words[4]))
      tag.append(fttag)

  fnumtag = np.array(tag)
  fnumext = np.array(ext)
  del ext, missing, tag
  return fnumtag, fnumext

def ufs_readin(fname, fnh, fsh):
  ''' ufs_readin(fname, nh, sh) -- read in the ufs northern and southern hemisphere 
        ice extents from file fname. Open the file here '''
  with open(fname, "r", encoding="utf-8") as fufs:
    fk = 0
    for line in fufs:
      words = line.split()
      fnh[fk] = float(words[5])
      fsh[fk] = float(words[6])
      fk += 1

#------------------------------------------------------------------------

numtag, numext = nsidc_readin("N_seaice_extent_daily_v4.0.csv")
sumtag, sumext = nsidc_readin("S_seaice_extent_daily_v4.0.csv")

lead = 16 # GFS
dh = 6
#lead = 366 # SFS
#dh = 24 #SFS
days = np.zeros((lead+1))
# Get the lead days observations
ttag = datetime.datetime(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
#debug: print(ttag, flush=True)

k = np.where(numtag == ttag)[0]
ks = np.where(sumtag == ttag)[0]
#debug: print(np.where(numtag == ttag), k, ks, flush=True)

dt = datetime.timedelta(1)
for i in range(0, lead+1):
  days[i] = i
  #debug: print(numtag[i+k], numext[i+k], sumext[i+ks], flush=True)
daynum = int(k[0])

#------------------------------------------------------------------------
gdays = np.zeros((int(24/dh*lead)))
nh    = np.zeros((int(24/dh*lead)))
sh    = np.zeros((int(24/dh*lead)))

ufs_readin(sys.argv[4], nh, sh)
for i in range(0, len(gdays)):
  gdays[i] = (i+1)*(dh/24)
#debug: print(gdays[i], nh[i], sh[i], flush=True)

#------------------------------------------------------------------------
matplotlib.use('Agg')
fig,ax = plt.subplots()
ax.plot(days, numext[daynum:int(daynum+lead+1)],label="nsidc.north")
ax.plot(days, sumext[daynum:int(daynum+lead+1)], label="nsidc.south")
ax.plot(gdays, nh, label="ufs_north")
ax.plot(gdays, sh, label="ufs_south")
ax.set(title = "GFS."+ttag.strftime("%Y%m%d") )
#ax.set(title = "SFS."+ttag.strftime("%Y%m%d") )
ax.legend()
ax.grid()
plt.savefig("overlay.png")
