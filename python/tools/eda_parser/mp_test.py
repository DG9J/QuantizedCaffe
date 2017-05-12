from multiprocessing import Pool
from multiprocessing import process
import os, time, random
import icComVar as icVar
import pyparsing as pp
import re
import fileinput as fi
import matplotlib.pyplot as plt
import numpy as np


def long_time_task(name,pattern,target_string):
    #print('Run task %s (%s)...' % (name, os.getpid()))
    #start = time.time()
    input_delay_result = pattern.searchString(target_string)
    #end = time.time()
    #print('Task %s runs %0.2f seconds.' % (name, (end - start)))
    #print name, input_delay_result
    return input_delay_result[0][0][1]

def plotList(data_list):

    #title = "honrizontal tt0p9v 100um"
    title = "vertical tt0p65v 100um"
    delay_list =   np.array(data_list).astype(np.float)

    print delay_list.max(),delay_list.min(),delay_list.mean()
    #print delay_list

    bin_min = int(delay_list.min()) - 1
    bin_max = int(delay_list.max()) + 1
    bins = range(bin_min,bin_max,2)

    hist ,bins  = np.histogram(delay_list, bins=bins)

    gaussian_numbers = np.asarray(delay_list)
    #plt.hist(gaussian_numbers)
    delay_avg = float("{0:.2f}".format(delay_list.mean()))
    delay_max = float("{0:.2f}".format(delay_list.max()))
    delay_min = float("{0:.2f}".format(delay_list.min()))
    xlabel = "Delay(avg="+ str(delay_avg)+"max=" + str(delay_max) + "min=" + str(delay_min)+")"
    ylable = "Count (total=" + str(len(delay_list))+ ")"
    plt.title(title)
    plt.xlabel(xlabel)

    plt.ylabel(ylable)
    #fig = plt.gcf()
    #plot_url = py.plot_mpl(fig, filename='mpl-basic-histogram')
    #plt.plot(delay_list,norm.pdf(delay_list,0.4))
    #width = 0.7*(bins[1]-bins[0])
    #center = delay_list.mean()
    #plt.bar(center, hist, align = 'center', width = width)
    plt.bar(bins[:-1],hist,width=2)
    plt.show()


if __name__=='__main__':
    rpt_file = r'C:/parser_case/df_cs_umc_t_8.ft.nlc.tt0p65v.rpt'
    delay = icVar.floatNum
    arrive = icVar.floatNum

    input_delay = pp.Group("input external delay" + delay + arrive + icVar.toggleType)
    data_arr_pat = pp.Group("data arrival time" + arrive)
    pt_path = ''
    pt_path_list = []


    path_end = re.compile(r'slack ')
    for line in fi.input(rpt_file,openhook=fi.hook_compressed):
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
        #print('Waiting for all subprocesses done...')
        output = [pt.get() for pt in results]
        print output
        p.close()
        p.join()
        #print('All subprocesses done.')
        #print len(pt_path_list)
        plotList(output)