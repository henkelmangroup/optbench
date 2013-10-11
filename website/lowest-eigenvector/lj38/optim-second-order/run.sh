#!/bin/bash -e

if [ -e simulation ]; then
    rm -rf simulation
fi
mkdir simulation && cd simulation
tar -xzf ../coords.tar.gz 

for i in {0..199}
do
    file=$(printf "%.4i.xyz" $i)
    file2=$(printf "%.4i_mode" $i)
    mkdir run-$i && cd run-$i
    echo run-$i
    cp ../../odata.preamble .
    ../../run_optim.sh ../coords/$file ../coords/$file2 
    cd ..
done

python ../getdata.py

echo "algorithm hybrid eigenvector following" >> benchmark.dat
echo "code OPTIM" >> benchmark.dat
echo "contributor Jacob Stevenson and Cheng Shang" >> benchmark.dat
echo "hidden True" >> benchmark.dat


mv benchmark.dat ..
cd ..

