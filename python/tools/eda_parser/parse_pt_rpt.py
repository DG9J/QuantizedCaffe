#!/usr/bin/env python
import sys
import os
import shutil
import re
import gzip
import pyparsing as pp

class parse_pt_rpt():
    '''
        self.pt_rpt_file = pt_rpt_file
        self.rpt_list = []
        self.startpoint = []
        self.endpoint = []
        self.clock = []
        self.slack = []
        self.skew = []
        self.crpr = []
        self.launch_latency = []
        self.capture_latency = []
        self.length = []
        self.path_type = []
        self.max_derate_factor = []
        self.sigma = []
        self.column = []
        self.launch_clock = []
        self.capture_clock = []
        self.clk_network = []
        self.arrive_time = []
        self.uncertainty = []
        self.cap_clk_pin = []
        self.lib_setup = []
        self.data_req_time = []
        self.stat_adj = []
    '''

    def __init__ (self,pt_rpt_file):
        self.pt_rpt_file = pt_rpt_file
        self.rpt_list = []
        self.startpoint = []
        self.endpoint = []
        self.clock = []
        self.slack = []
        self.skew = []
        self.crpr = []
        self.launch_latency = []
        self.capture_latency = []
        self.length = []
        self.path_type = []
        self.max_derate_factor = []
        self.sigma = []
        self.column = []
        self.launch_clock = []
        self.capture_clock = []
        self.clk_network = []
        self.arrive_time = []
        self.uncertainty = []
        self.cap_clk_pin = []
        self.lib_setup = []
        self.data_req_time = []
        self.stat_adj = []

        print "init parse_pt_rpt"


    def read_pt_rpt(self):
        COLON, LBRACK, RBRACK, LBRACE, RBRACE, TILDE, CARAT = map(pp.Literal, ":[]{}~^")
        LPAR, RPAR = map(pp.Suppress, "()")
        float       = pp.Word(pp.nums+'.'+'-')
        trans       = float
        delay       = float
        arrive      = float
        cap         = float
        factor      = float
        sigma       = float
        uncertainty = float
        slack       = float

        float_zero  = pp.Word("0"+'.')
        trans_zero  = float_zero
        delay_zero  = float_zero

        integer     = pp.Word(pp.nums)
        fanout      = integer



        name_rule   = pp.Word(pp.alphanums+'/'+'_'+'['+']')
        inst_name   = name_rule
        net_name    = name_rule
        pin_name    = name_rule
        clk_name    = name_rule

        lib_cell_name   = pp.Word(pp.alphas.upper()+pp.nums+"_")
        module_name     = pp.Word(pp.alphanums +'_')
        carve           = pp.Word('-')


        toggle      =  pp.Word("r" + "f" + "rise" + "fall")
        pt_name_rule = pp.Word(pp.alphanums+"-")
        pt_char     =  pt_name_rule
        clock_name  =  pt_char
        path_type   =  pp.Word("min" + "max" + "Min" + "Max")
        path_column =  pp.Word("Fanout"+"Cap"+"Trans" + "Incr" + "Path")
        clk_type    =  pp.Word("ideal" + "propagated")
        annotate    =  pp.Word("&" + "*")


        sp_pat          = pp.Group("Startpoint" + COLON + inst_name + LPAR + pp.OneOrMore(pt_char)+RPAR )
        ep_pat          = pp.Group("Endpoint" + COLON + inst_name + LPAR + pp.OneOrMore(pt_char) +RPAR )
        path_group_pat  = pp.Group("Path Group" + COLON + clock_name )
        path_type_pat   = pp.Group("Path Type" + COLON + path_type)
        derate_pat      = pp.Group(path_type + "Timing Check Derating Factor" + COLON + factor )
        sigma_pat       = pp.Group("Sigma" + COLON +  sigma )
        column_pat      = pp.Group("Point"   + pp.OneOrMore(path_column))
        clk_pat         = pp.Group("clock"+ clk_name + LPAR + toggle + "edge" + RPAR + trans + delay + arrive)
        lch_clk_pin_pat = pp.Group(pin_name + LPAR + lib_cell_name + RPAR + delay + annotate + arrive)

        flat_pin_pat    = pp.Group(pin_name+ LPAR + lib_cell_name + RPAR + trans + delay + pp.ZeroOrMore(annotate) + arrive + toggle)
        flat_net_pat    = pp.Group(net_name + LPAR + "net" + RPAR + fanout + cap)

        hier_pin_pat    = pp.Group(pin_name + LPAR + module_name + RPAR + trans_zero +  delay_zero + pp.ZeroOrMore(annotate)+ arrive + toggle)
        hier_net_pat    = pp.Group(net_name + LPAR + "net" + RPAR)

        clk_uncer_pat   = pp.Group("clock uncertainty" + uncertainty + arrive)
        clk_nw_pat      = pp.Group("clock network delay" + LPAR + clk_type + RPAR +  delay + arrive )
        crpr_pat        = pp.Group("clock reconvergence pessimism" + delay + arrive)
        cap_clk_pin_pat = pp.Group(pin_name + LPAR + lib_cell_name + RPAR  + arrive + toggle)
        lib_setup_pat   = pp.Group("library setup time" + delay + arrive)
        data_req_pat    = pp.Group("data required time" + arrive)
        data_arr_pat    = pp.Group("data arrival time" + arrive)
        stat_adj_pat    = pp.Group("statistical adjustment" + delay + arrive)
        slack_pat       = pp.Group("slack" + LPAR +"VIOLATED" + RPAR + slack  )

        #data_path_pat = pp.Group(pp.OneOrMore(flat_pin_pat)+pp.ZeroOrMore(flat_net_pat)+ pp.ZeroOrMore(hier_net_pat)+pp.ZeroOrMore(hier_pin_pat))
        data_path_pat = pp.Group(pp.OneOrMore(flat_pin_pat | flat_net_pat | hier_net_pat |hier_pin_pat))

        pt_path_pat = pp.Group(
            sp_pat +
            ep_pat +
            path_group_pat +
            path_type_pat +
            derate_pat +
            sigma_pat +
            column_pat +
            carve +
            clk_pat +
            clk_nw_pat +
            data_path_pat +
            data_arr_pat +
            clk_pat +
            clk_nw_pat +
            crpr_pat +
            clk_uncer_pat +
            cap_clk_pin_pat +
            lib_setup_pat +
            data_req_pat +
            carve +
            data_req_pat +
            data_arr_pat +
            carve +
            stat_adj_pat +
            slack_pat
        )
        rpt_file = self.pt_rpt_file
        print rpt_file
        if os.path.isfile(rpt_file):
            if rpt_file.split(".")[-1] == "gz":
                gzipfile = gzip.open(rpt_file,'r')
                rpt_string  = gzipfile.read()
                #print  len(rpt_string)
                #result = sp_pat.searchString(rpt_string)
                #result = ep_pat.searchString(rpt_string)
                #result = path_group_pat.searchString(rpt_string)
                #result = path_type_pat.searchString(rpt_string)
                #result = derate_pat.searchString(rpt_string)
                #result = sigma_pat.searchString(rpt_string)
                #rs = column_pat.searchString(rpt_string)
                #rs = clk_pat.searchString(rpt_string)
                #rs = lch_clk_pin_pat.searchString(rpt_string)
                #rs = flat_pin_pat.searchString(rpt_string)
                #rs = flat_net_pat.searchString(rpt_string)
                #rs = hier_pin_pat.searchString(rpt_string)
                #rs = hier_net_pat.searchString(rpt_string)

                #rs = clk_uncer_pat.searchString(rpt_string)
                #rs = clk_nw_pat.searchString(rpt_string)
                #rs = crpr_pat.searchString(rpt_string)
                #rs = cap_clk_pin_pat.searchString(rpt_string)
                #rs= lib_setup_pat.searchString(rpt_string)
                #rs = data_req_pat.searchString(rpt_string)
                #rs = data_arr_pat.searchString(rpt_string)
                #rs = stat_adj_pat.searchString(rpt_string)
                #rs = slack_pat.searchString(rpt_string)
                #rs = data_path_pat.searchString(rpt_string)
                #pt_rpt_db = pt_path_pat.searchString(rpt_string)
                self.rpt_list = pt_path_pat.searchString(rpt_string)
                #rs = carve.searchString(rpt_string)
                #for i in range(0,len(rs[0][0])):
                #   print rs[0][0][i]
                #print len(rs[0])
                #print rs[1]
                #for i in range(0,len(result)):
                #    print sp_result[i][0][2]
                #print len(pt_rpt_db), len(pt_rpt_db[0]),len(pt_rpt_db[0][0])
                self.length =  len(self.rpt_list)
                for i in range(0, self.length):
                    self.startpoint.append(self.rpt_list[i][0][0][2])
                    self.endpoint.append(self.rpt_list[i][0][1][2])
                    self.clock.append(self.rpt_list[i][0][2][2])
                    self.path_type.append(self.rpt_list[i][0][3])
                    self.max_derate_factor.append(self.rpt_list[i][0][4][3])
                    self.sigma.append(self.rpt_list[i][0][5][2])
                    self.column.append(self.rpt_list[i][0][6])
                    self.launch_clock.append(self.rpt_list[i][0][8][1])
                    self.clk_network.append(self.rpt_list[i][0][9][1])
                    self.arrive_time.append(self.rpt_list[i][0][11][1])
                    self.capture_clock.append(self.rpt_list[i][0][12][1])
                    self.crpr.append(self.rpt_list[i][0][14][1])
                    self.uncertainty.append(self.rpt_list[i][0][15][1])
                    self.cap_clk_pin.append(self.rpt_list[i][0][16][0])
                    self.lib_setup.append(self.rpt_list[i][0][17][1])
                    self.data_req_time.append(self.rpt_list[i][0][18][1])
                    self.stat_adj.append(self.rpt_list[i][0][23][1])
                    self.slack.append(self.rpt_list[i][0][2])




                    #print self.rpt_list[i][0][24]

                return self.rpt_list






