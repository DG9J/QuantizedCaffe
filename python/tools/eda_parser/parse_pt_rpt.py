#!/usr/bin/env python
import sys
import os
import shutil
import re
import gzip
import pyparsing as pp
import icComVar

class ptRpt():
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

    def read_ft_uncons(self):
        trans       = icComVar.floatNumNum
        delay       = icComVar.floatNumNum
        arrive      = icComVar.floatNumNum
        cap         = icComVar.floatNumNum
        factor      = icComVar.floatNumNum
        sigma       = icComVar.floatNumNum
        uncertainty = icComVar.floatNumNum
        slack       = icComVar.floatNumNum

        transZero  = icComVar.floatNumZero
        delayZero  = icComVar.floatNumZero
        fanout      = icComVar.intNum

        instName   = self.hierName
        netName    = self.hierName
        pinName    = self.hierName
        clkName    = self.hierName

        toggleType       =  pp.Word("r" + "f" + "rise" + "fall")
        clockName        =  self.hierName
        
        sp_pat          = pp.Group("Startpoint" + icComVar.COLON + instName + LPAR + pp.OneOrMore(clockName)+RPAR )
        ep_pat          = pp.Group("Endpoint" + icComVar.COLON + instName + LPAR + pp.OneOrMore(clockName) +RPAR )
        path_group_pat  = pp.Group("Path Group" + icComVar.COLON + LPAR + clock_name  + RPAR)
        path_type_pat   = pp.Group("Path Type" + icComVar.COLON + path_type)
        derate_pat      = pp.Group(path_type + "Timing Check Derating Factor" + icComVar.COLON + factor )
        sigma_pat       = pp.Group("Sigma" + icComVar.COLON +  sigma )
        column_pat      = pp.Group("Point"   + pp.OneOrMore(path_column))
        clk_pat         = pp.Group("clock"+ clkName + LPAR + toggleType + "edge" + RPAR + trans + delay + arrive)
        lch_clk_pin_pat = pp.Group(pinName + LPAR + lib_cell_name + RPAR + delay + annoType + arrive + toggleType)
        input_delay     = pp.Group("input external delay" + delay + arrive +toggleType)

        flat_pin_pat    = pp.Group(pinName+ LPAR + lib_cell_name + RPAR + trans + delay + pp.ZeroOrMore(annoType) + arrive + toggleType)
        flat_net_pat    = pp.Group(netName + LPAR + "net" + RPAR + fanout + cap)

        hier_pin_pat    = pp.Group(pinName + LPAR + moduleName + RPAR + transZero +  delayZero + pp.ZeroOrMore(annoType)+ arrive + toggleType)
        hier_net_pat    = pp.Group(netName + LPAR + "net" + RPAR)

        flat_io_pat     = pp.Group(pinName+ LPAR + pp.oneOf("in net out ") + RPAR + trans + delay + pp.ZeroOrMore(annoType) + arrive + toggleType)
        clk_uncer_pat   = pp.Group("clock uncertainty" + uncertainty + arrive)
        clk_nw_pat      = pp.Group("clock network delay" + LPAR + clkType + RPAR +  delay + arrive )
        crpr_pat        = pp.Group("clock reconvergence pessimism" + delay + arrive)
        cap_clk_pin_pat = pp.Group(pinName + LPAR + lib_cell_name + RPAR  + arrive + toggleType)
        lib_setup_pat   = pp.Group("library setup time" + delay + arrive)
        data_req_pat    = pp.Group("data required time" + arrive)
        data_arr_pat    = pp.Group("data arrival time" + arrive)
        stat_adj_pat    = pp.Group("statistical adjustment" + delay + arrive)
        slack_pat       = pp.Group("slack" + LPAR +"VIOLATED" + RPAR + slack  )
        unconst_path    = pp.Group(LPAR + "Path is unconstrained" + RPAR)
       
        data_path_pat = pp.Group(pp.OneOrMore(flat_pin_pat | flat_net_pat |flat_io_pat | hier_net_pat |hier_pin_pat))

        pt_path_pat = pp.Group(
            sp_pat +
            ep_pat +
            path_group_pat+
            path_type_pat +
            derate_pat +
            sigma_pat +
            column_pat +
            icComVar.dashLine +
            input_delay +
            data_path_pat+
            data_arr_pat +
            icComVar.dashLine +
            unconst_path
        )
        rpt_file = self.pt_rpt_file
        print rpt_file
        if os.path.isfile(rpt_file):
            if rpt_file.split(".")[-1] == "gz":
                gzipfile = gzip.open(rpt_file,'r')
                rpt_string  = gzipfile.read()
            else:
                file  = open(rpt_file,"r")
                rpt_string = file.read()

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
            #print rs[0][0][-1]
            #return
            #print "aa"
            #pt_rpt_db = pt_path_pat.searchString(rpt_string)
            self.rpt_list = pt_path_pat.searchString(rpt_string)
            #print      self.rpt_list
            #return
            #rs = icComVar.dashLine.searchString(rpt_string)
            #for i in range(0,len(rs[0][0])):
            #   print rs[0][0][i]
            #print len(rs[0])
            #print rs[1]
            #for i in range(0,len(result)):
            #    print sp_result[i][0][2]
            #print len(pt_rpt_db), len(pt_rpt_db[0]),len(pt_rpt_db[0][0])
            self.length =  len(self.rpt_list)
            for i in range(0, self.length):
                #print self.rpt_list[i][0][-3][-1]
                self.startpoint.append(self.rpt_list[i][0][0][2])
                self.endpoint.append(self.rpt_list[i][0][1][2])
                self.arrive_time.append(self.rpt_list[i][0][-3][-1])

                #self.clock.append(self.rpt_list[i][0][2][2])
                #self.path_type.append(self.rpt_list[i][0][3])
                #self.max_derate_factor.append(self.rpt_list[i][0][4][3])
                #self.sigma.append(self.rpt_list[i][0][5][2])
                #self.column.append(self.rpt_list[i][0][6])
                #self.launch_clock.append(self.rpt_list[i][0][8][1])
                #self.clk_network.append(self.rpt_list[i][0][9][1])
                #self.arrive_time.append(self.rpt_list[i][0][11][1])
                #self.capture_clock.append(self.rpt_list[i][0][12][1])
                #self.crpr.append(self.rpt_list[i][0][14][1])
                #self.uncertainty.append(self.rpt_list[i][0][15][1])
                #self.cap_clk_pin.append(self.rpt_list[i][0][16][0])
                #self.lib_setup.append(self.rpt_list[i][0][17][1])
                #self.data_req_time.append(self.rpt_list[i][0][18][1])
                #self.stat_adj.append(self.rpt_list[i][0][23][1])
                #self.slack.append(self.rpt_list[i][0][2])




                #print self.rpt_list[i][0][24]

            return self.rpt_list



    def readPtRpt(self):
        trans       = self.icComVar.floatNum
        delay       = self.icComVar.floatNum
        arrive      = self.icComVar.floatNum
        cap         = self.icComVar.floatNum
        factor      = self.icComVar.floatNum
        sigma       = self.icComVar.floatNum
        uncertainty = self.icComVar.floatNum
        slack       = self.icComVar.floatNum

        transZero   = self.icComVar.floatNumZero
        delayZero   = self.icComVar.floatNumZero
        fanout      = self.int
        instName    = self.hierName
        netName     = self.hierName
        pinName     = self.hierName
        clkName     = self.hierName
        moduleName  = self.flatName
        
        clockName     =  pt_self.hierName
        
        path_column =  pp.Word("Fanout"+"Cap"+"Trans" + "Incr" + "Path")
        clkType    =  pp.Word("ideal" + "propagated")
        annoType    =  pp.Word("&" + "*")


        sp_pat          = pp.Group("Startpoint" + icComVar.COLON + instName + pp.delimitedList(paraQuoteSting) )
        ep_pat          = pp.Group("Endpoint" + icComVar.COLON + instName + pp.delimitedList(paraQuoteSting) )
        path_group_pat  = pp.Group("Path Group" + icComVar.COLON + clock_name )
        path_type_pat   = pp.Group("Path Type" + icComVar.COLON + path_type)
        derate_pat      = pp.Group(path_type + "Timing Check Derating Factor" + icComVar.COLON + factor )
        sigma_pat       = pp.Group("Sigma" + icComVar.COLON +  sigma )
        column_pat      = pp.Group("Point"   + pp.OneOrMore(path_column))
        clk_pat         = pp.Group("clock"+ clkName + pp.delimitedList(paraQuoteSting) + trans + delay + arrive)
        lch_clk_pin_pat = pp.Group(pinName + LPAR + lib_cell_name + RPAR + delay + annoType + arrive)

        flat_pin_pat    = pp.Group(pinName+ pp.delimitedList(paraQuoteSting) + trans + delay + pp.ZeroOrMore(annoType) + arrive + toggleType)
        flat_net_pat    = pp.Group(netName + pp.delimitedList(paraQuoteSting) + fanout + cap)

        hier_pin_pat    = pp.Group(pinName + pp.delimitedList(paraQuoteSting) + transZero +  delayZero + pp.ZeroOrMore(annoType)+ arrive + toggleType)
        hier_net_pat    = pp.Group(netName + pp.delimitedList(paraQuoteSting))

        clk_uncer_pat   = pp.Group("clock uncertainty" + uncertainty + arrive)
        clk_nw_pat      = pp.Group("clock network delay" + pp.delimitedList(paraQuoteSting) +  delay + arrive )
        crpr_pat        = pp.Group("clock reconvergence pessimism" + delay + arrive)
        cap_clk_pin_pat = pp.Group(pinName + pp.delimitedList(paraQuoteSting)  + arrive + toggleType)
        lib_setup_pat   = pp.Group("library setup time" + delay + arrive)
        data_req_pat    = pp.Group("data required time" + arrive)
        data_arr_pat    = pp.Group("data arrival time" + arrive)
        stat_adj_pat    = pp.Group("statistical adjustment" + delay + arrive)
        slack_pat       = pp.Group("slack" + pp.delimitedList(paraQuoteSting) + slack  )
        
        data_path_pat = pp.Group(pp.OneOrMore(flat_pin_pat | flat_net_pat | hier_net_pat |hier_pin_pat))
        pt_path_pat = pp.Group(
            sp_pat +
            ep_pat +
            path_group_pat +
            path_type_pat +
            derate_pat +
            sigma_pat +
            column_pat +
            icComVar.dashLine +
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
            icComVar.dashLine +
            data_req_pat +
            data_arr_pat +
            icComVar.dashLine +
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
                #rs = icComVar.dashLine.searchString(rpt_string)
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


class iccQor():
    def __init__(self, qor_file):
        self.qor_file = qor_file
        self.qorAll = []
        print "parsing" , self.qor_file

    def read_icc_qor(self):        
        qorHeader  = pp.Group("Report"   + icComVar.COLON  + icComVar.flatName +
                              "Design"   + icComVar.COLON  + icComVar.flatName +
                              "Version"  + icComVar.COLON  + icComVar.flatName +
                              "Date"     +  icComVar.COLON + icComVar.date +
                              icComVar.starLine +
                              "Information: Timer using" + pp.delimitedList(icComVar.sQuoteString) + DOT  + pp.delimitedList(paraQuoteSting)
                             )
        sceTimGroup = pp.Group("Scenario" + pp.delimitedList(icComVar.sQuoteString) +
                               "Timing Path Group" + pp.delimitedList(icComVar.sQuoteString) +
                               icComVar.dashLine +
                               "Levels of Logic" + icComVar.COLON + icComVar.intNum +
                                "Critical Path Length" + icComVar.COLON + icComVar.floatNum +
                                "Critical Path Slack" + icComVar.COLON + icComVar.floatNum +
                                "Critical Path Clk Period" + icComVar.COLON + icComVar.floatNum +
                                "Total Negative Slack" + icComVar.COLON + icComVar.floatNum +
                                "No. of Violating Paths" + icComVar.COLON + icComVar.intNum +
                                icComVar.dashLine
                               )

        cellCount = pp.Group(
            "Cell Count" + icComVar.dashLine +
            "Hierarchical Cell Count:" +icComVar.intNum +
            "Hierarchical Port Count:" + icComVar.intNum +
            "Leaf Cell Count:" + icComVar.intNum +
            "Buf/Inv Cell Count:" + icComVar.intNum +
            "Buf Cell Count:" + icComVar.intNum +
            "Inv Cell Count:" + icComVar.intNum +
            "CT Buf/Inv Cell Count:" + icComVar.intNum +
            "Combinational Cell Count:" + icComVar.intNum +
            "Sequential Cell Count:" + icComVar.intNum +
            "Macro Count:" + icComVar.intNum +
            icComVar.dashLine
        )

        cellArea = pp.Group("Area" + icComVar.dashLine +
            "Combinational Area:" + icComVar.floatNum +
            "Noncombinational Area:" + icComVar.floatNum +
            'Buf/Inv Area:' + icComVar.floatNum +
            "Total Buffer Area:" + icComVar.floatNum +
            "Total Inverter Area:" + icComVar.floatNum +
            'Macro/Black Box Area:' + icComVar.floatNum +
            "Net Area:" + icComVar.floatNum +
            "Net XLength:" + icComVar.floatNum +
            "Net YLength:" + icComVar.floatNum +
            icComVar.dashLine +
            'Cell Area (netlist):' + icComVar.floatNum +
            'Cell Area (netlist and physical only):'     + icComVar.floatNum +
            "Net Length:" + icComVar.floatNum
        )

        designRule =pp.Group("Design Rules" +
                             icComVar.dashLine +
                             "Total Number of Nets:" + icComVar.intNum +
                             "Nets with Violations:" + icComVar.intNum +
                             "Max Trans Violations:" + icComVar.intNum +
                             "Max Cap Violations:"   + icComVar.intNum +
                             icComVar.dashLine)

        qorAll = pp.Group(qorHeader +
                         pp.OneOrMore(sceTimGroup) +
                         cellCount +
                         cellArea +
                         designRule)

        rpt_file = self.qor_file
        # print rpt_file
        if os.path.isfile(rpt_file):
            if rpt_file.split(".")[-1] == "gz":
                file = gzip.open(rpt_file, 'r')
            else:
                file = open(rpt_file,"r")
            rpt_string = file.read()
            #rst = designName.searchString(rpt_string)
            #rst = iccVersion.searchString(rpt_string)
            #rst = writeDate.searchString(rpt_string)
            #rst =  cellCount.searchString(rpt_string)
            #rst = cellArea.searchString(rpt_string)
            #rst = designRule.searchString(rpt_string)
            #print rpt_string
            #rst = designName.searchString(rpt_string)
            #print rst
            #rst = sceTimGroup.searchString(rpt_string)                                                                                                          9
            #rst =qorHeader.searchString(rpt_string)
            #rst = timer.searchString(rpt_string)
            self.qorAll = qorAll.searchString(rpt_string)
            #print rst
            #for i in range(0,len(rst)):
            #    print rst[i]

    def criticalData(self):
        timeData = []
        timeData.append(self.qorAll[0][0][3][1])
        timeData.append(self.qorAll[0][0][3][3])
        timeData.append(self.qorAll[0][0][3][9])
        timeData.append(self.qorAll[0][0][3][11])
        timeData.append(self.qorAll[0][0][3][13])
        #timeData.append(self.qorAll[0][0][3])
        return timeData


