#!/bin/bash -e


GMIN

# js850> note: the -a flag is necessary because some of the GMIN_out files might have binary characters which confuses grep
ncalls=$(grep -a "Target hit after" GMIN_out  | tail -1 | awk '{print $7}' || echo $tmp)
nquenches=$(grep -a "Target hit after" GMIN_out  | tail -1 | awk '{print $5}' || echo $tmp)
niter=$(grep -a "Target hit after" GMIN_out  | tail -1 | awk '{print $5}' || echo $tmp)
success=$(grep -a "Target hit after" GMIN_out > /dev/null && echo 1 || echo 0)
rms=$(grep -a "Final Quench" GMIN_out | tail -1 | awk '{print $10}')
energy=$(grep -a "Final Quench" GMIN_out | tail -1 | awk '{print $5}')

if [ "$ncalls" == "" ]; then ncalls="-1"; fi
if [ "$nquenches" == "" ]; then nquenches="-1"; fi
if [ "$rms" == "" ]; then rms="-1"; fi
if [ "$energy" == "" ]; then energy="-1"; fi
if [ "$niter" == "" ]; then eigenval="-1"; fi

echo "$(basename $1) $ncalls $nquenches $energy $rms $niter $success" >> ../results.txt
