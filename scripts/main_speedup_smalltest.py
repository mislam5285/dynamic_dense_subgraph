import networkx as nx
import time
from datetime import datetime, timedelta
from collections import OrderedDict
import matplotlib.pyplot as plt
import sys
import operator
import os
import copy
import numpy as np
#import utils
#import charikar, greedy, dynprogr, plotting
import uuid
from allutils import utils, charikar, greedy_speedup_log, greedy_log, dynprogr, plotting

#filepath = os.path.join("..", "Line_points_data", "out_6_72.txt")
#filepath = os.path.join("..", "Line_points_data", "out_overlap3.txt")

def main(outpath, alg, charikar_version, charikar_mode, pics, k, B, edgesTS, nodes, edges, timeIntervals, baseline = False, n_disc = 101, fast = True, entire = True):   
    
    G = nx.Graph()
    S = nx.Graph()

    nodes_covered = list(nodes)
    edges_covered = edges
    
    baseAvg, baseInt, baseEdges, baseNodes = 0.0, 0.0, 0.0, 0.0
    if baseline == True:
        baseAvg, baseInt, baseS = utils.getBaseline(edgesTS, B)
        baseEdges, baseNodes = baseS.number_of_edges(), baseS.number_of_nodes()

    counter = 0
    out = 0.0
    maxiter = 0
    first = True
    initCom = nx.Graph()
    #for maxiter in xrange(10):
    for maxiter in xrange(1):
        maxiter += 1
        #print timeIntervals
        rest_k, rest_B = k, B
        G.clear()
        S.clear()
        
        if not timeIntervals:
            timeIntervals = [(0, len(edgesTS)-1)]
            
        tic = time.clock()        
        #############  pile a graph (unweighted)
        G = utils.getGraphFrimIntervals(edgesTS, timeIntervals, charikar_mode)
        #G = utils.getGraphFrimIntervals(edgesTS, timeIntervals, 'weighted_emails')
        #print G.adj
        #print len(G.edges())
        #exit()
        toc = time.clock()
        #print 'pile graph', toc-tic
                
        if pics:
            plotting.plotGraph(outpath, counter, 'graph_G', G)
            counter += 1
            
        tic = time.clock()
        if alg == 'dynprogr':
            S, avg = charikar.charikar(copy.deepcopy(G), 'weighted', charikar_version)
        else:
            S, avg = charikar.charikar(copy.deepcopy(G), 'unweighted', charikar_version)
           
        toc = time.clock()
        #print 'Charikar', toc-tic
            
        if first == True:
            first = False
            initCom = copy.deepcopy(S)
        
        #print len(S.edges()), avg
        
        if pics:
            plotting.plotGraph(outpath, counter, 'subgraph_S', S,'subgraph', baseNodes, baseEdges, baseAvg)
            counter += 1
        
        nodes = S.nodes()
        
        # simple rule:
        timeIntervals = [(0, len( edgesTS)-1)]
        
        tic = time.clock()
        
        if entire == True:
            S = G
            
        if alg == 'greedy':
            if fast == True: 
                timeIntervals, edges_covered, usedB = greedy_speedup_log.greedy(S, edgesTS, k, timeIntervals, B)
            #timeIntervals, edges_covered, rest_B = greedy_emails.greedy(S, edgesTS, k, timeIntervals, B)
            if fast == False:
                timeIntervals, edges_covered, usedB = greedy_log.greedy(S, edgesTS, k, timeIntervals, B)
            #print timeIntervals, edges_covered, rest_B
        if alg == 'binary':  
            if fast == True:
                #timeIntervals, edges_covered, usedB = greedy_speedup.binary(S, edgesTS, k, timeIntervals, B)
                timeIntervals, edges_covered, usedB = greedy_speedup_log.binary(S, edgesTS, k, timeIntervals, B)
            if fast == False:
                #timeIntervals, edges_covered, usedB = greedy.binary(S, edgesTS, k, timeIntervals, B)
                timeIntervals, edges_covered, usedB = greedy_log.binary(S, edgesTS, k, timeIntervals, B)
        if alg == 'dynprogr':
            timeIntervals, edges_covered, usedB, D = dynprogr.dynprogr(S, edgesTS, k, timeIntervals, B, n_disc)
            #print timeIntervals, edges_covered, rest_B, D 
        #print timeIntervals, edges_covered, rest_B
        #exit()

        toc = time.clock()
        
        # if fast == True:
            # print 'fast interval search', toc-tic
        # if fast == False:
            # print 'basic interval search', toc-tic
         
        if pics:
            plotting.plotPoints(outpath, S, edgesTS, timeIntervals, counter, B, rest_B, k, edges_covered)
            counter += 1
        
        if pics:
            plotting.coveredSubgraphs(outpath, counter, edgesTS, timeIntervals, edges_covered)
            counter += 1    
         
        nodes_covered = set()
        for i in edges_covered:
            nodes_covered.add(i[0])
            nodes_covered.add(i[1])
        
        #e1 = set([set(i) for i in S.edges()])
        #e2 = set([set(i) for i in edges_covered])
        
        e1 = np.array(S.edges())
        e1.sort(1)
        e1 = map(tuple,e1)
        #print e1
        
        #print list(edges_covered)
        e2 = np.array(list(edges_covered))
        e2.sort(1)
        e2 = map(tuple,e2)
        
        #if (set(S.edges())).issubset(set(edges_covered)):
        #print 2.0*S.number_of_edges()/S.number_of_nodes() 
        #print len(e1), len(e2)
        
        if set(e1).issubset(set(e2)):
        #if set(S.nodes()).issubset(set(nodes_covered)):
            out = 2.0*len(edges_covered)/len(nodes_covered)            

            # print edges_covered       
            # print ' '.join(map(str,nodes_covered))
            # print 2.0*len(edges_covered)/len(nodes_covered), B, B-rest_B
            # print baseAvg, baseInt, baseEdges, baseS.number_of_nodes()
            # #print timeIntervals.keys()
            # for i in timeIntervals:
                # sys.stdout.write(str(i[0]) + ',' + str(i[1]) + ';')
            # print ''
            # for i in timeIntervals:
                # sys.stdout.write(str(edgesTS[i[0]][0]) + ',' + str(edgesTS[i[1]][0]) + ';')
            break      
    print toc-tic, out
    sys.stdout.flush()
    
    return out, baseAvg, nodes_covered
    #return nodes_covered, timeIntervals, usedB, S, edges_covered, initCom

