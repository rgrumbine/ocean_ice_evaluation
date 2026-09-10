#!/bin/bash 
#PBS -N rtofstran.out
#PBS -o rtofstran.out
#PBS -j oe
#PBS -A XFER-DEV
#PBS -q dev_transfer
#PBS -l walltime=0:01:00
#PBS -l select=1:ncpus=1

set -x

cd /u/robert.grumbine/rgdev/ocean_ice_evaluation/control/analysis

tag=${tag:-`date +"%Y%m%d"`}

for domain in 0 1 2 3
do
  scp rtofs$domain.$tag.png rgrumbine@emcrzdm:rgweb/ice/analy/
  scp rtofs$domain.$tag.png rgrumbine@emcrzdm:rgweb/ice/analy/rtofs$domain.png
done

