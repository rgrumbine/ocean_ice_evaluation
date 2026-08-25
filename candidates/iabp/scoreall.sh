#!/bin/sh
#Robert Grumbine
#22 Apr 2026

for f in *.sp
do
  if [ -s $f ] ; then
    python3 make_fcsts.py 20251210 8 $f > $f.verf
  fi
done
