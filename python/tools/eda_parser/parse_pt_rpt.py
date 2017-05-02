#!/usr/bin/env python
import sys
import os
import shutil
import re
import gzip
import pyparsing as pp

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
        trans       = floatNum
        delay       = floatNum
        arrive      = floatNum
        cap         = floatNum
        factor      = floatNum
        sigma       = floatNum
        uncertainty = floatNum
        slack       = floatNum

        transZero  = floatZero
        delayZero  = floatZero
        fanout      = intNum

        instName   = self.hierName
        netName    = self.hierName
        pinName    = self.hierName
        clkName    = self.hierName

        toggleType       =  pp.Word("r" + "f" + "rise" + "fall")
        clockName        =  self.hierName
        
        sp_pat          = pp.Group("Startpoint" + COLON + instName + LPAR + pp.OneOrMore(clockName)+RPAR )
        ep_pat          = pp.Group("Endpoint" + COLON + instName + LPAR + pp.OneOrMore(clockName) +RPAR )
        path_group_pat  = pp.Group("Path Group" + COLON + LPAR + clock_name  + RPAR)
        path_type_pat   = pp.Group("Path Type" + COLON + path_type)
        derate_pat      = pp.Group(path_type + "Timing Check Derating Factor" + COLON + factor )
        sigma_pat       = pp.Group("Sigma" + COLON +  sigma )
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
            self.dashLine +
            input_delay +
            data_path_pat+
            data_arr_pat +
            self.dashLine +
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
            #rs = self.dashLine.searchString(rpt_string)
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
        trans       = self.float
        delay       = self.float
        arrive      = self.float
        cap         = self.float
        factor      = self.float
        sigma       = self.float
        uncertainty = self.float
        slack       = self.float

        transZero   = self.floatZero
        delayZero   = self.floatZero
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


        sp_pat          = pp.Group("Startpoint" + COLON + instName + LPAR + pp.OneOrMore(clockName)+RPAR )
        ep_pat          = pp.Group("Endpoint" + COLON + instName + LPAR + pp.OneOrMore(clockName) +RPAR )
        path_group_pat  = pp.Group("Path Group" + COLON + clock_name )
        path_type_pat   = pp.Group("Path Type" + COLON + path_type)
        derate_pat      = pp.Group(path_type + "Timing Check Derating Factor" + COLON + factor )
        sigma_pat       = pp.Group("Sigma" + COLON +  sigma )
        column_pat      = pp.Group("Point"   + pp.OneOrMore(path_column))
        clk_pat         = pp.Group("clock"+ clkName + LPAR + toggleType + "edge" + RPAR + trans + delay + arrive)
        lch_clk_pin_pat = pp.Group(pinName + LPAR + lib_cell_name + RPAR + delay + annoType + arrive)

        flat_pin_pat    = pp.Group(pinName+ LPAR + lib_cell_name + RPAR + trans + delay + pp.ZeroOrMore(annoType) + arrive + toggleType)
        flat_net_pat    = pp.Group(netName + LPAR + "net" + RPAR + fanout + cap)

        hier_pin_pat    = pp.Group(pinName + LPAR + moduleName + RPAR + transZero +  delayZero + pp.ZeroOrMore(annoType)+ arrive + toggleType)
        hier_net_pat    = pp.Group(netName + LPAR + "net" + RPAR)

        clk_uncer_pat   = pp.Group("clock uncertainty" + uncertainty + arrive)
        clk_nw_pat      = pp.Group("clock network delay" + LPAR + clkType + RPAR +  delay + arrive )
        crpr_pat        = pp.Group("clock reconvergence pessimism" + delay + arrive)
        cap_clk_pin_pat = pp.Group(pinName + LPAR + lib_cell_name + RPAR  + arrive + toggleType)
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
            self.dashLine +
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
            self.dashLine +
            data_req_pat +
            data_arr_pat +
            self.dashLine +
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
                #rs = self.dashLine.searchString(rpt_string)
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


