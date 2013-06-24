import numpy as np
import os
import sys
import time

from pele.potentials.lj import LJ
from pele.optimize import lbfgs_scipy
from pele.optimize import lbfgs_py
from pele.optimize import fire
from pele.optimize import mylbfgs

def getXYZ(fname):
    with open(fname, "r") as fin:
        coords = None
        natoms = 3
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

class PotWrapper():
    """a LJ potential wrapper to count the number of function calls"""
    ncalls = 0
    def __init__(self, pot):
        self.pot = pot
    def getEnergy(self, coords):
        self.ncalls += 1
        return self.pot.getEnergy(coords)
    def getEnergyGradient(self, coords):
        self.ncalls += 1
        return self.pot.getEnergyGradient(coords)

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




class Minimizer(object):
    def __init__(self, label, pot, quencher, newtol=0.01, kwargs = dict(), **morekwargs):
        self.label = label
        self.pot = pot
        self.quencher = quencher
        self.kwargs = dict( kwargs.items() + morekwargs.items() )
        self.kwargs["nsteps"] = 10000
        self.morekwargs = morekwargs
        self.newtol = newtol

        self.ncalls = []
        self.quench_results = []

    def quench( self, coords ):
        coords = np.copy(coords)
        self.pot.ncalls = 0
        #kwargs = dict( self.kwargs.items() + self.morekwargs.items() )
        t0 = time.clock()
        ret = self.quencher( coords, self.pot.getEnergyGradient, **self.kwargs )
        t1 = time.clock()
        self.ncalls.append( self.pot.ncalls )
        print "ncalls", self.pot.ncalls, self.label

        #test tolerance
        newcoords = ret.coords
        e, G = self.pot.getEnergyGradient(newcoords)
        tester = MaxForceOnAtom()
        success = tester(gradient=G, tol=self.newtol) 
        success = int(success)

        rms = np.std(G)
        G = np.reshape(G, [-1,3])
        maxgrad = np.max( np.abs( G.sum(1) ) )
        maxgrad_component = np.max( np.abs( G ) )
        mytime = t1-t0
        qr = QuenchResult()
        qr.ncalls = self.pot.ncalls
        qr.success = success
        qr.energy = e
        qr.rms = rms
        qr.maxgrad = maxgrad
        qr.maxgrad_component = maxgrad_component
        qr.mytime = mytime
        self.quench_results.append( qr )
        


class QuenchBenchmark(object):
    def __init__(self, structuredir = "/home/js850/research/benchmark/henkelman/benchmarks/website/minimization/lj38/lj38-clusters",
            nstructures = 1000 ):
        self.nstructures = nstructures
        self.structuredir = structuredir

        self.minimizers=[]

    def addMinimizer(self, minimizer):
        self.minimizers.append( minimizer )

    def run(self):
        for i in range(self.nstructures):
            fname = self.structuredir +"/"+ mkname(i)
            print "importing data from file", fname
            coords = getXYZ(fname)
            coords = coords.reshape([-1])

            for minimizer in self.minimizers:
                minimizer.quench(coords)


class MaxForceOnAtom(object):
    def __call__( self, gradient = None, tol=None, **kwargs):
        G = np.reshape(gradient, [-1,3] )
        maxgrad = np.max( np.abs( G.sum(1) ) )
        return maxgrad < tol


