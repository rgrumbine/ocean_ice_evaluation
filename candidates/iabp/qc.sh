#!/bin/sh

export base=/u/robert.grumbine/

cd $HOME/noscrub/verification/iabp
EXDIR=$HOME/rgdev/ocean_ice_evaluation/candidates/iabp
source $HOME/env3.12/bin/activate
export PYTHONPATH=$PYTHONPATH:$HOME/rgops/mmablib/py

# Shouldn't need changes below here -----------------------

tag=${tag:-`date +"%Y%m%d"`}
tag=20261021

# Filter to 00 utc and since 2026/1/1 (hardwired in iabp_filter) 
cd $tag 
for f in *.dat
do
  python3 $EXDIR/iabp_filter.py $f > ${f}.out
done

find . -maxdepth 1 -type f -name '*.out' -size 0 -exec rm {} \;


# Now qc for speeds: ---------------------------------------

for f in *.dat.out
do
  python3 $EXDIR/iabp_speed.py $f > ${f}.sp 2> ${f}.sp.err
  sort -nr -k 7 ${f}.sp > ${f}.sp.7
done

if [ ! -d err ] ; then
  mkdir err
fi

for f in *.err
do
  if [ -s $f ] ; then
    b=`echo $f | cut -f1 -d\. `
    mv $b.* err
  fi
done

find . -maxdepth 1 -type f -name '*.sp*' -size 0 -exec rm {} \;
