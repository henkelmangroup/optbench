import argparse
import numpy as np

from tools import read_con_file

def main():
    parser = argparse.ArgumentParser(description="convert a con file to a coords file")
    parser.add_argument("confile", type=str, help="file to read from")
    parser.add_argument("outfile", type=str, help="file to write to")
    parser.add_argument("--frozen", type=str, help="file to write to write frozen atoms to", default="")
    parser.add_argument("--scale", type=float, help="scale the coordinates by this amount", default=None)
    parser.add_argument("--c-indexing", action="store_true", help="write the indices of the frozen atom with c-indexing (default fortran indexing)")
    parser.add_argument("--box-lengths", type=str, help="file to write to write box lengths to", default="")

    args = parser.parse_args()
    
    res = read_con_file(args.confile)
    
    coords = res.coords.reshape([-1,3])
    
    if args.scale is not None:
        coords *= args.scale
    
    
    np.savetxt(args.outfile, coords, fmt="%.16f")
    
    if args.frozen != "":
        # print the frozen atoms indices to file args.frozen
        # print maximum 8 indices on each line
        frozen_indices = np.where(res.frozen)[0]
        if not args.c_indexing:
            frozen_indices += 1
        with open(args.frozen, "w") as fout:
            i = 0
            while i < len(frozen_indices):
                try:
                    indices = frozen_indices[i:i+8]
                except IndexError:
                    indices = frozen_indices[i:]
                if len(indices) > 0:
                    istrings = map(str, indices)
                    fout.write(" ".join(istrings) + "\n")
                i  += 8
        
        
    
    if args.box_lengths != "":
        with open(args.box_lengths, "w") as fout:
            fout.write("%f %f %f\n" % tuple(res.boxvec))
            
    
    

if __name__ == "__main__":
    main()