#!/usr/bin/python
'''
prototxt_parser is parse , coverting the Caffe prototxt file inot a csv file
flow :
1. used a BNF to parse the prototxt to a hash file
layer_dict => [n] =>
                   {type} = ['Input']
                   {name} = ['data']
                   {dim}  = [1,3,32,32]
2. convet the hash to 2-D list
3. write the 2-D list as a csv file
'''

import argparse
import csv
from pyparsing import *


parser = argparse.ArgumentParser()
# Required arguments: input and output files.
parser.add_argument(
    "proto_file",
    help="Input the caffe protxt file."
)
parser.add_argument(
    "csv_file",
    help="Output the csv file."W
)
args = parser.parse_args()
def flatten(the_list,new_list):
    for i in the_list:
        if isinstance(i, list):
            flatten(i,new_list)
        else:
            new_list.append(i)


with open(args.proto_file) as f:
    s = f.read()

LBRACE,RBRACE,LBRACK,RBRACK,COMMA,COLON,DOT = map(Suppress,"{}[],:.")

key    = Word(alphanums+"_")
value  = Word(alphanums+"_")
attr_format  = Group(key +  COLON + Suppress(ZeroOrMore('"'))+ value + Suppress(ZeroOrMore('"')))
shape_format = Suppress("shape") + COLON + LBRACE + OneOrMore(attr_format) + RBRACE
para_format = Group(Suppress(key) + LBRACE  + ZeroOrMore(attr_format) + ZeroOrMore(shape_format) + RBRACE)
layer_format = Suppress("layer") + LBRACE + OneOrMore(attr_format) + ZeroOrMore(para_format) + RBRACE

layer_results = layer_format.searchString(s)
layer_dict = list()
layer_keys = list()
layer_names = list()

layer_numb = 0
for items in layer_results:
    layer_numb += 1
    layer_list = list()
    layer_name = "Unknow"
    flatten(items.asList(),layer_list)
    for i in range(0,len(layer_list)):
        if layer_list[i] == "name":
            layer_name = layer_list[i+1]
    if  layer_name not in layer_names:
        layer_names.append(layer_name)
    temp_dict = {}
    for i in range(0,len(layer_list),2):
        key = layer_list[i]
        value = layer_list[i+1]
        if key not in temp_dict:
            temp_dict[key]=list()
        temp_dict[key].append(value)
        if key not in layer_keys:
            layer_keys.append(key)
    layer_dict.append(temp_dict)
layer_keys.insert(1,"layer")

layer_array = list()
layer_array.append(layer_keys)
empty_list = [" " for i in range(len(layer_keys))]
base_line = 1
for i in range(0,len(layer_dict)):
    current_line = base_line
    jump_line = 0
    max_para = 0
    temp_dict = layer_dict[i]
    for t in temp_dict:
        if len(temp_dict[t]) > max_para :
            max_para = len(temp_dict[t])
    for t in range(0,max_para):
        layer_array.append(empty_list[:])
    for j in range(0,len(layer_keys)):
        key = layer_keys[j]
        if key == "layer":
            layer_array[current_line][j] = i
        elif key in temp_dict:
            for l in range(0,len(temp_dict[key])):
                next_line = current_line + l
                layer_array[next_line][j] = temp_dict[key][l]

    base_line += max_para

with open(args.csv_file, "wb") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(layer_array)
