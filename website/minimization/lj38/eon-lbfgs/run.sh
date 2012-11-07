#!/bin/sh
if [ -e simulation ]; then
    rm -rf simulation
fi
mkdir simulation
cp ../lj38-clusters.tgz simulation
cd simulation
tar xfz lj38-clusters.tgz
rm lj38-clusters/*.xyz
for i in {0..999}
do
    file=$(printf "cluster_%.4i.con" $i)
    mkdir run-$i
    echo run-$i
    mv lj38-clusters/$file run-$i/pos.con
    cp ../config.ini run-$i
    cd run-$i
    ../../client > stdout.dat
    cd ..
done
rm -rf lj38-clusters*
cd ..
./report.sh
