'''
Build N day forecasts of drift distance and bearing from output of iabp_speed
Robert Grumbine 9 Jan 2026
'''
import sys
import os
import datetime

import netCDF4

from utility import parse_8digits, harcdis, bearing
import latpt

#-----------------------------------------------------------------------------
#class obs_pt:
#  ''' proper obs_pt class -- time and place, but nothing derived '''

#RG: redo with obs_pt. Fcst_pt has final location and drift dist, bearing
class fcst_pt:
  ''' class to work with points filtered down to being daily, on the cycle '''
  def __init__(self, ymd, hms, lat, lon):
    self.ymd = ymd
    self.hms = hms
    self.lat = lat
    self.lon = lon
    self.llpt = latpt.latpt(lat, lon)
    self.tag = parse_8digits(ymd)
    #debug: print(hms, int(hms/10000), int(hms/100)%100, hms%100, flush=True)
    fdt = datetime.timedelta(hours = int(hms/10000), minutes = int(hms/100)%100, \
                          seconds = int(hms)%100)
    #debug: print(fdt, flush=True)
    self.tag += fdt

  def make_fcst(self, fy):
    ''' fcst_pt.make_fcst(y) -- give the drift distance and direction 
            from self to fcst_pt y '''
    fdelta = (fy.tag - self.tag).total_seconds()
    if (fdelta == 0):
        return (0, 0, 0, 0)
    fndist      = harcdis(self.llpt, fy.llpt)*1000. # harcdis is in km
    fdirection = bearing(self.llpt, fy.llpt)
    #debug: print("delta = ",delta, int(delta/86400+0.5), flush=True )
    fspeed = fndist / fdelta
    return (fndist, fdirection, fdelta, fspeed)

  @staticmethod
  def finddate(fcsts, fdate, toler = 1800):
    ''' finddate -- find the index, if it exists, of the drifter on given date ''' 
    np = len(fcsts)
    for fi in range(0, np):
      if (abs((fcsts[fi].tag - fdate).total_seconds()) < toler):
        #debug: print(fcsts[fi].tag , fdate, fcsts[fi].tag - fdate, flush = True)
        return fi
    return -1



#-----------------------------------------------------------------------------
#debug: print('python',sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], flush=True)

locations = []
fcst_date = parse_8digits(int(sys.argv[1]) )
#debug: print("fcst_date = ",fcst_date, flush=True)

fcst_len = int(sys.argv[2])

# Read in buoy file and print out drifts vs forecast lead -----
with open(sys.argv[3], encoding='utf-8') as fin:
  for line in fin:
    words = line.split()
    x = fcst_pt(int(words[1]), int(words[2]), float(words[3]), float(words[4]) )
    #debug: print(x.tag, flush=True)
    locations.append(x)
npts = len(locations)

obs_index = fcst_pt.finddate(locations, fcst_date)

## print out all forecasts derivable from buoy, out to fcst_len
#for i in range(0, npts):
#  for j in range(min(i+1,npts-1), min(npts, i+fcst_len+1) ):
#    (d, wdir, dt, speed) = locations[i].make_fcst(locations[j])
#    lead = int(dt/86400.+0.5)
#    if (0 < lead <= fcst_len ):
#      print(locations[i].ymd, 'lead', lead, d, wdir, speed)
#  print(" ")

# Print out just the forecasts for the given day
i = obs_index
for k in range(min(i+1,npts-1), min(npts, i+fcst_len+1) ):
    (d, wdir, dt, speed) = locations[i].make_fcst(locations[k])
    lead = int(dt/86400.+0.5)
    if (0 < lead <= fcst_len ):
      print(locations[i].ymd, locations[i].lat, locations[i].lon, 'lead', lead, d, wdir, speed)
print(" ")


#-----------------------------------------------------------------------------
# Newdrift model output is one file per forecast lead, lead in hours in fcst. name
#dbase = '/export/emc-lw-rgrumbi/rmg3/newdrift_fcst/'+fcst_date.strftime("%Y%m%d")
dbase = sys.argv[4]
dt = datetime.timedelta(1)
fbase = dbase + '/drift_f'


def nearest(oloc, mlats, mlons, toler = 50.):
    ''' nearest(oloc, mlats, mlons, toler = 50) -- Find the model point nearest the buoy.
        toler is the minimum distance for a match, in km. defaults to 50 km. '''
    np = len(mlons)
    mindist = 1.e6
    tloc = latpt.latpt()
    mi   = -1
    for fi in range(0, np):
      tloc.lat = mlats[fi]
      tloc.lon = mlons[fi]
      tmp  = harcdis(oloc, tloc)
      if (tmp < mindist):
        #debug: print(fi, tloc.lat, tloc.lon, tmp, flush=True)
        mi = fi
        mindist = tmp
    if (mindist < toler):
      return mi

    return -1


yyy = -1
for flead in range(1, fcst_len+1):
    hhh = f"{int(flead*24):03d}"
    fname = fbase+hhh+".nc"
    if not os.path.exists(fname) :
      continue
    #debug: else:
      #debug: print('have ',fname, flush=True)

    fmodel = netCDF4.Dataset(fname, 'r')
    nbuoy   = len(fmodel.dimensions['nbuoy'])
    ilat = fmodel.variables['Initial_Latitude'][:]
    ilon = fmodel.variables['Initial_Longitude'][:]
    flat = fmodel.variables['Final_Latitude'][:]
    flon = fmodel.variables['Final_Longitude'][:]
    fdir = fmodel.variables['Drift_Bearing'][:]
    fdist = fmodel.variables['Drift_Distance'][:]
    fdist *= 1000. # convert to meters
    #debug: print(nbuoy, ilat.max(), ilat.min(), flat.max(), flat.min(), \
            #fdir.max(), fdist.max(), flush=True )

    if (flead == 1):
      yyy = nearest(locations[obs_index], ilat, ilon)
      #debug: print("nearest index = ",yyy, flush=True)

    y = locations[obs_index+flead]
    z = locations[obs_index].make_fcst(y)
    (d, wdir, dt, speed) = locations[obs_index].make_fcst(y)
    if (yyy >= 0 and fdist[yyy] < 1.e10 and fdir[yyy] < 1.e10): #have a valid matchup
        print(flead, "obs ",d, wdir, 'fcst', fdist[yyy], fdir[yyy])
    else:
        print(flead, 'bad fcst ',yyy,  fdist[yyy], fdir[yyy])
