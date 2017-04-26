#!/usr/bin/env python

import sys
import os
import shutil
import re
import gzip
import datetime
import parse_def as p_def
import parse_pt_rpt as p_pt_rpt



def main():
    ##regression pt report
    #rpt_file = "fullchip.df_tcdx_t14.df_cs_umc_t8.sorted.gz"
    #rpt_file = "fullchip.umc_umcch_t100.df_cs_umc_t8.sorted.gz"
    #print "start time", datetime.datetime.now()
    #pt_rpt = p_pt_rpt.parse_pt_rpt(rpt_file)
    #print "end  time", datetime.datetime.now()

    #regression DEF parsing
    #def_file = r'D:/AMD/parser_case/Place.def'
    #def_fp = p_def.parse_def(def_file)
    #print "start time", datetime.datetime.now()
    #print def_fp.read_def()
    #print "start time", datetime.datetime.now()

    #regression icc qor parsing
    rpt_file =  "/proj/ariel_pd_vol38/yaguo/df_tcdx_t16/main/pd/tiles/df_tcdxd_t_16_r1_buf_org3_TileBuilder_Apr10_2238_13535_GUI/rpts/I2Place/qor.rpt.gz"
    icc_qor  =  p_pt_rpt.parse_icc_qor(rpt_file)


if __name__ == '__main__':
    main()