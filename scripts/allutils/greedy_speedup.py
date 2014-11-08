from networkx import *
from networkx.generators.random_graphs import *
import numpy as np
import matplotlib.pyplot as plt
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
        elif taken[0] > i[0] and taken[1] == i[1]:  
            out.append((i[0],taken[0]-1))
        elif taken[0] == i[0] and taken[1] == i[1]:
            pass
        else:
            out.append(i)    
    return out


def greedy(S, edgesTS, K, activeIntervals, B):    
    outInt, edges_covered, usedB = run(S, edgesTS, K, activeIntervals, B, 'greedy')    
    return outInt, edges_covered, usedB
    
def greedySubmodTrick(offset, nodes, edges_covered, edgesTS, rest_k, rest_B, mode, a):
    i2 = 0
    iNew = -1   
    bestScore = -sys.maxint 
    points = []
    pointsGain = {}
    pointLen = []
    bestInt, bestGain, bestCost, bestGraph, bestTime, bestT = 0, -1, 0, 0, timedelta(seconds = 0), sys.maxint 
    while i2 < len(edgesTS):        
        edge = edgesTS[i2][1]
        if edge[0] in nodes and edge[1] in nodes:
            points.append(i2)
            gain = float(len(set([edgesTS[i2][1]]).difference(edges_covered)))
            cost = 1.0/rest_k
            score = gain - a*cost
            #print score
            #exit()
            t2 = edgesTS[i2][0]
            if score > bestScore or (score == bestScore and bestT > 0.0):
                bestT = 0.0
                bestCost = cost
                bestScore = score
                #bestInt = {tuple([i2+offset,i2+offset]):(score, copy.deepcopy(set([edgesTS[i2][1]]).union(edges_covered)))}
                bestInt = tuple([i2+offset,i2+offset])
                bestGain = gain             
                #bestGraph = copy.deepcopy(set([edgesTS[i2][1]]).union(edges_covered))
                bestTime = t2-t2
            
            #print i2
            edgesSeen = set()
            edgesSeen = edgesSeen.union(edges_covered) 
            #edgesTS_cur = []
            #edgeCount = 0            
            toRemove = []
            for ind1 in range(0, len(points)-1):                
                i1 = points[ind1]
                i1_ = points[ind1+1]
                i2_ = points[-2]
                t1 = edgesTS[i1][0]
                if (t2 - t1) <= rest_B:
                #if True: 
                    #print 'points len:', points
                    pointsGain[(i1,i2)] = pointsGain.get((i1,i2_), set())
                    pointsGain[(i1,i2)].add(edgesTS[i2][1])
                    pointsGain[(i1,i2)].add(edgesTS[i1][1])
                    dt1 = float((t2-t1).days*24*60*60 + (t2-t1).seconds) 
                    B_rest_dt = float(rest_B.days*24*60*60 + rest_B.seconds)
                    cost1 = max(dt1/B_rest_dt, 1.0/rest_k)
                    gain1 = float(len(pointsGain[(i1,i2)].difference(edges_covered)))
                    score1 = gain1 - a*cost1
                    #print score1
                    
                    pointsGain[(i1_,i2)] = pointsGain.get((i1_,i2_), set())
                    pointsGain[(i1_,i2)].add(edgesTS[i2][1])
                    pointsGain[(i1_,i2)].add(edgesTS[i1_][1])
                    #print (i1_,i2)
                    t1_ = edgesTS[i1_][0]
                    dt2 = float((t2-t1_).days*24*60*60 + (t2-t1_).seconds)                    
                    cost2 = max(dt2/B_rest_dt, 1.0/rest_k)
                    gain2 = float(len(pointsGain[(i1_,i2)].difference(edges_covered)))
                    score2 = gain2 - a*cost2
                    
                    if score1 < score2:
                        toRemove.append(i1)
                    else:
                        if score1 > bestScore or (score1 == bestScore and bestT > dt1):
                            #print 'here:', a, score1, bestScore, bestT, dt1
                            bestT = dt1
                            bestScore = score1
                            bestInt = tuple([i1+offset,i2+offset])
                            bestGain = gain1
                            bestCost = cost1
                            #bestGraph = copy.deepcopy(pointsGain[(i1,i2)].union(edges_covered))
                            bestTime = (t2-t1)
                            #bestInt = {tuple([i1+offset,i2+offset]):(score1, copy.deepcopy(pointsGain[(i1,i2)].union(edges_covered)))}
                        
                        #points.remove(i1)
                else:
                    toRemove.append(i1)
            for i in toRemove:
                points.remove(i)
            pointLen.append(len(points))
            #print len(points)
        i2 += 1   

    return bestScore, bestInt, bestGain, bestCost,  bestTime 
    
