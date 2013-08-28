import numpy as np

from pele.systems.morse_bulk import MorseBulk
from pele.potentials import BasePotential
from pele.systems import BaseSystem

class _Result(object):
    pass

class PotWrapperIncr(BasePotential):
    """a LJ potential wrapper to count the number of function calls"""
    ncalls = 0
    def __init__(self, pot, incriment):
        self.pot = pot
        self.incriment = incriment
    def getEnergy(self, coords):
        self.incriment()
        return self.pot.getEnergy(coords)
    def getEnergyGradient(self, coords):
        self.incriment()
        return self.pot.getEnergyGradient(coords)


class MorseBulkFrozen(MorseBulk):
    def __init__(self, *args, **kwargs):
        self.frozen_atoms = kwargs.pop("frozen_atoms")
        self.reference_coords = kwargs.pop("reference_coords")
        super(MorseBulkFrozen, self).__init__(*args, **kwargs)


        self.frozen_dof = [range(i*3,i*3+3) for i in self.frozen_atoms]
        self.frozen_dof = np.array(self.frozen_dof, np.integer).flatten()
        self.frozen_dof.sort()
        self.mobile_atoms = np.array([i for i in xrange(self.reference_coords.size/3) if i not in self.frozen_atoms])
        
        self.pot = self.get_potential()
        self.coords_converter = self.pot.coords_converter
        
        self.nfree = self.reference_coords.size / 3 - len(self.frozen_atoms)
        
        self.params.takestep.stepsize = 1.
        self.params.basinhopping.insert_rejected = True
    
    def get_potential(self):
        pot = super(MorseBulkFrozen, self).get_potential()
        fpot = FrozenCCPotWrapper(pot, self.reference_coords, self.frozen_dof)
        return fpot
    
    def draw1(self, coords, *args, **kwargs):
        x = self.coords_converter.get_full_coords(coords)
        super(MorseBulkFrozen, self).draw(x, *args, **kwargs)
    
    def draw(self, coordslinear, index, subtract_com=True):
        """
        tell the gui how to represent your system using openGL objects
        
        Parameters
        ----------
        coords : array
        index : int
            we can have more than one molecule on the screen at one time.  index tells
            which one to draw.  They are viewed at the same time, so they should be
            visually distinct, e.g. different colors.  accepted values are 1 or 2        
        """
        subtract_com = False
        coordslinear = coordslinear.copy()
        coords = self.coords_converter.get_full_coords(coordslinear)


        from OpenGL import GL,GLUT
        coords = coords.reshape([-1, 3])
        if subtract_com:
            com = np.mean(coords, axis=0)
        else:
            com = np.zeros(3)
        size = 0.5 * self.r0
        if index == 1:
            color = [0.65, 0.0, 0.0, 1.]
        else:
            color = [0.00, 0.65, 0., 1.]
        GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_DIFFUSE, color)   
        for i in self.mobile_atoms:
            x=coords[i,:] - com
            GL.glPushMatrix()            
            GL.glTranslate(x[0],x[1],x[2])
            GLUT.glutSolidSphere(size, 30, 30)
            GL.glPopMatrix()

        # frozen atoms
        if index == 1:
            color = [0.25, 0.00, 0., 1.]
        else:
            color = [0.00, 0.25, 0., 1.]
        GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_DIFFUSE, color)   
        for i in self.frozen_atoms:
            x=coords[i,:] - com
            GL.glPushMatrix()            
            GL.glTranslate(x[0],x[1],x[2])
            GLUT.glutSolidSphere(size, 30, 30)
            GL.glPopMatrix()
        
    
    def get_random_configuration(self):
        x = self.coords_converter.get_reduced_coords(self.reference_coords)
        print "sizes", self.reference_coords.size, x.size
        return x.copy()
        
    def get_permlist(self):
        return [range(self.nfree)]


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

