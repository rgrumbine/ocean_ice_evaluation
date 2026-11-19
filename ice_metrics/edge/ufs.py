"""
Requires environment to provide:
    variables FIXDIR, EXDIR
    data files  skip_hr, seaice_alldist.bin 
    executables cscore_edge, find_edge_ufs

Currently hard codes (dbase) path to ufs cice output directories

Robert Grumbine
27 July 2023
"""
import os
import sys
import datetime

#------------------------------------------------------------

fixdir = os.getenv('FIXDIR')
if (type(fixdir) == str ):
    print("fixdir = ",fixdir)
else:
    print("Could not find environment variable FIXDIR")
    sys.exit(1)

exdir  = os.getenv('EXDIR')
if (type(exdir) == str):
    print("exdir = ",exdir)
else:
    print("Could not find environment variable EXDIR")
    sys.exit(1)

if (not os.path.exists(fixdir+"/skip_hr") ):
  print("could not find the required skip file")
  print("fixdir = ",fixdir)
  sys.exit(1)

#dbase="/u/robert.grumbine/noscrub/model_intercompare/rtofs_cice/rtofs."
dbase="/u/robert.grumbine/noscrub/v17/gfs."

dt    = datetime.timedelta(1)
start = datetime.datetime(2026,1,1)
#end   = datetime.datetime.today()
end   = datetime.datetime(2026,10,31)
end  -= 16*dt

#------------------------------------------------------------


while (start <= end):
  dy  = start.strftime("%03j")
  print("dy = ",dy, flush=True)
  valid    = start

  #valid -= dt
  nlead=0
  for lead in ("f006", "f024", "f048", "f072", "f096", "f120", "f144", "f168", "f192",
               "f216", "f240", "f264", "f288", "f312", "f336", "f360", "f384"):
    fname   = dbase+start.strftime("%Y%m%d")+"/00/model/ice/history/gfs.t00z.6hr_avg."+lead+".nc"

    valid_dy = valid.strftime("%03j")
    yy       = valid.strftime("%Y")

    for crit in (0.01, 0.03, 0.05, 0.10, 0.15 ):
      if (os.path.exists(fname)):
        critstring="{:3.2f}".format(crit)

        outname = "ufs_edges/ufs.edge."+lead+"."+start.strftime("%Y%m%d")+critstring

        if ( not os.path.exists(outname)):
          #find the edge:
          cmd=exdir+'/find_edge_ufs '+fixdir+"/skip_hr "+ fname +" "+critstring+" > "+outname
          #debug: print(cmd, flush=True)
          retval = os.system(cmd)
          if (retval != 0 ):
              print("Error ",retval,"in trying to run ",cmd)
              sys.exit(2)

        #score it:
        snamer = "ufs_scores/nr."+"{:1d}".format(nlead)+"."+start.strftime("%Y%m%d")+critstring
        sname  = "ufs_scores/n."+"{:1d}".format(nlead)+"."+start.strftime("%Y%m%d")+critstring

        if (not os.path.exists(sname)):
          cmd =  exdir+'/cscore_edge '+fixdir+'/seaice_alldist.bin ' + outname +' cleaned/n.'+yy+valid_dy+'.beta 50. > '+sname
          #debug print(cmd, flush=True)
          os.system(cmd)

        if (not os.path.exists(snamer)):
          cmd =  exdir+'/cscore_edge '+fixdir+'/seaice_alldist.bin ' + 'cleaned/n.'+yy+valid_dy+'.beta ' + outname + ' 50. > '+snamer
          #debug print(cmd, flush=True)
          os.system(cmd)
      else:
        print("could not find model file:",fname, flush=True)

    valid += dt
    nlead += 1

  start += dt
