#!/bin/bash 
#PBS -N v17tran.out
#PBS -o v17tran.out
#PBS -j oe
#PBS -A XFER-DEV
#PBS -q dev_transfer
#PBS -l walltime=0:05:00
#PBS -l select=1:ncpus=1

set -x

cd /u/robert.grumbine/rgdev/ocean_ice_evaluation/control/analysis

tag=`date +"%Y%m%d"`
for domain in 0 1 2 3
do
  scp v17dom$domain.$tag.png rgrumbine@emcrzdm:rgweb/ice/analy/
  scp v17dom$domain.$tag.png rgrumbine@emcrzdm:rgweb/ice/analy/v17dom$domain.png
done

