'''
read in a thinned buoy file and its positions
examine displacements for extreme values (high or low)

check: 
delta t is reasonable
speed is reasonable
time is monotonic in data file

fix:
use real distance computation

Robert Grumbine
22 Apr 2026
'''

#from math import sin, cos, atan2, sqrt, pi
import sys
import datetime

from utility import harcdis, bearing
import latpt

#-----------------------------------------------------------------
# Change these to suit
splim = 1.0   # fastest allowed ice drift, m/s
dtlim = 1800. # minimum time separation between obs, s
#-----------------------------------------------------------------
# Open file
# Internal format is N lines of data, possibly trailing BP, Ts, Ta
try:
  fin = open(sys.argv[1], "r", encoding='utf-8')
except:
  print("could not open ",sys.argv[1])
  sys.exit(1)

#-----------------------------------------------------------------

dt  = datetime.timedelta(1)
k   = 0
for more in fin:
  words = more.split()
  obs = datetime.datetime(int(words[0]), 1, 1)
  obs += (float(words[1])-1.) * dt
  position = ( float(words[2]), float(words[3]) )

  if (k == 0):
    prev_obs = obs
    prev_position = position
  else:
    delta = (obs - prev_obs).total_seconds()

    if (obs > prev_obs):
      p1 = latpt.latpt(position[0], position[1])
      p2 = latpt.latpt(prev_position[0], prev_position[1])
      dist  = harcdis(p1, p2)*1000. # harcdis is in km
      speed = dist /delta
      direction = bearing(p1, p2)
    else:
      speed = 0.
      direction = 0.

    if (delta >= dtlim and speed <= splim):
      print(f"{k:5d}", prev_obs.strftime("%Y%m%d"), prev_obs.strftime("%H%M%S"), \
            f"{p2.lat:.5f}", f"{p2.lon:.5f}",
            f"{delta:5.0f}", f"{dist:8.2f}", f"{direction:.5f}", f"{speed:.5f}" )
    elif (speed > splim and delta >= dtlim):
      print(k,position, prev_position, delta, dist, direction, speed, file=sys.stderr)

    prev_position = position
    prev_obs      = obs

  k += 1
