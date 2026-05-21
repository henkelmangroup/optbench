import numpy as np



from pele.potentials import LJ
from pele.systems import LJCluster
import pele.basinhopping as bh
from pele.takestep import displace
from pele.takestep import adaptive
from pele.optimize import mylbfgs as lbfgs
from pele.storage.savenlowest import SaveN as saveit
from pele.utils.xyz import read_xyz
from pele.optimize import Result


from tools import LJClusterWrap


#class PotWrapper():
#    """a LJ potential wrapper to count the number of function calls"""
#    ncalls = 0
#    def __init__(self, pot):
#        self.pot = pot
#    def getEnergy(self, coords):
#        self.ncalls += 1
#        return self.pot.getEnergy(coords)
#    def getEnergyGradient(self, coords):
#        self.ncalls += 1
#        return self.pot.getEnergyGradient(coords)

def getStartingStructure(fname = "/home/js850/research/benchmark/henkelman/benchmarks/website/globalopt/min_structure.con", natoms=38):
    coords = np.zeros( [natoms,3] )
    J = 11
    with open(fname, "r") as fin:
        for i, line in enumerate(fin):
            sline = line.split()
            if i >= J:
                coords[i-J,:] = [ float(s) for s in sline[:3] ]
    print coords.shape
    print coords
    return coords

def globalOpt( E_globmin=None, coords=None, nquenches=100000, Etol=1e-3):
    natoms = 38
    system = LJClusterWrap(natoms)
    pot = system.get_potential()

    if E_globmin is None:
        if False:
            gmin_coords = np.genfromtxt("38_globopt.coords")
            gmin_coords = np.reshape(gmin_coords, [-1])
            ret = lbfgs( gmin_coords, pot.getEnergyGradient, iprint=-1 )
            E_globmin = ret[1]
        else:
            E_globmin = -173.9284
        print "Energy of global minimum", E_globmin


    if coords is None:
        #get an initial random set of minimized coordinates
        coords=np.random.random(3*natoms)
        ret = lbfgs( coords, pot.getEnergyGradient, iprint=20 )
        coords = ret[0]


    system.params.structural_quench_params.tol = 1e-3
    system.params.basinhopping.temperature = 1.

    takeStep = displace.RandomDisplacement(stepsize=0.41)
    tsAdaptive = adaptive.AdaptiveStepsize(takeStep, acc_ratio=0.5, interval=100)

    system.ncalls = 0
    db = system.create_database()
    opt = system.get_basinhopping(database=db, takestep=tsAdaptive, coords=coords,
                                  )
    opt.printfrq = 100

    success = False
    for i in range(nquenches):
        opt.run(1)
        if opt.markovE <= E_globmin + Etol:
            print "found global minimum", opt.markovE, E_globmin
            success = True
            break
        if i % 100 == 1:
            print i, "number of function calls", system.ncalls, float(pot.ncalls)/i
            print i, "lowest structure found", db.minima()[0].energy


    ncalls = system.ncalls
    print "final number of function calls", ncalls

    if True:
        print "lowest structure found", db.minima()[0].energy

    res = Result()
    res.ncalls = ncalls
    res.nquenches = i
    res.energy = db.minima()[0].energy
    res.success = success
#    return {"nfuncalls":ncalls, "nquenches":i, "lowestE":db.minima()[0].energy, "success":success}
    return res

def run_one(i):
    sdir = "100_lj38"
    fname = sdir + "/%d.xyz" % i
    print "\n\n", fname
    coords = read_xyz(open(fname)).coords.flatten()
    return globalOpt(coords=coords)
    
    

def main():
    results = []
    for i in range(100):
        res = run_one(i)
        res.i = i
        results.append(res)
        
    
    with open("results.txt", "w") as fout:
        for res in results:
            out = [res.i, res.ncalls, res.energy, int(res.success)]
            outs = " ".join(map(str, out))
            fout.write(outs + "\n")
        
            
        
    
    

#def runGlobalOpt(niter=100, nquenches=100000, onestart=True):
#    startcoords = getStartingStructure()
#    startcoords = np.reshape(startcoords, [-1])
#    with open("results", "a") as fout:
#        fout.write( "#success nfuncalls nquenches lowestE maxquenches\n" )
#    for i in range(niter):
#        if onestart:
#            coords = np.copy(startcoords)
#            ret = globalOpt(nquenches=nquenches, coords=coords)
#        else:
#            ret = globalOpt(nquenches=nquenches)
#        with open("results", "a") as fout:
#            fout.write( "%d %d %d %f %d\n" % ( ret["success"], ret["nfuncalls"], ret["nquenches"], ret["lowestE"], nquenches ) )


if __name__ == "__main__":
#    run_one(0)
    main()
