'''
read in a buoy file and extract all valid locations within a time window.
then write those back out
qc:
    skip if latitude > 90 or < -90
    wrap in to -180, 180
Robert Grumbine
22 Apr 2026
'''

import sys
import datetime

#-------------------------------------------------------------------------
# Utility functions for detecting whether file has other variables than position
def hasbp(fwords):
    ''' hasbp(fwords) -- fwords is line.split() of the buoy's header line '''
    return  'BP' in fwords
def hasts(fwords):
    ''' hasts(fwords) -- fwords is line.split() of the buoy's header line '''
    return  'Ts' in fwords
def hasta(fwords):
    ''' hastafwords) -- fwords is line.split() of the buoy's header line '''
    return  'Ta' in fwords

# Check whether the data are 'near' the given hour
def nearcycle(fcycle, fincr, fnear):
  ''' nearcycle(cycle, fincr, fnear) checks to see if fincr (increment since 
      start of day) is 'near' the cycle time (hours since 00 UTC)
      cycle is hours, fincr is a timedelta, 
      fnear is the tolerance in time for being 'near' 
      RG: logic on 'near' is not well-tested
  '''
  return (abs(fincr.total_seconds()%86400 - fcycle*3600) <= fnear or \
          abs(86400-fincr.total_seconds() - fcycle*3600) <= fnear )

#-------------------------------------------------------------------------
# Change these
start = datetime.date(2024,1,1)
end   = datetime.date(2026,4,4)
cycle = 0 # hours UTC
dtlim = 60*30 # window in seconds of being 'near' cycle

#-------------------------------------------------------------------------
# Should need no changes below here

dt = datetime.timedelta(1)

# Open file
try:
  fin = open(sys.argv[1], "r", encoding='utf-8')
except:
  print("could not open ",sys.argv[1])
  sys.exit(1)

# IABP format is header line and then N lines of data. Position DOY may not match obs DOY
# Read and echo the header line
try:
    line = fin.readline()
    #debug: print(line,end="", flush=True)
    # The additional variables are not being used at this point, this is a preadaptation
    # BP is buoy pressure, Ts is surface (skin) temperature, Ta is atmospheric temperature
    hwords = line.split()
    usebp = False
    usets = False
    useta = False
    if hasbp(hwords):
        print('buoy ',sys.argv[1], 'has BP in index position ',hwords.index('BP'), file=sys.stderr )
        BP = hwords.index('BP')
        usebp = True
    if hasts(hwords):
        print('buoy ',sys.argv[1], 'has Ts in index position ',hwords.index('Ts'), file=sys.stderr )
        Ts = hwords.index('Ts')
        usets = True
    if hasta(hwords):
        print('buoy ',sys.argv[1], 'has Ta in index position ',hwords.index('Ta'), file=sys.stderr )
        Ta = hwords.index('Ta')
        useta = True

except:
    print("readline failed",line)
    sys.exit(1)

#-------------------------------------------------------------------------
for more in fin:
  words = more.split()
  #debug: print(words[1], words[5], words[6], words[7], flush=True )
  if (float(words[6]) <= -90. or float(words[6]) >= 90.0 or float(words[6]) == 0):
      continue
  lon = float(words[7])
  if (lon < -180):
      lon += 360.
  elif (lon > 180):
      lon -= 360.
  lat = float(words[6])

  obs = datetime.date(int(words[1]), 1, 1)
  incr = (float(words[5])-1.) * dt
  obs += incr

  # RG: preserve previous and only take new days' observations, vs. 
  #          multiple within the 2*dtlim window
  if (end >= obs >= start and nearcycle(cycle, incr, dtlim) ):
    print(words[1], words[5], lat, lon, end=" " )
    if (usebp):
        print(f"BP: {float(words[BP]):.2f}",end=" ")
    if (useta):
        print(f"Ta: {float(words[Ta]):.2f}",end=" ")
    if (usets):
        print(f"Ts: {float(words[Ts]):.2f}",end=" ")
    print("", flush=True)
