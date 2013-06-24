#!/bin/bash 
M=$1
maxstep=$2
python gmin_getdata.py "lbfgs_data.ncalls" "L-BFGS M=$M maxstep=$maxstep" pele
