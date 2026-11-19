#!/bin/sh
## wcoss2
#PBS -N edge.persist
#PBS -o edge.persist
#PBS -j oe
#PBS -A ICE-DEV
#PBS -q dev
#PBS -l walltime=6:40:00
#PBS -l select=1:ncpus=1

cd $HOME/rgdev/edges/

. $HOME/rgdev/ocean_ice_evaluation/ice_metrics/edge/bootstrap.sh
export EXDIR=$HOME/rgdev/ocean_ice_evaluation/ice_metrics/exec
export OBSDIR=$HOME/noscrub/model_intercompare/edge.eval/
export FIXDIR=$HOME/noscrub/archive/fix.retired/

# For persistence scoring, NIC vs. NIC
./nicedge_parse.sh
#exit

set -xe 
for dy in 1 2 3 4 5 6 7 8 10 16 365
do
  echo zzz working on $dy day lead
  time python3 dy_score.py 20260101 $dy 
done

./nic_plot_this_year.sh

#exit
## Find UFS (GFSv17 et al.) edges and score them
#time python3 ufs.py
## Produce graphics (relies on ufs_edge_rmse.py)
#echo zzz make ufs score graphics
#time ./ufs_score.sh
#
#exit
# For rtofs scoring (needs nicedge_parse.sh to have run, but doesn't need 
#   the others between there and here
# Find rtofs edges and score them
time python3 rtofs.py
# Produce graphics (relies on rtofs_edge_rmse.py)
echo zzz make rtofs score graphics
time ./rtofs_score.sh
