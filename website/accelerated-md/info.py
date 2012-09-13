#!/usr/bin/env python

import numpy
import sys
import math
############
nsamp = 400
#############
forcecalls = []
escapetime = []
fcar = []
esar = []
estd = []
numsamp = []
for i in range(nsamp):
	sys.path.append('0_'+str(i))
	filename = 'debug_results/0_'+str(i)+'/results_0.dat'
	count = 0
	for j in open(filename,'r'):
		w = j.split()
		if w[1] == 'total_force_calls':
		  forcecalls = numpy.append(forcecalls,float(w[0]))
		if w[1] == 'transition_time_s':
		  escapetime = numpy.append(escapetime,float(w[0]))
		count += 1
	if i > 1:
		numsamp = numpy.append(numsamp,i)
		fcar = numpy.append(fcar,numpy.sum(forcecalls))
		esar = numpy.append(esar,1/numpy.mean(escapetime))
		estd = numpy.append(estd,numpy.std(escapetime)*esar[i-2]*esar[i-2]/numpy.sqrt(i))	

ar01 = []
ar001 = []
for i in range(len(numsamp)):
	ar01 = numpy.append(ar01,0.1)
	ar001 = numpy.append(ar001,0.01)

totforcecalls = numpy.sum(forcecalls)

import matplotlib
matplotlib.use("agg") # Change to "agg" to run on FRI
from pylab import *

figure()
scatter(fcar,esar)
errorbar(fcar,esar,estd)
savefig('fcvrate.png')

pe = []
for i in range(len(esar)):
	pe = numpy.append(pe,estd[i]/esar[i])

figure()
scatter(numsamp,pe,c='g')
plot(numsamp,ar01,c='m')
plot(numsamp,ar001,c='c')
savefig('sampverror.png')

figure()
scatter(fcar,pe,c='g')
plot(fcar,ar01,c='m')
plot(fcar,ar001,c='c')
savefig('fcverror.png')

import pickle

out = open('rate.log','w')
pickle.dump(esar,out)


print 'total fc',totforcecalls 
#print escapetime	
print 'percent error',pe[len(esar)-1]

#sys.exit()

array = []
count = 0
for line in open('states/0/processtable'):
	x = line.split()
	if count > 0:
	 array = numpy.append(array,float(x[3]))
	count += 1
time = numpy.mean(array)
std = numpy.std(array)/numpy.sqrt(count)
rate = 1/time
rstd = std/(time*time)
print 'average time of escape',time,'s'
print 'standard deviation',std,'s'
print 'rate calculated','%e' % rate, '1/s'
print 'std of rate','%e' % rstd, '1/s'
pe = rstd/rate

out1 = open('r.log','w')
pickle.dump(rate,out1)
out2 = open('e.log','w')
pickle.dump(rstd,out2)
out3 = open('pe.log','w')
pickle.dump(pe,out3)
out4 = open('fc.log','w')
pickle.dump(totforcecalls,out4)
out5 = open('nsamp.log','w')
pickle.dump(nsamp,out5)




