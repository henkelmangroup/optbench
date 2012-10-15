#!/bin/sh
[ -e o1 ] || bunzip2 -k o1.bz2
grep converged o1 | awk -f f1.awk
