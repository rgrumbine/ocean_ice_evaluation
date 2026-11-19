#!/bin/bash
#--- WCOSS2
#PBS -N ufs_cice_eval
#PBS -o ufs_cice_eval
#PBS -j oe
#PBS -A ICE-DEV
#PBS -q batch
#PBS -l walltime=4:00:00
#PBS -l select=1:ncpus=1
#--- WCOSS2

## --- Ursa
##SBATCH -J ufs
##SBATCH -e ufs.err
##SBATCH -o ufs.out
##SBATCH -t 5:55:00
##SBATCH -q batch
##SBATCH -A marine-cpu
##SBATCH -N 1
##SBATCH --mail-type FAIL
##SBATCH --mail-user robert.grumbine@noaa.gov
## --- Ursa


set -xe
#ursa: 
#source /home/Robert.Grumbine/rg/env3.13/bin/activate
#wcoss2 
source $HOME/env3.12/bin/activate

#export modelout=$HOME/clim_data/rtofs_gross
#export modelout=/scratch1/NCEPDEV/climate/Lydia.B.Stefanova/Models/ufs_hr1/SeaIce/
export modelout=$HOME/noscrub/v17/
#export modelout=$HOME/clim_data/stream4/
if [ ! -d $modelout ] ; then
  echo could not open v17 output directory $modelout
  exit 1
fi

export modeltag=ufs_cice

export GDIR=$HOME/rgdev/ocean_ice_evaluation/gross/

export start=${start:-20261026}
export end=${end:-20261117}
#export end=$start
#------------------------ General across platforms --------------
set -x

export level=extreme

export PYTHONPATH=$PYTHONPATH:$GDIR/gross

if [ ! -d $HOME/scratch/gross/$modeltag ] ; then
  mkdir -p  $HOME/scratch/gross/$modeltag
  if [ $? -ne 0 ] ; then
    echo zzz could not create rundir  $HOME/scratch/gross/$modeltag
    exit 1
  fi
fi 
cd  $HOME/scratch/gross/$modeltag
ln -sf $GDIR/curves curves

set -x
for model in ufs_cice
do
  export MODEL=$model
  time $GDIR/$MODEL/${MODEL}_scan.sh
  # Now that all results have been scanned, check for errors:
done
