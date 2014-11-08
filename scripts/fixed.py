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
b = float(sys.argv[4])
#n = int(sys.argv[5])

#toc = time.clock()

pics = False

runMainAlgs = sys.argv[5]

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

avg_greedy, avg_binary, dy_avg_best = 0.0,0.0,0.0
gr_int_best, bi_int_best, dy_int_best = 0.0,0.0,0.0
num_nodes_gr, num_nodes_bi, dy_size_best = 0.0,0.0,0.0
avg_greedy, avg_dynamic, avg_binary = 0.0,0.0,0.0


#i1 = np.random.randint(len(edgesTS), size = n)
#i2 = np.random.randint(len(edgesTS), size = n)

best_avg = []
best_intervals = []

# _, _, baseS = utils.getBaseline(edgesTS, B)
# avg_base = 2.0*baseS.number_of_edges()/baseS.number_of_nodes()
# size_base = baseS.number_of_nodes()

 
initIntervals = []    

initIntervals.append((0, len(edgesTS)-1))
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
    print 'greedy done in: ', toc-tic
    
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
    print 'binary done in: ', toc-tic
    minspanBi, st, end  = utils.shortestInt(edgesTS, edges_coveredBi)
    minspanBi = minspanBi.total_seconds()/(60*60*24.0)
    sys.stdout.flush()

else:
    tic = time.time()
    baseS, _, _, S, _  = main.main(outpath, 'dynprogr', charikar_version, 'weighted', pics, k, B, edgesTS, nodes, edges, initIntervals, False)
    toc = time.time()
    print 'dynamic done in: ', toc-tic
    sys.stdout.flush()    

timeIntBi.sort()
len_gr, len_bi, gap_gr, gap_bi = [],[],[],[]
for i in xrange(0, len(timeIntGr)):
    gri = timeIntGr[i]
    s,t = gri[0],gri[1]
    l = (edgesTS[t][0] - edgesTS[s][0]).total_seconds()/(60.0*60*24)        
    len_gr.append(l)
    
    bii = timeIntBi[i]
    s,t = bii[0],bii[1]
    l = (edgesTS[t][0] - edgesTS[s][0]).total_seconds()/(60.0*60*24)        
    len_bi.append(l)
    
    
timeIntGr.sort()
for i in xrange(0, len(timeIntGr)-1):
    s,t = timeIntGr[i][1],timeIntGr[i+1][0]
    g = (edgesTS[t][0] - edgesTS[s][0]).total_seconds()/(60.0*60*24)        
    gap_gr.append(g)
    
    s,t = timeIntBi[i][1],timeIntBi[i+1][0]
    g = (edgesTS[t][0] - edgesTS[s][0]).total_seconds()/(60.0*60*24)        
    gap_bi.append(g) 
    
avgsGr, avgsBi = [], []
nodesGr, nodesBi = {}, {}
edgesGr, edgesBi = {}, {}
for ind in xrange(0, len(timeIntGr)):  
    stGr, endGr = timeIntGr[ind][0], timeIntGr[ind][1]
    stBi, endBi = timeIntBi[ind][0], timeIntBi[ind][1]
    avg, nodes, edges = utils.getDensity(edgesTS, edges_coveredGr, stGr, endGr)
    avgsGr.append(avg)
    for i in nodes:
        nodesGr[i] = nodesGr.get(i,0.0)+1.0
    for i in edges:
        edgesGr[i] = edgesGr.get(i,0.0)+1.0        
    
    avg, nodes, edges = utils.getDensity(edgesTS, edges_coveredBi, stBi, endBi)
    avgsBi.append(avg)
    for i in nodes:
        nodesBi[i] = nodesBi.get(i,0.0)+1.0
    for i in edges:
        edgesBi[i] = edgesBi.get(i,0.0)+1.0  

nGr = nodesGr.values()
nBi = nodesBi.values()

eGr = edgesGr.values()
eBi = edgesBi.values()

if not len_gr:
    len_gr.append(-1)
if not len_bi:
    len_bi.append(-1)
    
if not gap_gr:
    gap_gr.append(-1)
if not gap_bi:
    gap_bi.append(-1)
    
    
#print len(eGr), edgesGr

ff = open(outpath, "a")    
ff.write(' '.join([str(avg_greedy), str(avg_binary),    
str(num_nodes_gr), str(num_nodes_bi),
str(num_edges_gr), str(num_edges_bi),
str(usedBgr)[:6],str(minspanGr)[:6],
str(usedBbi)[:6],str(minspanBi)[:6],

str(np.mean(len_gr))[:6], str(np.mean(len_bi))[:6],
str(np.std(len_gr))[:6], str(np.std(len_bi))[:6],
str(np.min(len_gr))[:6], str(np.min(len_bi))[:6],
str(np.max(len_gr))[:6], str(np.max(len_bi))[:6],

str(np.mean(gap_gr))[:6], str(np.mean(gap_bi))[:6],
str(np.std(gap_gr))[:6], str(np.std(gap_bi))[:6],
str(np.min(gap_gr))[:6], str(np.min(gap_bi))[:6],
str(np.max(gap_gr))[:6], str(np.max(gap_bi))[:6],

str(np.mean(avgsGr))[:6], str(np.mean(avgsBi))[:6],
str(np.std(avgsGr))[:6], str(np.std(avgsBi))[:6],
str(np.min(avgsGr))[:6], str(np.min(avgsBi))[:6],
str(np.max(avgsGr))[:6], str(np.max(avgsBi))[:6],

str(np.mean(nGr))[:6], str(np.mean(nBi))[:6],
str(np.std(nGr))[:6], str(np.std(nBi))[:6],
str(np.min(nGr))[:6], str(np.min(nBi))[:6],
str(np.max(nGr))[:6], str(np.max(nBi))[:6],

str(np.mean(eGr))[:6], str(np.mean(eBi))[:6],
str(np.std(eGr))[:6], str(np.std(eBi))[:6],
str(np.min(eGr))[:6], str(np.min(eBi))[:6],
str(np.max(eGr))[:6], str(np.max(eBi))[:6],

';'.join(map(str,nodes_coveredBi)),
';'.join(map(str,nodes_coveredGr)),
';'.join(map(str,timeIntGr)),
';'.join(map(str,timeIntBi)),
';'.join(map(str,edges_coveredGr)),
';'.join(map(str,edges_coveredBi)),'\n']))
ff.close()
