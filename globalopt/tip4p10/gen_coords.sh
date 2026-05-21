#!/usr/bin/bash

for i in $(seq 0 1 9999); do
	echo 10 5.0 ${i} 1 T > randata;
	rancoordsaa;
	cp coords ${i}.aa;
done
