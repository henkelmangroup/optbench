import numpy as np

from pygmin.potentials.lj import LJ
from pygmin.optimize.transition_state.transition_state_refinement import findTransitionState
import pygmin.defaults as defaults

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

def getStructures(nfiles=200, directory="ts_candidates", prefix="ts_candidate"):
    for i in range(nfiles):
        fname = "%s/%s.%04d" % (directory, prefix, i)
        coords = np.genfromtxt(fname)
        yield coords, i, fname

def findTS(coords, pot):
    eigparams = defaults.lowestEigenvectorQuenchParams
    eigparams["tol"] = 1e-3
    eigparams["maxstep"] = 0.2
    eigparams["nsteps"] = 500
    ret = findTransitionState(coords, pot, tol=1e-3, nsteps=100)
    return ret


def main():
    potlj = LJ()
    pot = PotWrapper(potlj)
    resultsfname = "results"
    results = []
    for coords, ncount, fname in getStructures():
        coords = np.reshape(coords, [-1])
        pot.ncalls = 0
        ret = findTS(coords, pot)
        ncalls = pot.ncalls
        print "ncalls", ncalls, ncount

        results.append( (ncalls, ret.energy, ret.eigenval, ret.rms, ret.nsteps) )


        if False:
            #save ts coords
            tsfname = fname + ".ts"
            with open(tsfname, "w") as fout:
                tscoords = ret.coords
                tscoords = np.reshape(tscoords, [-1,3])
                for i in range(len(tscoords[:,0])):
                    fout.write( "%f %f %f\n" % tuple(tscoords[i,:]) )
    
    if True:
        #print results
        with open("results", "w") as fout:
            for ncalls, energy, eigenval, rms, nsteps in results:
                fout.write( "%d %f %g %g %d\n" % (ncalls, energy, eigenval, rms, nsteps) )


if __name__ == "__main__":
    main()



