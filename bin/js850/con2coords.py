import argparse
import numpy as np

from tools import read_con_file

def main():
    parser = argparse.ArgumentParser(description="convert a con file to a coords file")
    parser.add_argument("confile", type=str, help="file to read from")
    parser.add_argument("outfile", type=str, help="file to write to")
    parser.add_argument("--frozen", type=str, help="file to write to write frozen atoms to", default="")
    parser.add_argument("--scale", type=float, help="scale the coordinates by this amout", default=None)
    
    args = parser.parse_args()
    
    res = read_con_file(args.confile)
    
    coords = res.coords.reshape([-1,3])
    
    if args.scale is not None:
        coords *= args.scale
    
    
    np.savetxt(args.outfile, coords, fmt="%.16f")
    
    if args.frozen != "":
        frozen_indices = np.where(res.frozen)
        print frozen_indices
        
    

    
    

if __name__ == "__main__":
    main()