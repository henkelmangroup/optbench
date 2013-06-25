import numpy as np

from pele.transition_states import findTransitionState
from pele.systems import LJCluster
from pele.potentials import BasePotential
from pele.utils.xyz import read_xyz, write_xyz
from math import sqrt

def findTS(coords, pot):
    ''' routine to execute a single transition state refinement for the benchmark ''' 
    lowestEigenvectorQuenchParams={"nsteps":100, "tol":0.1}
    return findTransitionState(coords, pot, tol=1e-3/sqrt(3.*38.), nsteps_tangent1=3, 
                              nsteps_tangent2=25, nfail_max=200,nsteps=1000,
                              max_uphill_step=0.1,
                              tangentSpaceQuenchParams={"tol": 0.05},
                              lowestEigenvectorQuenchParams=lowestEigenvectorQuenchParams,
                              demand_initial_negative_vec=False)

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

def run(fname):
    ''' run benchmark for a single configuration '''
    system = LJCluster(38)
    pot = PotWrapper(system.get_potential())
    print "running ", fname
    xyz = read_xyz(open(fname))
    ret = findTS(xyz.coords.flatten(), pot)
    ncalls = pot.ncalls
    print "ncalls for %s:"%fname, ncalls, "success", ret.success

    return fname, ncalls, ret.energy, ret.eigenval, ret.rms, ret.nsteps, ret.success

if __name__ == "__main__":
    results = []
    for i in range(200):
        results.append(run("coords-xyz/%04d.xyz"%i))
    
    with open("results.txt", "w") as fout:
        for fname, ncalls, energy, eigenval, rms, nsteps, success in results:
            fout.write( "%s %d %f %g %g %d %d\n" % (fname, ncalls, energy, eigenval, rms, nsteps, success) )
