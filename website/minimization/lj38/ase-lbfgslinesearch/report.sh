#!/bin/bash
awk '$2~/total_force_calls/{fc+=$1;n+=1}END{print fc/n}' simulation/run-*/results.dat > force_calls.dat
awk '$2~/total_force_calls/{print $1}' simulation/run-*/results.dat | sort -g | tail -n 1 > force_calls_max.dat
awk '$2~/total_force_calls/{print $1}' simulation/run-*/results.dat | sort -gr | tail -n 1 > force_calls_min.dat
awk '$1 ~ /real/ && $3 ~ /seconds/ {sum+=$2;n+=1}END{print sum/n}' simulation/run-*/stdout.dat > wall_time.dat
fcalls=$(cat force_calls.dat)
walltime=$(cat wall_time.dat)
echo "scale=3;$fcalls / $walltime" | bc > force_calls_per_second.dat
