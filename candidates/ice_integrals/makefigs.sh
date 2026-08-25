#!/bin/sh
#Robert Grumbine
#22 Apr 2026

#ursa:
source ~/rg/env3.13/bin/activate
#wcoss: source ~/env3.12/bin/activate

# Get the NSIDC extent files for reference
./get02135.sh

#stream2: 20240601-20241130
#stream3: 20241201-20250531
#realtime: 20251121-20260211, et seq.
tag=20250601
while [ $tag -le 20260409 ]
do
  echo $tag

  if [ ! -f int.$tag ] ; then
    if [ -d gfs.$tag ] ; then
      time python3 integrals.py gfs.$tag $tag > int.$tag
    fi
  fi

  if [ -f int.$tag ] ; then
    if [ ! -f overlay_$tag.png ] ; then
      yy=`echo $tag | cut -c1-4`
      mm=`echo $tag | cut -c5-6`
      dd=`echo $tag | cut -c7-8`
      time python3 ufsfcst.py $yy $mm $dd int.$tag
      mv overlay.png overlay_$tag.png
    fi
  fi

  tag=`expr $tag + 1`
  tag=`$HOME/bin/dtgfix3 $tag`
done
