#!/bin/sh 

export start=${start:-20261026}
export end=${end:-20261117}

export PYTHONPATH=$PYTHONPATH:$HOME/ocean_ice_evaluation/mmablib/py:$HOME/rgdev/ocean_ice_evaluation/gross/
export MODDEF=$HOME/rgdev/ocean_ice_evaluation/gross/model_definitions

echo zzz module list
module list

export level=${level:-extreme}
export cyc=${cyc:-00}

set -xe

tag=$start
while [ $tag -le $end ]
do

  if [ -d $modelout/gfs.$tag ] ; then
    fhr=006
    while [ $fhr -le 384 ]
    do
      if [ ! -f $model.${tag}.$level.$fhr.results ] ; then
        time python3 $GDIR/universal2d.py \
             $modelout/gfs.$tag/${cyc}/model/ice/history/gfs.t${cyc}z.6hr_avg.f${fhr}.nc \
             $model.def \
             $GDIR/ctl/$model.${level} redone \
             > $model.${tag}.$level.$fhr.results
      fi
      fhr=`expr $fhr + 6`
      if [ $fhr -le 100 ] ; then
	fhr=0$fhr
      fi
    done
  fi

  tag=`expr $tag + 1`
  tag=`$HOME/bin/dtgfix3 $tag`
done

# Now that all results have been scanned, check for errors:---------------------------

cat ${model}.*.*.results > all.$model
for lead in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 
do
  fhr=`expr $lead \* 24 + 6`
  if [ $fhr -lt 10 ] ; then
    fhr=00$fhr
  elif [ $fhr -lt 100 ] ; then
    fhr=0$fhr
  fi

  cat ${model}.*.$level.$fhr.results > all.${model}.$fhr
done

python3 $GDIR/graphics/plot_errs.py all.$model all.$model 12. $tag

python3 $GDIR/exceptions/exceptions.py $GDIR/exceptions/physical.exceptions.$model all.$model > nonphysical.$model
python3 $GDIR/graphics/plot_errs.py nonphysical.$model nonphysical.$model 12. $tag

python3 $GDIR/exceptions/exceptions.py $GDIR/exceptions/known.errors nonphysical.$model > unknown.$model
python3 $GDIR/graphics/plot_errs.py unknown.$model unknown.$model 12. $tag


# ------------------ plot by parameter
$GDIR/$model/${model}_split.sh nonphysical.$model
if [ ! -d $model ] ; then
  mkdir $model
fi
for f in *.s
do
  if [ -s $f ] ; then
    python3 $GDIR/graphics/plot_errs.py $f $f 12 $tag
  fi
done
mv *.png *.s $model

