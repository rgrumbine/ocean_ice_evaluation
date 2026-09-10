#!/bin/bash 
#PBS -N rtofsplot.out
#PBS -o rtofsplot.out
#PBS -j oe
#PBS -A ICE-DEV
#PBS -q dev
#PBS -l walltime=0:05:00
#PBS -l select=1:ncpus=1

set -x

module list
source ~/env3.12/bin/activate
export COMROOT=$HOME/noscrub/model_intercompare/
export EXDIR=$HOME/rgdev/ocean_ice_evaluation/plotting

cd /u/robert.grumbine/rgdev/ocean_ice_evaluation/control/analysis

export tag=`date +"%Y%m%d"`
#export tag=20260907
for domain in 0 1 2 3
do
  python3 $EXDIR/rtofs_scalar.py $COMROOT/rtofs_cice/rtofs.$tag/rtofs_glo.t00z.n00.cice_inst.nc aice $domain "RTOFS $tag ice concentration"
  mv scalar.aice${domain}.png rtofs$domain.$tag.png
done

qsub rtofs_plots_transfer.sh
