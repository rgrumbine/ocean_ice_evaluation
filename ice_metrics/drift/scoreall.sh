#!/bin/sh
#Robert Grumbine
#22 Apr 2026

base=/u/robert.grumbine

IABPDIR=$base/noscrub/verification/iabp
EXDIR=$base/rgdev/ocean_ice_evaluation/ice_metrics/drift
OUTDIR=$base/noscrub/devdrift/

source $base/env3.12/bin/activate
export PYTHONPATH=$PYTHONPATH:$base/rgops/mmablib/py

# Shouldn't need changes below here -----------------------

tag=`date +"%Y%m%d"`
tag=20261021
INDIR=$IABPDIR/$tag/

lead=8
fcst=20260401

while [ $fcst -le 20260831 ]
do
  echo forecasts from $fcst
  cd $OUTDIR/$fcst
  if [ $? -ne 0 ] ; then
    echo could not cd to $fcst
  fi 

  #note that directory $tag contains buoy history info, 
  #  while $fcst is the date of the (single) forecast
  #set -x
  
  for f in $INDIR/*.sp
  do
    if [ -s $f ] ; then
      python3 $EXDIR/make_fcsts.py $fcst $lead $f $OUTDIR > `basename $f`.verf
    fi
  done

  fcst=`expr $fcst + 1`
  fcst=`$base/bin/dtgfix3 $fcst`
done
