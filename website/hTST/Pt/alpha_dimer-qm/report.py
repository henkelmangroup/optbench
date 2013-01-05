#!/usr/bin/env python
import numpy
import sys, copy
from sys import argv
from os.path import join

#path = argv[1]
path = './states/0/'

rate_accuracy = 0.999
#all the barriers below 1.5 eV
#barrier_list = [0.601, 0.601, 0.620, 0.986, 0.987, 0.989, 0.986, 0.987, 0.989, 1.196, 1.196, 1.196, 1.196, 1.207, 1.207, 1.479, 1.480, 1.480, 1.481, 1.481, 1.483, 1.483, 1.491, 1.491, 1.493, 1.493, 1.493, 1.493]
#all the barriers below 1.3 eV
barrier_list = [0.601, 0.601, 0.620, 0.986, 0.987, 0.989, 0.986, 0.987, 0.989, 1.196, 1.196, 1.196, 1.196, 1.207, 1.207]
barrier_list0 = copy.copy(barrier_list)
print barrier_list
print len(barrier_list)
rate_ref = 155015617.903

f = open(join(path, 'processtable'))
processes = {}
test_list = []
last_barrier = -1
last_rate    = -1
rate_sum = 0
for line in f:
    fields = line.split()
    if fields[0] == 'proc': continue
    number = int(fields[0])
    barrier = float(fields[6])
    barrier = round(barrier, 3)
    rate    = float(fields[7])
    frequency = int(fields[8])+1

    processes[number] = {'barrier':barrier, 'frequency':frequency}

    if barrier < 1.3 and barrier not in barrier_list0: 
        print "Found an unexped barrier, check it carefully:"
        print barrier
        #sys.exit()
    if barrier < 1.3:
        test_list.append(barrier)
    if barrier in barrier_list:
        i = barrier_list.index(barrier)
        del barrier_list[i]
    if len(barrier_list) == 0 and last_barrier < 0: 
        last_barrier = number

    rate_sum += rate * 1.2
    if rate_sum >= rate_ref * rate_accuracy and last_rate < 0:
        last_rate    = number

test_list.sort()
print test_list
print len(test_list)

f.close()
if last_barrier > 0:
    print "Found all the barriers less than 1.5eV. Total number of processes examined:"
    print last_barrier
else: 
    print "Failed, processes with the following barriers are missed:"
    print barrier_list
    print "Please run more searches."

if last_rate > 0:
    print "The escape rate reaches ", rate_accuracy, "of the reference hTST rate. Total number of processes examined:"
    print last_rate
else: 
    print "Failed, the escape rate did not reach the confidence of ", rate_accuracy
    print "Please run more searches."

f = open(join(path, 'search_results.txt'))
f.readline()
f.readline()
fcs_sum    = 0
search_num = 0
fcsbarrier_sum = 0
fcsrate_sum    = 0
searchbarrier_num  = 0
searchrate_num     = 0
for line in f:
    search_num +=1
    fields = line.split()
    saddle_forcecalls = int(fields[4])
    fcs_sum += saddle_forcecalls
    result_string = fields[-1]
    if '-' not in result_string:
        continue
    first_part = result_string.split('-')[0]
    if first_part not in ("good"):
        continue

    id = int(result_string.split('-')[1])
    if id == last_barrier: 
        searchbarrier_num = search_num
        fcsbarrier_sum    = fcs_sum
    if id == last_rate: 
        searchrate_num = search_num
        fcsrate_sum    = fcs_sum

print "Number of Barrier Searches:"
print searchbarrier_num - 2
print "ForceCalls:"
print "%.3e" % fcsbarrier_sum

print "Number of Rate Searches:"
print searchrate_num - 2
print "ForceCalls:"
print "%.3e" % fcsrate_sum

resultfile = open('benchmark.dat','w')
resultfile.write("barrier_jobs "+ str(searchbarrier_num - 2)+"\n")
resultfile.write("barrier_force_calls %.3e \n" % fcsbarrier_sum)
resultfile.write("rate_jobs "+ str(searchrate_num - 2)+"\n")
resultfile.write("rate_force_calls % .3e \n " % fcsrate_sum)
resultfile.write("average over %i \n" % 1)
resultfile.write("contributor Penghao Xiao\n")
resultfile.close()