def greedySubmodTrick_general(offset, nodes, edges_covered, edgesTS, rest_k, rest_B, mode, a):
    i2 = 0
    iNew = -1   
    bestScore = -sys.maxint 
    points = []
    pointsGain = {}
    pointLen = []
    bestInt, bestGain, bestCost, bestGraph, bestTime = 0, -1, 0, 0, timedelta(seconds = 0)
    while i2 < len(edgesTS):        
        edge = edgesTS[i2][1]
        if edge[0] in nodes and edge[1] in nodes:
            points.append(i2)
            gain = float(len(set([edgesTS[i2][1]]).difference(edges_covered)))
            cost = 1.0/rest_k
            score = gain - a*cost
            #print score
            #exit()
            t2 = edgesTS[i2][0]
            if score > bestScore:
                bestCost = cost
                bestScore = score
                #bestInt = {tuple([i2+offset,i2+offset]):(score, copy.deepcopy(set([edgesTS[i2][1]]).union(edges_covered)))}
                bestInt = tuple([i2+offset,i2+offset])
                bestGain = gain             
                bestGraph = copy.deepcopy(set([edgesTS[i2][1]]).union(edges_covered))
                bestTime = t2-t2
            
            #print i2
            edgesSeen = set()
            edgesSeen = edgesSeen.union(edges_covered) 
            #edgesTS_cur = []
            #edgeCount = 0            
            toRemove = []
            for ind1 in range(0, len(points)-1):                
                i1 = points[ind1]
                i1_ = points[ind1+1]
                i2_ = points[-2]
                t1 = edgesTS[i1][0]
                #if (t2 - t1) <= rest_B:                    
                #print 'points len:', points
                pointsGain[(i1,i2)] = pointsGain.get((i1,i2_), set())
                pointsGain[(i1,i2)].add(edgesTS[i2][1])
                pointsGain[(i1,i2)].add(edgesTS[i1][1])
                dt = float((t2-t1).days*24*60*60 + (t2-t1).seconds) 
                B_rest_dt = float(rest_B.days*24*60*60 + rest_B.seconds)
                cost = max(dt/B_rest_dt, 1.0/rest_k)
                gain = float(len(pointsGain[(i1,i2)].difference(edges_covered)))
                score1 = gain - a*cost
                #print score1
                
                pointsGain[(i1_,i2)] = pointsGain.get((i1_,i2_), set())
                pointsGain[(i1_,i2)].add(edgesTS[i2][1])
                pointsGain[(i1_,i2)].add(edgesTS[i1_][1])
                #print (i1_,i2)
                t1 = edgesTS[i1_][0]
                dt = float((t2-t1).days*24*60*60 + (t2-t1).seconds)                    
                cost = max(dt/B_rest_dt, 1.0/rest_k)
                gain = float(len(pointsGain[(i1_,i2)].difference(edges_covered)))
                score2 = gain - a*cost
                
                if score1 < score2:
                    toRemove.append(i1)
                else:
                    if score1 > bestScore: 
                        bestScore = score1
                        bestInt = tuple([i1+offset,i2+offset])
                        bestGain = gain
                        bestCost = cost
                        bestGraph = copy.deepcopy(pointsGain[(i1,i2)].union(edges_covered))
                        bestTime = (t2-t1)
                        #bestInt = {tuple([i1+offset,i2+offset]):(score1, copy.deepcopy(pointsGain[(i1,i2)].union(edges_covered)))}
                    
                    #points.remove(i1)
            for i in toRemove:
                points.remove(i)
            pointLen.append(len(points))
            
                
        i2 += 1    
    #print 'average points', float(sum(pointLen))/len(pointLen)
    #print bestScore
    #print bestScore, bestInt, bestGain, bestCost, bestGraph, bestTime
    return bestScore, bestInt, bestGain, bestCost, bestGraph, bestTime 
    
    
