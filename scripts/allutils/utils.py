from networkx import *
from networkx.generators.random_graphs import *
import numpy as np
#import matplotlib.pyplot as #plt
from datetime import datetime, timedelta
import os
import random
from collections import OrderedDict
import time
import charikar

def readFile(filepath):
    #edges = {}
    #edgesTS = OrderedDict()
    #nodesTS = []
    edgesTS = []   
    nodes = set()
    edges = set()
    lookup = {}
    c = 0
    with open(filepath,'r') as fd:
        for line in fd.readlines():
            
            line = line.strip()            
            items = line.split(' ')            
            tstamp = ' '.join(items[0:2])
            tstamp = tstamp[1:-1]
            #print tstamp
            tstamp = datetime.strptime(tstamp, '%Y-%m-%d %H:%M:%S')
            t = items[2:4]
            
            t = map(int,t)
            #num = t[-1] 
            #t = items[2:4]   
            if t[0] == t[1]:            
                continue
            t.sort(); #undirected
            #edges.setdefault(tuple(t), []).append(tstamp)
            #edgesTS.setdefault(tstamp,[]).append(tuple(t))
            if tuple(t) in lookup.keys():
                num = lookup[tuple(t)]
            else:
                num = c
                lookup[tuple(t)] = c
                c += 1
            edgesTS.append((tstamp, tuple(t), num ))
            #edgesTS.append((tstamp, tuple(t), float(items[4]), items[5][1:-1]))
            #nodesTS.append((tstamp, t[0]))
            #nodesTS.append((tstamp, t[1]))
            nodes.add(t[0])
            nodes.add(t[1])
            edges.add(tuple([t[0],t[1]]))
            #print tstamp, tuple(t), num
            
        edgesTS_mapped = []
    fd.close()
    return edgesTS, nodes, edges
    
def readFileWeighted(filepath):
    #edges = {}
    #edgesTS = OrderedDict()
    #nodesTS = []
    edgesTS = []   
    nodes = set()
    edges = set()
    lookup = {}
    c = 0
    with open(filepath,'r') as fd:
        for line in fd.readlines():
            
            line = line.strip()            
            items = line.split(' ')            
            tstamp = ' '.join(items[0:2])
            tstamp = tstamp[1:-1]
            #print tstamp
            tstamp = datetime.strptime(tstamp, '%Y-%m-%d %H:%M:%S')
            t = items[2:4]
            
            t = map(int,t)
            #num = t[-1] 
            #t = items[2:4]   
            if t[0] == t[1]:            
                continue
            t.sort(); #undirected
            #edges.setdefault(tuple(t), []).append(tstamp)
            #edgesTS.setdefault(tstamp,[]).append(tuple(t))
            if tuple(t) in lookup.keys():
                num = lookup[tuple(t)]
            else:
                num = c
                lookup[tuple(t)] = c
                c += 1
            w = float(items[4])
            edgesTS.append((tstamp, tuple(t), w))
            #edgesTS.append((tstamp, tuple(t), float(items[4]), items[5][1:-1]))
            #nodesTS.append((tstamp, t[0]))
            #nodesTS.append((tstamp, t[1]))
            nodes.add(t[0])
            nodes.add(t[1])
            edges.add(tuple([t[0],t[1]]))
            #print tstamp, tuple(t), num
            
        edgesTS_mapped = []
    fd.close()
    return edgesTS, nodes, edges

def getDensity(edgesTS, edges_cov, st, end):
    nodes = set()
    #S = networkx.Graph()
    edges = set()
    
    for i in xrange(st, end+1):
        
        if edgesTS[i][1] in edges_cov:
            edges.add(edgesTS[i][1])
            nodes.add(edgesTS[i][1][0])
            nodes.add(edgesTS[i][1][1])
            
    avg = 2.0*len(edges)/len(nodes)        
    return avg, nodes, edges
    
def getDensityWeighted(edgesTS, edges_cov, st, end):
    nodes = set()
    #S = networkx.Graph()
    edges = {}
    
    for i in xrange(st, end+1):
        
        if edgesTS[i][1] in edges_cov:
            edges[edgesTS[i][1]] = max(edges.get(edgesTS[i][1],0.0),edgesTS[i][2])
            #edges.add(edgesTS[i][1])
            nodes.add(edgesTS[i][1][0])
            nodes.add(edgesTS[i][1][1])
            
    #avg = 2.0*len(edges)/len(nodes)
    avg = 2.0*sum(edges.values())/len(nodes)
    return avg, nodes, edges

def getGraph(edgesTS):
    G = nx.Graph()
    for item in edgesTS:
        edge = item[1]
        G.add_edges_from([tuple(edge)])
    return G
    
# def getGraphWeighted(edgesTS):
    # G = nx.Graph()
    # for item in edgesTS:
        # #print item
        # edge = item[1]
        # w = item[2] 
        # #print w
        
        # G.add_edges_from([edge], weight=w)
        # #G.add_weighted_edges_from((edge[0], edge[1], w))
    # return G    


