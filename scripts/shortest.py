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
  
#filepath = os.path.join("..", "Line_points_data", "out_6_72.txt")
#filepath = os.path.join("..", "Line_points_data", "out_overlap3.txt")

#filepath = os.path.join("..","..","..", "DynGraphData", "CAStudents_300.txt")

filepath = os.path.join(".","..","DATA",sys.argv[1])

outdir = sys.argv[2]
outpath = outdir + '_' + str(uuid.uuid4())
        
k = int(sys.argv[3])
b = int(sys.argv[4])
n = int(sys.argv[5])

#toc = time.clock()

pics = False

runMainAlgs = sys.argv[6]

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

gr_avg_best, bi_avg_best, dy_avg_best = 0.0,0.0,0.0
gr_int_best, bi_int_best, dy_int_best = 0.0,0.0,0.0
gr_size_best, bi_size_best, dy_size_best = 0.0,0.0,0.0
avg_greedy, avg_dynamic, avg_binary = 0.0,0.0,0.0


#i1 = np.random.randint(len(edgesTS), size = n)
#i2 = np.random.randint(len(edgesTS), size = n)
#print i1
#print i2

best_avg = []
best_intervals = []

# _, _, baseS = utils.getBaseline(edgesTS, B)
# avg_base = 2.0*baseS.number_of_edges()/baseS.number_of_nodes()
# size_base = baseS.number_of_nodes()


initIntervals = [(0,len(edgesTS)-1)]

if runMainAlgs == 'grbi':
    tic = time.time()
    #avg_greedy, _, nodes_covered_gr = main.main(outpath, 'greedy', charikar_version, 'unweighted', pics, k, B, edgesTS, nodes, edges, initIntervals, False)
    _, _, usedBgr, S, edges_coveredGr = main.main(outpath, 'greedy', charikar_version, 'unweighted', pics, k, B, edgesTS, nodes, edges, initIntervals, False)
    usedBgr = usedBgr.total_seconds()/(60*60*24)    
    
    avg_greedy = 2.0*S.number_of_edges()/S.number_of_nodes()
    nodes_covered_gr = S.number_of_nodes()
    toc = time.time()
    
    print 'greedy done in: ', toc-tic
    
    minspanGr, st, end = utils.shortestInt(edgesTS, edges_coveredGr);
    minspanGr = minspanGr.total_seconds()/(60*60*24)
    S1 = utils.getGraph(edgesTS[st:end+1])
    _, avg_new_greedy = charikar.charikar(copy.deepcopy(S1))
    sys.stdout.flush()
    
    
    
    tic = time.time()
    #avg_binary, _, nodes_covered_bi = main.main(outpath, 'binary', charikar_version, 'unweighted', pics, k, B, edgesTS, nodes, edges, initIntervals, False)
    _, _, usedBbi, S, edges_coveredBi = main.main(outpath, 'binary', charikar_version, 'unweighted', pics, k, B, edgesTS, nodes, edges, initIntervals, False)
    usedBbi = usedBbi.total_seconds()/(60*60*24)
           
    avg_binary = 2.0*S.number_of_edges()/S.number_of_nodes()
    nodes_covered_bi = S.number_of_nodes()
    toc = time.time()
    print 'binary done in: ', toc-tic
    minspanBi, st, end  = utils.shortestInt(edgesTS, edges_coveredBi)
    minspanBi = minspanBi.total_seconds()/(60*60*24)
    S1 = utils.getGraph(edgesTS[st:end+1])
    _, avg_new_binary = charikar.charikar(copy.deepcopy(S1))    
   
   
    sys.stdout.flush()

else:
    tic = time.time()
    baseS, _, _, S, _  = main.main(outpath, 'dynprogr', charikar_version, 'weighted', pics, k, B, edgesTS, nodes, edges, initIntervals, False)
    toc = time.time()
    print 'dynamic done in: ', toc-tic
    sys.stdout.flush()    

ff = open(outpath, "a")
ff.write(' '.join([str(avg_greedy)[:6], str(avg_binary)[:6],
str(nodes_covered_gr), str(nodes_covered_bi),
str(usedBgr)[:6],str(minspanGr)[:6],
str(usedBbi)[:6],str(minspanBi)[:6],
str(avg_new_greedy)[:6],str(avg_new_binary)[:6],
'\n']))
ff.close()
 