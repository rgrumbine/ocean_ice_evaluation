#!/bin/sh

cd $HOME/noscrub/verification/iabp
EXDIR=$HOME/rgdev/ocean_ice_evaluation/candidates/iabp
source $HOME/env3.12/bin/activate

# Shouldn't need changes below here -----------------------

tag=`date +"%Y%m%d"`
tag=20261021

cd $tag 
for f in *.dat
do
  python3 $EXDIR/iabp_filter.py $f > ${f}.out
done

find . -maxdepth 1 -type f -name '*.out' -size 0 -exec rm {} \;
