import numpy as np
import sys, os
import shutil
import datetime

date = datetime.date.today()
datef = date.strftime("%d %b %Y")

datafile = "hits"
algorithm = "basinhopping"
code = "PyGMIN"
contributor = "Jacob Stevenson"

datafile_orig = "/home/js850/research/benchmark/henkelman/benchmarks/bin/js850/globalopt/pygmin/results"
if os.path.isfile(datafile_orig):
    if datafile_orig != datafile:
        shutil.copy2(datafile_orig, datafile)

data = np.genfromtxt(datafile)

ic=1

with open("benchmark.dat", "w") as fout:
    fout.write( "force_calls %.5e\n" % round( np.mean(data[:,ic])))
    fout.write( "force_calls_min %.4e\n" % round( np.min(data[:,ic])))
    fout.write( "force_calls_max %.4e\n" % round( np.max(data[:,ic])))
    fout.write( "algorithm %s\n" % algorithm )
    fout.write( "code %s\n" % code )
    fout.write( "contributor %s\n" % contributor )
    fout.write( "date %s\n" % datef )
