import numpy as np

from tools import MorseBulkFrozen, PotWrapperIncr, read_con_file

from dec_lj38 import do_local_connect

class MorseBulkFrozenWrap(MorseBulkFrozen):
    ncalls = 0
    def get_potential(self):
        pot = super(MorseBulkFrozenWrap, self).get_potential()
        def incr(): self.ncalls += 1
        wpot = PotWrapperIncr(pot, incr)
        wpot.coords_converter = pot.coords_converter
        return wpot

def set_params(system, natoms):
    system.params.double_ended_connect.local_connect_params.NEBparams.image_density = 1
    system.params.double_ended_connect.local_connect_params.NEBparams.iter_density = 30
    system.params.double_ended_connect.local_connect_params.NEBparams.reinterpolate = 50
    system.params.double_ended_connect.local_connect_params.NEBparams.adjustk_freq = 50
    system.params.double_ended_connect.local_connect_params.NEBparams.k = 0.05
    system.params.double_ended_connect.local_connect_params.NEBparams.verbose = True
    system.params.double_ended_connect.local_connect_params.NEBparams.NEBquenchParams["tol"] = 0.01 
    system.params.double_ended_connect.local_connect_params.NEBparams.NEBquenchParams["maxstep"] = 2. 
    tsparams = system.params.double_ended_connect.local_connect_params.tsSearchParams
    
    tsparams.lowestEigenvectorQuenchParams={"nsteps":1000, "tol":0.4, "maxstep":1.}
    tsparams.tol = 1e-3 / np.sqrt(3.*natoms)
#    nfail_max=200,
#    nsteps=1000,
    tsparams.max_uphill_step = .4
    tsparams.iprint = 1
    tsparams.verbosity=5
    tsparams.demand_initial_negative_vec = False

    tsparams.nsteps_tangent1=3
    tsparams.nsteps_tangent2=20
    tangent_quench = tsparams.tangentSpaceQuenchParams
    tangent_quench["maxstep"] = .4
    tangent_quench["iprint"] = -1

    print "tolerance", tsparams.tol

def run(i, usegui=False):
    f1 = "../pt-island-con/product_%d.con" % i
    f2 = "../pt-island-con/reactant.con"
    ret1 = read_con_file(f1)
    ret2 = read_con_file(f2)
    
    x = ret2.coords.flatten()
    boxvec = ret2.boxvec
    natoms = x.size / 3
    frozen = ret2.frozen
    frozen_atoms = np.where(frozen)[0]
    system = MorseBulkFrozenWrap(natoms, boxvec, rho=1.6047, r0=2.8970, A=0.7102,
                             rcut=9.5, 
                             frozen_atoms=frozen_atoms, reference_coords=x)
    xfree = system.coords_converter.get_reduced_coords(x)
    
    if usegui:
        db = system.create_database("test.db")
    else:
        db = system.create_database()
    
    pot = system.get_potential()
    x = ret1.coords.flatten()
    x = system.coords_converter.get_reduced_coords(x)
    E = pot.getEnergy(x)
    db.addMinimum(E, x)
    x = ret2.coords.flatten()
    x = system.coords_converter.get_reduced_coords(x)
    E = pot.getEnergy(x)
    db.addMinimum(E, x)
    
    # set parameters
    natoms = db.minima()[0].coords.size / 3
    set_params(system, natoms)

    if usegui:
        from pele.gui import run_gui
        run_gui(system, "test.db")
    
    
    res = do_local_connect(system, db)
    res.i = i
    res.fname1 = f1
    res.fname2 = f2
    return res
        

def main():
    results = []
    for i in range(1,59):
        print i
#        if i == 50: continue
#        if i == 54: continue
#        if i == 59: continue
        res = run(i)
        results.append(res)
    
    with open("results.txt", "w") as fout:
        for res in results:
            fout.write("%d %d %d %d\n" % (
                        res.i, res.ncalls, res.ncalls_neb, res.success          ))
        

if __name__ == "__main__":
#    run(3, usegui=False)
#    run(9, usegui=False)
#    run(10, usegui=True)
    main()