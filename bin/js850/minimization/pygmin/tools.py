import numpy as np

class _Result(object):
    pass


class FrozenCoordsConverter(object):
    def __init__(self, reference_coords, frozen_dof):
        
        self.reference_coords = reference_coords.copy()
        self.frozen_dof = np.array(np.sort(frozen_dof.copy()))
        
        fr = set(frozen_dof)
        self.mobile_dof = np.array([i for i in xrange(len(reference_coords)) if i not in fr])

        self.frozen_coords = self.reference_coords[frozen_dof].copy()
    
    def get_frozen_coords(self):
        return self.frozen_coords.copy()
    
    def get_reduced_coords(self, fullcoords):
        assert len(fullcoords) == len(self.reference_coords)
        return fullcoords[self.mobile_dof].copy()

    def get_full_coords(self, coords):
        assert len(coords) == len(self.mobile_dof)
        fullcoords = self.reference_coords.copy()
        fullcoords[self.mobile_dof] = coords
        return fullcoords

class FrozenCCPotWrapper():
    def __init__(self, potential, reference_coords, frozen_dof):
        self.underlying_pot = potential
        self.coords_converter = FrozenCoordsConverter(reference_coords, frozen_dof)

    def getEnergy(self, coords):
        fullcoords = self.coords_converter.get_full_coords(coords)
        e = self.underlying_pot.getEnergy(fullcoords)
        return e
    
    def getEnergyGradient(self, coords):
        fullcoords = self.coords_converter.get_full_coords(coords)
        e, grad = self.underlying_pot.getEnergyGradient(fullcoords)
        grad = self.coords_converter.get_reduced_coords(grad)
        return e, grad

class FrozenAtomPotWrapper():
    def __init__(self, potential, frozen_dof):
        self.pot = potential
        self.frozen_dof = np.array(frozen_dof)
    
    def getEnergy(self, x):
        return self.pot.getEnergy(x)
    
    def getEnergyGradient(self, x):
        e, v = self.pot.getEnergyGradient(x)
        v[self.frozen_dof] = 0.
        return e, v

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

def read_con_file(fname):
    with open(fname, "r") as fin:
        for i, line in enumerate(fin):
            sline = line.split() 
            if i == 2:
                boxvec = np.array(map(float, sline[:3]))
            elif i == 7:
                natoms = int(sline[0])
                x = np.zeros([natoms, 3])
                frozen = []
                j = 0
            elif i >= 11:
                if j >= natoms:
                    raise Exception("input error")
                x[j,:] = map(float, sline[:3])
                frozen.append(bool(int(sline[3])))
                j += 1
        res = _Result()
        res.coords = x
        res.boxvec = boxvec
        res.frozen = np.array(frozen)
        return res

