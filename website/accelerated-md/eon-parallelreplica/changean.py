#!/usr/bin/env python
import ase
import tsase
import numpy
import sys
import math

maxatomsm = 20
numsamp = 4
binam = numpy.zeros(maxatomsm)
products = []
numprod = []
pcount = 0
totar = []
filename = '0_0/reactant_0.con'
r = tsase.io.read_con(filename)
distar = []
prodmatrix = numpy.zeros((maxatomsm,numsamp))
q = numpy.ones(len(r.get_positions())) * 13


for i in range(numsamp):
	amov = [] 
	pfilename = '0_'+str(i)+'/product_0.con'
        p = tsase.io.read_con(pfilename)
	p.set_constraint(constraint=None)
	rfilename = '0_'+str(i)+'/reactant_0.con'
	r = tsase.io.read_con(rfilename)
	r.set_constraint(constraint=None)
	q = numpy.ones(len(r.get_positions())) * 13
	r.set_atomic_numbers(q)
	p.set_atomic_numbers(q)
	tot = 0
	totdist = 0
	for k in range(len(p.get_positions())):
		diff = 0
		for j in range(3):
                         x = math.fabs(r.get_positions()[k][j]- p.get_positions()[k][j])
			 if x > (14.317100/2):
                                x = 14.317100 - x
                         diff += x*x 
			 totdist += x*x
		diff = numpy.sqrt(diff)
		if diff > 0.5:
		###### change atomic number to highlight atoms
				s = p[k]
				s.set_atomic_number(tot + 3)	
				s = r[k]
                                s.set_atomic_number(tot + 3)
				amov = numpy.append(amov,k)
				if s.get_atomic_number() == 13:
					s.set_atomic_number(2)
                                tot += 1
	#### change atoms number to end of file so correct atoms are highlighted	
	xp = p.get_positions()
	xr = r.get_positions()
	for w in range(len(amov)):
	        index = len(p.get_positions()) - (len(amov) -w)		
		a = []
		b = []
		for u in range(3):
			a = numpy.append(a,xp[index][u])
			b = numpy.append(b,xr[index][u])
		xp[index] = xp[int(amov[w])] 
		xr[index] = xr[int(amov[w])]
		xp[int(amov[w])] = a
		xr[int(amov[w])] = b 
		for q in range(len(amov)):
			if amov[q] == index: 
				amov[q] = amov[w]
	p.set_positions(xp)
	r.set_positions(xr)
	totar = numpy.append(totar,tot)
	distar = numpy.append(distar,numpy.sqrt(totdist))
	binam[tot] += 1
	prodmatrix[tot][i] = 1	
	tsase.io.write_con(rfilename,r,'w')
	tsase.io.write_con(pfilename,p,'w')
	
print totar 
print distar
print binam


#print prodmatrix

import pickle 

for j in range(maxatomsm):
 ar = []
 for i in range(numsamp):
	if prodmatrix[j][i] == 1:
		ar = numpy.append(ar,i)
 if len(ar) > 0:
	filename = 'am'+str(j)+'.log'
	out = open(filename,'w')
	pickle.dump(ar,out)	


sys.exit()

for i in range(10):
	filename = '0_'+str(i)+'/product_0.con'
	p = tsase.io.read_con(filename)
	
	if i == 0:
		pcount += 1
		products.append(tsase.io.read_con(filename))
		numprod = numpy.append(numprod,1)
	else:
		a = 0
		print i
		for j in range(pcount):
			
			tot = 0
			for k in range(len(p.get_positions())):
			 x = p.get_positions()[k]- products[j].get_positions()[k]
			 diff = numpy.sqrt(numpy.vdot(x,x))
			 if diff > 12:
				diff = 14.317100 - diff 
			 if diff > 0.3:
				print 'atom',k
				print diff
				tot += 1	
			#	numprod[j] += 1
				a = 1
			totar = numpy.append(totar,tot)
			if tot < 1:
				numprod[j] += 1
				a = 0
				print 'found sim prod'
				break
			print 'tot atoms moved',tot
		if a == 1:
			pcount += 1
			products.append(tsase.io.read_con(filename))
			numprod = numpy.append(numprod,1)

import pickle

out = open('products.log','w')
pickle.dump(products,out)

out = open('numprod.log','w')
pickle.dump(numprod,out)

			
print len(products) 

print numprod
print 'atoms moved ar',totar
sys.exit()			

import matplotlib
matplotlib.use("agg") # Change to "agg" to run on FRI
from pylab import *




