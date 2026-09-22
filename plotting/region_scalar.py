'''
Plot scalar fields from the RTOFS native grid

Robert Grumbine
25 August 2026
'''

import sys

import netCDF4

import cartopy.crs as ccrs
import matplotlib
import matplotlib.pyplot as plt

from regions import *

#------------------------------------------------------------
parm = sys.argv[2]
fields = netCDF4.Dataset(sys.argv[1])
lats   = fields.variables['TLAT'][:,:]
lons   = fields.variables['TLON'][:,:]
scalar = fields.variables[parm][0,:,:]
fields.close()

# ---------- Begin plotting --------------------------------
matplotlib.use('Agg')
nhdomains = [1, 3, 4, 5, 6]
shdomains = [2, 7]

domain = int(sys.argv[3])
if (domain == 0):
  x = globe()
  proj = ccrs.PlateCarree()
elif (domain in nhdomains ):
  if (domain == nhdomains[0]):
    x = nh()
  elif (domain == nhdomains[1] ):
    x = alaska()
  elif (domain == nhdomains[2] ):
    x = nbering()
  elif (domain == nhdomains[3]):
    x = sbering()
  elif (domain == nhdomains[4]):
    x = nsr()
  proj = ccrs.NorthPolarStereo(central_longitude = x.central_longitude)
elif (domain in shdomains):
  if (domain == shdomains[0]):
    x = sh()
  elif (domain == shdomains[1]):
    x = ross()
  proj = ccrs.SouthPolarStereo(central_longitude = x.central_longitude)
else:
  print("domain out of range, defaulting to global lat-lon",domain)
  proj = ccrs.PlateCarree()
  domain = 0
#proj = ccrs.epsg(6931) #nsidc ease2 grid for NH -- currently doesn't work this way
#proj = ccrs.epsg(6932) #nsidc ease2 grid for SH -- ""

ax  = plt.axes(projection = proj)
fig = plt.figure(figsize = x.figsize)
ax  = fig.add_subplot(1,1,1, projection = proj)

cmap = matplotlib.colormaps.get_cmap('jet')

xlocs = x.xlocs
ylocs = x.ylocs
ax.set_extent(x.extent, crs=ccrs.PlateCarree() )

proj = ccrs.PlateCarree()
ax.coastlines(resolution='10m')
ax.gridlines(crs = proj, xlocs = xlocs, ylocs = ylocs)

cmap = matplotlib.colormaps.get_cmap('jet')
cs = ax.pcolormesh(lons, lats, scalar,
                         cmap = cmap,
                         transform= proj )
cb = plt.colorbar(cs, extend='both', orientation='horizontal', shrink=0.5, pad=.04)
title = sys.argv[4]
cbarlabel = '%s' % title
cb.set_label(cbarlabel, fontsize=12)

plt.savefig("scalar."+parm+f"{domain:d}"+".png")
plt.close()
