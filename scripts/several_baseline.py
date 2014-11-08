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
from allutils import utils, charikar
import uuid
import loop_and_short_function
  
#filepath = os.path.join("..", "Line_points_data", "out_6_72.txt")
#filepath = os.path.join("..", "Line_points_data", "out_overlap3.txt")

#filepath = os.path.join("..","..","..", "DynGraphData", "CAStudents_300.txt")

filepath = os.path.join(".","..","DATA",sys.argv[1])

outdir = sys.argv[2]
outpath = outdir + '_' + str(uuid.uuid4())
#outpath = outdir
#outpath =  os.path.join(outdir, outdir + '_' + str(uuid.uuid4()))
#print outdir, outpath

#if not os.path.exists(outdir):
#        os.makedirs(outdir)
        
k = int(sys.argv[3])
b = int(sys.argv[4])
n = int(sys.argv[5])
comN = int(sys.argv[6])

#toc = time.clock()

pics = False

runMainAlgs = sys.argv[7]

#alg = 'dynprogr'
#alg = 'greedy'
#alg = 'binary'

charikar_version = 'basic'
#charikar_version = 'fixed'

# if alg == 'greedy' or alg == 'binary':
    # charikar_mode = 'unweighted'

# if alg == 'dynprogr':
    # charikar_mode = 'weighted'

#k = 3
#B = timedelta(seconds = 20)
B = timedelta(days = b)

#n = 1000

edgesTS, nodes, edges =  utils.readFile(filepath)  

# gr_avg_best, bi_avg_best, dy_avg_best = 0.0,0.0,0.0
# gr_int_best, bi_int_best, dy_int_best = 0.0,0.0,0.0
# gr_size_best, bi_size_best, dy_size_best = 0.0,0.0,0.0
# avg_greedy, avg_dynamic, avg_binary = 0.0,0.0,0.0


#print i1
#print i2

best_avg = []
best_intervals = []

initIntervals = [(0,len(edgesTS)-1)]

edgesTSBi = copy.deepcopy(edgesTS)
edgesTSGr = copy.deepcopy(edgesTS)
#G = utils.getGraph(edgesTS)

for ind in xrange(0, comN):

    baseAvg, baseInt, S = utils.getBaseline(edgesTS, B)
    #S, avg_char = charikar.charikar(copy.deepcopy(G))
    #G.remove_edges_from(S.edges())
    #Sedges = S.edges()
    Sedges = np.array(S.edges())
    Sedges.sort(1)
    Sedges = map(tuple,Sedges)
    #minspanChar, _, _ = utils.shortestInt(edgesTS, Sedges)
    #minspanChar = minspanChar.total_seconds()/(60*60*24.0)
    
    
    T = []
    #print len(edgesTSGr)
    for i in edgesTS:
        if i[1] not in Sedges:
            T.append(i)
    edgesTS = copy.deepcopy(T)
        
    if runMainAlgs == 'grbi': 

        #avg_greedy, _, num_nodes_gr = main.main(outpath, 'greedy', charikar_version, 'unweighted', pics, k, B, edgesTS, nodes, edges, initIntervals, False)
        #nodes_coveredGr, timeIntGr, usedBgr, S, edges_coveredGr = loop_and_short_function.gamble(edgesTSGr, k, B, n, 'gr', nodes, edges, [(0,len(edgesTSGr)-1)])
        nodes_coveredGr, timeIntGr, usedBgr, Sgr, edges_coveredGr = main.main(outpath, 'greedy', charikar_version, 'unweighted', pics, k, B, edgesTSGr, nodes, edges, [(0,len(edgesTSGr)-1)], False)
        #print edges_coveredGr
        usedBgr = usedBgr.total_seconds()/(60*60*24.0)  
        
        #avg_greedy = 2.0*S.number_of_edges()/S.number_of_nodes()
        avg_greedy = 2.0*len(edges_coveredGr)/len(nodes_coveredGr)
        num_nodes_gr = len(nodes_coveredGr)
        num_edges_gr = len(edges_coveredGr)
        
        
        T = []
        #print len(edgesTSGr)
        for i in edgesTSGr:
            if i[1] not in edges_coveredGr:
                T.append(i)
        edgesTSGr = copy.deepcopy(T)
        #print len(edgesTSGr)
        # minspanGr, st, end = utils.shortestInt(edgesTS, edges_coveredGr);
        # minspanGr = minspanGr.total_seconds()/(60*60*24.0)
        
            
        #nodes_coveredBi, timeIntBi, usedBbi, S, edges_coveredBi = loop_and_short_function.gamble(edgesTSGr, k, B, n, 'bi',  nodes, edges, [(0,len(edgesTSGr)-1)])
        nodes_coveredBi, timeIntBi, usedBbi, Sbi, edges_coveredBi = main.main(outpath, 'binary', charikar_version, 'unweighted', pics, k, B, edgesTSBi, nodes, edges, [(0,len(edgesTSBi)-1)], False)
        usedBbi = usedBbi.total_seconds()/(60*60*24.0)
        
        avg_binary = 2.0*len(edges_coveredBi)/len(nodes_coveredBi)
        num_nodes_bi = len(nodes_coveredBi)
        num_edges_bi = len(edges_coveredBi)
        
        T = []
        for i in edgesTSBi:
            if i[1] not in edges_coveredBi:
                T.append(i)
        edgesTSBi = copy.deepcopy(T)
        
        # minspanBi, st, end  = utils.shortestInt(edgesTS, edges_coveredBi)
        # minspanBi = minspanBi.total_seconds()/(60*60*24.0)
        sys.stdout.flush()
    
    else:
        tic = time.time()
        baseS, _, _, Sdi, _  = main.main(outpath, 'dynprogr', charikar_version, 'weighted', pics, k, B, edgesTS, nodes, edges, initIntervals, False)
        toc = time.time()
        #print 'dynamic done in: ', toc-tic
        sys.stdout.flush()    
    
    ff = open(outpath, "a")    
    ff.write(' '.join([str(avg_greedy)[:6], str(avg_binary)[:6], str(baseAvg)[:6],
    str(num_nodes_gr), str(num_nodes_bi),str(S.number_of_nodes()),
    str(num_edges_gr), str(num_edges_bi),str(S.number_of_edges()),
    str(usedBgr)[:6],
    str(usedBbi)[:6],
    str(B)[:6],
    
    
    
    ';'.join(map(str,nodes_coveredGr)),
    ';'.join(map(str,nodes_coveredBi)),
    ';'.join(map(str,S.nodes())),
    # ';'.join(map(str,timeIntGr)),
    # ';'.join(map(str,timeIntBi)),
    # ';'.join(map(str,edges_coveredGr)),
    # ';'.join(map(str,edges_coveredBi)),
    
    '\n']))
    ff.close()
 