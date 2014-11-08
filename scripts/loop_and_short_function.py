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

  
def gamble(edgesTS, k, B, n, alg, nodes, edges):
    print 'CALLED', alg

    charikar_version = 'basic'
    outpath = ''
    pics = False
   
    i1 = np.random.randint(len(edgesTS), size = n)
    i2 = np.random.randint(len(edgesTS), size = n)


    b_nodes_covered, b_timeInt, b_usedB, b_S, b_edges_covered, b_avg = [],[],[],[],[], -1.0

    for ind in xrange(0,n):
        i,j = i1[ind], i2[ind]
        st, end = min(i,j), max(i,j)    
        initIntervals = []    
        #initIntervals[(st, end)] = 0
        initIntervals.append((st, end))
        #try:
        
        if alg == 'gr':
            print 'HERE1'
            #avg_greedy, _, num_nodes_gr = main.main(outpath, 'greedy', charikar_version, 'unweighted', pics, k, B, edgesTS, nodes, edges, initIntervals, False)
            nodes_coveredGr, timeIntGr, usedBgr, S, edges_coveredGr = main.main(outpath, 'greedy', charikar_version, 'unweighted', pics, k, B, edgesTS, nodes, edges, initIntervals, False)
            
            avg_greedy = 2.0*len(edges_coveredGr)/len(nodes_coveredGr)
            if avg_greedy > b_avg:
                b_avg = avg_greedy
                b_nodes_covered, b_timeInt, b_usedB, b_S, b_edges_covered = copy.deepcopy(nodes_coveredGr), copy.deepcopy(timeIntGr), usedBgr, copy.deepcopy(S), copy.deepcopy(edges_coveredGr)
            
        elif alg == 'bi':   
            #avg_binary, _, num_nodes_bi = main.main(outpath, 'binary', charikar_version, 'unweighted', pics, k, B, edgesTS, nodes, edges, initIntervals, False)
            nodes_coveredBi, timeIntBi, usedBbi, S, edges_coveredBi = main.main(outpath, 'binary', charikar_version, 'unweighted', pics, k, B, edgesTS, nodes, edges, initIntervals, False)
            
            avg_binary = 2.0*len(edges_coveredBi)/len(nodes_coveredBi)
            if avg_binary > b_avg:
                b_avg = avg_binary
                b_nodes_covered, b_timeInt, b_usedB, b_S, b_edges_covered = copy.deepcopy(nodes_coveredBi), copy.deepcopy(timeIntBi), usedBbi, copy.deepcopy(S), copy.deepcopy(edges_coveredBi)        
            
        
        else:
            tic = time.time()
            baseS, _, _, S, _  = main.main(outpath, 'dynprogr', charikar_version, 'weighted', pics, k, B, edgesTS, nodes, edges, initIntervals, False)
            toc = time.time()
            print 'dynamic done in: ', toc-tic
            sys.stdout.flush()    
   
    return b_nodes_covered, b_timeInt, b_usedB, b_S, b_edges_covered
 