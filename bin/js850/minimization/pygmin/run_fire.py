import argparse
import numpy as np

import opt

from pele.optimize import fire
from pele.potentials import LJ

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="compute benchmarks for fire with pele")
    
#    parser.add_argument("fname", type=str, help="Database file name")
#    parser.add_argument("-M", type=int, default=4, help="fire history length")
    parser.add_argument("--maxstep", type=float, default=0.1, help="fire maximum step size")
    parser.add_argument("-natoms", type=int, default=38, help="number of atoms")
    args = parser.parse_args()
    
    tol = 0.01

    potLJ = LJ()
    pot = opt.PotWrapper(potLJ)


    structuredir = "../lj38-clusters"
    nstructures = 1000
    benchmarker = opt.QuenchBenchmark(structuredir, nstructures)
    stop_crit = opt.MaxForceOnAtom()

    kwargs = dict()
    if False:
        # use the maximum force on an atom as the stop criterion
        stop_crit = opt.MaxForceOnAtom()
        kwargs["alternate_stop_criterion"]=stop_crit
    else:
        # use the norm of the gradient.  This is sqrt(natoms) times the rms
        tol /= np.sqrt(3. * args.natoms)

    
    minimizer = opt.Minimizer("results_data", pot, fire,
                              tol=tol, maxstep=args.maxstep, **kwargs )
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
                    
                    

