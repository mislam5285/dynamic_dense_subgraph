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
n = 2

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
#noise = 5
number_of_communities = 3

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
nodesInCom = 5
truth = []
for i in xrange(number_of_communities):
    truth.append(set(range(i*nodesInCom,(i+1)*nodesInCom)))

noise = 0.5
while noise < 6.1:
    noise += 0.5
    avgBack = []
    precGr, precBi = [], []
    recallGr, recallBi = [], []
    #FmGr, FmBi = {},{}
    for ind in xrange(0,n):
        nodes, edges = [],[]
        edgesTS, avg_back, _ = generate.generate(k, B, number_of_communities, noise, nodesInCom-1, nodesInCom)
        avgBack.append(avg_back)
        edgesTSBi = copy.deepcopy(edgesTS)
        edgesTSGr = copy.deepcopy(edgesTS)
        nodesGr, nodesBi = [], []
        for ind in xrange(0, number_of_communities):        
           
            initIntervals = []    
            #initIntervals.append((st, end))
            initIntervals.append((0, len(edgesTS)))
            #try:
            
            if runMainAlgs == 'grbi': 

                #avg_greedy, _, num_nodes_gr = main.main(outpath, 'greedy', charikar_version, 'unweighted', pics, k, B, edgesTS, nodes, edges, initIntervals, False)
                #nodes_coveredGr, timeIntGr, usedBgr, S, edges_coveredGr = loop_and_short_function.gamble(edgesTSGr, k, B, n, 'gr', nodes, edges, [(0,len(edgesTSGr)-1)])
                nodes_coveredGr, timeIntGr, usedBgr, Sgr, edges_coveredGr = main.main(outpath, 'greedy', charikar_version, 'unweighted', pics, k, B, edgesTSGr, nodes, edges, [(0,len(edgesTSGr)-1)], False)
                #print edges_coveredGr
                usedBgr = usedBgr.total_seconds()/(60*60*24.0)  
                nodesGr.append(nodes_coveredGr)
                
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
                nodesBi.append(nodes_coveredBi)
                
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
                #sys.stdout.flush()
            
            else:
                tic = time.time()
                baseS, _, _, Sdi, _  = main.main(outpath, 'dynprogr', charikar_version, 'weighted', pics, k, B, edgesTS, nodes, edges, initIntervals, False)
                toc = time.time()
                #print 'dynamic done in: ', toc-tic
                #sys.stdout.flush() 
        
        #print nodesGr, nodesBi
        greedyBest = []
        for iind in xrange(number_of_communities):
            i = nodesGr[iind]                
            bestFm, bestPr, bestRec, num = -1, -1, -1, -1            
            for jind in xrange(number_of_communities):
                j = truth[jind]
                inter = set(i).intersection(set(j))
                pr = 1.0*len(inter)/len(i)
                rec = 1.0*len(inter)/len(j)
                try:                       
                    fm = 2.0*pr*rec/(pr+rec)
                except:
                    fm = 0.0
                if bestFm < fm:
                    bestFm = fm                        
                    num = jind 
                    bestPr = pr 
                    bestRec = rec
            greedyBest.append([bestFm, num, bestPr, bestRec])
        greedyBest = np.array(greedyBest)    
        t = greedyBest[:,0].argsort(0)
        precGr.append(greedyBest[t[1]][2])
        recallGr.append(greedyBest[t[1]][3])
         
        binaryBest = []
        for iind in xrange(number_of_communities):
            i = nodesBi[iind]                
            bestFm, bestPr, bestRec, num = -1, -1, -1, -1            
            for jind in xrange(number_of_communities):
                j = truth[jind]
                inter = set(i).intersection(set(j))
                pr = 1.0*len(inter)/len(i)
                rec = 1.0*len(inter)/len(j)
                try:                       
                    fm = 2.0*pr*rec/(pr+rec)
                except:
                    fm = 0.0
                if bestFm < fm:
                    bestFm = fm                        
                    num = jind 
                    bestPr = pr 
                    bestRec = rec
            binaryBest.append([bestFm, num, bestPr, bestRec])
        binaryBest = np.array(binaryBest)    
        t = binaryBest[:,0].argsort(0)        
        precBi.append(binaryBest[t[1]][2])
        recallBi.append(binaryBest[t[1]][3])   
        #print binaryBest
        #print t
        #print precBi[-1], recallBi[-1]
        
        
        
        # inter = set(nodes_coveredGr).intersection(truth)
        # precGr[avg_back] = 1.0*len(inter)/len(nodes_coveredGr)
        # recallGr[avg_back] = 1.0*len(inter)/len(truth)
        # #FmGr[avg_back] = 2.0*precGr[avg_back]*recallGr[avg_back]/(precGr[avg_back]+recallGr[avg_back])
        
        # inter = set(nodes_coveredBi).intersection(truth)
        # precBi[avg_back] = 1.0*len(inter)/len(nodes_coveredBi)
        # recallBi[avg_back] = 1.0*len(inter)/len(truth)
        # #FmBi[avg_back] = 2.0*precBi[avg_back]*recallBi[avg_back]/(precBi[avg_back]+recallBi[avg_back])
    
    try:
        fmGr = 2.0*np.mean(precGr)*np.mean(recallGr)/(np.mean(precGr)+np.mean(recallGr))
    except:
        fmGr = 0.0
    try:
        fmBi = 2.0*np.mean(precBi)*np.mean(recallBi)/(np.mean(precBi)+np.mean(recallBi))
    except:
        fmBi = 0.0
    #print np.mean(precGr.keys()),
    print np.mean(avgBack), np.mean(precGr), np.mean(precBi), np.mean(recallGr), np.mean(recallBi), fmGr, fmBi
    #2.0*np.mean(precGr.values())*np.mean(recallGr.values())/(np.mean(precGr.values())+np.mean(recallGr.values())),
    #2.0*np.mean(precBi.values())*np.mean(recallBi.values())/(np.mean(precBi.values())+np.mean(recallBi.values()))
    