def shortestInt(edgesTS, edges):
    seen = {}
    for i in edges:
        seen[i] = 0
    count, j = 0, 0
    st,end = 0,0
    
    bestdt = edgesTS[-1][0]-edgesTS[0][0]
    #print bestdt
    
    for i in xrange(0,len(edgesTS)):
        e = edgesTS[i]
        if e[1] in edges:
            seen[e[1]]+=1
            if seen[e[1]] == 1:
                count+=1
        if count==len(edges):
            while edgesTS[j][1] not in edges or seen[edgesTS[j][1]] > 1:
                if seen.get(edgesTS[j][1],0) > 1:
                    seen[edgesTS[j][1]]-=1
                j+=1
        
            dt = edgesTS[i][0]-edgesTS[j][0]            
            if dt < bestdt:
                st, end = j, i
                #print j,i
                #print dt
                bestdt = dt
    
    return bestdt, st, end
    
def getGraphFrimIntervals(edgesTS, timeIntervals, charikar_mode = 'unweighted'):
    G = nx.Graph()
    if charikar_mode == 'unweighted':
        for tList in timeIntervals:
            t1, t2 = tList[0], tList[1]        
            for item in edgesTS[t1:(t2+1)]:
                edge = item[1]
                #if edge in edges_covered:
                #if edge[0] in nodes_covered and edge[1] in nodes_covered:
                G.add_edges_from([tuple(edge)])
                
    elif charikar_mode == 'weighted':
        for tList in timeIntervals:
            t1, t2 = tList[0], tList[1]
            #print t1, t2, ":"
            e = set()
            for item in edgesTS[t1:(t2+1)]:
            #for item in TS_[t1:(t2+1)]:
                edge = item[1]
                #if edge in edges_covered:
                e.add(tuple(edge))
                #if edge[0] in nodes_covered and edge[1] in nodes_covered:
            for i in e:
                if G.has_edge(i[0],i[1]):
                    G[i[0]][i[1]]['weight']+=1
                else:
                    G.add_edge(i[0],i[1],weight=1)
    elif charikar_mode == 'weighted_emails':
        for tList in timeIntervals:
            t1, t2 = tList[0], tList[1]
            #print t1, t2, ":"
            e = {}
            for item in edgesTS[t1:(t2+1)]:
            #for item in TS_[t1:(t2+1)]:
                edge = item[1]
                #if edge in edges_covered:
                w = max(e.get(edge,0), item[2])
                e[edge] = w
                #if edge[0] in nodes_covered and edge[1] in nodes_covered:
            for i in e.keys():
                if G.has_edge(i[0],i[1]):
                    G[i[0]][i[1]]['weight'] = max(G[i[0]][i[1]]['weight'], e[i])
                else:
                    G.add_edge(i[0],i[1],weight=e[i])
    return G
        
        
def plotInitial(edgesTS):
    TS = np.array(edgesTS)

    helper = np.vectorize(lambda x: (x-datetime(1970, 1, 1)).total_seconds())
    dt_sec = helper(TS[:,0])    
    y = list(TS[:,-1])
    #plt.scatter(dt_sec, list(y), c = list(y))
    #plt.figure("points")
    #plt.scatter(dt_sec, y, c = y)
    #plt.axvspan(helper(datetime(2010, 12, 01, 00, 00, 30)), helper(datetime(2010, 12, 01, 00, 01, 00)), facecolor = 'k', alpha = 0.5)
    #plt.axvspan(helper(datetime(2010, 12, 01, 00, 1, 30)), helper(datetime(2010, 12, 01, 00, 2, 00)), facecolor = 'k', alpha = 0.5)
    #plt.title('comunity 1: avg degree = 7; duration: 30 sec'+
    #'\n comunity 2: avg degree = 6; duration: 30 sec, background avg deg = 6.72')
    #plt.savefig('All_edges.png')
    
def getBaseline(edgesTS, B): 
    bestAvg, bestInt = 0,0
    for i in xrange(0,len(edgesTS)):
        st = edgesTS[i][0]
        #print i, edgesTS[i][0]
        end = st + B
        if end > edgesTS[-1][0]:
            break
        
        for j in xrange(i,len(edgesTS)):
            if (edgesTS[j][0] > end):
                j -= 1
                G = getGraph(edgesTS[i:j+1])
                S, avg = charikar.charikar(copy.deepcopy(G))
                if avg > bestAvg:   
                    bestAvg, bestInt = avg, (i,j)
                    bestS = copy.deepcopy(S)
                break
    # #plt.figure('bestS')
    # nx.draw(bestS)
    # #plt.show()
    # print bestInt
    # print bestAvg
    # d = bestS.degree()
    # print d
    # avg_degree = float(sum(d.values())) / len(d)
    # print avg_degree
    # print bestS.nodes()
    # print bestS.edges()
    # exit()
    #return bestAvg, bestInt, bestS.number_of_edges(), bestS.number_of_nodes()
    return bestAvg, bestInt, bestS
    
def getBaselineWeighted(edgesTS, B): 
    bestAvg, bestInt = 0,0
    for i in xrange(0,len(edgesTS)):
        st = edgesTS[i][0]
        #print i, edgesTS[i][0]
        end = st + B
        if end > edgesTS[-1][0]:
            break
        
        for j in xrange(i,len(edgesTS)):
            if (edgesTS[j][0] > end):
                j -= 1
                G = getGraphFrimIntervals(edgesTS[i:j+1], [(0, len(edgesTS[i:j+1])-1)], charikar_mode = 'weighted_emails')
                #G = getGraphWeighted(edgesTS[i:j+1])
                S, avg = charikar.charikar(copy.deepcopy(G), 'weighted', 'basic')
                if avg > bestAvg:   
                    bestAvg, bestInt = avg, (i,j)
                    bestS = copy.deepcopy(S)
                break

    return bestAvg, bestInt, bestS
 