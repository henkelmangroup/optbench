import numpy as np



import pygmin.potentials.lj as lj
import pygmin.basinhopping as bh
from pygmin.takestep import displace
from pygmin.takestep import adaptive
from pygmin.optimize.quench import lbfgs_py as lbfgs
from pygmin.storage.savenlowest import SaveN as saveit


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

def globalOpt( E_globmin=None, coords = None, nquenches=100000, Etol = 1e-3):
    natoms = 38
    ljpot = lj.LJ()
    pot = PotWrapper(ljpot)

    if E_globmin is None:
        if True:
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



    takeStep = displace.RandomDisplacement( stepsize=0.41 )
    tsAdaptive = adaptive.AdaptiveStepsize(takeStep, acc_ratio = 0.5, frequency = 100)

    storage = saveit(nsave=10)

    pot.ncalls = 0
    opt = bh.BasinHopping(coords, pot, takeStep=tsAdaptive, storage=storage.insert)
    opt.setPrinting(frq=20)
    success = False
    for i in range(nquenches):
        opt.run(1)
        if opt.markovE <= E_globmin + Etol:
            print "found global minimum", opt.markovE, E_globmin
            success = True
            break
        if i % 100 == 1:
            print i, "number of function calls", pot.ncalls, float(pot.ncalls)/i
            print i, "lowest structure found", storage.data[0].energy


    ncalls = pot.ncalls
    print "final number of function calls", ncalls

    if True:
        print "lowest structure found", storage.data[0].energy

    return {"nfuncalls":ncalls, "nquenches":i, "lowestE":storage.data[0].energy, "success":success}

def runGlobalOpt(niter = 100, nquenches=100000, onestart = True):
    startcoords = getStartingStructure()
    startcoords = np.reshape(startcoords, [-1])
    with open("results", "a") as fout:
        fout.write( "#success nfuncalls nquenches lowestE maxquenches\n" )
    for i in range(niter):
        if onestart:
            coords = np.copy(startcoords)
            ret = globalOpt(nquenches=nquenches, coords = coords)
        else:
            ret = globalOpt(nquenches=nquenches)
        with open("results", "a") as fout:
            fout.write( "%d %d %d %f %d\n" % ( ret["success"], ret["nfuncalls"], ret["nquenches"], ret["lowestE"], nquenches ) )


if __name__ == "__main__":
    runGlobalOpt(niter=90)
