import networkx as nx
import time
from datetime import datetime, timedelta
from collections import OrderedDict
#import matplotlib.pyplot as plt
import sys
import operator
import os
import copy
import main
from allutils import utils
import uuid

filepath = os.path.join(".","..","DATA",sys.argv[1])

outdir = sys.argv[2]
outpath = outdir + '_' + str(uuid.uuid4())
        
k = int(sys.argv[3])
b = float(sys.argv[4])
n = int(sys.argv[5])

#toc = time.clock()

pics = False

runMainAlgs = sys.argv[6]

#alg = 'dynprogr'
#alg = 'greedy'
#alg = 'binary'

#charikar_version = 'basic'
charikar_version = 'fixed'

# if alg == 'greedy' or alg == 'binary':
    # charikar_mode = 'unweighted'

# if alg == 'dynprogr':
    # charikar_mode = 'weighted'

#k = 3
#B = timedelta(seconds = 20)
B = timedelta(days = b)

#n = 1000

edgesTS, nodes, edges =  utils.readFile(filepath)  

_, _, baseS = utils.getBaseline(edgesTS, B)
avg_base = 2.0*baseS.number_of_edges()/baseS.number_of_nodes()
size_base = baseS.number_of_nodes()

ff = open(outpath, "a")
#ff.write(' '.join([str(gr_avg_best), str(bi_avg_best), str(dy_avg_best), str(gr_int_best), str(bi_int_best), str(dy_int_best),
#str(gr_size_best), str(bi_size_best), str(dy_size_best), '\n']))
ff.write(' '.join([str(avg_base), str(size_base),'\n']))
ff.close()
