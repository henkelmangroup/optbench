#!/usr/bin/env python
from sys import exit

f = open('states/0/search_results.txt')
f.readline()
f.readline()
nfound = 0
ntofind = 27
cutoff = 1.5
force_calls = 0
for line in f:
    fields = line.split()
    barrier = float(fields[2])
    force_calls += int(fields[4]) + int(fields[5])
    result = fields[-1]
    if 'good' in result and barrier < cutoff:
        nfound += 1
        if nfound >= ntofind:
            print 'found %i/%i %i force calls' % (nfound,ntofind, force_calls)
            exit(0)
print 'found %i/%i %i force calls' % (nfound,ntofind, force_calls)
exit(1)
