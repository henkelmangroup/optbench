import argparse
import numpy as np

import opt

from pele.optimize import mylbfgs
from pele.potentials import LJ

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="compute benchmarks for lbfgs with pele")
    
#    parser.add_argument("fname", type=str, help="Database file name")
    parser.add_argument("-M", type=int, default=4, help="lbfgs history length")
    parser.add_argument("--maxstep", type=float, default=0.1, help="lbfgs maximum step size")
    args = parser.parse_args()
    
    tol = 0.01

    potLJ = LJ()
    pot = opt.PotWrapper(potLJ)


    structuredir = "../lj38-clusters"
    nstructures = 1000
    benchmarker = opt.QuenchBenchmark(structuredir, nstructures)
    stop_crit = opt.MaxForceOnAtom()

    
    minimizer = opt.Minimizer("lbfgs_data", pot, mylbfgs, alternate_stop_criterion=stop_crit,
                               M=args.M, tol=tol, maxstep=args.maxstep )
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
                    
                    