class iccQor:
    def __init__(self, qor_file):
        self.qor_file = qor_file
        self.qorAll = []
        print "parsing" , self.qor_file

    def read_icc_qor(self):
        LBRACK, RBRACK, LBRACE, RBRACE, TILDE, CARAT,COMMA = map(pp.Literal, "[]{}~^,")
        UNDERSCORE,  BSLASH, SLASH = map(pp.Literal, '_/\\')
        PLUS, DASH ,COLON,DOT = map(pp.Suppress, "+-:.")
        LPAR, RPAR = map(pp.Suppress, "()")
        SEMICOLON, DQUOTA = map(pp.Suppress, ';"')
        SQUOTA,DQUOTA = map(pp.Suppress, "\'\"")
        STAR = map(pp.Literal,'*')


        float = pp.Word(pp.nums + '.' + "_" + '-')
        integer = pp.Word(pp.nums + '-')
        flatName = pp.Word(pp.alphanums + "_"+"-" + '.')
        hierName = pp.Word(pp.alphanums + '/' + '_' + '[' + ']')
        pathGroupName = pp.Word(pp.alphanums+'\*' + '_' + "'")
        scenarioName = pp.Word(pp.alphanums + "_" + "'")
        date = pp.Word(pp.alphanums + " " + ":")

        sQuoteString = pp.QuotedString("'")
        dQuoteString = pp.QuotedString('"')
        starQuoteString = pp.QuotedString('*')
        eqQuoteString = pp.QuotedString('=')
        paraQuoteSting = pp.QuotedString('(', endQuoteChar=')')
        tildeQuoteString = pp.QuotedString('~')
        angleQuoteString = pp.QuotedString('<', endQuoteChar='>')



        designName = pp.Group("Design" + COLON + flatName)

        #qorHeader = pp.Group("Report" + COLON + flatName +
        #                    "Design" + COLON + flatName +
        #                    "Version" + COLON + flatName +
        #                    "Date" + COLON + date +
        #                    starLine +
        #                    "Information: Timer using" + pp.delimitedList(sQuoteString) + DOT  + pp.delimitedList(paraQuoteSting)
        #                     )
        qorHeader = pp.Group("Report" + COLON + flatName +
                            "Design" + COLON + flatName +
                            "Version" + COLON + flatName +
                            "Date" + COLON + date +
                            starLine +
                            "Information: Timer using" + pp.delimitedList(sQuoteString) + DOT  + pp.delimitedList(paraQuoteSting)
                             )

        designName = pp.Group("Design" + COLON + flatName)
        iccVersion = pp.Group("Version" + COLON + flatName)
        writeDate  = pp.Group("Date" + COLON + date)
        timer  = pp.Group("Information" + COLON + "Timer using" + pp.delimitedList(sQuoteString) + DOT  + pp.delimitedList(paraQuoteSting) )
        #timer  = pp.Group(pp.delimitedList(paraQuoteSting))
        #timer = pp.Group(pp.delimitedList(sQuoteString))
        #timerType = pp.Group("Design" + COLON + flatName)



        sceTimGroup = pp.Group("Scenario" +pp.delimitedList(sQuoteString) +
                               "Timing Path Group" + pp.delimitedList(sQuoteString) +
                               self.dashLine +
                               "Levels of Logic" + COLON + integer +
                                "Critical Path Length" + COLON + float +
                                "Critical Path Slack" + COLON + float +
                                "Critical Path Clk Period" + COLON + float +
                                "Total Negative Slack" + COLON + float +
                                "No. of Violating Paths" + COLON + integer +
                                self.dashLine
                               )

        cellCount = pp.Group(
            "Cell Count" + self.dashLine +
            "Hierarchical Cell Count:" +integer +
            "Hierarchical Port Count:" + integer +
            "Leaf Cell Count:" + integer +
            "Buf/Inv Cell Count:" + integer +
            "Buf Cell Count:" + integer +
            "Inv Cell Count:" + integer +
            "CT Buf/Inv Cell Count:" + integer +
            "Combinational Cell Count:" + integer +
            "Sequential Cell Count:" + integer +
            "Macro Count:" + integer +
            self.dashLine
        )

        cellArea = pp.Group("Area" + self.dashLine +
            "Combinational Area:" + float +
            "Noncombinational Area:" + float +
            'Buf/Inv Area:' + float +
            "Total Buffer Area:" + float +
            "Total Inverter Area:" + float +
            'Macro/Black Box Area:' + float +
            "Net Area:" + float +
            "Net XLength:" + float +
            "Net YLength:" + float +
            self.dashLine +
            'Cell Area (netlist):' + float +
            'Cell Area (netlist and physical only):'     + float +
            "Net Length:" + float
        )

        designRule =pp.Group("Design Rules" +
                             self.dashLine +
                             "Total Number of Nets:" + integer +
                             "Nets with Violations:" + integer +
                             "Max Trans Violations:" + integer +
                             "Max Cap Violations:" + integer +
                             self.dashLine)


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


