import numpy as np

from pele.systems import LJCluster
from pele.utils.xyz import read_xyz
from pele.utils.hessian import sort_eigs

system = LJCluster(38)

datadir = "../coords"
for i in range(200):
    fname = datadir + "/%04d.xyz" % i
    xyz = read_xyz(open(fname, "r"))
    freqs, vecs = system.get_normalmodes(xyz.coords.flatten())
    
    freqs, vecs = sort_eigs(freqs, vecs)
    
    if True:
        vec = vecs[:,0]
        fnameout = datadir + "/%04d_mode" % i
        with open(fnameout, "w") as fout:
            fout.write("#eigenvalue " + str(freqs[0]) + "\n")
            for v in np.real(vec):
                fout.write(str(v) + "\n")
    print fname, np.min(freqs)
