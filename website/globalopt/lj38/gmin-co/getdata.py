import numpy as np
import sys, os
import shutil
import datetime
import argparse

parser = argparse.ArgumentParser(description="create file benchmarks.dat from a results file")
parser.add_argument("--datafile", type=str, help="results file to read from", default="results.txt")
args = parser.parse_args()

date = datetime.date.today()
datef = date.strftime("%d %b %Y")

datafile = args.datafile
algorithm = "hybrid eigenvector following"
code = "pele"
contributor = "Jacob Stevenson"

data = np.genfromtxt(datafile)
ncalls = []
nquenches = []
for i in range(data.shape[0]):
    if data[i,-1] == 0:
        data[i,1] = 10000
    else:
        ncalls.append(data[i,1])
        nquenches.append(data[i,2])
ncalls = np.array(ncalls)
nquenches = np.array(nquenches)

with open("benchmark.dat", "w") as fout:
    fout.write( "basin_hopping_steps_mean %.5e\n" % round( np.mean(nquenches)))
    fout.write( "basin_hopping_steps_stddev %.5e\n" % round( np.std(nquenches)))
    fout.write( "force_calls_mean %.5e\n" % round( np.mean(ncalls)))
    fout.write( "force_calls_stddev %.5e\n" % round( np.std(ncalls)))
    fout.write( "nfailed %d\n" % np.sum(1. - data[:,-1]) )
#    fout.write( "algorithm %s\n" % algorithm )
#    fout.write( "code %s\n" % code )
#    fout.write( "contributor %s\n" % contributor )
    fout.write( "date %s\n" % datef )

