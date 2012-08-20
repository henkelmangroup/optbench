#!/bin/bash
awk '$2~/total_force_calls/{if ($1<10000){fc+=$1;n+=1}}END{printf("%.0f\n", fc/n)}' simulation/run-*/results.dat > force_calls.dat
awk '$2~/total_force_calls/{if ($1<10000){printf("%.0f\n", $1)}}' simulation/run-*/results.dat | sort -g | tail -n 1 > force_calls_max.dat
awk '$2~/total_force_calls/{if ($1<10000){printf("%.0f\n", $1)}}' simulation/run-*/results.dat | sort -gr | tail -n 1 > force_calls_min.dat
awk 'BEGIN{n=0} $2~/total_force_calls/{if ($1>=10000){n+=1}}END{print n}' simulation/run-*/results.dat > nfailed.dat
awk '$1 ~ /real/ && $3 ~ /seconds/ {sum+=$2;n+=1}END{printf("%.4f\n", sum/n)}' simulation/run-*/stdout.dat > wall_time.dat
fcalls=$(cat force_calls.dat)
walltime=$(cat wall_time.dat)
printf "%.0f\n" `echo "scale=3;$fcalls / $walltime" | bc` > force_calls_per_second.dat
