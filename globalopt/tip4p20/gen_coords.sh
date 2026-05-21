#!/usr/bin/bash

mkdir 100_tip4p20
dir=100_tip4p20

for i in $(seq 0 1 99); do
	echo 20 10.0 ${i} 1 T > randata;
	rancoordsaa;
	cp coords ${dir}/${i}.aa;
done
