BEGIN {
	nrun=0;
	nc=0;
	nfcmin=10000000;
	nfcmax=0;
	nfail=0;
}
{
	nrun++;
	nc=$3
	if($2=="F") nfail++;
	if(nc<nfcmin) nfcmin=nc;
	if(nc>nfcmax) nfcmax=nc;
	nfcavg+=nc;
	time_tot+=$4;
}
END {
	nfc_per_sec=nfcavg/time_tot;
	nfcavg=nfcavg/nrun;
	printf("nconf,nfail,nfcmin,nfcmax,nfcavg,nfc_per_sec: %5d  %5d  %5d  %5d  %10.1f  %10.1f  \n",nrun,nfail,nfcmin,nfcmax,nfcavg,nfc_per_sec);
	printf("%10.1f\n",nfcavg)        > "force_calls.dat";
	printf("%10.1f\n",nfcmin)        > "force_calls_min.dat";
	printf("%10.1f\n",nfcmax)        > "force_calls_max.dat";
	printf("%10.1f\n",nfc_per_sec)   > "force_calls_per_second.dat";
	printf("%10.5f\n",time_tot/nrun) > "wall_time.dat";

	#printf("%10.1f\n",nfcavg)        ;
	#printf("%10.1f\n",nfcmin)        ;
	#printf("%10.1f\n",nfcmax)        ;
	#printf("%10.1f\n",nfc_per_sec)   ;
	#printf("%10.5f\n",time_tot/nrun) ;
}

#force_calls.dat  force_calls_max.dat  force_calls_min.dat  force_calls_per_second.dat  wall_time.dat
