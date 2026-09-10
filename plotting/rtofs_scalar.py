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

parm = sys.argv[2]
fields = netCDF4.Dataset(sys.argv[1])
lats   = fields.variables['TLAT'][:,:]
lons   = fields.variables['TLON'][:,:]
scalar = fields.variables[parm][0,:,:]
fields.close()

# ---------- Begin plotting --------------------------------
matplotlib.use('Agg')
nhdomains = [1,3]

domain = int(sys.argv[3])
if (domain == 0):
  proj = ccrs.PlateCarree()
elif (domain in nhdomains ):
  if (domain == nhdomains[0]):
    proj = ccrs.NorthPolarStereo(central_longitude = -80.0)
  elif (domain == nhdomains[1]):
    proj = ccrs.NorthPolarStereo(central_longitude = -170.0)
elif (domain == 2):
  proj = ccrs.SouthPolarStereo(central_longitude = -80.0)
else:
  print("domain out of range, defaulting to global lat-lon",domain)
  proj = ccrs.PlateCarree()
  domain = 0
#proj = ccrs.epsg(6931) #nsidc ease2 grid for NH -- currently doesn't work this way
#proj = ccrs.epsg(6932) #nsidc ease2 grid for SH -- ""

ax = plt.axes(projection = proj)
fig = plt.figure(figsize=(9,9))
ax = fig.add_subplot(1,1,1, projection = proj)

xlocs = list(range(-180,181,30))
if (domain == 0):
  #Globe
  ax.set_extent((-180, 180, -90, 90),crs=ccrs.PlateCarree() )
elif (domain in nhdomains ):
  #Arctic:
  if (domain == nhdomains[0]):
    ax.set_extent((-180, 180, 30, 90), crs=ccrs.PlateCarree() )
  elif (domain == nhdomains[1]):
    ax.set_extent((-180, -120, 55, 80), crs=ccrs.PlateCarree() )
    xlocs = list(range(-180,-119,10))
elif (domain == 2):
  #AA
  ax.set_extent((-180,180, -90, -40), crs=ccrs.PlateCarree() )
else:
    print("domain still out of range, aborting")
    sys.exit(1)

proj = ccrs.PlateCarree()
ax.coastlines(resolution='10m')
ax.gridlines(crs = proj, xlocs = xlocs)

cmap = matplotlib.colormaps.get_cmap('bwr')
cs = ax.pcolormesh(lons, lats, scalar,
                         cmap = cmap,
                         transform= proj )
cb = plt.colorbar(cs, extend='both', orientation='horizontal', shrink=0.5, pad=.04)
title = sys.argv[4]
cbarlabel = '%s' % title
cb.set_label(cbarlabel, fontsize=12)

plt.savefig("scalar."+parm+f"{domain:d}"+".png")
plt.close()
