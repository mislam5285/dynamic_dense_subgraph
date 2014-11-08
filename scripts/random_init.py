import networkx as nx
import time
from datetime import datetime, timedelta
from collections import OrderedDict
#import matplotlib.pyplot as plt
import sys
import operator
import os
import copy
import numpy as np
import main
from allutils import utils
import uuid

def random_run(outpath, charikar_version, pics, k, B, edgesTS, nodes, edges, n, alg):

    avg_best, int_best, size_best, avg = 0.0, 0.0, 0.0, 0.0
    i1 = np.random.randint(len(edgesTS), size = n)
    i2 = np.random.randint(len(edgesTS), size = n)

    for ind in xrange(0,n):
        i,j = i1[ind], i2[ind]
        st, end = min(i,j), max(i,j)    
        initIntervals = []    
        
        initIntervals.append((st, end))
        
        if alg == 'greedy':
            tic = time.time()
            avg, _, nodes_covered = main.main(outpath, 'greedy', charikar_version, 'unweighted', pics, k, B, edgesTS, nodes, edges, initIntervals, False)
            toc = time.time()
            print 'greedy done in: ', toc-tic
            sys.stdout.flush()
        
        elif alg == 'binary':
            tic = time.time()
            avg, _, nodes_covered = main.main(outpath, 'binary', charikar_version, 'unweighted', pics, k, B, edgesTS, nodes, edges, initIntervals, False)
            toc = time.time()
            print 'binary done in: ', toc-tic
            sys.stdout.flush()
        
        elif alg == 'dynprogr':
            tic = time.time()
            avg,_, nodes_covered  = main.main(outpath, 'dynprogr', charikar_version, 'weighted', pics, k, B, edgesTS, nodes, edges, initIntervals, False)
            toc = time.time()
            print 'dynamic done in: ', toc-tic
            sys.stdout.flush()    
        
        if avg_best < avg:
            avg_best = avg
            int_best = (st, end)
            size_best = len(nodes_covered)        

    return avg_best, int_best, nodes_covered
        
if __name__ == "__main__":
    #filepath = os.path.join("..", "DynGraphData", "meme_10000.txt")
    #filepath = os.path.join("..", "..", "DynGraphData", "CAStudents_500.txt")
    #filepath = os.path.join("DATA","CAStudents_1000.txt")
    #filepath = os.path.join("..", "DynGraphData", "twitter_10000.txt")
    #filepath = os.path.join("..", "Line_points_data", "out.txt")
    #filepath = os.path.join("..", "DynGraphData", "telecom_10000.txt")
    #filepath = os.path.join("..", "DynGraphData", "meme_1000.txt")
    #filepath = os.path.join("..", "Line_points_data", "line_point_short1_tight_groups.txt")
    #filepath = os.path.join("..", "Line_points_data", "out_6_72.txt")
    #filepath = os.path.join("..", "Line_points_data", "out_overlap3.txt")

    #filepath = os.path.join("..","..","..", "DynGraphData", "CAStudents_300.txt")

    filepath = os.path.join(".","..","DATA",sys.argv[1])

    outdir = sys.argv[2]
    outpath =  os.path.join(outdir, outdir + '_' + str(uuid.uuid4()))
    #print outdir, outpath

    if not os.path.exists(outdir):
            os.makedirs(outdir)
            
    k = int(sys.argv[3])
    b = int(sys.argv[4])
    n = int(sys.argv[5])

    #toc = time.clock()

    pics = False

    runMainAlgs = bool(sys.argv[6])

    #alg = 'dynprogr'
    #alg = 'greedy'
    #alg = 'binary'

    #charikar_version = 'basic'
    charikar_version = 'fixed'

    # if alg == 'greedy' or alg == 'binary':
        # charikar_mode = 'unweighted'

    # if alg == 'dynprogr':
        # charikar_mode = 'weighted'

    #k = 3
    #B = timedelta(seconds = 20)
    B = timedelta(days = b)

    #n = 1000

    edgesTS, nodes, edges =  utils.readFile(filepath)  

    avg_best, int_best, size_best = random_run(outpath, charikar_version, pics, k, B, edgesTS, nodes, edges, n)

    ff = open(outpath, "a")
    ff.write(' '.join([str(gr_avg_best), str(avg_best), str(avg_best), str(gr_int_best), str(int_best), str(int_best),
    str(gr_size_best), str(bi_size_best), str(size_best), '\n']))
    ff.close()
    
