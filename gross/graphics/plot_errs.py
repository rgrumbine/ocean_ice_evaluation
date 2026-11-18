'''
Plot output from gross error check
Robert Grumbine
'''

import sys

import matplotlib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from plot_regions import *

#----------------------------------------------------------
fin = open(sys.argv[1],"r", encoding='utf-8')

try:
  title_tag = sys.argv[2]
except:
  title_tag = "ref"

try:
  markersize = float(sys.argv[3])
except:
  markersize = 12

dtg = sys.argv[4]

parm = []
i = []
j = []
lon = []
lat = []

for line in fin:
  if ("pm" in line):
    words = line.split()
    try:
      tp = (words[0].split(":"))[1]
    except:
      tp = words[0]
    parm.append(tp)
    i.append(int(words[1]))
    j.append(int(words[2]))
    lon.append(float(words[3]))
    tll = float(words[4])
    lat.append(tll)

print("found ",len(i)," error points")
if (len(i) == 0):
    sys.exit(0)

#debug print(max(lat), min(lat), max(lon), min(lon) )
latmax = max(lat)
latmin = min(lat)
lonmax = max(lon)
lonmin = min(lon)


# i-j plot of error points ----------------------------------
matplotlib.use('Agg') #batch mode
if markersize <= 12:
    alpha = 1
else:
    alpha = 0.2/25

#Elaborations:
#  title
#  axis labels
#  separate color/symbol per parameter
#  different sizes per parameter

fig,ax = plt.subplots()
plt.scatter(i,j, c = 'r', s = markersize)
ax.grid() 
plt.title(title_tag)
plt.savefig("ij_errs_"+title_tag+dtg+".png")
plt.close()

# geographic -- NH -- plot of error points ---------------------------------
domain = 1
x = nh()
proj = ccrs.NorthPolarStereo(central_longitude=x.central_longitude, true_scale_latitude = 60.)

ax = plt.axes(projection = proj)
fig = plt.figure(figsize = (8,6))
ax = fig.add_subplot(1,1,1,projection = proj)
plt.title(title_tag)

xlocs = x.xlocs
ylocs = x.ylocs

ax.set_extent(x.extent, crs=ccrs.PlateCarree() )
ax.gridlines(crs=ccrs.PlateCarree(), xlocs=xlocs, ylocs=ylocs )
# not on hera: 
ax.coastlines()
#ax.add_feature(cfeature.GSHHSFeature(levels=[1,2], scale="l") )

plt.scatter(lon, lat, transform=ccrs.PlateCarree(), c = 'r', s = markersize, alpha = alpha)
plt.savefig("nh_errs_"+title_tag+dtg+".png")
plt.close()

# ---------- SH plot ----------------------------------------------------------
domain = 2
x = sh()
proj = ccrs.SouthPolarStereo(central_longitude= x.central_longitude, true_scale_latitude = -60.)

ax = plt.axes(projection = proj)
fig = plt.figure(figsize = (8,6))
ax = fig.add_subplot(1,1,1,projection = proj)
plt.title(title_tag)

xlocs = x.xlocs
ylocs = x.ylocs
ax.set_extent(x.extent, crs=ccrs.PlateCarree() )
ax.gridlines(crs=ccrs.PlateCarree(), xlocs=xlocs, ylocs=ylocs )
# not on hera: ax.coastlines()
ax.coastlines()
#ax.add_feature(cfeature.GSHHSFeature(levels=[1,2], scale="l") )

plt.scatter(lon, lat, transform=ccrs.PlateCarree(), c = 'r', s = markersize, alpha = alpha)
plt.savefig("sh_errs_"+title_tag+dtg+".png")
plt.close()

# ------ Non-polar plot -------------------------------------------------------------
domain = 0
x = globe()
proj = ccrs.PlateCarree()

ax = plt.axes(projection = proj)
fig = plt.figure(figsize = (8,6))
ax = fig.add_subplot(1,1,1,projection = proj)
plt.title(title_tag)

xlocs = x.xlocs
ylocs = x.ylocs
ax.set_extent(x.extent, crs=ccrs.PlateCarree() )
ax.gridlines(crs=ccrs.PlateCarree(), xlocs=xlocs, ylocs=ylocs )
# not on hera: 
ax.coastlines()
#ax.add_feature(cfeature.GSHHSFeature(levels=[1,2], scale="l") )

plt.scatter(lon, lat, transform=ccrs.PlateCarree(), c = 'r', s = markersize, alpha = alpha)
plt.savefig("nonpolar_errs_"+title_tag+dtg+".png")
plt.close()

