import numpy as np
import os
import sys
import time
import subprocess

from pygmin.potentials.lj import LJ

def getXYZ(fname):
    with open(fname, "r") as fin:
        coords = None
        natoms = 3 #will be overwritten
        for i, line in enumerate(fin):
            if i == 0:
                natoms = int(line.split()[0])
                coords = np.zeros([natoms,3])
            elif i == 1:
                pass
            elif i <= natoms + 1:
                sline = line.split()
                coords[i-2,:] = [float(s) for s in sline[1:4]]
    return coords

def mkname(n):
    return "cluster_%04d.xyz" % n

def getCoords(nfiles=1000, directory = "/home/js850/research/benchmark/henkelman/benchmarks/website/minimization/lj38/lj38-clusters" ):
    """
    a generator return the coords one at a time
    """
    for i in range(nfiles):
        fname = directory + "/" + mkname(i)
        coords = getXYZ(fname)
        yield coords, fname








class MaxForceOnAtom(object):
    def __call__( self, gradient = None, tol=None, **kwargs):
        G = np.reshape(gradient, [-1,3] )
        maxgrad = np.max( np.abs( G.sum(1) ) )
        return maxgrad < tol

class QuenchResult(object):
    def __init__(self):
        self.ncalls = 0
        self.success = 0
        self.energy = 0.
        self.rms = 0.
        self.maxgrad = 0.
        self.maxgrad_component = 0.
        self.mytime = 0.
    @staticmethod
    def header():
        return "#nfuncalls success energy rms maxgrad maxgrad_component time"
    def datastring(self):
        return "%d %d %f %g %g %g %g" % (self.ncalls, self.success, self.energy, self.rms, self.maxgrad, self.maxgrad_component, self.mytime)

def doQuench( tol = 0.01, GMIN = "/home/js850/git/GMIN/source/build/GMIN" ):
    #run GMIN
    t0 = time.clock()
    subprocess.call( GMIN )
    t1 = time.clock()

    GMINout = "output"
    #now try to extract the important information from the output file
    if False:
        with open(GMINout, "r") as fin:
            for line in fin:
                sline = line.split()
                if sline[0] == "Qu":
                    if sline[1] == "0":
                        energy = float(sline[3])
                        steps = int(sline[5])
                        rms = float(sline[7])
                        time_internal = float(sline[12])
                        break
    if True:
        with open(GMINout, "r") as fin:
            for line in fin:
                sline = line.split()
                if "NPCALL" in line:
                    energy = float(sline[4])
                    rms = float(sline[5])
                    steps = int(sline[7])
                    ncalls = int(sline[13])
                    gmax = float(sline[15])
                elif len(sline) >= 2: 
                    #end when the 0th quench is reported
                    if sline[0] == "Qu" and sline[1] == "0":
                        break
    
    qr = QuenchResult()
    qr.ncalls = ncalls #not really
    qr.success = gmax <= tol
    qr.energy = energy
    qr.rms = rms
    qr.maxgrad = gmax
    #qr.maxgrad_component = maxgrad_component
    qr.mytime = t1-t0
    #print "time internal", time_internal
    return qr



def main( structuredir = "/home/js850/research/benchmark/henkelman/benchmarks/website/minimization/lj38/lj38-clusters",
        nstructures = 1000
        ):

    #make potential
    pot = LJ()
    natoms = 38

    quench_results = []
    for coords, fname in getCoords():
        #subtract center of mass
        print fname
        com = coords.sum(0) / len(coords[:,0])
        coords -= com
        with open("coords", "w") as fout:
            for i in range(natoms):
                fout.write("%lf %lf %lf\n" % tuple(coords[i,:]) )
        qr = doQuench() 
        #print qr.header()
        print qr.datastring()
        quench_results.append( qr)


    if True:
        print ""
        print ""
        ncalls = np.array( [qr.ncalls for qr in quench_results] )
        if True:
            print "mean ncalls", np.mean(ncalls)
            print "max ncalls", np.max(ncalls)
            print "min ncalls", np.min(ncalls)

        if True:
            label = "gmin"
            fname = label + ".ncalls"
            with open(fname, "w") as fout:
                fout.write( QuenchResult.header() + "\n" )
                for qr in quench_results:
                    fout.write( qr.datastring() + "\n" )



if __name__ == "__main__":
    main()





