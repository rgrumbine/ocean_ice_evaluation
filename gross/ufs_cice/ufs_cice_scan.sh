#!/bin/sh 

export start=${start:-20261026}
export end=${end:-20261117}

export PYTHONPATH=$HOME/ocean_ice_evaluation/mmablib/py:$HOME/rgdev/ocean_ice_evaluation/gross/
export MODDEF=$HOME/rgdev/ocean_ice_evaluation/gross/model_definitions

echo zzz module list
module list

export level=${level:-extreme}
export cyc=${cyc:-00}

set -xe

f=$start
while [ $f -le $end ]
do

  tag=$f
  if [ -d $modelout/gfs.$tag ] ; then
    fhr=006
    while [ $fhr -le 384 ]
    do
      time python3 $GDIR/universal2d.py \
             $modelout/gfs.$tag/${cyc}/model/ice/history/gfs.t${cyc}z.6hr_avg.f${fhr}.nc \
             ufs_cice.def \
             $GDIR/ctl/ufs_cice.${level} redone \
             > gfs.cice.${f}.$level.$fhr.results
      fhr=`expr $fhr + 6`
      if [ $fhr -le 100 ] ; then
	fhr=0$fhr
      fi
    done
  fi

  f=`expr $f + 1`
  f=`$HOME/bin/dtgfix3 $f`
done

model=gfs
cat ${model}.cice.*.results > all.$model
for lead in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 
do
  fhr=`expr $lead \* 24 + 6`
  if [ $fhr -lt 10 ] ; then
    fhr=00$fhr
  elif [ $fhr -lt 100 ] ; then
    fhr=0$fhr
  fi

  cat ${model}.cice.*.$level.$fhr.results > all.${model}.$fhr
done

