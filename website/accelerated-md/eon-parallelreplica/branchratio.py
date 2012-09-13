#!/usr/bin/env python
import ase
import tsase
import numpy
import sys
import math

############ function to distinguish between products and give ar of index of various products #####
def getproddist(am2):
 products = []
 numprod = []
 prodindex = []
 pcount = 0
 totar = []
 for i in range(len(am2)):
        filename = '0_'+str(int(am2[i]))+'/product_0.con'
        p = tsase.io.read_con(filename)
        if i == 0:
                pcount += 1
                products.append(tsase.io.read_con(filename))
                numprod = numpy.append(numprod,1)
                prodindex = numpy.append(prodindex,am2[i])
                cell = p.get_cell()[0][0]
        else:
                a = 0
                for j in range(pcount):
                        totdist = 0
                        tot = 0
                        for k in range(len(p.get_positions())):
                         diff = 0
                         for q in range(3):
                           x = math.fabs(p.get_positions()[k][q]- products[j].get_positions()[k][q])
                           if x > (cell/2):
                                x = cell - x
                           diff += x*x
                           totdist += x*x
                         diff = numpy.sqrt(diff)
                         if diff > 0.5:
                                tot += 1
                                a = 1
                        totar = numpy.append(totar,tot)
                        if tot < 1:
                                numprod[j] += 1
                                a = 0
                                break
                if a == 1:
                        pcount += 1
                        products.append(tsase.io.read_con(filename))
                        numprod = numpy.append(numprod,1)
                        prodindex = numpy.append(prodindex,am2[i])
 return numprod,prodindex

####################################################################################################
############## determines number of atoms moved in various products ######################
maxatomsm = 20
numsamp = 1000
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
                                tot += 1
	totar = numpy.append(totar,tot)
	distar = numpy.append(distar,numpy.sqrt(totdist))
	binam[tot] += 1
	prodmatrix[tot][i] = 1	
	
print binam
######################################################################
### creates output files for product distributions####################

#from branchratio2 import *
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
 	numprod,prodindex = getproddist(ar)
	print 'numatoms moved',j
	print 'numprod',numprod
	print 'prodindex',prodindex
	filename1 = 'numprod' + str(j) + '.log'
	out1 = open(filename,'w') 
	pickle.dump(numprod,out1)

	filename2 = 'prodindex' + str(j) + '.log'
        out2 = open(filename,'w')
        pickle.dump(prodindex,out2)


sys.exit()





