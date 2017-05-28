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
import pyparsing as pp
import icComVar as icVar
import itertools

def pattern_match(pattern,target_string):
    #print "pattern:", pattern
    result = pattern.searchString(target_string).asList()
    #print "result:", result
    return result

def list_flatten(l, a=None):
    #check a
    if a is None:
        #initialize with empty list
        a = []
    for i in l:
        if isinstance(i, list):
            list_flatten(i, a)
        else:
            a.append(i)
    return a
def get_values(lVals):
    for val in lVals:
        if isinstance(val, list):
            get_values(val)
        else:
            return val


'''

parser = argparse.ArgumentParser()
# Required arguments: input and output files.
parser.add_argument(
    "proto_file",
    help="Input the caffe protxt file."
)
parser.add_argument(
    "csv_file",
    help="Output the csv file."
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
'''
file = "./example/ResNet-50-deploy.prototxt"
with open(file) as f:
    s = f.read()
    s = s.replace('"',"")
    s = s.replace(":","")

flatName    = pp.Word(pp.alphanums + "_"+":")
attrDefine = pp.Group(flatName   + flatName )
paraAttr = pp.Group(pp.OneOrMore(flatName + flatName))
paraDefine = pp.Group(flatName + icVar.LBRACE + paraAttr + icVar.RBRACE)
layerAttr = pp.Group(pp.OneOrMore(attrDefine|paraDefine))
layerDefine = pp.Group("layer" + icVar.LBRACE + layerAttr  + icVar.RBRACE)
protoDefine = pp.Group(pp.OneOrMore(attrDefine) + pp.OneOrMore(layerDefine))
#print type(s),s
result = pattern_match(protoDefine,s)[0][0]
#print type(result), len(result),result
j = 0
for i in range(0,len(result)):
    if result[i][0] == "layer":
        result[i][0] = j
        j += 1
    else:
        result[i][0] = result[i][0].replace(":", "").replace('"','')
        if result[i][0] == "input_dim":
            result[i][0] += str(j)
            j += 1

#print len(result),result
protoDict= dict(result)
j = 0
for key, value in protoDict.iteritems():
    if isinstance(key,str):
        print "attr",key, value
    elif isinstance(key,int):
        if isinstance(value,list):
            protoDict[key] = dict(value)
            j += 1
            for l_key , l_value in protoDict[key].iteritems():
                l_key = l_key.replace(":", "")
                if isinstance(l_value,list):
                    #print dict(l_value)
                    protoDict[key][l_key] = dict(itertools.izip_longest(*[iter(l_value)] * 2, fillvalue=""))
                    #print key,l_key,protoDict[key][l_key]
                elif isinstance(l_value,str):
                    #print "str:",key, l_key, l_value
                    protoDict[key][l_key]= l_value.replace("\"", "")
                else:
                    print "Error:", l_value
                print key,l_key,protoDict[key][l_key]
            #for l_attr in value:
            #    print type(l_attr),len(l_attr), l_attr, dict(l_attr)
            #protoDict[key] = dict(value)
            #for layer_key, layer_value in protoDict[key].iteritems():
            #    print "layer dict", layer_key,layer_value
    else:
        print "Error:"




#with open(args.csv_file, "wb") as csvfile:
#    writer = csv.writer(csvfile)
#    writer.writerows(layer_array)
