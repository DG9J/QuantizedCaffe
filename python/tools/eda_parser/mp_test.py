from multiprocessing import Pool
from multiprocessing import process
import os, time, random
import icComVar as icVar
import pyparsing as pp
import re
import fileinput as fi


def long_time_task(name,pattern,target_string):
    #print('Run task %s (%s)...' % (name, os.getpid()))
    #start = time.time()
    input_delay_result = pattern.searchString(target_string)
    #end = time.time()
    #print('Task %s runs %0.2f seconds.' % (name, (end - start)))
    #print name, input_delay_result
    return input_delay_result[0][0][1]

if __name__=='__main__':
    rpt_file = r'C:/parser_case/df_cs_umc_t_8.ft.nlc.tt0p65v.rpt'
    delay = icVar.floatNum
    arrive = icVar.floatNum

    input_delay = pp.Group("input external delay" + delay + arrive + icVar.toggleType)
    data_arr_pat = pp.Group("data arrival time" + arrive)
    pt_path = ''
    pt_path_list = []


    path_end = re.compile(r'slack ')
    for line in fi.input(rpt_file):
        match = path_end.search(line)
        if match:
            # print "match :" ,line
            pt_path_list.append(pt_path)
            pt_path = ""
        else:
            pt_path = pt_path + line
    print "complete read the", rpt_file

    MP = 1

    if MP == 0 :
        i = 0
        while i < len(pt_path_list):
            pt_path = pt_path_list[i]
            input_delay_result = input_delay.searchString(pt_path)
            i = i + 1
        print "Serial run finshed"
    else:

        print('Parent process %s.' % os.getpid())
        p = Pool(4)

        results = [p.apply_async(long_time_task, args=(k,data_arr_pat,pt_path_list[k])) for k in range(1,1000)]
        print('Waiting for all subprocesses done...')
        output = [pt.get() for pt in results]
        print output
        p.close()
        p.join()
        print('All subprocesses done.')
        print len(pt_path_list)