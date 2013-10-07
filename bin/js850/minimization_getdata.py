import numpy as np
import sys, os
import shutil
import datetime

"""
to be run from within the data folder.  Will first try to update the datafile,
the will use the datafile to generate force_calls.dat, and the other files used
to generate html

usage:
    python ../gmin_getdata.py /path/to/datafile/ algorithm code contributor
"""

date = datetime.date.today()
datef = date.strftime("%d %b %Y")

datafile = "hits"
algorithm = "unkown"
code = "unkown"
contributor = "Jacob Stevenson"

if len(sys.argv) > 1:
    datafile_orig = sys.argv[1]
    datafile = datafile_orig
    if False and os.path.isfile(datafile_orig):
        if datafile_orig != datafile:
            shutil.copy2(datafile_orig, datafile)
#if len(sys.argv) > 2:
#    algorithm = sys.argv[2]
#if len(sys.argv) > 3:
#    code = sys.argv[3]
#if len(sys.argv) > 4:
#    contributor = sys.argv[4]

data = np.genfromtxt(datafile)
ic=0
iq=1

#timetot = np.sum( data[:,6] )
ncalls = np.sum( data[:,ic] )

nfailed = np.sum( data[:,iq] * -1. + 1 )  # (0,1) -> (1,0)

with open("benchmark.dat", "w") as fout:
    fout.write( "force_calls %.5e\n" % round( np.mean(data[:,ic])))
    fout.write( "force_calls_min %.4e\n" % round( np.min(data[:,ic])))
    fout.write( "force_calls_max %.4e\n" % round( np.max(data[:,ic])))
#    fout.write( "force_calls_per_second %d\n" % int(ncalls/timetot) )
    fout.write( "nfailed %d\n" % int(nfailed) )
#    fout.write( "algorithm %s\n" % algorithm )
#    fout.write( "code %s\n" % code )
#    fout.write( "contributor %s\n" % contributor )
    fout.write( "date %s\n" % datef )

