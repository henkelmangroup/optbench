#!/bin/bash
./refresh_scripts.sh

M=100
maxstep=2.0
python run_morse.py -M $M --maxstep=$maxstep
./report.sh $M $maxstep
