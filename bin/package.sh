#!/usr/bin/env bash
set -e
set -x

for entry in */*/*/benchmark.dat
do
    input_tar_file=$(printf "%s.tgz" $(basename $(dirname $entry)))
    path=$(dirname $entry)
    echo $path
    cd $path
    [ -e $input_tar_file ] && rm $input_tar_file
    tar czf $input_tar_file *
    cd ../../..
done
