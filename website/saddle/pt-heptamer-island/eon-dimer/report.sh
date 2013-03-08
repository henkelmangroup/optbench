#!/bin/bash
awk '{s+=$5;m+=$6;n+=1}END{printf "nsaddle %f\nnrelax %f\nntotal %f\n", s/n, m/n, (s+m)/n}' states/0/search_results.txt > benchmark.dat
awk '$1 ~ /[0-9]+/{n+=1}END{print "ns", n}' states/0/processtable >> benchmark.dat
awk '/good|repeat/{n+=1}END{print "rho", n/100}' states/0/search_results.txt >> benchmark.dat


echo "code Eon" >> benchmark.dat
echo "code_version r2067" >> benchmark.dat
echo "date $(date +'%d %b %Y')" >> benchmark.dat
echo "contributor Sam Chill" >> benchmark.dat
echo "code_file eon-r2067.tgz" >> benchmark.dat
