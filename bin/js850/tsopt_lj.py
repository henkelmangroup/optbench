import numpy as np
import argparse
import os, sys

print os.path.dirname(__file__)
sys.path.insert(0, os.path.dirname(__file__))

from pele.optimize import mylbfgs
from pele.transition_states import findTransitionState, findLowestEigenVector
from pele.systems import LJCluster
from pele.potentials import BasePotential
from pele.utils.xyz import read_xyz, write_xyz

from findTS_local import findTS

np.random.seed(0)

#def findTS(coords, pot, first_order=True):
#    ''' routine to execute a single transition state refinement for the benchmark ''' 
#    lowestEigenvectorQuenchParams={"nsteps":101, "tol":0.1}
#    return findTransitionState(coords, pot, tol=1e-3/np.sqrt(3.*38.), 
#                               lowestEigenvectorQuenchParams=lowestEigenvectorQuenchParams,
#                               tangentSpaceQuenchParams={"tol":0.05},#, "maxstep":.05},
#                               demand_initial_negative_vec=False,
#                               nsteps_tangent1=4, 
#                               nsteps_tangent2=26, 
#                               nfail_max=200,
#                               nsteps=1001,
#                               max_uphill_step=0.051,
#                               first_order=first_order,
#                               )
#
#def findTS_gen_dimer(coords, pot, first_order=True):
#    ''' routine to execute a single transition state refinement for the benchmark ''' 
#    print "starting findts Gen dimer"
#    dimer = GeneralizedDimer(
#                    coords, pot,
#                    translational_steps=7, 
#                    rotational_steps=20,
#                    leig_kwargs=dict(tol=1e-1,
#                                     iprint=1,
#                                     dx=1e-6,
#                                     maxstep=1.,
#                                     first_order=first_order
#                                     ),
#                    minimizer_kwargs=dict(tol=1e-3 / np.sqrt(3.*38.), 
#                                          maxstep=.2,
#                                          iprint=1,
#                                          ),
#                                    )
#    ret = dimer.run()
##    dimer = GeneralizedDimer(pot, findLowestEigenVector, eigenvec0, H0_evec=H0, 
##                             leig_tol=1e-4,
##                             n_translational_steps=5, n_rotational_steps=10)
##    ret = mylbfgs(coords, dimer, tol=1e-3/sqrt(3.*38.), maxstep=.4)
##    ret.energy = dimer.energy
##    ret.eigenval = dimer.eigenval
#    
#    
#    return ret
    

class PotWrapper(BasePotential):
    ''' a LJ potential wrapper to count the number of function calls '''
    def __init__(self, pot):
        self.pot = pot
        self.ncalls = 0

    def getEnergy(self, coords):
        self.ncalls += 1
        return self.pot.getEnergy(coords)
    def getEnergyGradient(self, coords):
        self.ncalls += 1
        return self.pot.getEnergyGradient(coords)

def run(fname, generalized_dimer=False, first_order=False):
    ''' run benchmark for a single configuration '''
    system = LJCluster(38)
    pot = PotWrapper(system.get_potential())
    print ""
    print "running ", fname
    xyz = read_xyz(open(fname))
    ret = findTS(xyz.coords.flatten(), pot)
    ncalls = pot.ncalls
    print "ncalls for %s:"%fname, ncalls, "success", ret.success

    return fname, ncalls, ret.energy, ret.eigenval, ret.rms, ret.nsteps, ret.success

def main():
    np.random.seed(0)
#    import sys
    parser = argparse.ArgumentParser(description="optimize transition state for LJ")
    parser.add_argument("-n", type=int, default=-1, help="do only this number")
#    parser.add_argument("-g", action="store_true", help="use generalized dimer method")
#    parser.add_argument("--first-order", action="store_true", help="use the forward finite differences first order method")
    args = parser.parse_args()
#    print args
    
    if args.n >= 0:
        run("coords-xyz/%04d.xyz" % args.n)
        return
    
    results = []
    for i in range(200):
        results.append(run("coords-xyz/%04d.xyz"%i))
    
    with open("results.txt", "w") as fout:
        for fname, ncalls, energy, eigenval, rms, nsteps, success in results:
            fout.write( "%s %d %f %g %g %d %d\n" % (fname, ncalls, energy, eigenval, rms, nsteps, success) )

if __name__ == "__main__":
    main()
