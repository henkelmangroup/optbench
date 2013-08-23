import numpy as np
import os

from dec_lj38 import LJClusterWrap

from pele.optimize import Result
from pele.utils.xyz import read_xyz

def set_params(system, natoms):
    system.params.double_ended_connect.local_connect_params.NEBparams.image_density = 3
    system.params.double_ended_connect.local_connect_params.NEBparams.iter_density = 10
    system.params.double_ended_connect.local_connect_params.NEBparams.reinterpolate = 50
    system.params.double_ended_connect.local_connect_params.NEBparams.adjustk_freq = 50
    system.params.double_ended_connect.local_connect_params.NEBparams.adaptive_niter = True
    system.params.double_ended_connect.local_connect_params.NEBparams.adaptive_nimages = True
    system.params.double_ended_connect.local_connect_params.NEBparams.k = 1.5
    system.params.double_ended_connect.local_connect_params.NEBparams.verbose = False

    system.params.double_ended_connect.local_connect_params.NEBparams.NEBquenchParams["tol"] = 0.01 
    tsparams = system.params.double_ended_connect.local_connect_params.tsSearchParams

    
    tsparams.lowestEigenvectorQuenchParams={"nsteps":20, "tol":0.1}
    tsparams.tol = 1e-3 / np.sqrt(3.*natoms)
    tsparams.nsteps_tangent1=3
    tsparams.nsteps_tangent2=35 
#    nfail_max=200
#    nsteps=1000
    tsparams.max_uphill_step = 0.4
    tsparams.iprint = 1
    tsparams.verbosity = 5
    
    tangent_quench = tsparams.tangentSpaceQuenchParams
    tangent_quench["maxstep"] = .05
    tangent_quench["iprint"] = -1
    
    print "tolerance", tsparams.tol


def run(i, usegui=False):
    f1 = "../coords/start_%d.xyz" % i
    f2 = "../coords/end_%d.xyz" % i
    ret1 = read_xyz(open(f1))
    ret2 = read_xyz(open(f2))
    
    natoms = ret1.coords.flatten().size / 3
    system = LJClusterWrap(natoms)
    if usegui:
        dbfname = "test.sqlite"
        try:
            os.remove(dbfname)
        except OSError:
            pass
        db = system.create_database(dbfname)
    else:
        db = system.create_database()
    
    pot = system.get_potential()
    x = ret1.coords.flatten()
    E = pot.getEnergy(x)
    db.addMinimum(E, x)
    x = ret2.coords.flatten()
    E = pot.getEnergy(x)
    db.addMinimum(E, x)

    natoms = db.minima()[0].coords.size / 3
    set_params(system, natoms)
    
    if usegui:
        from pele.gui import run_gui
        run_gui(system, dbfname)
    
    

    m1, m2 = db.minima()[:2]
    connect = system.get_double_ended_connect(m1, m2, db)
    connect.connect()
    ncalls_final = system.ncalls
    
    res = Result()
    res.ncalls = ncalls_final
#    fres.ncalls_neb = ncalls_neb
    res.success = connect.success()
#    fres.neb = neb
#    fres.tsres = ret
    
    res.nts_total = db.number_of_transition_states()  
    res.nmin_total = db.number_of_minima()
    if res.success:
        path = connect.returnPath()
        res.nts_in_path = (len(path[0]) - 1) / 2
    else:
        res.nts_in_path = 0
    
    res.i = i
    res.fname1 = f1
    res.fname2 = f2
    res.distance = connect.getDist(m1, m2)
    
    print "done", i, res.success, res.ncalls, res.nts_in_path, res.nmin_total, res.nts_total
    return res

def main():
    i = 0
    results = []
    for i in range(50):
        print "\n"
        print i
        res = run(i)
        results.append(res)
    
    with open("results.txt", "w") as fout:
        fout.write("#index ncalls nts_in_path nmin_tot nts_tot success dist\n")
        for res in results:
            out = [res.i, res.ncalls, res.nts_in_path, res.nmin_total, res.nts_total,
                   res.distance, 
                   int(res.success)]
            out = map(str, out)
            outstr = " ".join(out) + "\n"
            fout.write(outstr)
#            fout.write("%d %d %d %d %d\n" % (
#                        res.i, res.ncalls, res.success          ))
        

if __name__ == "__main__":
#    run(4, usegui=True)
    main()