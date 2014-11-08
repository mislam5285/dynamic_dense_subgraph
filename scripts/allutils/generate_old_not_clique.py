#import networkx as nx
from networkx import *
from networkx.generators.random_graphs import *
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
#import datetime
#from numpy import array
import os
import random

#import time
#import string

#filepath = ".\/DynGraphData\/CAStudents.txt"
#filepath =  os.path.join("..", "DynGraphData", "CAStudents.txt")

def charikar(G):
    #d = G.degree(weight = 'weight')
    #print d    
    d = G.degree()
    best_avg = 0.0
    S = nx.Graph()
    while d:
        avg_degree = float(sum(d.values())) / len(d)
        if best_avg <= avg_degree:
            best_avg = avg_degree
            S = G.copy()
        min_deg_node = min(d, key = d.get)
        G.remove_node(min_deg_node)
        d = G.degree()    
        #d = G.degree(weight = 'weight')
    return S, best_avg
    
def generateRG(nodes, edges_p):
    G = fast_gnp_random_graph(nodes, edges_p, seed=None, directed=False)
    return G
    
def generateComsCharikar(G, num): #com_descr - size, probability
    
    tmp = nx.Graph()
    C = nx.Graph()
    #communities = {}
    communities = []
    for i in xrange(0, num):
        C.clear()
        C, _ = charikar(copy.deepcopy(G))
        #print "nodes in C:", len(C.nodes())
        #print "nodes in G:", len(G.nodes())
        G.remove_nodes_from(C.nodes())
        #print "Rest:", len(G.nodes())
        #communities[i] = copy.deepcopy(C)
        communities.append(copy.deepcopy(C))
    return communities
    
    
def generateCom(com_descr): #com_descr - size, probability
    st = 0
    tmp = nx.Graph()
    C = nx.Graph()
    #communities = {}
    communities = []
    for i in com_descr:
        tmp.clear()
        C.clear()
        size, p = i[0], i[1]
        tmp = generateRG(size, p)
        
        C.add_nodes_from(range(st, st+size))
        t = map(tuple, np.array(tmp.edges())+st)
        C.add_edges_from(t)
        
        communities.append(copy.deepcopy(C))

        st = st + size
        #st = st + size - 3
    return communities
 
def genTS(Graph, p, tstamp, end, step):
    TS = []    
    num_edges = len(Graph.edges())
    edgesG = np.array(Graph.edges())
    
    while tstamp <= end:
        r = np.random.rand(num_edges)
        happened = edgesG[r <= p]
       
        for i in happened:           
            TS.append((tstamp, tuple(i)))
        tstamp += step
    return TS
 
def genTS_random(Graph, tstamp, end, step):
    TS = []    
    num_edges = len(Graph.edges())
    edgesG = Graph.edges()
    
    
    while tstamp <= end:
        r = random.choice(edgesG)
        TS.append((tstamp, tuple(r)))        
        tstamp += step
    return TS
    
 
def genTS2(Graph, tstamp, end, step):
    TS = []
    covered = set()   
    num_edges = len(Graph.edges())
    #edgesG = array(Graph.edges())
    edgesG = Graph.edges()
    offset = min(Graph.nodes())
    
    while tstamp <= end:
        #r = np.random.rand(num_edges)
        #happened = edgesG[r <= p]
        #r = random.choice(Graph.edges())
        r = random.randint(0, num_edges-1)
        
        #for i in happened:           
        #    TS.append((tstamp, tuple(i)))
        e = list(edgesG[r])
        #print e
        e.sort()
        #TS.append((tstamp, tuple(e), lookup[tuple(e)]))
        TS.append((tstamp, tuple(e)))
        tstamp += step
        covered.add(tuple(e))
    return TS
    
    
def genTS3(Graph, tstamp, end, step, n):
    num_edges = Graph.number_of_edges()
    rnd = range(0, num_edges)
    m = len(rnd)
    #print m, n, num_edges
    res = n/num_edges
    t = []
    for i in xrange(0,res):
        t += rnd
    t += random.sample(range(0, num_edges), n - res*m)
    # if 5*num_edges < n:  
        # rnd = rnd+ rnd +rnd+ rnd+ rnd+ random.sample(range(0, num_edges), n - 5*m)
    # elif 4*num_edges < n:  
        # rnd = rnd+ rnd +rnd+ rnd+ random.sample(range(0, num_edges), n - 4*m)
    # elif 3*num_edges < n:  
        # rnd = rnd+ rnd +rnd+ random.sample(range(0, num_edges), n - 3*m)
    # elif 2*num_edges < n:    
        # rnd = rnd+ rnd + random.sample(range(0, num_edges), n - 2*m)
    # else:
        # rnd = rnd + random.sample(range(0, num_edges), n-m)
    rnd = t
    random.shuffle(rnd)
 
    
    TS = []
    covered = set()   
    num_edges = len(Graph.edges())
    #edgesG = array(Graph.edges())
    edgesG = Graph.edges()
    offset = min(Graph.nodes())
    i = 0
    #print len(rnd)
    while tstamp <= end:
        #r = np.random.rand(num_edges)
        #happened = edgesG[r <= p]
        #r = random.choice(Graph.edges())
        #print i
        r = rnd[i]
        
        #for i in happened:           
        #    TS.append((tstamp, tuple(i)))
        e = list(edgesG[r])
        #print e
        e.sort()
        #TS.append((tstamp, tuple(e), lookup[tuple(e)]))
        TS.append((tstamp, tuple(e)))
        tstamp += step
        covered.add(tuple(e))
        i += 1
    return TS
    
