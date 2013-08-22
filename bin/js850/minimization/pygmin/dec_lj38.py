import numpy as np

from pele.potentials import LJ, BasePotential
from pele.systems import LJCluster
from pele.utils.xyz import read_xyz
from pele.transition_states import findTransitionState
from pele.optimize import Result
#from tools import PotWrapper


class PotWrapperIncr(BasePotential):
    """a LJ potential wrapper to count the number of function calls"""
    ncalls = 0
    def __init__(self, pot, incriment):
        self.pot = pot
        self.incriment = incriment
    def getEnergy(self, coords):
        self.incriment()
        return self.pot.getEnergy(coords)
    def getEnergyGradient(self, coords):
        self.incriment()
        return self.pot.getEnergyGradient(coords)


class LJClusterWrap(LJCluster):
    ncalls = 0
    def get_potential(self):
        lj = LJ()
        def incr(): self.ncalls += 1
        pot = PotWrapperIncr(lj, incr)
        return pot

def get_from_file(fname):
    ret1 = read_xyz(open(f1))
    return ret1.coords

def do_local_connect(system, db):
    natoms = db.minima()[0].coords.size / 3
    system.params.double_ended_connect.local_connect_params.NEBparams.image_density = 4
    system.params.double_ended_connect.local_connect_params.NEBparams.NEBquenchParams["tol"] = 0.01 
    tsparams = system.params.double_ended_connect.local_connect_params.tsSearchParams

    
    tsparams.lowestEigenvectorQuenchParams={"nsteps":20, "tol":0.4}
    tsparams.tol = 1e-3 / np.sqrt(3.*natoms)
#    tsparams.nsteps_tangent1=10, 
#    tsparams.nsteps_tangent2=45, 
#    nfail_max=200,
#    nsteps=1000,
    tsparams.max_uphill_step = 0.2
    tsparams.iprint = 1
    
    print "tolerance", tsparams.tol




    min1, min2 = db.minima()[:2]
    system.ncalls = 0
    connect = system.get_double_ended_connect(min1, min2, db, verbosity=0)
    lcon = connect._getLocalConnectObject()

    climbing_images, neb = lcon._doNEB(min1, min2)
    ncalls_neb = system.ncalls
    images = sorted(range(neb.nimages), key=lambda i: neb.energies[i])
    i = images[-1] #highest energy image
    if i == 0: i += 1
    if i == len(images) - 1: i -= 1

    #get guess for initial eigenvector from NEB tangent
    eigenvec0 = neb.tangent( neb.energies[i], neb.energies[i-1], neb.energies[i+1],
                             neb.distance(neb.coords[i,:], neb.coords[i-1,:])[1],
                             neb.distance(neb.coords[i,:], neb.coords[i+1,:])[1],
                                )

    coords = neb.coords[i,:].copy()
    pot = system.get_potential()
    ret = findTransitionState(coords, pot, eigenvec0=eigenvec0, **lcon.tsSearchParams)

    print "ncalls", system.ncalls, "ncalls from NEB", ncalls_neb
    fres = Result()
    fres.ncalls = system.ncalls
    fres.ncalls_neb = ncalls_neb
    fres.success = ret.success
    fres.neb = neb
    fres.tsres = ret
    return fres

def run(i):
    f1 = "../coords/start_%02d.xyz" % i
    f2 = "../coords/end_%02d.xyz" % i
    ret1 = read_xyz(open(f1))
    ret2 = read_xyz(open(f2))
    
    usegui = False
    natoms = ret1.coords.flatten().size / 3
    system = LJClusterWrap(natoms)
    if usegui:
        db = system.create_database("test.db")
    else:
        db = system.create_database()
    
    pot = system.get_potential()
    x = ret1.coords.flatten()
    E = pot.getEnergy(x)
    db.addMinimum(E, x)
    x = ret2.coords.flatten()
    E = pot.getEnergy(x)
    db.addMinimum(E, x)
    
    if usegui:
        from pele.gui import run_gui
        run_gui(system, "test.db")
    
    
    res = do_local_connect(system, db)
    res.i = i
    res.fname1 = f1
    res.fname2 = f2
    return res
        

def main():
    i = 0
    results = []
    for i in range(50):
        print i
        res = run(i)
        results.append(res)
    
    with open("results.txt", "w") as fout:
        for res in results:
            fout.write("%d %d %d %d\n" % (
                        res.i, res.ncalls, res.ncalls_neb, res.success          ))
        

if __name__ == "__main__":
#    run(3)
    main()