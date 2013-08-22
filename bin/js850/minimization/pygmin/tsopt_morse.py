import numpy as np

from pele.transition_states import findTransitionState
from pele.systems.morse_bulk import MorseBulk
from pele.potentials import Morse
from pele.potentials import BasePotential
from pele.utils.xyz import read_xyz, write_xyz
from math import sqrt

from tools import read_con_file, PotWrapper, FrozenAtomPotWrapper, MorseBulkFrozen
import tools



def findTS(coords, pot, vec0=None):
    ''' routine to execute a single transition state refinement for the benchmark ''' 
    lowestEigenvectorQuenchParams={"nsteps":100, "tol":0.1}
    lowestEigenvectorQuenchParams={"iprint":-1, "tol":0.02, "maxstep":3. }
    
    tangentSpaceQuenchParams = {"maxstep":2.}
    
    natoms = coords.size / 3
    return findTransitionState(coords, pot,
                               orthogZeroEigs=None,
                               tol=1e-3/sqrt(3.*natoms),
                               eigenvec0=vec0,
                               verbosity=5, 
                               iprint=1,
                               lowestEigenvectorQuenchParams=lowestEigenvectorQuenchParams,
                               tangentSpaceQuenchParams=tangentSpaceQuenchParams,
                               nsteps_tangent1=3, 
                               nsteps_tangent2=25,
                               nsteps=10, 
                               max_uphill_step=2.1,
                               demand_initial_negative_vec=False,
                               )
#    , 
#                               tangentSpaceQuenchParams={"tol": 0.05},
#                               nfail_max=200,
#                               )

def run(fname, reactant_file=None):
    ''' run benchmark for a single configuration '''
    res = read_con_file(fname)
    x = res.coords.flatten()
    boxvec = res.boxvec
    natoms = x.size / 3
    frozen = res.frozen
    frozen_atoms = np.where(frozen)[0]
    
    system = MorseBulkFrozen(natoms, boxvec, rho=1.6047, r0=2.8970, A=0.7102,
                             rcut=9.5, 
                             frozen_atoms=frozen_atoms, reference_coords=x)
    xfree = system.coords_converter.get_reduced_coords(x)
    
    if False:
        from pele.gui import run_gui
#        db = system.create_database("test.sqlite")
        run_gui(system, "test.sqlite")
        exit(1)

    if reactant_file is not None:
        # get a starting vector
        reactantfile = ""
        res = read_con_file(reactant_file)
        x0 = res.coords.flatten()
        x0 = system.coords_converter.get_reduced_coords(x0)
        vec0 = xfree - x0
        vec0 /= np.linalg.norm(vec0)
    
    
    pot = PotWrapper(system.get_potential())
    if False: # for testing only
        e, g = pot.getEnergyGradient(xfree)
        print "recalc rms", np.linalg.norm(g) / np.sqrt(float(g.size)), "norm", np.linalg.norm(g)
    
    print "running ", fname
    ret = findTS(xfree, pot, vec0=vec0)
    ncalls = pot.ncalls
    print "ncalls for %s:" % fname, ncalls, "success", ret.success

    return fname, ncalls, ret.energy, ret.eigenval, ret.rms, ret.nsteps, ret.success

def main():
    results = []
    reactant_file = "../pt-island-con/reactant.con"
    for i in range(49):
        print "\n"
        print i
        results.append(run("../pt-island-con/initial_%d.con" % i, reactant_file=reactant_file))
    
    with open("results.txt", "w") as fout:
        for fname, ncalls, energy, eigenval, rms, nsteps, success in results:
            fout.write( "%s %d %f %g %g %d %d\n" % (fname, ncalls, energy, eigenval, rms, nsteps, success) )

def run_one(i):
    reactant_file = "../pt-island-con/reactant.con"
    return run("../pt-island-con/initial_%d.con" % i, reactant_file=reactant_file)

    
if __name__ == "__main__":
#    run_one(32)
    main()