#!/bin/bash

M=1
maxstep=0.1
python run_lbfgs.py -M $M --maxstep=$maxstep
./report.sh $M $maxstep
