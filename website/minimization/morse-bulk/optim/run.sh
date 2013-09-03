#!/bin/bash -e

if [ -e simulation ]; then
    rm -rf simulation
fi
mkdir simulation && cd simulation
tar xzf ../morse-bulk.tgz

for i in {0..99}
do
    file=$(printf "pos_%04d.con" $i)
    mkdir run-$i && cd run-$i
    echo run-$i
    cp ../../odata.preamble odata
    python ../../con2coords.py ../morse-bulk/$file coords
    echo "points" >> odata
    awk '{print "M", $1, $2, $3}' coords >> odata
    ../../run_optim.sh $file 
    cd ..
done

python ../getdata.py

cat ../admin.dat >> benchmark.dat


mv benchmark.dat ..
cd ..

