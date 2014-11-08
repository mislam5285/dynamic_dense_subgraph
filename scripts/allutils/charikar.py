from networkx import *
from networkx.generators.random_graphs import *
import numpy as np
#import matplotlib.pyplot as #plt
from datetime import datetime, timedelta
import os
import random
from collections import OrderedDict
import time
import fibonacci_heap_mod

def charikar(G, mode = 'unweighted', version = 'basic'):
    if version == 'basic':
        S, best_avg = charikarBasic(G, mode)
    if version == 'fixed':
        S, best_avg = charikarFixed(G, mode)
    return S, best_avg 

def charikarBasic(G, mode = 'unweighted'):
    if mode == 'weighted':
        attr = 'weight'
    else:
        attr = None
        
    E = G.number_of_edges()
    N = G.number_of_nodes()
    fib_heap = fibonacci_heap_mod.Fibonacci_heap()
    entries = {}
    order = []
    S = copy.deepcopy(G)
    
    for node, deg in G.degree_iter():
        entries[node] = fib_heap.enqueue(node, deg)
        
    best_avg = 0.0    
    iter = 0
    
    while fib_heap:
        avg_degree = (2.0 * E)/N
        
        if best_avg <= avg_degree:
            best_avg = avg_degree
            best_iter = iter
            
        min_deg_obj = fib_heap.dequeue_min()
        min_deg_node = min_deg_obj.get_value()
        order.append(min_deg_node)
            
        for n in G.neighbors_iter(min_deg_node):
            fib_heap.decrease_key(entries[n], -1)
            E -= 1
            
        G.remove_node(min_deg_node)
        N -= 1
        iter += 1
        
    for i in xrange(best_iter):
        S.remove_node(order[i])
    return S, best_avg

    
def charikarFixed(G, mode = 'unweighted'):
    if mode == 'weighted':
        attr = 'weight'
    else:
        attr = None

    d = G.degree(weight = attr)        
    best_avg = 0.0
    S = nx.Graph()
    while d:
        #avg_degree = 2.0*sum((nx.get_edge_attributes(G, 'weight')).values())/G.number_of_nodes()
        avg_degree = float(sum(d.values())) / len(d)
        #print avg_degree  
        if best_avg <= avg_degree:
            best_avg = avg_degree
            S = copy.deepcopy(G)
            
        conComp = nx.connected_component_subgraphs(G)        
        stat, min_deg_node = [], []
        
        #find component of a smallest avg degree
        min_avg, i = sys.maxint, -1
        for c in xrange(0, len(conComp)):
            d = conComp[c].degree(weight = attr)
            avg = float(sum(d.values())) / len(d)
            if avg < min_avg:
                min_avg, i = avg, c
                    
        d = conComp[i].degree(weight = attr)
        min_deg_node = min(d, key = d.get)       
        G.remove_node(min_deg_node)
         
        d = G.degree(weight = attr)
    return S, best_avg
