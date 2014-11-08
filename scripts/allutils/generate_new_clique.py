from networkx import *
from networkx.generators.random_graphs import *
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
import random

#filepath = ".\/DynGraphData\/CAStudents.txt"
#filepath =  os.path.join("..", "DynGraphData", "CAStudents.txt")

def plant(interval, B, C):
    b = int(B.total_seconds())
    edges = C.edges()
    random.shuffle(edges)
    pos = random.sample(range(b), len(edges))
    poss = {}
    map = []
    available = []
    for i in interval:
        available += range(i[0], i[1]+1)    
    
    for i in interval:
        poss[i[0]] = edges.pop()
        poss[i[1]] = edges.pop()
        
    while edges:
        poss[available[pos.pop()]] = edges.pop()
        
    return poss
    
    
def plantBackground(span, G):
    span = int(span.total_seconds())
    edges = G.edges()
    #random.shuffle(edges)
    pos = random.sample(range(span), len(edges))    
    poss = {}
    while edges:
        poss[pos.pop()] = edges.pop()           
    return poss
    
        
def generateRG(n, edges_p, nodes):
    G = fast_gnp_random_graph(n, edges_p, seed=None, directed=False)
    gnodes = G.nodes()
    
    relabel = {gnodes[i]: nodes[i] for i in xrange(n)}    
    G = relabel_nodes(G, relabel) 
    return G
    
def getRandomInt(k, B, start, end):
    b = B.total_seconds()
    span = (end - start).total_seconds()
    #start, end = start.total_seconds(), end.total_seconds()
    partition = [random.random() for i in xrange(k)]
    partition.sort()
    
    while True:
        r = [random.randint(0, span) for i in xrange(k)]        
        out, s = [], 0
        for i in xrange(k):
            st = r[i]
            e = int(st + np.ceil(b*partition[i]))
            s += e - st
            next = span if i == k-1 else r[i+1] 
            if e <= next:
                out.append((st,e))
            else:
                break
        if len(out)==k:
            res = int(b - s)
            if res == 0:
                break
            else:
                extra = out[-1][1] + res
                if extra <= span:
                    out[-1] = (out[-1][0],extra)
                    break
    return out
    
def generate(k, B, com_number, noise):

    #k = 3
    #B = timedelta(seconds = 100)

    #com_number = 3
    nCom = 5
    desired_avgCom = 4 

    #noise = 2
    n = 100
    desired_avg_degree = noise   
        
    start = datetime(2000, 01, 01, 00, 00, 00)
    span =  timedelta(seconds = 1000)
    end = start + span

    TS = []

    edges_p = float(desired_avg_degree)/(n-1)
    G = generateRG(n, edges_p, range(n))
    outBack = plantBackground(span, G)
    #print outBack


    for key, val in outBack.iteritems():
        t = start + timedelta(seconds = key)
        TS.append([t, val])
        
    #print 'back'
        
    for i in xrange(com_number):
        #print i, k
        intervals = getRandomInt(k, B, start, end)
        edges_pCom = float(desired_avgCom)/(nCom - 1)
        C = generateRG(nCom, edges_pCom, range(i*nCom,(i+1)*nCom))
        outCom = plant(intervals, B, C)
        #print 'out'
        for key, val in outCom.iteritems():
            t = start + timedelta(seconds = key)
            TS.append([t, val])
            
    TS.sort()
    #print len(TS) 
    out = 2.0*G.number_of_edges()/G.number_of_nodes()
    return TS, out
