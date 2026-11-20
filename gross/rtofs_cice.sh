#!/bin/bash
#--- WCOSS2
#PBS -N rtofs_ice_eval
#PBS -o rtofs_ice_eval
#PBS -j oe
#PBS -A ICE-DEV
#PBS -l walltime=6:00:00
#PBS -l select=1:ncpus=1
#--- WCOSS2

## --- Ursa
##SBATCH -J hr5
##SBATCH -e hr5.err
##SBATCH -o hr5.out
##SBATCH -t 5:55:00
##SBATCH -q batch
##SBATCH -A marine-cpu
##SBATCH -N 1
##SBATCH --mail-type FAIL
##SBATCH --mail-user robert.grumbine@noaa.gov
## --- Ursa

set -xe

# Ursa:
#source /home/Robert.Grumbine/rg/env3.13/bin/activate
# Wcoss2
source $HOME/env3.12/bin/activate

export model=rtofs_cice
export MODEL=rtofs_cice

export modelout=$HOME/noscrub/model_intercompare/$MODEL
if [ ! -d $modelout ] ; then
  echo could not find model output directory $modelout
  exit 1
fi
export GDIR=$HOME/rgdev/ocean_ice_evaluation/gross/
if [ ! -d $GDIR ] ; then
  echo could not find gross check source directory $GDIR
  exit 1
fi

export start=20260801
export end=`date +"%Y%m%d"`
end=`expr $end - 1`
end=`$HOME/bin/dtgfix3 $end`
end=`expr $end - 1`
end=`$HOME/bin/dtgfix3 $end`
#export end=20260804
echo $start $end

#------------------------ General across platforms --------------
set -x

export level=extreme

export PYTHONPATH=$PYTHONPATH:$GDIR/gross

if [ ! -d $HOME/scratch/gross/$model ] ; then
  mkdir -p  $HOME/scratch/gross/$model
  if [ $? -ne 0 ] ; then
    echo zzz could not create rundir  $HOME/scratch/gross/$model
    exit 1
  fi
fi 
cd  $HOME/scratch/gross/$model

ln -sf $GDIR/curves curves
time $GDIR/$MODEL/${MODEL}_scan.sh

