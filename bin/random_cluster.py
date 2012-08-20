#!/usr/bin/env python
import aselite as ase
from sys import argv, exit
import numpy
import random

class RandomStructure:
    def __init__(self, atoms):
        self.radii = numpy.array([ ase.covalent_radii[z]
                                   for z in atoms.get_atomic_numbers() ])
        self.box_center = numpy.diagonal(atoms.get_cell())/2.0
        self.p = 0.1
        self.atoms = atoms

    def generate(self):
        indexes = range(len(self.atoms))
        random.shuffle(indexes)
         
        rs = ase.Atoms()
        first = indexes[0]
        rs += ase.Atom(self.atoms.get_chemical_symbols()[first])

        failures = 0
        INDEX=1
        for i in indexes[1:]:
            rs += ase.Atom(self.atoms.get_chemical_symbols()[i])
            rs.cell = self.box_p(rs)

            while True:
                rs.positions[-1] = numpy.random.uniform(-rs.cell[0][0]/2.0,rs.cell[0][0]/2.0,3)
                d_min = 1e9
                for j in range(len(rs)-1):
                    d = numpy.linalg.norm(rs.positions[-1]-rs.positions[j])
                    if d < d_min:
                        d_min = d
                        bond_length = self.radii[i] + self.radii[j]
                        if d_min < 0.8*bond_length:
                            break

                if 0.8*bond_length < d_min < 1.3*bond_length:
                    break
            print INDEX
            INDEX += 1

        rs.set_cell(self.atoms.get_cell())
        #XXX: shift to center of box, only correct for cubic cells
        rs.positions += rs.cell.diagonal()/2.0
        print "RandomStructure made new structure"
        return rs

    def box_p(self, rs):
        V_atoms = sum(4./3*3.14159*self.radii[0:len(rs)])
        a = (V_atoms/self.p)**(1/3.)
        return numpy.array( ((a,0,0),(0,a,0),(0,0,a)) )

if len(argv) < 3 or '-h' in argv:
    print 'usage: random_cluster.py natoms symbol [nstructures] [prefix]'
    exit()
natoms = int(argv[1])
symbol = argv[2]
if len(argv) > 3:
    nstructures = int(argv[3])
else:
    nstructures = 1
if len(argv) > 4:
    prefix = argv[4]
else:
    prefix = 'cluster'
atoms = ase.Atoms('H'*natoms)
atoms.set_cell((100.0,100.0,100.0))
rs = RandomStructure(atoms)
for i in range(nstructures):
    atoms = rs.generate()
    ase.write_xyz('%s_%.4i.xyz'%(prefix,i), atoms, comment='lj38_benchmark')
    ase.write_con('%s_%.4i.con'%(prefix,i), atoms)