if __name__ == "__main__":

    #filepath = os.path.join("..","..", "DynGraphData", "CAStudents_300.txt")

    outpath = 'out.txt'
    #print 'ARGS', sys.argv
    
    filepath = os.path.join(".","..","DATA", sys.argv[1])
    b = float(sys.argv[2])
    #filepath = os.path.join(".","..","DATA","students.txt")
    #outpath = sys.argv[2] + '_' + str(uuid.uuid4())
    # if not os.path.exists(outpath):
        # os.makedirs(outpath)

    toc = time.clock()

    pics = False

    #alg = 'dynprogr'
    alg = sys.argv[3]
    fastArg = sys.argv[4]
    entireArg = sys.argv[5]
    
    if fastArg == 'fast':
        fastArg = True
    else:
        fastArg = False
        
    if entireArg == 'all':
        entireArg = True
    else:
        entireArg = False
        
    #alg = 'binary'
    #alg = 'binary_fast'

    charikar_version = 'basic'
    #charikar_version = 'fixed'

    # if alg == 'greedy' or alg == 'binary':
        # charikar_mode = 'unweighted'

    if alg == 'dynprogr':
        charikar_mode = 'weighted'
    else:
        charikar_mode = 'unweighted'


    k = 1
    #B = timedelta(seconds = 20) 
    B = timedelta(days = b)

    #print 'read file:'
    edgesTS, nodes, edges =  utils.readFile(filepath)

    #utils.plotInitial(edgesTS)
    timeIntervals = []
    timeIntervals.append((0, len(edgesTS)-1))  

    #print 'run main:'
    #for i in xrange(500,10001,500):
    #for i in [1000,5000,10000]:
    for i in [15000,20000,25000]:
    #for i in [100, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]:
        
        tic = time.clock()
        out, b, nodes_covered = main(outpath, alg, charikar_version, charikar_mode, pics, k, B, edgesTS[:i], nodes, edges, timeIntervals, baseline = False, n_disc = i, fast = fastArg, entire = entireArg)
        toc = time.clock()
        #print i, out, toc-tic
        print i
        sys.stdout.flush()
        
        # tic = time.clock()
        # out, b, nodes_covered = main(outpath, alg, charikar_version, charikar_mode, pics, k, B, edgesTS[:i], nodes, edges, timeIntervals, baseline = False, n_disc = i, fast = True)
        # toc = time.clock()
        ##print i, out, toc-tic
        # sys.stdout.flush()
    
    ff = open(outpath, "a")
    ff.write(' '.join([str(i), str(toc-tic), '\n']))
    ff.close()
