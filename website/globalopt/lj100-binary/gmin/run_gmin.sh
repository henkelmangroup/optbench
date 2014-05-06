#!/bin/bash -e


GMIN

# js850> note: the -a flag is necessary because some of the GMIN_out files might have binary characters which confuses grep
energy=$(head -2 lowest | tail -1 | awk '{print $5}')
if [ "$energy" == "" ]; then energy="nan"; fi

echo "$(basename $1) $energy" >> ../results.txt
