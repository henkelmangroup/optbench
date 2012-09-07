#!/usr/bin/gnuplot -persist
set terminal png
set output 'graph.png'
set logscale x
set logscale y
set xlabel 'ln(fcalls)'
set ylabel 'ln(E-Eo)'
plot \
'graph.dat' using 1:3 with l title 'Average energy and forcecalls for each basin hopping step'