def main( structuredir = "../../../../../benchmarks/website/minimization/lj38/lj38-clusters",
        nstructures = 1000
        ):

    #make potential
    potLJ = LJ()
    pot = PotWrapper(potLJ)

    benchmarker = QuenchBenchmark( structuredir, nstructures )

    tol = 0.01
    stop_crit = MaxForceOnAtom()

    optimizer_args = dict()
    optimizer_args["tol"] = tol

    if False:
        min_lbfgs_py = Minimizer( "lbfgs_py-M4-new", pot, lbfgs_py, kwargs=optimizer_args, alternate_stop_criterion = stop_crit, M=4 )
        benchmarker.addMinimizer( min_lbfgs_py )

    if True:
        min_lbfgs_py = Minimizer( "lbfgs_py-M1", pot, lbfgs_py, kwargs=optimizer_args, alternate_stop_criterion = stop_crit, M=1 )
        benchmarker.addMinimizer( min_lbfgs_py )
        min_lbfgs_py = Minimizer( "lbfgs_py-M2", pot, lbfgs_py, kwargs=optimizer_args, alternate_stop_criterion = stop_crit, M=2 )
        benchmarker.addMinimizer( min_lbfgs_py )
        min_lbfgs_py = Minimizer( "lbfgs_py-M6", pot, lbfgs_py, kwargs=optimizer_args, alternate_stop_criterion = stop_crit, M=6 )
        benchmarker.addMinimizer( min_lbfgs_py )
        min_lbfgs_py = Minimizer( "lbfgs_py-M8", pot, lbfgs_py, kwargs=optimizer_args, alternate_stop_criterion = stop_crit, M=8 )
        benchmarker.addMinimizer( min_lbfgs_py )
        min_lbfgs_py = Minimizer( "lbfgs_py-M10", pot, lbfgs_py, kwargs=optimizer_args, alternate_stop_criterion = stop_crit, M=10 )
        benchmarker.addMinimizer( min_lbfgs_py )
        min_lbfgs_py = Minimizer( "lbfgs_py-M20", pot, lbfgs_py, kwargs=optimizer_args, alternate_stop_criterion = stop_crit, M=20 )
        benchmarker.addMinimizer( min_lbfgs_py )
    if True:
        mymin = Minimizer( "mylbfgs-M1", pot, mylbfgs, kwargs=optimizer_args, alternate_stop_criterion = stop_crit, M=1 )
        benchmarker.addMinimizer( mymin )
        mymin = Minimizer( "mylbfgs-M2", pot, mylbfgs, kwargs=optimizer_args, alternate_stop_criterion = stop_crit, M=2 )
        benchmarker.addMinimizer( mymin )
        mymin = Minimizer( "mylbfgs-M4", pot, mylbfgs, kwargs=optimizer_args, alternate_stop_criterion = stop_crit, M=4 )
        benchmarker.addMinimizer( mymin )
        mymin = Minimizer( "mylbfgs-M6", pot, mylbfgs, kwargs=optimizer_args, alternate_stop_criterion = stop_crit, M=6 )
        benchmarker.addMinimizer( mymin )
        mymin = Minimizer( "mylbfgs-M8", pot, mylbfgs, kwargs=optimizer_args, alternate_stop_criterion = stop_crit, M=8 )
        benchmarker.addMinimizer( mymin )
        mymin = Minimizer( "mylbfgs-M10", pot, mylbfgs, kwargs=optimizer_args, alternate_stop_criterion = stop_crit, M=10 )
        benchmarker.addMinimizer( mymin )
        mymin = Minimizer( "mylbfgs-M20", pot, mylbfgs, kwargs=optimizer_args, alternate_stop_criterion = stop_crit, M=20 )
        benchmarker.addMinimizer( mymin )
    if True:
        mymin = Minimizer( "mylbfgs-M4-maxstep0.05", pot, mylbfgs, kwargs=optimizer_args, alternate_stop_criterion = stop_crit, M=4, maxstep=0.05 )
        benchmarker.addMinimizer( mymin )
        mymin = Minimizer( "mylbfgs-M4-maxstep0.1", pot, mylbfgs, kwargs=optimizer_args, alternate_stop_criterion = stop_crit, M=4, maxstep=0.1 )
        benchmarker.addMinimizer( mymin )
        mymin = Minimizer( "mylbfgs-M4-maxstep0.2", pot, mylbfgs, kwargs=optimizer_args, alternate_stop_criterion = stop_crit, M=4, maxstep=0.2 )
        benchmarker.addMinimizer( mymin )


    if False:
        min_lbfgs_py = Minimizer( "lbfgs_py", pot, lbfgs_py, kwargs=optimizer_args, alternate_stop_criterion = stop_crit )
        benchmarker.addMinimizer( min_lbfgs_py )

        min_mylbfgs = Minimizer( "mylbfgs", pot, mylbfgs, kwargs=optimizer_args, alternate_stop_criterion = stop_crit )
        benchmarker.addMinimizer( min_mylbfgs )

    if False:
        min_lbfgs_scipy = Minimizer( "lbfgs_scipy", pot, lbfgs_scipy, kwargs=optimizer_args, tol=.005 )
        benchmarker.addMinimizer( min_lbfgs_scipy )

    if True:
        min_fire = Minimizer( "fire", pot, fire, kwargs=optimizer_args, alternate_stop_criterion = stop_crit )
        benchmarker.addMinimizer( min_fire )

    benchmarker.run()

    for minimizer in benchmarker.minimizers:
        print ""
        print ""
        print minimizer.label
        ncalls = np.array( minimizer.ncalls )
        if True:
            print "mean ncalls", np.mean(ncalls)
            print "max ncalls", np.max(ncalls)
            print "min ncalls", np.min(ncalls)

        if True:
            fname = minimizer.label + ".ncalls"
            with open(fname, "w") as fout:
                fout.write( QuenchResult.header() + "\n" )
                for qr in minimizer.quench_results:
                    fout.write( qr.datastring() + "\n" )



if __name__ == "__main__":
    main()





