import argparse
import numpy as np

import minimization_tools as opt
from tools import read_con_file

from pele.optimize import mylbfgs
from pele.potentials import Morse



def mkname(n):
    return "pos_%04d.con" % n

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="compute benchmarks for lbfgs with pele")
    
#    parser.add_argument("fname", type=str, help="Database file name")
    parser.add_argument("-M", type=int, default=4, help="lbfgs history length")
    parser.add_argument("-natoms", type=int, default=256, help="number of atoms")
    parser.add_argument("--maxstep", type=float, default=0.1, help="lbfgs maximum step size")
    args = parser.parse_args()
    
    tol = 1e-3

    boxl = 16.387907
    boxvec = np.ones(3) * boxl
    potm = Morse(rho=1.6047, A=0.7102, r0=2.8970, boxvec=boxvec, rcut=9.5)
    pot = opt.PotWrapper(potm)


    structuredir = "./morse-bulk/"
    nstructures = 100
    reader = lambda fname: read_con_file(fname).coords
    benchmarker = opt.QuenchBenchmark(structuredir, nstructures, make_name=mkname, read_coords=reader)
    
    kwargs = dict()
    if False:
        # use the maximum force on an atom as the stop criterion
        stop_crit = opt.MaxForceOnAtom()
        kwargs["alternate_stop_criterion"]=stop_crit
    else:
        # use the norm of the gradient.  This is sqrt(natoms) times the rms
        tol /= np.sqrt(3. * args.natoms)

    #print "tolerance", tol, args.natoms
    

    
    minimizer = opt.Minimizer("results_data", pot, mylbfgs,
                               M=args.M, tol=tol, maxstep=args.maxstep, 
                               **kwargs )
    benchmarker.addMinimizer(minimizer)


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
                fout.write( opt.QuenchResult.header() + "\n" )
                for qr in minimizer.quench_results:
                    fout.write( qr.datastring() + "\n" )
                    
                    

