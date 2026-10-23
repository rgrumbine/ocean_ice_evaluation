#!/bin/sh
#Robert Grumbine
#22 Apr 2026

base=/u/robert.grumbine

IABPDIR=$base/noscrub/verification/iabp
EXDIR=$base/rgdev/ocean_ice_evaluation/candidates/iabp
OUTDIR=$base/noscrub/devdrift/
source $base/env3.12/bin/activate
export PYTHONPATH=$PYTHONPATH:$base/rgops/mmablib/py

# Shouldn't need changes below here -----------------------

tag=`date +"%Y%m%d"`
tag=20261021
lead=8
fcst=20260830

cd $IABPDIR/$tag
#note that directory $tag contains buoy history info, 
#  while $fcst is the date of the (single) forecast
for f in *.sp
do
  if [ -s $f ] ; then
    python3 $EXDIR/make_fcsts.py $fcst $lead $f $OUTDIR > $f.verf
  fi
done
