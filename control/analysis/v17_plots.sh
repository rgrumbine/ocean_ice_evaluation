#!/bin/bash 
#PBS -N v17plot.out
#PBS -o v17plot.out
#PBS -j oe
#PBS -A ICE-DEV
#PBS -q dev
#PBS -l walltime=0:05:00
#PBS -l select=1:ncpus=1

set -x

module list
source ~/env3.12/bin/activate
export COMROOT=/lfs/h2/emc/gfstemp/emc.global/comroot/retrov17_01_realtime/
export EXDIR=/u/robert.grumbine/rgdev/ocean_ice_evaluation/plotting

cd /u/robert.grumbine/rgdev/ocean_ice_evaluation/control/analysis/

tag=`date +"%Y%m%d"`
for domain in 0 1 2 3
do
  python3 $EXDIR/rtofs_scalar.py $COMROOT/gdas.$tag/00/model/ice/history/gdas.t00z.ic.nc aice_h $domain "v17 $tag ice concentration"

  mv scalar.aice_h${domain}.png v17dom$domain.$tag.png
done
qsub v17_plots_transfer.sh