def splitCom(C):
    parts = strongly_connected_component_subgraphs(C)
    return parts
    
def splitCom_Randomly(C, k):
    e = C.edges()
    random.sample(e, k)
    return parts
    
def splitCom(C):
    clique_size = 5
    nodes = C.nodes()
    offset = min(nodes)
    tmp = nx.complete_graph(clique_size)
    part1 = nx.Graph()
    part1.add_nodes_from(range(offset, offset + clique_size))
    t = map(tuple, np.array(tmp.edges())+offset)
    part1.add_edges_from(t)
    
    C.remove_edges_from(part1.edges())
    parts =(part1, C)
    return parts
    
def readGraph(filepath):
    G = nx.Graph()
    with open(filepath,'r') as fd:
        for line in fd.readlines():
            line = line.strip()            
            items = line.split(' ')
            t = items[2:4]
            t = map(int,t)
            # if t[0] == t[1]:            
                # continue
            # t.sort(); #undirected
            G.add_edge(t[0],t[1])
    return G
    
    
def printOutTS(TS, outpath, outfile):
    #TS.sort()
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    f = open(outfile, 'w')
    for i in TS:
        #print "\""+ str(i[0])+ "\"", i[1][0], i[1][1], i[2]
        out=' '.join(["\""+ str(i[0])+ "\"", str(i[1][0]), str(i[1][1])])
        f.write(out+'\n')
    f.close()
    
