#!/bin/sh
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
export FIXDIR=$HOME/noscrub/archive/alt.fix/

set -xe

# Find UFS (GFSv17 et al.) edges and score them
time python3 ufs.py
# Produce graphics (relies on ufs_edge_rmse.py)
echo zzz make ufs score graphics
time ./ufs_score.sh

