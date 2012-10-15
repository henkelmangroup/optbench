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
	if(nc>10000) ntoomany++;
	nfcavg+=nc;
	time_tot+=$4;
}
END {
	nfc_per_sec=nfcavg/time_tot;
	nfcavg=nfcavg/nrun;
	printf("nconf,nfail,nfcmin,nfcmax,nfcavg,nfc_per_sec: %5d  %5d  %5d  %5d  %10.1f  %10.1f  \n",nrun,nfail,nfcmin,nfcmax,nfcavg,nfc_per_sec);
	printf("force_calls %10.1f\n",nfcavg)                 > "benchmark.dat";
	printf("force_calls_min %10.1f\n",nfcmin)             >> "benchmark.dat";
	printf("force_calls_max %10.1f\n",nfcmax)             >> "benchmark.dat";
	printf("force_calls_per_second %10.1f\n",nfc_per_sec) >> "benchmark.dat";
	printf("wall_time %10.5f\n",time_tot/nrun) >> "benchmark.dat";
	printf("nfailed %i\n", ntoomany+nfail) >> "benchmark.dat";

    print "code Alireza/Nocedal" >> "benchmark.dat";
	print "contributor Alireza" >> "benchmark.dat";
	print "algorithm L-BFGS Line Search" >> "benchmark.dat";
	print "date ", strftime("%d %b %Y") >> "benchmark.dat";

}
