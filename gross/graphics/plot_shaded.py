import sys
import netCDF4
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature

import matplotlib
import matplotlib.pyplot as plt



def plot_map(lons, lats, data, lonrange, latrange, tag, fn):
    vmin = max(-1., np.nanmin(data))
    vmax = min( 1., np.nanmax(data))

    proj = ccrs.PlateCarree()
    #proj = ccrs.LambertConformal(central_longitude=-170, central_latitude=60., cutoff=25.)
    #proj = ccrs.NorthPolarStereo(true_scale_latitude=60.)
    #proj = ccrs.Stereographic(central_longitude=+170, central_latitude=60. )

    ax = plt.axes(projection = proj)
    fig = plt.figure(figsize=(640/50,480/50))
    #fig = plt.figure( )
    ax = fig.add_subplot(1, 1, 1, projection = proj)

    #ax.set_extent([-100, 100, 30, 90], crs = proj)
    ax.set_extent((lonrange[0],lonrange[1], latrange[0], latrange[1]), crs=ccrs.PlateCarree())

    xlocs = np.arange(min(lonrange[0],lonrange[1]), max(lonrange[0],lonrange[1]), 5.)
    ylocs = np.arange(min(latrange[0],latrange[1]), max(latrange[0],latrange[1]), 5.)
    ax.gridlines(crs=ccrs.PlateCarree(), xlocs=xlocs , ylocs=ylocs )

    #'natural earth' -- coast only -- ax.coastlines(resolution='10m')
    ax.add_feature(cfeature.GSHHSFeature(levels=[1], scale="c") )
    ax.add_feature(cfeature.GSHHSFeature(levels=[2,3,4], scale="l") )

    cbarlabel = '%s' % ("sla")
    plttitle = 'Plot of %s' % (tag)
    plt.title(plttitle)

    #Establish the color bar
    #colors=matplotlib.colormaps.get_cmap('jet')
    #colors=matplotlib.colormaps.get_cmap('gray')
    colors=matplotlib.colormaps.get_cmap('terrain')

    cs = ax.pcolormesh(lons, lats, data,vmin=vmin,vmax=1.0,cmap=colors, transform=ccrs.PlateCarree() )
    cb = plt.colorbar(cs, extend='both', orientation='horizontal', shrink=0.5, pad=.04)
    cb.set_label(cbarlabel, fontsize=12)

    plt.savefig(fn+".png")

    plt.close('all')

#----------------------------------------------------------------------

# -- read lats, lons, sla
topo = netCDF4.Dataset(sys.argv[1],"r")
dtag=sys.argv[2]

lon = topo.variables['longitude'][:]
lat = topo.variables['latitude'][:]
sla  = topo.variables['sla'][0,:,:]
#debug: print("lon ",lon.max(), lon.min(), 'lats',lat.max(), lat.min(), flush=True )
print("sla ",sla.max(), sla.min(), flush=True)

# NW NATL
region = "NW_NATL"
lonrange = (-80., -30.)
latrange = (30., 60.)
plot_map(lon, lat, sla, lonrange, latrange, "copernicus_sla"+dtag, region+"_"+dtag)

# Drake Passage
region = "drake"
lonrange = (-80., -30.)
latrange = (-80., -45.)
plot_map(lon, lat, sla, lonrange, latrange, "copernicus_sla"+dtag, region+"_"+dtag)

# Broader AA
region = 'broader'
lonrange = (-80, +60)
latrange = (-80, -30)
plot_map(lon, lat, sla, lonrange, latrange, "copernicus_sla"+dtag, region+"_"+dtag)

