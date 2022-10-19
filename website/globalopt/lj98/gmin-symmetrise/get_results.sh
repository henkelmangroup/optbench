#!/bin/bash

cd simulation
python ../getdata.py --datafile=results.txt
cat ../admin.dat >> benchmark.dat
mv benchmark.dat ..
cd ..
