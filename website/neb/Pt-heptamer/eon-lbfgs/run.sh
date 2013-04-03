#!/usr/bin/env bash
set -e
cd minima

for d in min??
do
    cd $d
    cp a.con reactant.con
    cp b.con product.con
    cp ../../config.ini .
    eonclient > /dev/null
    echo -n $d
    awk '/neb/{print " ", $1/8}' results.dat
    cd ..
done
