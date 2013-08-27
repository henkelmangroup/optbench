#!/bin/bash
./refresh_scripts.sh

M=100
maxstep=0.2
python run_lbfgs.py -M $M --maxstep=$maxstep
./report.sh $M $maxstep

echo "hidden $hidden" >> benchmark.dat
