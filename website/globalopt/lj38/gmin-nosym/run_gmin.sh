#!/bin/bash -e


GMIN

ncalls=$(grep "Target hit after" GMIN_out  | tail -1 | awk '{print $7}' || echo $tmp)
niter=$(grep "Target hit after" GMIN_out  | tail -1 | awk '{print $5}' || echo $tmp)
success=$(grep "Target hit after" GMIN_out > /dev/null && echo 1 || echo 0)
rms=$(grep "Final Quench" GMIN_out | tail -1 | awk '{print $10}')
energy=$(grep "Final Quench" GMIN_out | tail -1 | awk '{print $5}')

if [ "$ncalls" == "" ]; then ncalls="-1"; fi
if [ "$rms" == "" ]; then rms="-1"; fi
if [ "$energy" == "" ]; then energy="-1"; fi
if [ "$niter" == "" ]; then eigenval="-1"; fi

echo "$(basename $1) $ncalls $energy $rms $niter $success" >> ../results.txt
