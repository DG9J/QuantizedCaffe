!/usr/bin/env python

from __future__ import print_function
import sys
import os
import shutil
import re
import gzip

#!/usr/bin/env python

import sys
import os
import shutil
import re
import gzip
import glob


def main():
    copy_tile_def()

def copy_tile_def():
    Files = glob.glob('/proj/unb_scratch_6/ariel/04092017_tcdx/main/pd/tiles/df_*_DEF/data/Synthesize.placed.def.gz')
    Files = glob.glob('/proj/unb_scratch_6/ariel/04092017_tcdx/main/pd/tiles/df_*_DEF/data/Synthesize.v.gz')
    Files = glob.glob('/proj/ariel_pd_vol97/yaguo/DF_TILES/defs_NLC3/*.def.gz')
    Files = glob.glob('/proj/unb_scratch_6/ariel/04042017_soc/main/pd/tiles/df_*ariel_preNLA_TileBuilder_Apr04_1748_22453_ariel_regression/data/Synthesize.v.gz')
    for f in Files:
        tileFile =  f.split('/')[8]
        regex = re.compile(r'(\S+)_ariel_preNLA_TileBuilder_Apr04_1748_22453_ariel_regression')
        match = regex.search(tileFile)
        if match:
            tileName =  match.group(1)
        tilePath = "/proj/ariel_pd_vol97/yaguo/DF_TILES/NLC/" + tileName
        #print tileName, tileFile, f
        #file = f.split('/')[-1]
        if not os.path.exists(tilePath):
            os.makedirs(tilePath)
        #new_f = tile + "/" + file
        new_f  = tilePath + "/Synthesize.v.gz"
        shutil.copy2(f,new_f)
        print new_f , f

def run_df():
    rls_dir = '/proj/ariel/a0/tile_misc/rundir_link/W14_20170403_fp01/'
    rt_rpt = '/rpts/I2Route/'
    short_dir = '/home/yaguo/ariel/short/'
    drc_sum = '/home/yaguo/ariel/short/drc_sum.csv'
    f_drc_sum = open(drc_sum,'w')

    for tn in os.listdir(rls_dir):
        tm = re.compile(r"^df_")
        if tm.match(tn):
            drc = {'short': 0, 'spacing' : 0 , 'total' : 0 }
            #rpt_file = 'short.png'
            #rpt_file_path = rls_dir+tn+rt_rpt+rpt_file
            #new_png = short_dir+tn+'_'+'shorts.png'
            #if os.path.isfile(rpt_file_path):
            #    shutil.copy2(rpt_file_path ,new_png)
            #else:
            #    print rpt_file_path

            rpt_file = 'icc2_drc.rpt.gz'
            rpt_file_path = rls_dir + tn + rt_rpt + rpt_file
            if os.path.isfile(rpt_file_path):
                #print rpt_file_path
                gfile = gzip.open(rpt_file_path,'r')
                for line in gfile:
                    ##match DRC: total , short+ spacing
                    regex = re.compile(r'\S+\s+VIOLATIONS\s+=\s+(\d+)')
                    match = regex.search(line)
                    if match:
                        drc['total'] = match.group(1)

                    regex = re.compile(r'Short\s+\:\s+(\d+)')
                    match = regex.search(line)
                    if match:
                        drc['short'] = int(match.group(1))

                    regex = re.compile(r'Diff net spacing\s+\:\s+(\d+)')
                    match = regex.search(line)
                    if match:
                        drc['spacing'] = int(match.group(1))
            #else:
            #    print rpt_file_path
            #print(tn,',', drc['total'],',', drc['spacing']+drc['short'],file=f_drc_sum)
            #f_drc_sum.write(tn,drc['total'], drc['spacing']+drc['short'])
    f_drc_sum.close()

if __name__ == '__main__':
    main()
