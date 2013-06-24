import numpy as np
import pickle

from pygmin.NEB.NEB import NEB
from pygmin.mindist.minpermdist_stochastic import minPermDistStochastic as mindist
from pygmin.potentials.lj import LJ
from pygmin.optimize.quench import lbfgs_py
from pygmin.optimize.quench import quench as lbfgs_scipy
import pygmin.defaults as defaults


def getTSCandidate(coords1, coords2, pot):
    neb = NEB(coords1, coords2, pot)
    defaults.NEBquenchRoutine = lbfgs_py
    #defaults.NEBquenchRoutine = lbfgs_scipy
    #defaults.NEBquenchParams["debug"] = True
    defaults.NEBquenchParams["iprint"] = 50
    defaults.NEBquenchParams["nsteps"] = 200
    neb.optimize()
    maxi = np.argmax( neb.energies )
    return neb.coords[maxi,:]


def main():
    pot = LJ()
    natoms = 38
    with open("coords.1.dat", "rb") as fin:
        count = 0
        for coords1, coords2, path_array in pickle.load( fin ):
            ret1 = lbfgs_py(coords1, pot.getEnergyGradient)
            ret2 = lbfgs_py(coords2, pot.getEnergyGradient)
            coords1 = ret1[0]
            coords2 = ret2[0]
            dist, coords1, coords2 = mindist(coords1, coords2, permlist=[range(natoms)])
            print "mindist dist", dist

            tscoords = getTSCandidate(coords1, coords2, pot)
            tscoords = np.reshape( tscoords, [-1,3] )
            outfname = "ts_candidates/ts_candidate.%04d" % count
            with open(outfname, "w") as fout:
                for i in range(natoms):
                    fout.write( "%f %f %f\n" % tuple( tscoords[i,:] ) )

            count += 1



if __name__ == "__main__":
    main()





