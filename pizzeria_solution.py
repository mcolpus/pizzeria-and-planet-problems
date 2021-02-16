import math
import os
import sys

NM = input().split()
N = int(NM[0])
M = int(NM[1])

pizzerias = [list(map(int, input().rstrip().split())) for i in range(M)]

# initialize array to store number of available pizzerias
arr = [ [0 for i in range(N)] for j in range(N)]
maximum = 0

# d = {}

for (x,y,r) in pizzerias:
    # adjust x and y to match 0-indexing
    x = x-1
    y = y-1

    # Note that we need to stay in bounds
    for i in range( max(-x, -r), min(N - x, r + 1) ):
        r2 = r- abs(i)
        for j in range( max(-y, -r2), min(N - y, r2 + 1) ):
            arr[x+i][y+j] += 1
            maximum = max(maximum, arr[x+i][y+j])

            # d[(x+i, y+j)] = d.get((x+i, y+j), 0) + 1
            # maximum = max(maximum, d[(x+i, y+j)])

sys.stdout.write(str(maximum))

