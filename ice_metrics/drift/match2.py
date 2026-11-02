'''
read in buoy file and
extract model values for point closest to given initial lat-lon

RG: Need to filter out buoys that aren't on sea ice
'''
import sys
import os
import datetime

import numpy as np
import netCDF4

from utility import parse_8digits, harcdis, arcdis, bearing
import latpt

#----------------------------------------------------------
def nearest(flat, flon, fblats, fblons):
    ''' find the point in the fb vector that is closest to flat,flon '''
    mindist = 9.e9
    jbuoy   = -1
    #tlat = latpt.latpt(flat, flon)
    for j in range(0,len(fblats)):
      if (abs(flat - fblats[j]) > 1.):
        continue
      dist = arcdis(flat, flon, fblats[j], fblons[j])
      if (dist < mindist):
        jbuoy = j
        mindist = dist

    return jbuoy, mindist

#----------------------------------------------------------
dist_toler = 50.  # point must be within 50 km of the buoy
toler = 3600. #time tolerance for matching 00z
dt = datetime.timedelta(1)

#----------------------------------------------------------
# Read in a buoy for a given date (arg1)
start  = parse_8digits(sys.argv[1])
length = int(sys.argv[2])
# find nearest point in model output and extract forecasts for that point
base = sys.argv[3]
fname = base+'/'+sys.argv[1]+'/drift_f024.nc' # don't use 00 as that isn't available for GFS
if (not os.path.exists(fname)):
    print("could not find ",fname)
    print(sys.argv[1], sys.argv[3], fname)
    sys.exit(1)

fcsts = netCDF4.Dataset(fname,"r")
ilats = fcsts.variables['Initial_Latitude'][:]
ilons = fcsts.variables['Initial_Longitude'][:]
ilons[ilons > 180. ] -= 360.
flats = fcsts.variables['Final_Latitude'][:]
flons = fcsts.variables['Final_Longitude'][:]
flons[flons > 180. ] -= 360.
ddist = fcsts.variables['Drift_Distance'][:]
dbear = fcsts.variables['Drift_Bearing'][:]
fcsts.close()
#sys.exit(0)

outdir = sys.argv[4]

for fin in sys.argv[5:]:
  obslat = np.zeros((length+1))
  obslon = np.zeros((length+1))
  finlat = np.zeros((length+1))
  finlon = np.zeros((length+1))
  obsbear = np.zeros((length+1))
  obsdist = np.zeros((length+1))
  fcstbear = np.zeros((length+1))
  fcstdist = np.zeros((length+1))

  #debug: print('fin = ',fin)
  try:
    fbuoy  = open(fin, "r", encoding='utf-8')
  except:
    print("could not open input")
    sys.exit(1)
  w1 = fin.split('/')
  words = w1[-1].split('.')
  fout = open(outdir+'/fcst.'+words[0], "w", encoding = 'utf-8')
  #debug: print('opened ',outdir+'/fcst.'+words[0])

  #read file down to given date -- exit if not present

  found = False
  for more in fbuoy:
    words = more.split()

    if (float(words[2]) <= -90. or float(words[2]) >= 90.0 or float(words[2]) == 0):
        continue
    lat = float(words[2])

    lon = float(words[3])
    if (lon < -180):
        lon += 360.
    elif (lon > 180):
        lon -= 360.

    obs = datetime.datetime(int(0.5+float(words[0])), 1, 1)
    incr = (float(words[1])-1.) * dt
    obs += incr
    if (not found and abs((obs - start).total_seconds()) < toler) :
      #debug: print("obs: ",obs,start,(obs - start).total_seconds() , flush=True)
      sllpt = latpt.latpt(lat, lon)
      obslat[0] = lat
      obslon[0] = lon
      found = True
    #debug: print(obs, start, obs - start, flush=True)
    lead = int(0.5 + (obs - start).total_seconds()/86400)
    if found and 0 < lead <= length:
      fllpt = latpt.latpt(lat, lon)
      #debug: print(lead,'day lead',f"{sllpt.lat:.5f}", f"{sllpt.lon:.5f}", f"{fllpt.lat:.5f}", \
      #debug: f"{fllpt.lon:.5f}", f"{harcdis(sllpt, fllpt):6.3f}", f"{bearing(sllpt, fllpt):6.1f}")
      # n.b. if multiple obs at same lead, last one is used
      finlat[lead] = lat
      finlon[lead] = lon
      obsbear[lead] = bearing(sllpt, fllpt)
      #obsdist[lead] = harcdis(sllpt, fllpt)
      obsdist[lead] = arcdis(obslat[0], obslon[0], lat, lon)

  #debug: print("closing ",fin, flush=True)
  fbuoy.close()

  if (not found):
    #debug: print("could not find valid observed drift for ",fin, flush=True)
    fout.close()
    continue

#saved day 1-N obsd location, distance, bearing

#---------------------------------------------------------

  # find nearest point in model output and extract forecasts for that point
  jnear, delta = nearest(sllpt.lat, sllpt.lon, ilats, ilons)
  if (delta > dist_toler):
    #debug: print("nearest forecast point is too far away from buoy point: ",delta,
    #        'vs',dist_toler,file=sys.stderr, flush=True)
    continue

#debug: sys.exit(0)
  #debug: print(jnear, delta, flush=True)
  # UFS is 6 hourly output, so valid at 24 is in 18 file
  for hh in range(18, int(length*24+1), 24):
  # Rtofs is in 2 ranges:
  # import itertools
  # for hh in itertools.chain(range (23, 73, 24), range(93, int(length*24+1), 24)):
    day = int(hh/24 + 0.5)

    fname=base+'/'+sys.argv[1]+'/drift_f' + f"{hh:03d}" + '.nc'
    fcsts = netCDF4.Dataset(fname,"r")
    ilats = fcsts.variables['Initial_Latitude'][:]
    ilons = fcsts.variables['Initial_Longitude'][:]
    ilons[ilons > 180. ] -= 360.
    flats = fcsts.variables['Final_Latitude'][:]
    flons = fcsts.variables['Final_Longitude'][:]
    flons[flons > 180. ] -= 360.
    ddist = fcsts.variables['Drift_Distance'][:]
    dbear = fcsts.variables['Drift_Bearing'][:]
    fcsts.close()

    delta = ddist[jnear] - obsdist[day]
    fcstdist[day] = ddist[jnear]
    fcstbear[day] = dbear[jnear]
    if ((ddist[jnear] != 0) or (dbear[jnear] != 0)) and (ddist[jnear] < 1.e9) :
      print(f"{jnear:6d}",f"{24*day:3d}",f"{ilats[jnear]:7.3f}", f"{ilons[jnear]:8.3f}", \
            f"{flats[jnear]:9.5f}", f"{flons[jnear]:10.5f}", \
            f"{ddist[jnear]:6.3f}", f"{dbear[jnear]:6.1f}", ' ', \
            f"{obslat[0]:9.5f}",    f"{obslon[0]:10.5f}", \
            f"{finlat[day]:9.5f}",  f"{finlon[day]:10.5f}", \
            f"{obsdist[day]:6.3f}", f"{obsbear[day]:6.1f}", f"{delta:7.3f}", file = fout)
  fout.close()
