#!/bin/sh

#reset and cleanup any output from previous runs
eon -Rf
#run eon
eon
#register the results from the finished calculations
eon -n
#generate benchmark.dat
./report.sh
