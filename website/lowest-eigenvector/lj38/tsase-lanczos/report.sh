#!/bin/bash
Lfcalls=$(awk '$2~/Lanczos_force_calls/{if ($1<10000){fc+=$1;n+=1}}END{printf("%.0f\n", fc/n)}' runs/run-*/results.dat)
Lfcalls_max=$(awk '$2~/Lanczos_force_calls/{if ($1<10000){printf("%.0f\n", $1)}}' runs/run-*/results.dat | sort -g | tail -n 1)
Lfcalls_min=$(awk '$2~/Lanczos_force_calls/{if ($1<10000){printf("%.0f\n", $1)}}' runs/run-*/results.dat | sort -gr | tail -n 1)

Bfcalls=$(awk '$2~/BFGS_force_calls/{if ($1<10000){fc+=$1;n+=1}}END{printf("%.0f\n", fc/n)}' runs/run-*/results.dat)
Bfcalls_max=$(awk '$2~/BFGS_force_calls/{if ($1<10000){printf("%.0f\n", $1)}}' runs/run-*/results.dat | sort -g | tail -n 1)
Bfcalls_min=$(awk '$2~/BFGS_force_calls/{if ($1<10000){printf("%.0f\n", $1)}}' runs/run-*/results.dat | sort -gr | tail -n 1)

Cfcalls=$(awk '$2~/CG_force_calls/{if ($1<10000){fc+=$1;n+=1}}END{printf("%.0f\n", fc/n)}' runs/run-*/results.dat)
Cfcalls_max=$(awk '$2~/CG_force_calls/{if ($1<10000){printf("%.0f\n", $1)}}' runs/run-*/results.dat | sort -g | tail -n 1)
Cfcalls_min=$(awk '$2~/CG_force_calls/{if ($1<10000){printf("%.0f\n", $1)}}' runs/run-*/results.dat | sort -gr | tail -n 1)

#nfailed=$(awk 'BEGIN{n=0} $2~/termination_reason/&&$1!=0{n+=1}END{print n}' runs/run-*/results.dat)
nfailed=0
#fcalls_median=$(grep -h force_calls runs/*/results.dat | sort -g | awk '{count[NR] = $1}END{if (NR%2) { print count[(NR+1)/2]; }else{ print (count[NR/2]+count[(NR/2)+1])/2;} }')

echo "Lanczos_force_calls $Lfcalls" > benchmark.dat
echo "Lanczos_force_calls_max $Lfcalls_max" >> benchmark.dat
echo "Lanczos_force_calls_min $Lfcalls_min" >> benchmark.dat
echo "dimer_BFGS_force_calls $Bfcalls" >> benchmark.dat
echo "dimer_BFGS_force_calls_max $Bfcalls_max" >> benchmark.dat
echo "dimer_BFGS_force_calls_min $Bfcalls_min" >> benchmark.dat
echo "dimer_CG_force_calls $Cfcalls" >> benchmark.dat
echo "dimer_CG_force_calls_max $Cfcalls_max" >> benchmark.dat
echo "dimer_CG_force_calls_min $Cfcalls_min" >> benchmark.dat
echo "nfailed $nfailed" >> benchmark.dat
echo "code TSASE" >> benchmark.dat
echo "date $(date +'%d %b %Y')" >> benchmark.dat
echo "contributor Penghao Xiao" >> benchmark.dat
#echo "code_version r2156" >> benchmark.dat
#echo "code_file eon-r2156.tgz" >> benchmark.dat
