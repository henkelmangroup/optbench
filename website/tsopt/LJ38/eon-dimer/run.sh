#!/bin/sh
set -e

if [ -e runs ]; then
    rm -rf runs
fi
mkdir -p runs
cd runs
tar xfz ../../coords-con.tar.gz
for i in {0..199}
do
    file=$(printf "%.4i.con" $i)
    mkdir -p run-$i
    echo run-$i
    cp coords-con/$file run-$i/pos.con
    cp coords-con/$file run-$i/displacement.con
    cp ../config.ini run-$i
    cd run-$i
    ../../random_mode.py $i
    eonclient > stdout.dat
    cd ..
done
cd ..
./report.sh
