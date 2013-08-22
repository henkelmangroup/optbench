#!/bin/bash -e

if [ -e benchmark.dat ]; then
    rm benchmark.dat
fi

if [ -e simulation ]; then
    rm -rf simulation
fi

mkdir simulation && cd simulation

tar xzf ../../coords-xyz.tar.gz

python ../tsopt_lj.py
python ../getdata.py

mv benchmark.dat ..
cd ..