def runGreedyBS(offset, nodes, edges_covered, edgesTS, rest_k, rest_B, mode, a, ub):

    lb = 0.0;  
    n = len(nodes)
    #ub = float(((n*n-n)/2.0)*rest_k)
    #ub = float(((n*n-n)/2.0)*rest_k) - len(edges_covered)
    crudeub = float(((n*n-n)/2.0 - len(edges_covered))*rest_k)
    if ub == -1:
        ub = crudeub
    else:
        ub = min(crudeub, ub)
    bestIntOut = {}
    
    c = 0
    legal_TI, legal_EC, legal_T = [], [], 0.0    
 
    
    a = (lb + ub)/2.0
    #print 'start',a
    #a = 2*600.0/B.total_seconds()
    #a = 20.
    #uGain, lGain = sys.maxint, -sys.maxint 
    
    _, lbestInt, lGain, lCost, lTime =  greedySubmodTrick(offset, nodes, edges_covered, edgesTS, rest_k, rest_B, mode, lb)
    _, ubestInt, uGain, uCost, uTime =  greedySubmodTrick(offset, nodes, edges_covered, edgesTS, rest_k, rest_B, mode, ub)
    #print 'bounds:', ubestInt, uGain, lbestInt, lGain
    
    bestHScore, bestInt, bestGain, bestCost, bestTime =  greedySubmodTrick(offset, nodes, edges_covered, edgesTS, rest_k, rest_B, mode, a)
    
    # if uGain > -1:
        # bestIntOut = {ubestInt:(float(uGain)/uCost, uGraph)}
            
    if bestHScore > 0:
        lb = a
        lGain = bestGain
        lbestInt = bestInt
        lCost = bestCost
        lTime = bestTime
    if bestHScore <= 0:
        ub = a
        uGain = bestGain
        ubestInt = bestInt
        uCost = bestCost   
        #uGraph = bestGraph
        uTime = bestTime
    #while (uGain - lGain) > 1e-14 and (ub - lb) > 1e-14 and c < 100:
    while (lGain - uGain) > 1e-14 and c < 100:
        c += 1
        #print c
        a = (lb + ub)/2.0
        #print 'alpha', a
        bestHScore, bestInt, bestGain, bestCost, bestTime =  greedySubmodTrick(offset, nodes, edges_covered, edgesTS, rest_k, rest_B, mode, a)

        #print 'hscore', bestHScore
        if bestHScore > 0:
            lb = a
            lGain = bestGain
            lbestInt = bestInt
            lCost = bestCost
            lTime = bestTime
        if bestHScore <= 0:
            ub = a
            uGain = bestGain
            ubestInt = bestInt
            uCost = bestCost 
            #uGraph = bestGraph
            uTime = bestTime
        #print 'gains', lGain, uGain
        
        
        #if bestGain > -1:
        #    bestIntOut = {ubestInt:(float(bestGain)/uCost, uGraph)}  
    #print rest_k, rest_B, ubestInt, lbestInt, uCost, lCost, uGain, lGain
    if uGain == -1:
        return -sys.maxint, (-1,-1)
    else:
        a = float(uGain)/lCost
        bestHScore, bestInt, bestGain, bestCost, bestTime =  greedySubmodTrick(offset, nodes, edges_covered, edgesTS, rest_k, rest_B, mode, a)
        return float(bestGain)/bestCost, bestInt

def getBestT_speedupBinary(offset, nodes, edges_covered, edgesTS, rest_k, rest_B, mode, a):
    i2 = 0
    iNew = -1      
    
    bestInt = (-1,-1)
    bestScore = -sys.maxint 
    points = []
    pointsGain = {}
    pointLen = []
    while i2 < len(edgesTS):        
        edge = edgesTS[i2][1]
        if edge[0] in nodes and edge[1] in nodes:
            points.append(i2)
            score = float(len(set([edgesTS[i2][1]]).difference(edges_covered)))
            if score > bestScore: 
                bestScore = score
                #bestInt = {tuple([i2+offset,i2+offset]):(score, copy.deepcopy(set([edgesTS[i2][1]]).union(edges_covered)))}
                bestInt = (i2+offset, i2+offset) 
            
            #print i2
            edgesSeen = set()
            edgesSeen = edgesSeen.union(edges_covered) 
            #edgesTS_cur = []
            #edgeCount = 0
            t2 = edgesTS[i2][0]
            toRemove = []
            for ind1 in range(0, len(points)-1):                
                i1 = points[ind1]
                i1_ = points[ind1+1]
                i2_ = points[-2]
                #print 'points len:', points
                pointsGain[(i1,i2)] = pointsGain.get((i1,i2_), set())
                pointsGain[(i1,i2)].add(edgesTS[i2][1])
                pointsGain[(i1,i2)].add(edgesTS[i1][1])
                #print (i1,i2)
                t1 = edgesTS[i1][0]
                dt = float((t2-t1).days*24*60*60 + (t2-t1).seconds)
                gain = float(len(pointsGain[(i1,i2)].difference(edges_covered)))
                score1 = gain - a*dt
                #print score1
                
                pointsGain[(i1_,i2)] = pointsGain.get((i1_,i2_), set())
                pointsGain[(i1_,i2)].add(edgesTS[i2][1])
                pointsGain[(i1_,i2)].add(edgesTS[i1_][1])
                #print (i1_,i2)
                t1 = edgesTS[i1_][0]
                dt = float((t2-t1).days*24*60*60 + (t2-t1).seconds)
                gain = float(len(pointsGain[(i1_,i2)].difference(edges_covered)))
                score2 = gain - a*dt
                
                if score1 < score2:
                    toRemove.append(i1)
                else:
                    if score1 > bestScore: 
                        bestScore = score1
                        #bestInt = {tuple([i1+offset,i2+offset]):(score1, copy.deepcopy(pointsGain[(i1,i2)].union(edges_covered)))}
                        bestInt = (i1+offset, i2+offset) 
                    
                    #points.remove(i1)
            for i in toRemove:
                points.remove(i)
            pointLen.append(len(points))
                
        i2 += 1   
    #print 'average points', float(sum(pointLen))/len(pointLen)
    #print np.mean(pointLen), np.median(pointLen), np.min(pointLen), np.max(pointLen), a
    return bestScore, bestInt, pointLen
    