def generateNotClique(noise):

    delete_edges = noise
    
    # id = sys.argv[2]
    # outpath = delete_edges
    # outfile = delete_edges + '_' + id + '.txt'
    # outfile = os.path.join(outpath, outfile)
    
    delete_edges = int(delete_edges)
    

    # generate graph (random graph)     
    nodes = 100
    # edges_p = 0.001
    #desired_avg_degree = noise
    desired_avg_degree = 4
    edges_p = float(desired_avg_degree)/(nodes-1)
    G = generateRG(nodes, edges_p)

    # read graph (random graph)     
    # G = readGraph(filepath)
    
    d = G.degree()
    #print "expected avg degree", (nodes-1)*edges_p
    #print "generated avg degree", float(sum(d.values())) / len(d)
    #print "generated avg degree", float(sum(d.values())) / len(d)
    # print (2.0*G.number_of_edges())/G.number_of_nodes()
    #plt.figure("Initial graph")

    #nx.draw(G)
    #plt.show()
    #exit()

    #generate communities by description
    #desc = [(4,1),(7,0.9), (10, 0.9)]
    #com_nodes = 10
    
    #community 1
    com_nodes = 8
    #desired_avg_degree = 9
    desired_avg_degree = com_nodes - 1
    com_edges_p = float(desired_avg_degree)/(com_nodes-1)
    desc = [(com_nodes, com_edges_p)]
    
    
    #community 2
    # com_nodes = 5
    # #desired_avg_degree = 9
    # desired_avg_degree = 4
    # com_edges_p = float(desired_avg_degree)/(com_nodes-1)
    # desc.append((com_nodes, com_edges_p))
    
    coms = generateCom(desc);
    r = random.sample(coms[0].edges(), delete_edges)
    coms[0].remove_edges_from(r)
    
    
    d = coms[0].degree()
    #print "expected avg degree com1", (com_nodes-1)*com_edges_p
    #print "generated avg degree com1", float(sum(d.values())) / len(d)
    #print "edges", coms[0].number_of_edges()
    #plt.figure("Com1")
    #nx.draw(coms[0])
    #plt.show()
    #print (2.0*G.number_of_edges())/G.number_of_nodes(), (2.0*coms[0].number_of_edges())/coms[0].number_of_nodes()
    
    # d = coms[1].degree()
    # print "expected avg degree com2", (com_nodes-1)*com_edges_p
    # print "generated avg degree com2", float(sum(d.values())) / len(d)
    # print "edges", coms[1].number_of_edges()
    #plt.figure("Com2")
    #nx.draw(coms[1])
    #plt.show()
    
    #coms += generateCom([(2,1),(3,1),(4,1)])
    #coms += generateCom([(5,1)])
    #print coms    
    # t = (coms[0]).edges()
    # t.sort()
    # lookup = {e: i for i, e in enumerate(t)}
    #print lookup

    # generate by Charikar
    # num = 2
    # coms = generateComsCharikar(copy.deepcopy(G), num)


    #separate background
    # backGrGraph = copy.deepcopy(G)
    # for com in coms:
        # backGrGraph.remove_edges_from(com.edges())
    # d = backGrGraph.degree()
    # print "background avg degree", float(sum(d.values())) / len(d)
    # plt.figure("Background")
    # nx.draw(backGrGraph)
    #plt.show()
    
    #union cimmunities with G
    backGrGraph = copy.deepcopy(G)
    for com in coms:
        backGrGraph.add_edges_from(com.edges())
    #d = backGrGraph.degree()
    backGrGraph=nx.Graph(backGrGraph)
    d = backGrGraph.degree()    
    #print "generated avg degree", float(sum(d.values())) / len(d)
    

    #Background activity
    TS = []
    # desired_fire_rate = 1
    #p = 1.0/nodes
    #p = 1.0/backGrGraph.number_of_edges()
    #p = 3.0/120
    p = 3.0/180
    start = datetime(2010, 12, 01, 00, 00, 00) #start
    # #end = datetime(2010, 12, 30, 00, 00, 00) #end
    #end = datetime(2010, 12, 01, 00, 06, 40) #end
    end = datetime(2010, 12, 01, 00, 03, 00) #end
    step = timedelta(seconds = 1)
    # edgesTS_withRep = [] 
    #TS += genTS_random(backGrGraph, start, end, step)
    TS += genTS(backGrGraph, p, start, end, step)
    #TS += genTS3(backGrGraph, start, end, step, 401)
    #TS += genTS3(backGrGraph, start, end, step, 251)


    #points on line short
    # int_desc = [(0, datetime(2010, 12, 01, 00, 00, 30), datetime(2010, 12, 01, 00, 01, 00), timedelta(seconds = 1)),        
        # (1, datetime(2010, 12, 01, 00, 1, 30), datetime(2010, 12, 01, 00, 2, 00), timedelta(seconds = 1))      
    # ]
    #int_desc = [(0, datetime(2010, 12, 01, 00, 00, 30), datetime(2010, 12, 01, 00, 01, 00), timedelta(seconds = 1)),        
    #    (1, datetime(2010, 12, 01, 00, 1, 30), datetime(2010, 12, 01, 00, 1, 40), timedelta(seconds = 1))      
    #]
    int_desc = [(0, datetime(2010, 12, 01, 00, 01, 00), datetime(2010, 12, 01, 00, 01, 30), timedelta(seconds = 1))]
    
    #c = copy.deepcopy(coms[2])
    #s = splitCom(c)
    
    #add community  activity
    # for i in int_desc:
        # #num, p, start, end, step = i[0], i[1], i[2], i[3], i[4]
        # num, start, end, step = i[0], i[1], i[2], i[3]
        # #TS += genTS(coms[num], p, start, end, step)
        
        # #TS += genTS2(coms[num], start, end, step)
        # TS += genTS3(coms[num], start, end, step, 31)
        
    i = int_desc[0]
    num, start, end, step = i[0], i[1], i[2], i[3]
    TS += genTS3(coms[num], start, end, step, 31)
    # i = int_desc[1]
    # num, start, end, step = i[0], i[1], i[2], i[3]
    # TS += genTS3(coms[num], start, end, step, 11)
                
    TS.sort()
    
    #print TS
    #TS = np.array(TS)
    #print TS
    
    # helper = np.vectorize(lambda x: (x-datetime(1970, 1, 1)).total_seconds())
    # dt_sec = helper(TS[:,0])
    #print len(dt_sec)
    
    # y = list(TS[:,-1])
    # print len(y)
        
    # print "y", y
    # cc = np.random.random(len(y))
    # print "cc",cc
    # #cc = np.cos(list(y))
    # cc = list(y)
    # print "cos", cc
    
    # cc = y/(1.0*max(y))
    
    # print cc
    # plt.scatter(dt_sec, list(y), c = list(y))
    # plt.figure("points")
    # plt.scatter(dt_sec, y, c = y)
    # plt.show()
    #printOutTS(TS, outpath, outfile)
    
    return TS
    
