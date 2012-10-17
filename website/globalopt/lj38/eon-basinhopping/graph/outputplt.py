#!/usr/bin/python
#Outputs a file for gnuplot plotting

import glob
import os

datfiles = glob.glob('*.dat')
with open('batch.plt','w') as bplt:
	bplt.write("""#!/usr/bin/gnuplot -persist
set logscale x
set logscale y
set xlabel 'ln(fcalls)'
set ylabel 'ln(E-Eo)'
plot \\\n""")

	for i, file in enumerate(datfiles):
		if i != len(datfiles) - 1:
			bplt.write("""'%s' using 1:3 with l title '%s', \\\n""" % (file, file))

		else:
			bplt.write("""'%s' using 1:3 with l title '%s'""" % (file, file))

