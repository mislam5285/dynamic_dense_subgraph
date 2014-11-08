from networkx import *
from networkx.generators.random_graphs import *
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
import random

def plant(interval, B, C):
    b = int(B.total_seconds())
    edges = C.edges()
    random.shuffle(edges)
    #pos = random.sample(range(b), len(edges))
    pos = [random.choice(range(b)) for i in xrange(len(edges))]
    poss = []
    map = []
    available = []
    for i in interval:
        available += range(i[0], i[1]+1)    
    
    for i in interval:
        if not edges:
            break
        e = list(edges.pop())
        e.sort()
        poss.append((i[0], tuple(e)))
        if not edges:
            break
        e = list(edges.pop())
        e.sort()
        poss.append((i[1], tuple(e)))
        
    while edges:
        e = list(edges.pop())
        e.sort()
        poss.append((available[pos.pop()],tuple(e)))
        
    return poss
    
    
def plantBackground(span, G):
    span = int(span.total_seconds())
    edges = G.edges()
    #print len(edges)
    #random.shuffle(edges)
    #pos = random.sample(range(span), len(edges))  
    pos = [random.choice(range(span)) for i in xrange(len(edges))]
    poss = []
    for p in pos:
        #poss[pos.pop()] = edges.pop()
        e = list(edges.pop())
        e.sort()
        poss.append((p, tuple(e)))
    #print len(poss)
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
    
def generate(k, B, com_number, noise, innerdegree, nodesInCom, backgoundN, wholeSpan):

    #k = 3
    #B = timedelta(seconds = 100)

    #com_number = 3
    nCom = nodesInCom
    desired_avgCom = innerdegree

    #noise = 2
    #n = 100
    #n = 40
    n = backgoundN
    desired_avg_degree = noise   
        
    start = datetime(2000, 01, 01, 00, 00, 00)
    #span =  timedelta(seconds = 1000)
    #span =  timedelta(seconds = 100)
    span = timedelta(seconds = wholeSpan)
    end = start + span

    TS = []

    edges_p = float(desired_avg_degree)/(n-1)
    G = generateRG(n, edges_p, range(n))
    outBack = plantBackground(span, G)
    #print outBack


    for i in outBack:
        key, val = i[0],i[1]
        t = start + timedelta(seconds = key)
        TS.append([t, val])
        
    #print 'back'
    innerNoise = []
    
    for i in xrange(com_number):
        #print i, k
        intervals = getRandomInt(k, B, start, end)
        edges_pCom = float(desired_avgCom)/(nCom - 1)
        C = generateRG(nCom, edges_pCom, range(i*nCom,(i+1)*nCom))
        outCom = plant(intervals, B, C)
        #print 'out'
        for i in outCom:
            key, val = i[0],i[1]
            t = start + timedelta(seconds = key)
            TS.append([t, val])
        t = 2.0*C.number_of_edges()/C.number_of_nodes()
        innerNoise.append(t)
            
    TS.sort()
    #print len(TS) 
    backNoise = 2.0*G.number_of_edges()/G.number_of_nodes()
    innerNoiseout = np.mean(innerNoise)
    
    return TS, backNoise, innerNoiseout
