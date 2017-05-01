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
    ##regression pt report
    #rpt_file = "fullchip.df_tcdx_t14.df_cs_umc_t8.sorted.gz"
    #rpt_file = "fullchip.umc_umcch_t100.df_cs_umc_t8.sorted.gz"
    #print "start time", datetime.datetime.now()
    #pt_rpt = p_pt_rpt.parse_pt_rpt(rpt_file)
    #print "end  time", datetime.datetime.now()

    ##regression pt report
    rpt_file = "fullchip.df_tcdx_t14.df_cs_umc_t8.sorted.gz"
    rpt_file = "fullchip.umc_umcch_t100.df_cs_umc_t8.sorted.gz"
    rpt_file = "/home/yaguo/ariel/df_tcdxd_t_16.ft.tt0p9v.rpt"
    #rpt_file = "/proj/ariel_pd_vol38/yaguo/df_tcdx_t16/main/pd/tiles/df_tcdxd_t_16_r1_buf_test3_1_TileBuilder_Apr10_2238_13535_GUI/df_tcdxd_t_16.ft.tt0p9v.rpt.small"
    #print "start time", datetime.datetime.now()
    p_pt_rpt = rpt.ptRpt(rpt_file)
    p_pt_rpt.read_ft_uncons()
    #print "end  time", datetime.datetime.now()
    #print p_pt_rpt.startpoint[0], p_pt_rpt.endpoint[0] , p_pt_rpt.arrive_time[0]


    delay_list =   np.array(p_pt_rpt.arrive_time).astype(np.float)
    #delay_list =   p_pt_rpt.arrive_time
    sum_delay = np.sum(delay_list)
    print delay_list.sum(),delay_list.max(),delay_list.min(),delay_list.mean()
    print delay_list

    bins = [delay_list.min(),delay_list.max()]
    uvals = np.unique(delay_list+[10,])
    hist ,bins  = np.histogram(delay_list, bins=uvals)

    gaussian_numbers = np.asarray(delay_list)
    #plt.hist(gaussian_numbers)
    delay_avg = float("{0:.2f}".format(delay_list.mean()))
    delay_max = float("{0:.2f}".format(delay_list.max()))
    delay_min = float("{0:.2f}".format(delay_list.min()))
    xlabel = "Delay(avg="+ str(delay_avg)+"max=" + str(delay_max) + "min=" + str(delay_min)+")"
    ylable = "Count(" + str(len(delay_list))+ ")"
    plt.title("df_tcdxd_t16")
    plt.xlabel(xlabel)

    plt.ylabel(ylable)
    #fig = plt.gcf()
    #plot_url = py.plot_mpl(fig, filename='mpl-basic-histogram')
    #plt.plot(delay_list,norm.pdf(delay_list,0.4))
    #width = 0.7*(bins[1]-bins[0])
    #center = delay_list.mean()
    #plt.bar(center, hist, align = 'center', width = width)
    plt.bar(bins[:-1],hist,width=np.diff(bins))
    plt.show()


    #xbins=range(0,len(delay_list))
    #plt.hist(delay_list,bins=xbins)
    #plt.title("Gaussian Histogram")
    #plt.xlabel("Value")
    #plt.ylabel("Frequency")
    #plt.show()

    #fig = plt.gcf()

    #plot_url = py.plot_mpl(fig, filename='mpl-basic-histogram')
    #regression DEF parsing
    #def_file = r'D:/AMD/parser_case/Place.def'
    #def_fp = p_def.parse_def(def_file)
    #print "start time", datetime.datetime.now()
    #print def_fp.read_def()
    #print "start time", datetime.datetime.now()

    #regression icc qor parsing

    #basRunDir = "/proj/ariel_pd_vol38/yaguo/df_tcdx_t16/main/pd/tiles/"
    #basNickName = "r1_buf_org3"
    #
    #refRunDir = "/proj/ariel_pd_vol38/yaguo/df_tcdx_t16/main/pd/tiles/"
    #refNickNmae = "r1_buf_test3_1"
    #
    #stageRpt = "/rpts/I2ReRoute/qor.rpt.gz"
    #
    #basRptFile =  basRunDir + basNickName + stageRpt
    #refRptFile =refRunDir + refNickNmae + stageRpt
    #
    #basIccQor  =  rpt.iccQor(basRptFile)
    #basIccQor.read_icc_qor()
    #
    #refIccQor   =  rpt.iccQor(refRptFile)
    #refIccQor.read_icc_qor()
    #
    #print basNickName,basIccQor.criticalData()
    #print refNickNmae,refIccQor.criticalData()


if __name__ == '__main__':
    main()