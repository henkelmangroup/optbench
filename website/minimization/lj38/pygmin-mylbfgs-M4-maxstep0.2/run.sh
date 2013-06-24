#!/bin/bash

M=4
maxstep=0.2
python run_lbfgs.py -M $M --maxstep=$maxstep
./report.sh $M $maxstep
