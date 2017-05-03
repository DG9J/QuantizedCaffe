import sys
import os
import shutil
import re
import gzip
import pyparsing as pp
import icComVar


class parse_def():
    def __init__(self, def_file):
        self.def_file = def_file
        self.designName = "None"
        self.viaSect = []
        print "parsing" , self.def_file

    def read_def(self):
        delimPair = pp.Word("[" + "]")
        pinName =  icComVar.icComVar.hierName
        instName = icComVar.icComVar.hierName
        net_name = icComVar.icComVar.hierName
        propName = icComVar.icComVar.flatName
        propVal  = icComVar.icComVar.flatName
        icComVar.intNum   = icComVar.icComVar.intNum
        icComVar.flatName = icComVar.icComVar.flatName
        rowName  = icComVar.icComVar.flatName
        siteName = icComVar.icComVar.flatName
        viaName  = icComVar.icComVar.flatName
        ndrName  = icComVar.icComVar.flatName

        # header
        version     = pp.Group("VERSION" + self.float + icComVar.SEMICOLON)
        dividerchar = pp.Group("DIVIDERCHAR" + pp.delimitedList(icComVar.dQuoteString) + icComVar.SEMICOLON)
        busbitchars = pp.Group("BUSBITCHARS" + pp.delimitedList(icComVar.dQuoteString) + icComVar.SEMICOLON)
        designName =  pp.Group("DESIGN" + icComVar.flatName + icComVar.SEMICOLON)
        technology =  pp.Group("TECHNOLOGY" + icComVar.flatName + icComVar.SEMICOLON)
        unit =        pp.Group("UNITS DISTANCE MICRONS" + icComVar.intNum + icComVar.SEMICOLON)
        history =     pp.Group("HISTORY" + icComVar.flatName + icComVar.SEMICOLON)
        property =    pp.Group("PROPERTYDEFINITIONS" + objectType + icComVar.flatName + propType + icComVar.flatName + "END PROPERTYDEFINITIONS ")
        die_area = pp.Group("DIEAREA" + icComVar.polygon + icComVar.SEMICOLON)
        compMaskShift = pp.Group(pp.oneOf("COMPONENTMASKSHIFT ") + pp.OneOrMore(icComVar.layerName))
        maskShift = pp.Group("MASKSHIFT" + icComVar.intNum)

        #COMMON
        #propDefine = pp.Group(self.icComVar.PLUS + "PROPERTY" + pp.OneOrMore(   LBRACE + propName + propVal + RBRACE) )
        propDefine = pp.Group(self.icComVar.PLUS + "PROPERTY" + pp.OneOrMore(pp.delimitedList(braceQuoteString)))
        # ROW
        
        row = pp.Group("ROW" + rowName + siteName + icComVar.orig + icComVar.orient +
                       pp.Optional("DO" + icComVar.intNum + "BY" + icComVar.intNum + pp.Optional("STEP" + icComVar.intNum + icComVar.intNum)) +
                       pp.Optional(icComVar.PLUS + "PROPERTY" + pp.OneOrMore(LBRACE + icComVar.flatName + icComVar.flatName + RBRACE)) + icComVar.SEMICOLON)
        rows = pp.Group(pp.OneOrMore(row))

        # TRACK SECTION
        track = pp.Group("TRACKS" + icComVar.routDir + icComVar.intNum + "DO" + icComVar.intNum + "STEP" + icComVar.intNum +
                          pp.Optional("MASK" + icComVar.intNum + pp.Optional("SAMEMASK")) +
                          pp.Optional("LAYER"+ icComVar.layerName) + icComVar.SEMICOLON)
        tracks = pp.Group(pp.OneOrMore(track))

        # VIA SECTION
        viaRule = pp.Group(icComVar.PLUS + "VIARULE" + icComVar.flatName +
                                    icComVar.PLUS + "CUTSIZE" + icComVar.intNum + icComVar.intNum +
                                    icComVar.PLUS + "LAYERS" + icComVar.metalName + icComVar.cutName + icComVar.metalName +
                                    icComVar.PLUS + "CUTSPACING" + icComVar.intNum + icComVar.intNum +
                                    icComVar.PLUS + "ENCLOSE" + icComVar.intNum + icComVar.intNum + icComVar.intNum + icComVar.intNum +
                                    pp.Optional(icComVar.PLUS + "ROWCOL" + icComVar.intNum + icComVar.intNum) +
                                    pp.Optional(icComVar.PLUS + "icComVar.origIN" + icComVar.intNum + icComVar.intNum) +
                                    pp.Optional(icComVar.PLUS + "OFFSET" + icComVar.intNum + icComVar.intNum + icComVar.intNum + icComVar.intNum) +
                                    pp.Optional(icComVar.PLUS + "PATTERN" + icComVar.flatName)
                        )
        viaRect   = pp.Group(icComVar.PLUS + "RECT"    + icComVar.layerName + pp.Optional(icComVar.PLUS + "MASK" + icComVar.intNum ) + icComVar.rectangle)
        viaPoly   = pp.Group(icComVar.PLUS + "icComVar.polygon" + icComVar.layerName + pp.Optional(icComVar.PLUS + "MASK" + icComVar.intNum) +  icComVar.polygon)
        viaDefine = pp.Group(icComVar.DASH + viaName + pp.Optional(viaRule) + pp.ZeroOrMore(viaRect) + pp.ZeroOrMore(viaPoly) + icComVar.SEMICOLON )
        viaSect   = pp.Group("VIAS" + icComVar.intNum + icComVar.SEMICOLON + pp.OneOrMore(viaDefine) + "END VIAS")

        #NonDefault rule
        ndrLayer = pp.Group(icComVar.PLUS + "LAYER" + icComVar.layerName + "WIDTH" + icComVar.intNum +
                                            pp.Optional("DIAGWIDTH" + icComVar.intNum) +
                                            pp.Optional("SPACING"   + icComVar.intNum) +
                                            pp.Optional("WIREEXT"   +  icComVar.flatName) )


        ndrDefine  = pp.Group(icComVar.DASH + icComVar.flatName +
                            pp.Optional(icComVar.PLUS + "HARDSPACING") +
                            pp.OneOrMore(ndrLayer) +
                            pp.Optional(icComVar.PLUS + "VIA" + viaName) +
                            pp.Optional(icComVar.PLUS + "VIARULE" + icComVar.flatName) +
                            pp.ZeroOrMore(icComVar.PLUS + "MINCUTS" + icComVar.cutName + icComVar.intNum) +
                            pp.ZeroOrMore(propDefine) +
                            icComVar.SEMICOLON)
        ndrSect    = pp.Group("NONDEFAULTRULES" + icComVar.intNum + icComVar.SEMICOLON + pp.OneOrMore(ndrDefine) + "END NONDEFAULTRULES" )

        # REGION SECTION
        regionDefine = pp.Group(icComVar.DASH + icComVar.flatName + icComVar.polygon +
                                pp.Optional(icComVar.PLUS + "TYPE" + pp.oneOf("FENCE GUIDE")) +
                                pp.ZeroOrMore(propDefine) +
                                icComVar.SEMICOLON)
        regionSect  = pp.Group("REGIONS" + icComVar.intNum + icComVar.SEMICOLON + pp.OneOrMore(regionDefine) + "END REGIONS")

        # COMPONENTS
        cellLoc  = pp.Group(icComVar.PLUS + pp.oneOf("FIXED COVER PLACED UNPLACED") + pp.Optional(icComVar.orig)  + pp.Optional(icComVar.orient) )
        compDefine = pp.Group(icComVar.DASH + icComVar.hierName + icComVar.flatName +
                              pp.Optional(icComVar.PLUS + "EEQMASTER" + icComVar.flatName) +
                              pp.Optional(icComVar.PLUS + "SOURCE" + pp.oneOf("NETLIST DIST USER TIMING")) +
                              pp.Optional(cellLoc) +
                              pp.Optional(icComVar.PLUS + maskShift) +
                              pp.Optional(icComVar.PLUS + "HALO" + pp.Optional("SOFT") + icComVar.rectangle) +
                              pp.Optional(icComVar.PLUS + "ROUTEHALO" + icComVar.intNum + icComVar.layerName + icComVar.layerName) +
                              pp.Optional(icComVar.PLUS + "WEIGHT" + icComVar.intNum) +
                              pp.Optional(icComVar.PLUS + "REGION" + icComVar.flatName) +
                              pp.Optional(propDefine) +
                              icComVar.SEMICOLON
                              )
        compSect = pp.Group("COMPONENTS" + icComVar.intNum  + icComVar.SEMICOLON + pp.OneOrMore(compDefine) + "END COMPONENTS")

        ##pin section

        rpt_file = self.def_file
        # print rpt_file
        if os.path.isfile(rpt_file):
            if rpt_file.split(".")[-1] == "gz":
                file = gzip.open(rpt_file, 'r')
            else:
                file = open(rpt_file,"r")
            rpt_string = file.read()
            #self.designName = designName.searchString(rpt_string)
            #print rpt_string
            #rst = rows.searchString(rpt_string)
            #rst = tracks.searchString(rpt_string)
            #rst = viaSect.searchString(rpt_string)
            #rst = viaSect.searchString(rpt_string)
            #rst = ndrLayer.searchString(rpt_string)
            #rst = ndrDefine.searchString(rpt_string)
            #rst = ndrSect.searchString(rpt_string)
            #self.viaSect = viaSect.searchString(rpt_string)
            #rst = regionDefine.searchString(rpt_string)
            #rst  = regionSect.searchString(rpt_string)
            #rst = compDefine.searchString(rpt_string)
            rst = compSect.searchString(rpt_string)
            print len(rst) , rst

