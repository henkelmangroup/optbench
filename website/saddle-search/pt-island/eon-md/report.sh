#!/bin/bash
./done.py > benchmark.dat

echo "code Eon" >> benchmark.dat
echo "code_version r2156" >> benchmark.dat
echo "date $(date +'%d %b %Y')" >> benchmark.dat
echo "contributor Sam Chill" >> benchmark.dat
echo "code_file eon-r2156.tgz" >> benchmark.dat
