#!/usr/bin/python
import os, pickle, csv, sys
import numpy as np

CHAR_MAX = 127
CHAR_MIN = -127

min = float(9999)
max = float(-9999)

def compute_MSE(weight_matrix,weight_matrix_approximate,alpha,beta,row,col):
    mse = float(0)
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            approximate_value = alpha * (weight_matrix_approximate[row][col] - CHAR_MIN) + beta
            mse += (weight_matrix[row][col] - approximate_value) * (weight_matrix[row][col] - approximate_value)
    return mse/(float(NUM_ROWS)*float(NUM_COLS))

weight_csv_fp = open('weight.csv', 'r')
reader = csv.reader(weight_csv_fp)
weight_list = []
for row in reader:
    weight_list.append(row)
weight_matrix = np.array(weight_list,dtype=float)

NUM_ROWS = list(weight_matrix.shape)[0]
NUM_COLS = list(weight_matrix.shape)[1]

weight_csv_fp.close()
avg = 0
for i in np.nditer(weight_matrix):
    if i < min :min = i
    if i > max: max = i
    avg += i
avg /= (NUM_ROWS*NUM_COLS)

MAX_WEIGHT = max
MIN_WEIGHT = min

appr_weight_matrix  = np.full((NUM_ROWS,NUM_COLS),MAX_WEIGHT,dtype=np.uint8)

for row in range(NUM_ROWS):
    for col in range(NUM_COLS):
        #print appr_weight_matrix[row][col],weight_matrix[row][col], MIN_WEIGHT, MAX_WEIGHT, MIN_WEIGHT, CHAR_MAX, CHAR_MIN, CHAR_MIN
        appr_weight_matrix[row][col] = int((weight_matrix[row][col] - MIN_WEIGHT)/(MAX_WEIGHT - MIN_WEIGHT) * (CHAR_MAX- CHAR_MIN) + CHAR_MIN)

alpha = (MAX_WEIGHT - MIN_WEIGHT)/(CHAR_MAX - CHAR_MIN)
beta = MIN_WEIGHT
print "alpha = %f  beta = %f " %(alpha,beta)
print "MSE= %f " % compute_MSE(weight_matrix,appr_weight_matrix,alpha,beta,NUM_ROWS,NUM_COLS)

appr_weight_matrix_file = open('appr_weight_matrix.csv', 'wb')
writer = csv.writer(appr_weight_matrix_file)

for row in range(NUM_ROWS):
    writer.writerow(appr_weight_matrix[row])
appr_weight_matrix_file.close()






