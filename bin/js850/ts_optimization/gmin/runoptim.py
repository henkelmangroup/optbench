import numpy as np
import subprocess
import time

def getSpecificStructure(i, directory="../pygmin/ts_candidates", prefix="ts_candidate"):
    fname = "%s/%s.%04d" % (directory, prefix, i)
    coords = np.genfromtxt(fname)
    return coords, fname

def getStructures(nfiles=200, directory="../pygmin/ts_candidates", prefix="ts_candidate"):
    for i in range(nfiles):
        coords, fname = getSpecificStructure(i, directory=directory, prefix=prefix)
        yield coords, i, fname

def makeodata(coords):
    subprocess.call( ["cp", "-p", "odata.preamble", "odata" ]  )
    with open("odata", "a") as fout:
        fout.write("points\n")
        for i in range(len(coords[:,0])):
            fout.write("AX %f %f %f\n" % tuple(coords[i,:]) )
    
def refindTS(index):
    coords, fname = getSpecificStructure(index)
    findTS(index, coords)

def findTS(index, coords, OPTIM="/home/js850/git/OPTIM/source/build/OPTIM"):
    #set up odata file
    makeodata(coords)

    #run OPTIM
    oout = "Oout.%04d" % index
    runOPTIM = OPTIM + " > " + oout
    print runOPTIM
    t0 = time.clock()
    subprocess.call( runOPTIM, shell=True )
    t1 = time.clock()

def analyzeTS(index):

    #run OPTIM
    oout = "Oout.%04d" % index


    success = False
    ncalls = -1
    eigenval = 100
    while True:
        #sometimes python starts to read the oout file before the shell has finished reading it.
        #this is a hacky way of avoiding that problem
        #subprocess.call( ["sleep", "0.2"] )
        #subprocess.call( ["sync"] )


        with open(oout, "r") as fin:
            for line in fin:
                sline = line.split()
                if "energy+gradient calls=" in line:
                    ncalls = int(sline[5])
                elif "bfgsts> RMS grad=" in line:
                    rms = float(sline[3])
                elif "mylbfgs> Final energy is" in line:
                    energy = float(sline[4])
                elif "xmylbfgs> Eigenvalue and RMS=" in line:
                    eigenval = float(sline[4])
                #elif "xmylbfgs> Smallest eigenvalue converged in" in line:
                    #eigenval = float(sline[8])
                elif "mylbfgs> Energy and RMS force=" in line:
                    steps = int(sline[8])
                elif "**** CONVERGED ****" in line:
                    success = True
        if ncalls < 0:
            print "can't find ncalls: this usually means there was a problem dumping optim output into a file"
            print "    rerunning optim"
            refindTS(index)
        else:
            break
    
    return (ncalls, energy, eigenval, rms)
    exit(1)

def main():
    resultsfname = "results"
    results = []

    nfiles_tot = 200
    nfiles = 0
    t0 = time.clock()
    if True:
        for coords, ncount, fname in getStructures():
            print fname
            findTS(nfiles, coords)
            nfiles += 1
        nfiles_tot = nfiles
    t1 = time.clock()

    for count in range(nfiles_tot):
        ncalls, energy, eigenval, rms = analyzeTS(count)
        print "ncalls", ncalls, count

        results.append( (ncalls, energy, eigenval, rms) )


        if False:
            #save ts coords
            tsfname = fname + ".ts"
            with open(tsfname, "w") as fout:
                tscoords = coords
                tscoords = np.reshape(tscoords, [-1,3])
                for i in range(len(tscoords[:,0])):
                    fout.write( "%f %f %f\n" % tuple(tscoords[i,:]) )
    
    if True:
        #results[-1]
        #print results
        with open("results", "w") as fout:
            for ncalls, energy, eigenval, rms in results:
                fout.write( "%d %f %g %g\n" % (ncalls, energy, eigenval, rms) )
    
    #print "time spent loading coords and in OPTIM", t1-t0


if __name__ == "__main__":
    main()


