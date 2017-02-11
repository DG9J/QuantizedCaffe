import os, pickle, csv, sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import random

R = 1
TOTAL = 10000000
HIT = 0

for j in range(1,100):
    for i in range(TOTAL):
        x = random.uniform(-1,1)
        y = random.uniform(-1,1)
        r = np.sqrt(x*x+y*y)
        if r < 1:
            HIT = HIT + 1
    pi = float(HIT)/float(TOTAL*j)*4
    print j,HIT, TOTAL, pi
