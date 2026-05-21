#!/bin/sh
set -e

if [ -e runs ]; then
    rm -rf runs
fi
mkdir -p runs
cd runs
tar xfz ../coords-bart.tar.gz
for i in {0..199}
do
    file=$(printf "%.4i" $i)
    mkdir -p run-$i
    /bin/echo -n run-$i 
    cp coords-bart/$file run-$i/refconfig
    cp coords-bart/$file run-$i/posinp
    cp ../bart.sh run-$i
    cd run-$i
    ./bart.sh | grep SADDLE
    cd ..
done
