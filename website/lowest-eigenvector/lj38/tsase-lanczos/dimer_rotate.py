#!/usr/bin/env python

'''
Neb optimization example for TiO2
'''

import lanczos
import ssdimer
import powershift
#from tsase.dimer import ssdimer
from tsase.io import read_con, write_con
from tsase.neb.util import vunit, vrand, vmag
from ase.io import read, write
import os,sys
from ase.calculators.lammps import LAMMPS
import numpy as np
#import pylab as pl


#filenumber = sys.argv[1]
#posfile    = str(filenumber).zfill(4) + '.con'
#modefile   = str(filenumber).zfill(4) + '_mode'
posfile    = 'pos.con'
modefile   = 'true_mode'
    
p1 = read_con(posfile)

pair_coeff = [' * * 1 1']
parameters = { 'pair_style':'lj/cut/opt 40.0', 'pair_coeff':pair_coeff, 'mass':['1 1']}
calc = LAMMPS(parameters=parameters)
p1.set_calculator(calc)
E0 = p1.get_potential_energy()

natoms = len(p1)
mode      = np.loadtxt('direction.dat')
mode      = np.vstack(( mode, np.zeros((3,3)) ))
mode = vunit(mode)
lowestmode  = np.loadtxt(modefile).flatten()
lowestmode  = np.reshape(lowestmode, (-1, 3))
lowestmode  = np.vstack(( lowestmode, np.zeros((3,3)) ))

tol = np.arccos(0.99) / np.pi * 180.0

#dimer_BFGS
dB = ssdimer.SSDimer_atoms(p1, mode = mode, rotationMax = 500, phi_tol= tol, ss = False, dR = 0.001, lowestmode = lowestmode , rotationOpt = 'bfgs')
dB.get_forces()
print "BFGS:", dB.get_curvature()
BFGS_forceCalls = dB.forceCalls

#Lanczos
dL = lanczos.lanczos_atoms(p1, mode = mode, rotationMax = 500, phi_tol= tol, ss = False, dR = 0.001, lowestmode = lowestmode)
dL.get_forces()
print "Lanczos:", dL.get_curvature()
Lanczos_forceCalls = dL.forceCalls

#CG    
dC = ssdimer.SSDimer_atoms(p1, mode = mode, rotationMax = 500, phi_tol= tol, ss = False, dR = 0.001, lowestmode = lowestmode , rotationOpt = 'cg')
dC.get_forces()
print "CG:", dC.get_curvature()
CG_forceCalls = dC.forceCalls

'''
#dimer rotation with steepest descent for the plane direction
dS = ssdimer.SSDimer_atoms(p1, mode = mode, rotationMax = 500, phi_tol= tol, ss = False, dR = 0.001, lowestmode = lowestmode , rotationOpt = 'sd')
dS.get_forces()
print "SD:", dS.get_curvature()

#Shiftted Power
dP = powershift.SSDimer_atoms(p1, mode = mode, rotationMax = 500, phi_tol= tol, ss = False, dR = 0.001, lowestmode = lowestmode )
dP.get_forces()
print "Power:", dP.get_curvature()
'''

resultfile = open('results.dat','w')
resultfile.write(str(Lanczos_forceCalls)+" Lanczos_force_calls\n")
resultfile.write(str(BFGS_forceCalls)+" BFGS_force_calls\n")
resultfile.write(str(CG_forceCalls)+" CG_force_calls\n")
resultfile.close()


if len(sys.argv) > 1:
    figset = 211
    ax1 = pl.subplot(figset)
    ax2 = pl.subplot(figset+1)
    #fig, ax1 = pl.subplots()
    #ax2 = ax1.twinx()
    ax1.plot(dB.record[0],dB.record[1],'-hm',markersize=4, lw=1, clip_on=False, label = 'Dimer_BFGS')
    ax2.plot(dB.record[0],dB.record[2],'-hm',markersize=4, lw=1, clip_on=False, label = 'Dimer_BFGS')
    ax1.plot(dL.record[0],dL.record[1],'-xk',markersize=4, lw=1, clip_on=False, label = 'Lanczos')
    ax2.plot(dL.record[0],dL.record[2],'-xk',markersize=4, lw=1, clip_on=False, label = 'Lanczos')
    ax1.plot(dC.record[0],dC.record[1],'-sr',markersize=4, lw=1, clip_on=False, label = 'Dimer_CG')
    ax2.plot(dC.record[0],dC.record[2],'-sr',markersize=4, lw=1, clip_on=False, label = 'Dimer_CG')
    '''
    ax1.plot(dS.record[0],dS.record[1],'-^g',markersize=4, lw=1, clip_on=False, label = 'Dimer_SD')
    ax2.plot(dS.record[0],dS.record[2],'-^g',markersize=4, lw=1, clip_on=False, label = 'Dimer_SD')
    ax1.plot(dP.record[0],dP.record[1],'-ob',markersize=4, lw=1, clip_on=False, label = 'Power')
    ax2.plot(dP.record[0],dP.record[2],'-ob',markersize=4, lw=1, clip_on=False, label = 'Power')
    '''

    xx = dL.record[0]
    yy = np.zeros(len(xx))
    ax2.plot(xx,yy,'k--',linewidth=0.8)
    ax1.set_ylabel('Angle towards the true minimum mode')
    ax2.set_ylabel('Minimum Curvature')
    ax2.set_xlabel("Iterations")
    ax1.legend(loc='upper right')
    pl.savefig('Compare.eps')
