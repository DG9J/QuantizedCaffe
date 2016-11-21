#!/usr/bin/python
import os, pickle, csv, sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

CHAR_MAX = 127
CHAR_MIN = -127

min = float(9999)
max = float(-9999)
avg = 0

def compute_MSE(weight_matrix,weight_matrix_approximate,alpha,beta,row,col):
    mse = float(0)
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            approximate_value = alpha * (weight_matrix_approximate[row][col] - CHAR_MIN) + beta
            mse += (weight_matrix[row][col] - approximate_value) * (weight_matrix[row][col] - approximate_value)
    return mse/(float(NUM_ROWS)*float(NUM_COLS))

def parse_args():
    """Parse input arguments
    """

    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument('input_csv_file',
                        help='Input weight_matrix.csv')
    parser.add_argument('output_csv_file',
                        help='Output appr_weight_matrix.csv')
    parser.add_argument('--mode',
                        help=('mode:a b c'
                              'a: beta = min'
                              'b: beta = 0'
                              'c: beta = smart'),
                        default='a')
    args = parser.parse_args()
    return args


args = parse_args()

###process input csv file
with open(args.input_csv_file, 'r') as fr:
    reader = csv.reader(fr)
    weight_list = []
    for row in reader:
        weight_list.append(row)
    weight_matrix = np.array(weight_list,dtype=float)
fr.close()


NUM_ROWS = list(weight_matrix.shape)[0]
NUM_COLS = list(weight_matrix.shape)[1]


weight_list = weight_matrix.flatten()
weight_list.sort()

max_index = -1
min_index = 0
if args.mode == "smart":
    max_index = int(len(weight_list) *  0.99)
    min_index = int(len(weight_list) *  0.01)

max = weight_list[max_index]
min = weight_list[min_index]
avg = sum(weight_list[min_index:max_index]) / len(weight_list[min_index:max_index])

MAX_WEIGHT = max
MIN_WEIGHT = min

alpha = (MAX_WEIGHT - MIN_WEIGHT)/(CHAR_MAX - CHAR_MIN)
beta = 0
if args.mode == "min":
    beta = MIN_WEIGHT
elif args.mode == "smart":
    beta = 0
elif args.mode != "0":
    print  'Unknow mode: ' + args.mode

appr_weight_matrix  = np.full((NUM_ROWS,NUM_COLS),MAX_WEIGHT,dtype=np.int8)

for row in range(NUM_ROWS):
    for col in range(NUM_COLS):
        appr_weight_matrix[row][col] = (weight_matrix[row][col] - MIN_WEIGHT)/(MAX_WEIGHT - MIN_WEIGHT) * (CHAR_MAX- CHAR_MIN) + CHAR_MIN
        #print appr_weight_matrix[row][col],weight_matrix[row][col], MIN_WEIGHT, MAX_WEIGHT, MIN_WEIGHT, CHAR_MAX, CHAR_MIN, CHAR_MIN


print "alpha = %f  beta = %f " %(alpha,beta)
print "MSE= %f " % compute_MSE(weight_matrix,appr_weight_matrix,alpha,beta,NUM_ROWS,NUM_COLS)

###write out new matrix table
with open(args.output_csv_file, 'wb') as fw:
    writer = csv.writer(fw)
    for row in range(NUM_ROWS):
        writer.writerow(appr_weight_matrix[row])
fw.close()

#weight_list = weight_matrix.tolist()
#weight_list = appr_weight_matrix.tolist()
#hist,bin_edges = np.histogram(weight_list,bins=20)
#print(hist)
#print(bin_edges)

#plt.hist(weight_list, bins=50, normed=1, facecolor='green',alpha=0.75,histtype='stepfilled')

#plt.xlabel('value')
#plt.ylabel('number')
#plt.title(r'pre  process  matrix')
#plt.axis([40,160,0,0.03])
#plt.grid(True)

#print type(bin_edges), type(weight_list)
#fig = plt.figure()
#fig.savefig('pre_compute.png')

#plt.show()
#plt.close(fig)



