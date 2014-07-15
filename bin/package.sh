#!/usr/bin/env bash
set -e
set -x

for entry in */*/*/benchmark.dat
do
    input_tar_file=$(printf "%s.tgz" $(basename $(dirname $entry)))
    path=$(dirname $entry)
    echo $path
    cd $path/..
    entry_name=$(basename $path)
    [ -e $entry_name/$input_tar_file ] && rm $entry_name/$input_tar_file
    tar chzf $entry_name/$input_tar_file $entry_name/*
    cd ../..
done
