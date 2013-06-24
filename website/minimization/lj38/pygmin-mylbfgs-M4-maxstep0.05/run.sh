#!/bin/bash

M=4
maxstep=0.05
python run_lbfgs.py -M $M --maxstep=$maxstep
./report.sh $M $maxstep
