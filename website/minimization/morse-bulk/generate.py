#!/usr/bin/env python
from ase.lattice.cubic import FaceCenteredCubic
from tsase.io import write_con
a=4.0969766901948566
atoms = FaceCenteredCubic(size=(4,4,4), symbol='Pt', pbc=(1,1,1),latticeconstant=a)

for i in xrange(100):
    atoms_disordered = atoms.copy()
    atoms.rattle(.025, seed=i+1024*i)
    write_con('pos_%.4i.con'%i, atoms)
