#!/bin/bash
#--- WCOSS2
#PBS -N ufs_cice_eval
#PBS -o ufs_cice_eval
#PBS -j oe
#PBS -A ICE-DEV
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
# Ursa: 
#source /home/Robert.Grumbine/rg/env3.13/bin/activate
# Wcoss2 
source $HOME/env3.12/bin/activate

#export modelout=$HOME/clim_data/stream4/
export modelout=$HOME/noscrub/v17/
if [ ! -d $modelout ] ; then
  echo could not open v17 output directory $modelout
  exit 1
fi

export model=ufs_cice

export GDIR=$HOME/rgdev/ocean_ice_evaluation/gross/

export start=${start:-20261026}
export end=${end:-`date +"%Y%m%d"`}
#export end=$start
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


time $GDIR/$model/${model}_scan.sh