def getBestT(offset, nodes, edges_covered, edgesTS, rest_k, rest_B, mode, a):
    if mode == 'binary':
        bestScore, bestInt, pointLen = getBestT_speedupBinary(offset, nodes, edges_covered, edgesTS, rest_k, rest_B, mode, a)
 
        return bestScore, bestInt, pointLen 
    return -1

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
    pointLen = []
    ub = -1.0
    for i in xrange(0, k):
        #tempInt = OrderedDict()
        bestSc, bestInt = -sys.maxint, (-1,-1)        
        if local_timeIntervals:
            freeIntervals = getListOfIntervals2(freeIntervals, new_taken) 
        else:           
            freeIntervals = timeIntervals
            
        #print 'free:', i, freeIntervals
        
        for j in freeIntervals:
            t1, t2 = j[0], j[1]
            if mode == 'greedy':
                sc, interval = runGreedyBS(t1, nodes, edges_covered, edgesTS[t1:t2+1], rest_k, rest_B, mode, a, ub)
            elif mode == 'binary':
                sc, interval, pLen = getBestT_speedupBinary(t1, nodes, edges_covered, edgesTS[t1:t2+1], rest_k, rest_B, mode, a)      
            #tempInt.update(bestInt)
            #pointLen += pLen
            
            if bestSc < sc:
                bestSc, bestInt = sc, interval
 
        if bestSc == -sys.maxint:  break
        
        for i in xrange(bestInt[0],bestInt[1]+1):
            if edgesTS[i][1][0] in nodes and edgesTS[i][1][1] in nodes:
                edges_covered.add(edgesTS[i][1])
        
        new_taken = bestInt
        local_timeIntervals.append(bestInt)      

        rest_k -= 1
        t1, t2 = bestInt[0],bestInt[1]
        rest_B -= edgesTS[t2][0] - edgesTS[t1][0]
        #print 'local int', local_timeIntervals
        
    timeIntervals = local_timeIntervals
    #print 'average points', float(sum(pointLen))/len(pointLen)
    return timeIntervals, edges_covered, B-rest_B

def binary(S, edgesTS, k, timeIntervals, B):
    #a = 100.0
    
    t = S.number_of_nodes()
    lb = 0; ub = float((t*t-t)/2.0)/B.total_seconds();
    #lb = 0; ub = 100.0     
    
    c = 0
    a_list, T_list, E_list = [], [], []
    legal_TI, legal_EC, legal_T = [], [], 0.0
    
    #a = 2*600.0/B.total_seconds()
    a = (ub + lb)/2.0;
    #a = 20.0
    
    timeIntervals_out, edges_covered, T = run(S, edgesTS, k, timeIntervals, B, 'binary', a)
    #print T, B
    #T = B-rest
    if T > B:
        lb = a
    if T <= B:
        legal_TI, legal_EC, legal_T = timeIntervals_out, edges_covered, T
        ub = a
    a_list.append(a)
    T_list.append(T)
    E_list.append(len(edges_covered))

    #while (ub - lb) > 1e-14 and c < 50:
    #while (ub - lb) > 1e-14 and c < 20:
    while (ub - lb) > 1e-14 and c < 10:
        c += 1
        a = (lb + ub)/2   
        #print a, c
        timeIntervals_out, edges_covered, T = run(S, edgesTS, k, timeIntervals, B, 'binary', a)
        #print T, B
        #T = B-rest
        if T > B:            
            lb = a
            #print 'highter lb', a, B
        if T <= B:
            legal_TI, legal_EC, legal_T = timeIntervals_out, edges_covered, T
            ub = a
            #print 'lower ub', a, B
        a_list.append(a)
        T_list.append(T)
        E_list.append(len(edges_covered))
        #print T, a, lb, ub
    return legal_TI, legal_EC, legal_T
