#!/usr/bin/env python
from ase.io import read
from ase.optimize import BFGSLineSearch
from tsase.calculators import morse
import numpy as np
from time import time
from os import system
from sys import stdout
import datetime

system("tar xf morse-bulk.tgz")

fcs = []
for i in xrange(100):
    print 'run-%i ' % i,
    stdout.flush()
    
    atoms = read('morse-bulk/POSCAR_%i' % i)
    calc = morse(rc=7.0)
    atoms.set_calculator(calc)

    opt = BFGSLineSearch(atoms, maxstep=.2, alpha=1.0/0.04, logfile=None)
    t0 = time()
    opt.run(fmax=1e-4, steps=10000)
    t1 = time()

    fc = opt.force_calls
    print '%.1f' % (t1-t0), fc
    fcs.append(fc)

benchmark = {}
benchmark['force_calls'] = np.mean(fcs)
benchmark['force_calls_min'] = np.min(fcs)
benchmark['force_calls_max'] = np.max(fcs)
benchmark['code'] = 'ASE'
benchmark['code_version'] = '3.6.0'
benchmark['contributor'] = 'Sam Chill'
benchmark['code_file'] = 'python-ase-3.6.0.2515.tar.gz'
benchmark['date'] = datetime.date.today().strftime('%d %b %Y')

f = open('benchmark.dat', 'w')
for k,v in benchmark.iteritems():
    f.write('%s %s\n' % (k,v))
f.close()
