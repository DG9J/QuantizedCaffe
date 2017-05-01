#!/usr/bin/env python

import sys
import os
import shutil
import re
import gzip
import datetime
import parse_def as p_def
import parse_pt_rpt as rpt
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm


def main():


    ft_delay_file = "/home/yaguo/ariel/df_cs_umc_t8.ft.tt0p65v.delay.list"
    title = "honrizontal tt0p65v 100um"

    #ft_delay_file = "/home/yaguo/ariel/df_cs_umc_t8.ft.tt0p9v.delay.list"
    #title = "honrizontal tt0p9v 100um"

    #ft_delay_file = "/home/yaguo/ariel/df_tcdxd_t_16.ft.tt0p9v.delay.list"
    #title = "vertical tt0p9v 100um"

    #ft_delay_file = "/home/yaguo/ariel/df_tcdxd_t_16.ft.tt0p65v.delay.list"
    #title = "vertical tt0p65v 100um"
    with open(ft_delay_file) as f:
        lines = f.read().splitlines()
    delay_list =   np.array(lines).astype(np.float)

    #print delay_list.sum(),delay_list.max(),delay_list.min(),delay_list.mean()
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

if __name__ == '__main__':
    main()