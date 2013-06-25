#!/bin/bash

maxstep=0.1
python run_fire.py --maxstep=$maxstep
./report.sh $maxstep
