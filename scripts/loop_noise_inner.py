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
from allutils import utils, generate
import uuid

  
#filepath = os.path.join(".","..","DATA",sys.argv[1])

outpath = 'out.txt'
# outdir = sys.argv[2]
# outpath = outdir + '_' + str(uuid.uuid4())
        
# k = int(sys.argv[3])
# b = int(sys.argv[4])
# n = int(sys.argv[5])
n = 1

#toc = time.clock()

pics = False

#runMainAlgs = sys.argv[6]
runMainAlgs = 'grbi'

#alg = 'dynprogr'
#alg = 'greedy'
#alg = 'binary'

charikar_version = 'basic'
#charikar_version = 'fixed'

# if alg == 'greedy' or alg == 'binary':
    # charikar_mode = 'unweighted'

# if alg == 'dynprogr':
    # charikar_mode = 'weighted'
k = 3
B = timedelta(seconds = 100)

#n = 1000

#edgesTS, nodes, edges =  utils.readFile(filepath)  

gr_avg_best, bi_avg_best, dy_avg_best = 0.0,0.0,0.0
gr_int_best, bi_int_best, dy_int_best = 0.0,0.0,0.0
gr_size_best, bi_size_best, dy_size_best = 0.0,0.0,0.0
avg_greedy, avg_dynamic, avg_binary = 0.0,0.0,0.0




# i1 = np.random.randint(len(edgesTS), size = n)
# i2 = np.random.randint(len(edgesTS), size = n)
#print i1
#print i2

best_avg = []
best_intervals = []
nodesInCom = 8
truth = set(range(0,nodesInCom))
noise = 4.0

innernoise = 1.5

while innernoise < 6.9:

    innernoise += 0.5
    avgBack = []
    precGr, precBi = [],[]
    recallGr, recallBi = [],[]
    #FmGr, FmBi = {},{}
    for ind in xrange(0,n):
    
        nodes, edges = [],[]
        edgesTS, _, inner_out = generate.generate(k, B, 1, noise, innernoise, nodesInCom, 500, 1000)
        print len(edgesTS)
        break
        #i,j = i1[ind], i2[ind]
        #st, end = min(i,j), max(i,j)    
        initIntervals = []    
        #initIntervals.append((st, end))
        initIntervals.append((0, len(edgesTS)))
        #try:
        
        if runMainAlgs == 'grbi':
            tic = time.time()
            #avg_greedy, _, num_nodes_gr = main.main(outpath, 'greedy', charikar_version, 'unweighted', pics, k, B, edgesTS, nodes, edges, initIntervals, False)
            nodes_coveredGr, timeIntGr, usedBgr, S, edges_coveredGr = main.main(outpath, 'greedy', charikar_version, 'unweighted', pics, k, B, edgesTS, nodes, edges, initIntervals, False)
            usedBgr = usedBgr.total_seconds()/(60*60*24.0)  
            
            #avg_greedy = 2.0*S.number_of_edges()/S.number_of_nodes()
            avg_greedy = 2.0*len(edges_coveredGr)/len(nodes_coveredGr)
            num_nodes_gr = len(nodes_coveredGr)
            num_edges_gr = len(edges_coveredGr)
            toc = time.time()
            #print 'greedy done in: ', toc-tic
            
            minspanGr, st, end = utils.shortestInt(edgesTS, edges_coveredGr);
            minspanGr = minspanGr.total_seconds()/(60*60*24.0)
            
            sys.stdout.flush()
            
            tic = time.time()
            #avg_binary, _, num_nodes_bi = main.main(outpath, 'binary', charikar_version, 'unweighted', pics, k, B, edgesTS, nodes, edges, initIntervals, False)
            nodes_coveredBi, timeIntBi, usedBbi, S, edges_coveredBi = main.main(outpath, 'binary', charikar_version, 'unweighted', pics, k, B, edgesTS, nodes, edges, initIntervals, False)
            usedBbi = usedBbi.total_seconds()/(60*60*24.0)
            
            avg_binary = 2.0*len(edges_coveredBi)/len(nodes_coveredBi)
            num_nodes_bi = len(nodes_coveredBi)
            num_edges_bi = len(edges_coveredBi)
            toc = time.time()
            #print 'binary done in: ', toc-tic
            minspanBi, st, end  = utils.shortestInt(edgesTS, edges_coveredBi)
            minspanBi = minspanBi.total_seconds()/(60*60*24.0)
            sys.stdout.flush()
        
        else:
            tic = time.time()
            baseS, _, _, S, _  = main.main(outpath, 'dynprogr', charikar_version, 'weighted', pics, k, B, edgesTS, nodes, edges, initIntervals, False)
            toc = time.time()
            #print 'dynamic done in: ', toc-tic
            sys.stdout.flush()
    
        avgBack.append(inner_out)
        inter = set(nodes_coveredGr).intersection(truth)
        precGr.append(1.0*len(inter)/len(nodes_coveredGr))
        recallGr.append(1.0*len(inter)/len(truth))
        #FmGr[avg_back] = 2.0*precGr[avg_back]*recallGr[avg_back]/(precGr[avg_back]+recallGr[avg_back])
        
        inter = set(nodes_coveredBi).intersection(truth)
        precBi.append(1.0*len(inter)/len(nodes_coveredBi))
        recallBi.append(1.0*len(inter)/len(truth))
        #FmBi[avg_back] = 2.0*precBi[avg_back]*recallBi[avg_back]/(precBi[avg_back]+recallBi[avg_back])
    
    # try:
        # fmGr = 2.0*np.mean(precGr)*np.mean(recallGr)/(np.mean(precGr)+np.mean(recallGr))
    # except:
        # fmGr = 0.0
    # try:
        # fmBi = 2.0*np.mean(precBi)*np.mean(recallBi)/(np.mean(precBi)+np.mean(recallBi))
    # except:
        # fmBi = 0.0
    #print np.mean(precGr.keys()),
    print np.mean(avgBack), np.mean(precGr), np.mean(precBi), np.mean(recallGr), np.mean(recallBi)#, fmGr, fmBi
    #2.0*np.mean(precGr.values())*np.mean(recallGr.values())/(np.mean(precGr.values())+np.mean(recallGr.values())),
    #2.0*np.mean(precBi.values())*np.mean(recallBi.values())/(np.mean(precBi.values())+np.mean(recallBi.values()))
    
    
 
    
    
    