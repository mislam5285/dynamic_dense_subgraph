from networkx import *
from networkx.generators.random_graphs import *
import numpy as np
#import matplotlib.pyplot as #plt
from datetime import datetime, timedelta
import os
import random
from collections import OrderedDict
import time

def getInterval(S, edgesTS, timeIntervals):
    
    timeIntervals.sort() 
    pad = (-1,(-1,-1),-1)
    padIdx = -1
    TS_, revertIndex = [], []
    for item in timeIntervals:
        s,t = item[0],item[1]
        for i in xrange(s, t+1):        
            edge = edgesTS[i][1]        
            if edge[0] in S.nodes() and edge[1] in S.nodes():  
                TS_.append(edgesTS[i])
                revertIndex.append(i)
        TS_.append(pad)
        revertIndex.append(padIdx)
    TS_ = TS_[0:-1]
    revertIndex = revertIndex[0:-1]
    
    return TS_, revertIndex

def discreteB (B, num):
    B = int(B.total_seconds())
    B_disc = []
    step = int(B/num) 
    if step == 0:
       step = 1 
    for i in xrange(0, B, step):
        B_disc.append(i)
    B_disc.append(B)
    #print B_disc 
    return B_disc 

def dynprogr(S, edgesTS, k, timeIntervals, Budget, num):

    B_disc = discreteB (Budget, num)
    #print B_disc
    blen = len(B_disc)
    Bmax = B_disc[-1] 
    
    TS, revertIndex = getInterval(S, edgesTS, timeIntervals)
    n = len(TS)
    D = np.zeros((n+1, k+1, blen), float)
    B = np.zeros((n+1, k+1, blen), float)
    Ind = np.zeros((n+1, k+1, blen), float)
    Ind_ = np.zeros((n+1, k+1, blen), float)
    #print timeIntervals
    #print len(TS),len(edgesTS)
     
    D[0,:,:] = 0.0
    D[:,0,:] = 0.0
    B[0,:,:] = 0.0
    B[:,0,:] = 0.0
    Ind[0,:,:] = 0.0
    Ind[:,0,:] = 0.0
    Ind_[0,:,:] = 0.0
    Ind_[:,0,:] = 0.0
        
    for b in xrange(0,blen):
        #while val <= k and i <= n:         
        for i in xrange(1, min(k+1,n+1)):
            #if not np.isnan(D[i,0,b]):
            for j in xrange(i, k+1):
                #if i < n+1:
                #print i,j, val
                D[i,j,b] = i
                B[i,j,b] = 0
                Ind[i,j,b] = 0
                Ind_[i,j,b] = 0
                #RestB[i,j] = B.total_seconds()
            #val += 1    
        
    TS = np.array(TS)
    # print TS
    # print Bmax
    print TS
   
    for b in xrange(0,blen):
        for m in xrange(1,k+1):
            for i in xrange(1,n+1):
                #if ~np.isnan(D[i, m, b]):
                bestD, bestJ, bestJ_, BestSpent = -sys.maxint, -1, -1, -1
                for j in xrange(m-1, i+1): 
                    for j_ in xrange(j+1, i+1):
                        for bs in xrange(0, b+1):
                            Bs, Bt = B_disc[bs], B_disc[b]-B_disc[bs]
                            #print Bs, Bt
                            #print TS
                            #t = len(set(TS[(j_-1):i,2]))
                            #print TS[(j_-1):i,1]
                            t = len(set(TS[(j_-1):i,1]))
                            #print t
                            cost = D[j, m-1, bs] + t
                            span = (TS[i-1][0] - TS[j_-1][0]).total_seconds()
                            #print cost, bestD, Bt, span
                            if cost > bestD and span <= Bt:
                                #print 'HERE', cost, j, j_, bs
                                #print bestD, span, Bt
                                bestD, bestJ, bestJ_, BestSpent = cost, j, j_, bs
                            
                if bestD != -sys.maxint:
                    D[i, m, b] = bestD
                B[i, m, b] = BestSpent
                Ind[i, m, b] = bestJ
                Ind_[i, m, b] = bestJ_ 

    # print "out D", D[:,:,-1]
    # print "out D", D[:,:,-2]
    # print "out B", B
    # print "out B", B[:,:,-2]
    # print "out Idx", Ind[:,:,-1]
    # print "out Idx_", Ind_[:,:,-1]
    
    
    st = -1


    end = np.nanargmax(D[:,k, -1])
    # print D[:, k, -1]
    # print end
 
    intervals = []
    #b = int(B[end,k,b])
    #print b
    
    s = int(Ind_[end, k, -1]) 
    #print s
    
    #used = B_disc[b]+(TS[end-1][0] - TS[s-1][0]).total_seconds()
    #print 'used:',  used
    #exit()
    used = -1

    b = -1
    for i in xrange(k,0,-1):
        #print end
        st = int(Ind_[end,i, b])
        #print end, st
        intervals.append(tuple([st-1, end-1]))
        b_new = int(B[end,i,b])
        end_new = int(Ind[end,i,b])
        b, end = b_new, end_new
        
    
    edges_covered = set()

    #ECovered = set()
    #print intervals
    for i in intervals:        
        for j in xrange(i[0],i[1]+1):
            #print j, TS[j,:]                     
            edges_covered.add(tuple(TS[j,1]))
    
   
    timeIntervals = []
    for item in intervals:
        timeIntervals.append((revertIndex[item[0]],revertIndex[item[1]]))    
    #print timeIntervals, edges_covered
    #return timeIntervals, edges_covered, timedelta(seconds = Budget.total_seconds()-used), max(D[:,k,-1])
    return timeIntervals, edges_covered, used, max(D[:,k,-1])
