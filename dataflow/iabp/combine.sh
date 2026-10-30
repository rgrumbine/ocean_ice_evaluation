#!/bin/sh
# Robert Grumbine
# 29 October 2026

base=`pwd`
ref=20261027
end=20261001

tag=`expr $ref - 1`
tag=`$HOME/bin/dtgfix3 $tag`

echo $tag
cd $base/$ref

while [ $tag -ge $end ]
do
   echo $base $tag

   if [ -d $base/$tag ] ; then
     cd $base/$tag
     find . -maxdepth 1 -type f -name '*.dat' -exec ifm {} $base/$ref \;
   fi
   tag=`expr $tag - 1 `
   tag=`$HOME/bin/dtgfix3 $tag`
done
