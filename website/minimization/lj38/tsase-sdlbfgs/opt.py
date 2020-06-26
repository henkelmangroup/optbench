#Compute the Hessian for Newton's Method and continue optimization until force cutoff is reached. 
#step size is 0.25 as default but testing it with few different values. 
#!/usr/bin/env python
import numpy as np
from numpy.linalg import eigh
from itertools import product
from ase.units import Hartree, Bohr
import scipy.linalg as la
import sys
import ase
import time
import ase.io
from sys import argv, stderr
from ase.io import read, write
np.set_printoptions(threshold=sys.maxsize)
import pickle
import tsase
from tsase.calculators import lj

#Read the cluster structure from lj38 clusters.

atoms = ase.io.read(argv[1])
atoms.center(100.0)
calc = lj(cutoff=35.0)
atoms.set_calculator(calc)


t0 = time.time()
opt = tsase.optimize.SDLBFGS(atoms, maxstep=0.1, memory=100)

opt.run(fmax=0.01, steps=10000)
    


t1 = time.time()
print('real %5.8f seconds' %(t1-t0))
write('atoms.xyz',atoms,format='xyz')
f3 = open("results.dat", 'w')
f3.write('%i total_force_calls' %calc.force_calls)
f3.flush()
f3.close()
f4 = open("final_energy.dat", 'w')
f4.write('final energy is %5.8f \n' % atoms.get_potential_energy())
f4.flush()
f4.close()
