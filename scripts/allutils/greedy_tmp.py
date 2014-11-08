from networkx import *
from networkx.generators.random_graphs import *
import numpy as np
#import matplotlib.pyplot as #plt
from datetime import datetime, timedelta
import os
import random
from collections import OrderedDict
import time

def getListOfIntervals2(initial_set, taken):
    out = []
    initial_set.sort()
    for i in initial_set:
        if taken[0] > i[0] and taken[1] < i[1]:
            out.append((i[0],taken[0]-1))
            out.append((taken[1]+1, i[1]))
        elif taken[0] == i[0] and taken[1] < i[1]:            
            out.append((taken[1]+1, i[1]))
        elif taken[0] < i[0] and taken[1] == i[1]:  
            out.append((i[0],taken[0]-1))
        elif taken[0] == i[0] and taken[1] == i[1]:
            pass
        else:
            out.append(i)
    return out

# def getListOfIntervals(initial, taken):
    # out = []
    
    # in1 = [(x[0], 'st') for x in initial]
    # in2 = [(x[1], 'end') for x in initial]
    # initial = in1 + in2
    
    # t1 = [(x[0]-1, 'end') for x in taken]
    # t2 = [(x[1]+1, 'st') for x in taken]
    # taken = t1 + t2
    
    # t = taken + initial
    # t.sort()
    # #print t
    
    # st, end = -10,-10
    # found = False
    # for i in t:
        # if i[1] == 'st':
            # st = i[0]
        # else:
            # end = i[0]
        # if st > -10 and end > -10:
            # out.append(tuple([st, end]))
            # st, end = -10,-10
 
    # #print out
    # #exit()
    # return out

def greedy(S, edgesTS, K, activeIntervals, B):
    outInt, edges_covered, usedB = run(S, edgesTS, K, activeIntervals, B, 'greedy')
    
    return outInt, edges_covered, usedB

def getBestT(offset, nodes, edges_covered, edgesTS, rest_k, rest_B, mode, a):
    i1 = 0
    iNew = -1      
    
    bestInt = OrderedDict()
    bestScore = -sys.maxint 
    while i1 < (len(edgesTS)):        
        #tic = time.clock()
        nodesSeen, edgesSeen = set(), set()        
        edgesSeen = edgesSeen.union(edges_covered)
       
        edgesTS_cur = []
        edgeCount = 0
        t1 = edgesTS[i1][0]
        for i2 in xrange(i1, len(edgesTS)):           
            t2 = edgesTS[i2][0]  
            if mode == 'greedy':
                if (t2 - t1 <= rest_B):
                    edge = edgesTS[i2][1]
                    #print edge, nodes
                    if edge[0] in nodes and edge[1] in nodes:                
                        edgeCount += 1
                        #nodesSeen.add(edge[0])
                        #nodesSeen.add(edge[1])
                        edgesSeen.add(tuple(edge))
                                  
                        dt = (t2-t1).days*24*60*60 + (t2-t1).seconds
                        
                        #diff = edgesSeen.difference(edges_covered)
                        gain = float(len(edgesSeen.difference(edges_covered)))
                        #w = [i[2] for i in edgesTS] 
                        t = float(dt)
                        #if mode == 'greedy':
                        r_B = rest_B.days*24*60*60 + rest_B.seconds
                        #print r_B,  rest_k
                        if r_B == 0.0 or rest_k == 0:
                            score = 0.0
                        else:
                            cost = max(t/r_B, 1.0/rest_k)                
                            score = gain/cost
                        # if mode == 'binary':
                            # score = gain - a*t 
                            # #print gain, t, a, gain - a*t
                        
                        if score > bestScore: 
                            bestScore = score
                            bestInt = {tuple([i1+offset,i2+offset]):(score, copy.deepcopy(edgesSeen))}
                        
                        if iNew == -1:
                           iNew = i2            
            elif mode == 'binary':
                edge = edgesTS[i2][1]
                #print edge, nodes
                if edge[0] in nodes and edge[1] in nodes:                
                    edgeCount += 1
                    #nodesSeen.add(edge[0])
                    #nodesSeen.add(edge[1])
                    edgesSeen.add(tuple(edge))
                              
                    dt = (t2-t1).days*24*60*60 + (t2-t1).seconds
                    
                    #diff = edgesSeen.difference(edges_covered)
                    gain = float(len(edgesSeen.difference(edges_covered)))
                    #w = [i[2] for i in edgesTS] 
                    t = float(dt)
                    
                    score = gain - a*t 
                    #print gain, t, a, gain - a*t
                    
                    if score > bestScore: 
                        bestScore = score
                        bestInt = {tuple([i1+offset,i2+offset]):(score, copy.deepcopy(edgesSeen))}
                    
                    if iNew == -1:
                       iNew = i2
        i1 = max(iNew, i1+1)
        iNew = -1
        #toc = time.clock()

    return bestInt

def run(S, edgesTS, k, timeIntervals, B, mode, a = 0.0):
    nodes = S.nodes()
    
    local_timeIntervals = []
    new_taken = tuple()
    freeIntervals = timeIntervals
    
    edges_covered = set() 
    #edges_covered = {}
    end = len(edgesTS)-1
    
    #print 'Nodes:', nodes
    #print timeIntervals
    
    rest_k, rest_B = k, B
    for i in xrange(0, k):
        tempInt = OrderedDict()        
        if local_timeIntervals:
            #freeIntervals = getListOfIntervals2(timeIntervals, local_timeIntervals)   
            freeIntervals = getListOfIntervals2(freeIntervals, new_taken) 
        else:           
            freeIntervals = timeIntervals
            
        #print 'free:',freeIntervals
        
        for j in freeIntervals:
            t1, t2 = j[0], j[1]
            bestInt = getBestT(t1, nodes, edges_covered, edgesTS[t1:t2+1], rest_k, rest_B, mode, a)      
            tempInt.update(bestInt)
 
        t = sorted(tempInt.items(), key = lambda t: t[1][0], reverse = True)[:1]
        if not t: break
        #print 'before:',edges_covered
        #print t
        #edges_covered.update(t[0][1][1])
        
        
        edges_covered = edges_covered.union(t[0][1][1])  
        #print 'after:',edges_covered        
        new_taken = t[0][0]
        #print 'new taken :',new_taken
        local_timeIntervals.append(new_taken)

        rest_k -= 1
        t1, t2 = t[0][0][0], t[0][0][1]
        rest_B -= edgesTS[t2][0] - edgesTS[t1][0]
        
    timeIntervals = local_timeIntervals
    #exit()
    return timeIntervals, edges_covered, B-rest_B

def binary(S, edgesTS, k, timeIntervals, B):
    a = 100.0
    lb = 0; ub = a
    c = 0
    a_list, T_list, E_list = [], [], []
    legal_TI, legal_EC, legal_T = [], [], 0.0

    while (ub - lb) > 1e-14 and c < 100:
        c += 1
        a = (lb + ub)/2   
        print a, c
        timeIntervals_out, edges_covered, T = run(S, edgesTS, k, timeIntervals, B, 'binary', a)
        print T, B
        #T = B-rest
        if T > B:
            lb = a
        if T <= B:
            legal_TI, legal_EC, legal_T = timeIntervals_out, edges_covered, T
            ub = a
        a_list.append(a)
        T_list.append(T)
        E_list.append(len(edges_covered))
        #print T, a, lb, ub
    return legal_TI, legal_EC, legal_T, a
