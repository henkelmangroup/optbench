#!/usr/bin/bash

mkdir 500_tip4p15
dir=500_tip4p15

for i in $(seq 0 1 499); do
	echo 15 7.0 ${i} 1 T > randata;
	rancoordsaa;
	cp coords ${dir}/${i}.aa;
done
