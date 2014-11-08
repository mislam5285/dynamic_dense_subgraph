import networkx as nx
import time
#import datetime
#from datetime import datetime, timedelta
from datetime import datetime, timedelta
from collections import OrderedDict
import matplotlib.pyplot as plt
import sys
import operator
import os
import copy
import numpy as np
import utils

def plotGraph(outpath, id, title, G, type = 'graph', baseNodes = '', baseEdges = '', baseAvg = ''):
    #id = datetime.datetime.now().total_seconds()

    t = title+'_'+str(id)
    plt.figure(t)
    header = 'nodes = ' + str(G.number_of_nodes()) + '; edges = ' + str(G.number_of_edges()) + '; avg degree = ' + str((2.0*G.number_of_edges())/G.number_of_nodes())[:6]
    if type == 'subgraph':
        header += '\n baseline nodes = ' + str(baseNodes) + '; baseline edges = ' + str(baseEdges) + '; baseline avg = ' + str(baseAvg)[:6]
 
    plt.title(header)
    nx.draw(G)     
    plt.savefig(os.path.join(outpath, t + '.png'))
    
def coveredSubgraphs(outpath, id, edgesTS_withRep, timeIntervals, edges_covered):
    plt.figure('Covered_subgraphs'+str(id))   
    colors = ['r','g','b','c','m','y','k','pink','tomato','Khaki','BlanchedAlmond', 'RosyBrown']    
    c = 0 
    for i in timeIntervals:
        T = nx.Graph()
        for t in xrange(i[0],i[1]+1):
            if edgesTS_withRep[t][1] in edges_covered:
                T.add_edges_from([edgesTS_withRep[t][1]])
        nx.draw(T, node_color = colors[c])
        T.clear()
        c += 1
    plt.savefig(os.path.join(outpath, 'Covered_subgraphs'+str(id) + '.png'))
    
def plotPoints(outpath, S, edgesTS, timeIntervals, counter, B, rest_B, k, edges_covered):
    TS = []
    for i in xrange(0, len(edgesTS)):        
        edge = edgesTS[i][1]        
        if edge[0] not in S.nodes() or edge[1] not in S.nodes():            
            TS.append(tuple([edgesTS[i][0],edgesTS[i][1],-1]))
            #TS.append(tuple([edgesTS[i][0],edgesTS[i][1],-1,-1]))
        else:      
            TS.append(edgesTS[i])
            
    TS = np.array(TS)
    helper = np.vectorize(lambda x: (x-min(TS[:,0])).total_seconds())
    dt_sec = helper(TS[:,0])
    y = list(TS[:, -1])
    plt.figure('Coverage_'+str(counter))
    plt.scatter(dt_sec, y, c = y)
    
    #TS = np.array(edgesTS)
    colors = ['r','g','b','c','m','y','k','pink','tomato','Khaki','BlanchedAlmond', 'RosyBrown']    

    #dt_sec = helper(TS[:,0])
    #y = list(TS[:,-1])
    c = 0

    for i in timeIntervals:
        #plt.axvspan(helper(edgesTS[i[0]][0]), helper(edgesTS[i[1]][0]), facecolor = '0.5', alpha = 0.5)
        plt.axvspan(helper(edgesTS[i[0]][0]), helper(edgesTS[i[1]][0]), facecolor = colors[c], alpha = 0.5)
        c += 1    
        
    #plt.axvspan(helper(edgesTS[baseInt[0]][0]), helper(edgesTS[baseInt[1]][0]), facecolor = colors[c], alpha = 0.5)
    
    plt.title('total edges = '+str(S.number_of_edges()) + '; budget (sec) = ' + str(B) + '; K = ' + str(k) + 
        '\n used budget (sec) = '+ str(B - rest_B) + '; covered edges = ' +str(len(edges_covered)))
    plt.xlabel('time line (sec)')
    plt.ylabel('edges')
    #print os.path.join(outpath, str(global_counter)+'_Coverage_'+str(counter) + '.png')
    plt.savefig(os.path.join(outpath, 'Coverage_'+str(counter) + '.png'))