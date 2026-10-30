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
tag=`expr $tag - 1`
tag=`$base/bin/dtgfix3 $tag`
tag=`expr $tag - 1`
tag=`$base/bin/dtgfix3 $tag`

#tag=20261028
INDIR=$IABPDIR/$tag/


lead=8
fcst=20261001

d=0
end=$tag
while [ $d -lt $lead ] 
do
  end=`expr $end - 1`
  end=`$base/bin/dtgfix3 $end`
  d=`expr $d + 1`
done
echo data through $tag forecasts through $end


while [ $fcst -le $end ]
do
  echo forecasts from $fcst
  cd $OUTDIR/$fcst
  if [ $? -ne 0 ] ; then
    echo could not cd to $fcst
  fi 

  #note that directory $INDIR contains buoy history info, 
  #  while $fcst is the date of the (single) forecast
  #set -x
  
  for f in $INDIR/*.sp
  do
    if [ -s $f ] ; then
      time python3 $EXDIR/make_fcsts.py $fcst $lead $f $OUTDIR > `basename $f`.verf
    fi
  done

  fcst=`expr $fcst + 1`
  fcst=`$base/bin/dtgfix3 $fcst`
done
