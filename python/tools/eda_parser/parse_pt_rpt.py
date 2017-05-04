#!/usr/bin/env python
import sys
import os
import shutil
import re
import gzip
import pyparsing as pp
import icVar as icVar

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
        self.icVar.pathType = []
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
        trans       = icVar.floatNumNum
        delay       = icVar.floatNumNum
        arrive      = icVar.floatNumNum
        cap         = icVar.floatNumNum
        factor      = icVar.floatNumNum
        sigma       = icVar.floatNumNum
        uncertainty = icVar.floatNumNum
        slack       = icVar.floatNumNum

        transZero  = icVar.floatNumZero
        delayZero  = icVar.floatNumZero
        fanout      = icVar.intNum

        netName    = icVar.hierName
        instName   = icVar.hierName
        pinName    = icVar.hierName
        clkName    = icVar.hierName

        icVar.toggleType       =  pp.Word("r" + "f" + "rise" + "fall")
        clockName        =  icVar.hierName
        
        sp_pat          = pp.Group("Startpoint" + icVar.COLON + instName + pp.delimitedList(icVar.paras) )
        ep_pat          = pp.Group("Endpoint" + icVar.COLON + instName + pp.delimitedList(icVar.paras)  )
        path_group_pat  = pp.Group("Path Group" + icVar.COLON + pp.delimitedList(icVar.paras))
        path_type_pat   = pp.Group("Path Type" + icVar.COLON + icVar.pathType)
        derate_pat      = pp.Group(icVar.pathType + "Timing Check Derating Factor" + icVar.COLON + factor )
        sigma_pat       = pp.Group("Sigma" + icVar.COLON +  sigma )
        column_pat      = pp.Group("Point"   + pp.OneOrMore(pathColumn))
        clk_pat         = pp.Group("clock"+ clkName + LPAR + icVar.toggleType + "edge" + RPAR + trans + delay + arrive)
        lch_clk_pin_pat = pp.Group(pinName + LPAR + lib_cell_name + RPAR + delay + icVar.annoType + arrive + icVar.toggleType)
        input_delay     = pp.Group("input external delay" + delay + arrive +icVar.toggleType)

        flat_pin_pat    = pp.Group(pinName+ LPAR + lib_cell_name + RPAR + trans + delay + pp.ZeroOrMore(icVar.annoType) + arrive + icVar.toggleType)
        flat_net_pat    = pp.Group(netName + LPAR + "net" + RPAR + fanout + cap)

        hier_pin_pat    = pp.Group(pinName + LPAR + moduleName + RPAR + transZero +  delayZero + pp.ZeroOrMore(icVar.annoType)+ arrive + icVar.toggleType)
        hier_net_pat    = pp.Group(netName + LPAR + "net" + RPAR)

        flat_io_pat     = pp.Group(pinName+ LPAR + pp.oneOf("in net out ") + RPAR + trans + delay + pp.ZeroOrMore(icVar.annoType) + arrive + icVar.toggleType)
        clk_uncer_pat   = pp.Group("clock uncertainty" + uncertainty + arrive)
        clk_nw_pat      = pp.Group("clock network delay" + LPAR + clkType + RPAR +  delay + arrive )
        crpr_pat        = pp.Group("clock reconvergence pessimism" + delay + arrive)
        cap_clk_pin_pat = pp.Group(pinName + LPAR + lib_cell_name + RPAR  + arrive + icVar.toggleType)
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
            icVar.dashLine +
            input_delay +
            data_path_pat+
            data_arr_pat +
            icVar.dashLine +
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
            #rs = icVar.dashLine.searchString(rpt_string)
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
                #self.icVar.pathType.append(self.rpt_list[i][0][3])
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
        trans       = icVar.floatNum
        delay       = icVar.floatNum
        arrive      = icVar.floatNum
        cap         = icVar.floatNum
        factor      = icVar.floatNum
        sigma       = icVar.floatNum
        uncertainty = icVar.floatNum
        slack       = icVar.floatNum

        transZero   = icVar.floatNumZero
        delayZero   = icVar.floatNumZero
        fanout      = icVar.intNum
        instName    = icVar.hierName
        netName     = icVar.hierName
        pinName     = icVar.hierName
        clkName     = icVar.hierName
        moduleName  = icVar.flatName        
        clockName     =  icVar.hierName
        
        sp_pat          = pp.Group("Startpoint" + icVar.COLON + instName + pp.delimitedList(icVar.paras) )
        ep_pat          = pp.Group("Endpoint" + icVar.COLON + instName + pp.delimitedList(icVar.paras) )
        path_group_pat  = pp.Group("Path Group" + icVar.COLON + clock_name )
        path_type_pat   = pp.Group("Path Type" + icVar.COLON + icVar.pathType)
        derate_pat      = pp.Group(icVar.pathType + "Timing Check Derating Factor" + icVar.COLON + factor )
        sigma_pat       = pp.Group("Sigma" + icVar.COLON +  sigma )
        column_pat      = pp.Group("Point"   + pp.OneOrMore(pathColumn))
        clk_pat         = pp.Group("clock"+ clkName + pp.delimitedList(icVar.paras) + trans + delay + arrive)
        lch_clk_pin_pat = pp.Group(pinName + pp.delimitedList(icVar.paras) + delay + icVar.annoType + arrive)

        flat_pin_pat    = pp.Group(pinName+ pp.delimitedList(icVar.paras) + trans + delay + pp.ZeroOrMore(icVar.annoType) + arrive + icVar.toggleType)
        flat_net_pat    = pp.Group(netName + pp.delimitedList(icVar.paras) + fanout + cap)

        hier_pin_pat    = pp.Group(pinName + pp.delimitedList(icVar.paras) + transZero +  delayZero + pp.ZeroOrMore(icVar.annoType)+ arrive + icVar.toggleType)
        hier_net_pat    = pp.Group(netName + pp.delimitedList(icVar.paras))

        clk_uncer_pat   = pp.Group("clock uncertainty" + uncertainty + arrive)
        clk_nw_pat      = pp.Group("clock network delay" + pp.delimitedList(icVar.paras) +  delay + arrive )
        crpr_pat        = pp.Group("clock reconvergence pessimism" + delay + arrive)
        cap_clk_pin_pat = pp.Group(pinName + pp.delimitedList(icVar.paras)  + arrive + icVar.toggleType)
        lib_setup_pat   = pp.Group("library setup time" + delay + arrive)
        data_req_pat    = pp.Group("data required time" + arrive)
        data_arr_pat    = pp.Group("data arrival time" + arrive)
        stat_adj_pat    = pp.Group("statistical adjustment" + delay + arrive)
        slack_pat       = pp.Group("slack" + pp.delimitedList(icVar.paras) + slack  )
        
        data_path_pat = pp.Group(pp.OneOrMore(flat_pin_pat | flat_net_pat | hier_net_pat |hier_pin_pat))
        pt_path_pat = pp.Group(
            sp_pat +
            ep_pat +
            path_group_pat +
            path_type_pat +
            derate_pat +
            sigma_pat +
            column_pat +
            icVar.dashLine +
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
            icVar.dashLine +
            data_req_pat +
            data_arr_pat +
            icVar.dashLine +
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
                #rs = icVar.dashLine.searchString(rpt_string)
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
                    self.icVar.pathType.append(self.rpt_list[i][0][3])
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
        qorHeader  = pp.Group("Report"   + icVar.COLON  + icVar.flatName +
                              "Design"   + icVar.COLON  + icVar.flatName +
                              "Version"  + icVar.COLON  + icVar.flatName +
                              "Date"     +  icVar.COLON + icVar.date +
                              icVar.starLine +
                              "Information: Timer using" + pp.delimitedList(icVar.squotes) + DOT  + pp.delimitedList(icVar.paras)
                             )
        sceTimGroup = pp.Group("Scenario" + pp.delimitedList(icVar.squotes) +
                               "Timing Path Group" + pp.delimitedList(icVar.squotes) +
                               icVar.dashLine +
                               "Levels of Logic" + icVar.COLON + icVar.intNum +
                                "Critical Path Length" + icVar.COLON + icVar.floatNum +
                                "Critical Path Slack" + icVar.COLON + icVar.floatNum +
                                "Critical Path Clk Period" + icVar.COLON + icVar.floatNum +
                                "Total Negative Slack" + icVar.COLON + icVar.floatNum +
                                "No. of Violating Paths" + icVar.COLON + icVar.intNum +
                                icVar.dashLine
                               )

        cellCount = pp.Group(
            "Cell Count" + icVar.dashLine +
            "Hierarchical Cell Count:" +icVar.intNum +
            "Hierarchical Port Count:" + icVar.intNum +
            "Leaf Cell Count:" + icVar.intNum +
            "Buf/Inv Cell Count:" + icVar.intNum +
            "Buf Cell Count:" + icVar.intNum +
            "Inv Cell Count:" + icVar.intNum +
            "CT Buf/Inv Cell Count:" + icVar.intNum +
            "Combinational Cell Count:" + icVar.intNum +
            "Sequential Cell Count:" + icVar.intNum +
            "Macro Count:" + icVar.intNum +
            icVar.dashLine
        )

        cellArea = pp.Group("Area" + icVar.dashLine +
            "Combinational Area:" + icVar.floatNum +
            "Noncombinational Area:" + icVar.floatNum +
            'Buf/Inv Area:' + icVar.floatNum +
            "Total Buffer Area:" + icVar.floatNum +
            "Total Inverter Area:" + icVar.floatNum +
            'Macro/Black Box Area:' + icVar.floatNum +
            "Net Area:" + icVar.floatNum +
            "Net XLength:" + icVar.floatNum +
            "Net YLength:" + icVar.floatNum +
            icVar.dashLine +
            'Cell Area (netlist):' + icVar.floatNum +
            'Cell Area (netlist and physical only):'     + icVar.floatNum +
            "Net Length:" + icVar.floatNum
        )

        designRule =pp.Group("Design Rules" +
                             icVar.dashLine +
                             "Total Number of Nets:" + icVar.intNum +
                             "Nets with Violations:" + icVar.intNum +
                             "Max Trans Violations:" + icVar.intNum +
                             "Max Cap Violations:"   + icVar.intNum +
                             icVar.dashLine)

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


