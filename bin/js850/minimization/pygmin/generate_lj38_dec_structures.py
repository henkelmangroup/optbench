import os
import numpy as np

import networkx as nx

from pele.systems import LJCluster
from pele.utils.disconnectivity_graph import database2graph
from pele.utils.xyz import write_xyz

def test(G, m1, m2):
    path = nx.shortest_path(G, m1, m2)
    print [m._id for m in path]
    print path

def main():
    write = False
    natoms = 38
    system = LJCluster(natoms)
    db = system.create_database("lj38.big.sqlite")
#    db = system.create_database("lj38.small.sqlite")

    
    print "making graph from database"
    graph = database2graph(db)
    print "done making graph"
    
    dist = 2
    for count, m in enumerate(db.minima()):
        if count > 50: break
        
        # get the distances from this graph
        distances = nx.single_source_shortest_path_length(graph, m, cutoff=dist)
#        print distances
        
        for m2, d in distances.iteritems():
            if d == dist:
                break
#        print d, m2
        if d != dist:
            print "failed to find a minimum at distance", dist 
            continue
        
        print m.energy, m2.energy
        test(graph, m, m2)
        
        
        # put them in best alignment
        mindist = system.get_mindist(niter=100)
        xdist, x1, x2 = mindist(m.coords, m2.coords)
        
        if write:
            dir = "dec_lj38_dist%d" % dist
            write_xyz(open(dir + "/start_%d.xyz"%count, "w"), x1, title="energy %f" % m.energy)
            write_xyz(open(dir + "/end_%d.xyz"%count, "w"), x2, title="energy %f" % m2.energy)
        
    

if __name__ == "__main__":
    main()
