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
import main
from allutils import utils

#filepath = os.path.join(".","..","DATA",sys.argv[1])
filepath = os.path.join(".","..","DATA","facebook.txt")
outpath = 'test_' + str(uuid.uuid4())

if not os.path.exists(outpath):
    os.makedirs(outpath)

toc = time.clock()

pics = True

#alg = 'dynprogr'
#alg = 'greedy'
alg = 'binary'

charikar_version = 'basic'

if alg == 'greedy' or alg == 'binary':
    charikar_mode = 'unweighted'

if alg == 'dynprogr':
    charikar_mode = 'weighted'

k = 10
#B = timedelta(seconds = 20) 
B = timedelta(days = 7)

#print 'read file:'
edgesTS, nodes, edges =  utils.readFile(filepath)

utils.plotInitial(edgesTS)
timeIntervals = []
timeIntervals.append((0, len(edgesTS)-1))  
tic = time.time()
nodes_covered, timeIntervals, usedB, S, edges_covered = main.main(outpath, alg, charikar_version, charikar_mode, pics, k, B, edgesTS, nodes, edges, timeIntervals, baseline = False, n_disc = 1000)
toc = time.time()
print 'total running time (sec): ', toc-tic
print 'average degree of discovered community: ', 2.0*len(edges_covered)/len(nodes_covered)
print 'number of intervalsL ', k
print 'allowed time budget: ', B
print 'used time budget: ', usedB
sys.stdout.flush()
    
