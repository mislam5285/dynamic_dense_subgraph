import networkx as nx
import time
from datetime import datetime
from collections import OrderedDict
import matplotlib.pyplot as plt
import sys
import operator
import random
import copy
import charikar

filepath = sys.argv[1]


edges = {}
edgesTS = OrderedDict()
nodesTS = []
edgesTS_withRep = []   
nodes = set()
G = nx.Graph()

with open(filepath,'r') as fd:
    for line in fd.readlines():
        line = line.strip()            
        items = line.split(' ')
        tstamp  = ' '.join(items[0:2])
        tstamp = tstamp[1:-1]
        tstamp = datetime.strptime(tstamp, '%Y-%m-%d %H:%M:%S')
        t = items[2:4]
        t = map(int,t)
        if t[0] == t[1]:            
            continue
        t.sort(); #undirected
        
        edgesTS.setdefault(tstamp,[]).append(tuple(t))
        
        edgesTS_withRep.append((tstamp, t))       
        
        G.add_edges_from([tuple([t[0], t[1]])])
        
        #nodes.add(t[0])
        #nodes.add(t[1])
        
print "Nodes:", len(G.nodes())
print "Edges", len(G.edges())
print "Distinct timestaps", len(edgesTS)
print "Total timestaps", len(edgesTS_withRep)
print "Time start:", str(edgesTS_withRep[0][0]), "Time end:", str(edgesTS_withRep[-1][0]), "Total:", edgesTS_withRep[-1][0]-edgesTS_withRep[0][0]
d = G.degree()
print "avg degree", float(sum(d.values()))/len(d)
print "min degree", min(d.values())
print "max degree", max(d.values())


t = edgesTS.keys()
t.sort()
dt = t[0] - t[0]
for i in range(1, len(t)):
    dt += t[i] - t[i-1]
    #print t[i-1], t[i], t[i] - t[i-1]
avg_dt = dt/(len(t)-1)
print "avg time gaps (distinct)", avg_dt


dt = edgesTS_withRep[0][0] - edgesTS_withRep[0][0]
for i in range(1, len(edgesTS_withRep)):
    dt += edgesTS_withRep[i][0] - edgesTS_withRep[i-1][0]
avg_dt = dt/(len(edgesTS_withRep)-1)
print "avg time gaps (total)", avg_dt


c = 0
for i in edgesTS.values():
    c += len(i)
c = float(c)/len(edgesTS)
print "avg activity at one timestamp", c

toc = time.time()
#S, avg = charikar.charikar(G,'unweighted', 'basic')
S, avg = charikar.charikar(G)
tic = time.time()
print tic-toc
print 'charikar on underlying network', avg
print 'charikar on underlying network', 2.0*S.number_of_edges()/S.number_of_nodes()
print 'size of charikar on underlying network', S.number_of_nodes()
print 'size of charikar on underlying network, edges', S.number_of_edges()

