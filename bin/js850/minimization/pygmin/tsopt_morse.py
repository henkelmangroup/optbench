import numpy as np

from pele.transition_states import findTransitionState
from pele.systems.morse_bulk import MorseBulk
from pele.potentials import Morse
from pele.potentials import BasePotential
from pele.utils.xyz import read_xyz, write_xyz
from math import sqrt

from tools import read_con_file, PotWrapper, FrozenAtomPotWrapper
import tools

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
        
        fpot = tools.FrozenCCPotWrapper(pot, self.reference_coords, self.frozen_dof)
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


def findTS(coords, pot):
    ''' routine to execute a single transition state refinement for the benchmark ''' 
    lowestEigenvectorQuenchParams={"nsteps":100, "tol":0.1}
    lowestEigenvectorQuenchParams={"iprint":-1}
    
    natoms = coords.size / 3
    return findTransitionState(coords, pot, 
                               orthogZeroEigs=None,
                               tol=1e-3/sqrt(3.*natoms),
                               verbosity=5, 
                               iprint=1,
                               lowestEigenvectorQuenchParams=lowestEigenvectorQuenchParams,
                               )
#    , 
#                               tangentSpaceQuenchParams={"tol": 0.05},
#                               demand_initial_negative_vec=False,
#                               nsteps_tangent1=3, 
#                               nsteps_tangent2=25, 
#                               nfail_max=200,
#                               nsteps=1000,
#                               max_uphill_step=0.1,
#                               )

def run(fname):
    ''' run benchmark for a single configuration '''
    res = read_con_file(fname)
    x = res.coords.flatten()
    boxvec = res.boxvec
    natoms = x.size / 3
    frozen = res.frozen
    frozen_atoms = np.where(frozen)[0]
    
    system = MorseBulkFrozen(natoms, boxvec, rho=1.6047, r0=2.8970, A=0.7102, 
                             frozen_atoms=frozen_atoms, reference_coords=x)
    
    if False:
        from pele.gui import run_gui
#        db = system.create_database("test.sqlite")
        run_gui(system, "test.sqlite")
        exit(1)
    
    xfree = system.coords_converter.get_reduced_coords(x)
    
    pot = PotWrapper(system.get_potential())
    print "running ", fname
    ret = findTS(xfree, pot)
    ncalls = pot.ncalls
    print "ncalls for %s:" % fname, ncalls, "success", ret.success

    return fname, ncalls, ret.energy, ret.eigenval, ret.rms, ret.nsteps, ret.success

def main():
    results = []
    for i in range(200):
        print "\n"
        results.append(run("../pt-island-con/initial_%d.con" % i))
    
    with open("results.txt", "w") as fout:
        for fname, ncalls, energy, eigenval, rms, nsteps, success in results:
            fout.write( "%s %d %f %g %g %d %d\n" % (fname, ncalls, energy, eigenval, rms, nsteps, success) )

if __name__ == "__main__":
    main()