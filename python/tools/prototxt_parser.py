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
import re
import json

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


protoFile = args.proto_file
csvFile = args.csv_file
#protoFile = "./example/ResNet-50-deploy.prototxt"
#protoFile = "./example/ResNet-101-deploy.prototxt"
#protoFile = "./example/ResNet-152-deploy.prototxt"
#csvFile = "./example/ResNet-50-deploy.csv"
#csvFile = "./example/ResNet-101-deploy.csv"
#csvFile = "./example/ResNet-152-deploy.csv"
with open(protoFile) as f:
    s = f.read()
    s = s.replace('"',"")
    s = s.replace(":","")


csvFp = open(csvFile,'w')

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
layerCount = 0
k = 0
for i in range(0,len(result)):
    if result[i][0] == "layer":
        result[i][0] = layerCount
        layerCount += 1
    else:
        if result[i][0] == "input_dim":
            result[i][0] += str(k)
            k += 1

#print len(result),result
protoDict= dict(result)
allKeys = []

protoDictFlat = {}

for key, value in protoDict.iteritems():
    if isinstance(key,str):
        #print "attr",key, value
        allKeys.append(key)
        protoDictFlat[key] = value
    elif isinstance(key,int):
        protoDictFlat[key] = {}
        protoDictFlat[key]["layer"] = str(key)
        if isinstance(value,list):
            protoDict[key] = dict(value)
            for l_key , l_value in protoDict[key].iteritems():
                if isinstance(l_value,list):
                    #print dict(l_value)
                    protoDict[key][l_key] = dict(itertools.izip_longest(*[iter(l_value)] * 2, fillvalue=""))
                    for p_key, p_value in protoDict[key][l_key].iteritems():
                        newKey =l_key+'.'+p_key
                        allKeys.append(newKey)
                        protoDictFlat[key][newKey] = p_value
                    #print key,l_key,protoDict[key][l_key]
                elif isinstance(l_value,str):
                    #print "str:",key, l_key, l_value
                    newKey = l_key
                    allKeys.append(l_key)
                    protoDictFlat[key][newKey] = l_value
                else:
                    print "Error:", l_value
                #print key,l_key,protoDict[key][l_key]
    else:
        print "Error:"

with open('proto.json', 'w') as fp:
    json.dump(protoDictFlat, fp)
fp.close()
print "allKey",len(allKeys) , allKeys
uniqKey = list(set(allKeys))
print "unqiKey",len(uniqKey) , uniqKey
uniqKey = [k for k in uniqKey if 'layer' not in k]
uniqKey = [k for k in uniqKey if 'input_dim' not in k]
uniqKey = [k for k in uniqKey if 'bottom' not in k]
uniqKey = [k for k in uniqKey if 'name' not in k]
uniqKey = [k for k in uniqKey if 'type' not in k]
uniqKey = [k for k in uniqKey if 'top' not in k]
sortKey= "bottom,layer,name,type,top,"+','.join(uniqKey)
sortKey = sortKey.split(",")
print "sortKey",len(sortKey) , sortKey
columnList = ','.join(sortKey)

csvFp.write(columnList + "\n")
for i in range(0,layerCount):
    attrList = []
    for key in sortKey:
        if key in protoDictFlat[i]:
            attrList.append(protoDictFlat[i][key])
        else:
            #print "key miss", key, protoDictFlat[i]
            attrList.append("NA")
    layerLine = ','.join(attrList)
    csvFp.write(layerLine + "\n")

csvFp.close()