import math
import os
import sys
import random
import time
from queue import LifoQueue

zearth_pos = tuple(map(float, input().rstrip().split()))
earth_pos = (0.0, 0.0, 0.0)
N = int(input())
M = 10000

stations = [tuple(map(float, input().rstrip().split())) for i in range(N)]


# helper function
def dist(u, v):
    return math.sqrt( sum([ (u[i]-v[i])**2 for i in range(3) ]) )

def generate_samples(num_samples):
    samples = [(random.uniform(-M,M), random.uniform(-M,M), random.uniform(-M,M)) 
                    for i in range(num_samples)]
    return samples



def is_possible(C):
    # Check if route is possible with max edge length C

    d = {} # will store state for each station. 0 is unreached, 1 is visiting, 2 is visited
    for station in stations:
        d[station] = 0
    d[earth_pos] = 1
    visiting = LifoQueue()
    visiting.put(earth_pos)

    while(visiting.qsize() != 0):
        here = visiting.get()
        d[here] = 2
        if(dist(here, zearth_pos) <= C):
            return True
        
        for station, value in d.items():
            if(value == 0 and dist(here, station) <= C):
                d[station] = 1
                visiting.put(station)

    return False

def capacity_scaling():
    # capacity scaling, binary search approach (more interesting)

    # C will be the max allowable distance. a and b are the search range
    a, b = 0.0, dist(earth_pos, zearth_pos)+1.0

    while(b-a >= 0.01):
        C = (a+b)/2
        possible = is_possible(C)

        if(possible):
            b = C
        else:
            a = C

    # just need a bit of logic due to rounding
    a = round(a, 2)
    b = round(b, 2)
    if(a == b):
        ans = a
    else:
        if(is_possible( (a+b)/2 )):
            ans = a
        else:
            ans = b
    
    return ans




def kruskal():
    stations.append(earth_pos)
    stations.append(zearth_pos)

    L = len(stations)

    # list and sort all edges in the graph
    edges = [(stations[i], stations[j]) for i in range(L) for j in range(i+1,L)]
    edges = sorted(edges, key = lambda x : dist(x[0],x[1]))

    parents = {s : s for s in stations}

    # find root with path compression
    def root(x):
        if(parents[x] == x):
            return x
        else:
            parents[x] = root(parents[x])
            return parents[x]

    # merges sets
    def union(x, y):
        root_x = root(x)
        root_y = root(y)
        if(root_x != root_y):
            parents[root_x] = root_y
    
    maximum = 0
    for a, b in edges:
        if(root(a) != root(b)):
            maximum = dist(a, b)
            union(a, b)

            if(root(earth_pos) == root(zearth_pos)):
                break
    
    return round(maximum, 2)


# cap_ans = capacity_scaling()
kru_ans = kruskal()

sys.stdout.write(str(kru_ans))
