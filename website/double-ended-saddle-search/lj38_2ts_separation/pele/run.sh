#!/bin/bash
tar -xzf coords.tgz

python dec_lj38_2ts.py
python getdata.py
echo "algorithm DNEB + hybrid eigenvector following" >> benchmark.dat
echo "code pele" >> benchmark.dat
echo "contributor Jacob Stevenson" >> benchmark.dat


rm -r coords

