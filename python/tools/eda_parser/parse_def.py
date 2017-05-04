import sys
import os
import shutil
import re
import gzip
import pyparsing as pp
import icComVar as icVar


class parse_def():
    def __init__(self, def_file):
        self.def_file = def_file
        self.designName = "None"
        self.viaSect = []
        print "parsing" , self.def_file

    def read_def(self):
        pinName =  icVar.hierName
        instName = icVar.hierName
        net_name = icVar.hierName
        propName = icVar.flatName
        propVal  = icVar.flatName
        flatName = icVar.flatName
        intNum   = icVar.intNum
        rowName  = icVar.flatName
        siteName = icVar.flatName
        viaName  = icVar.flatName
        ndrName  = icVar.flatName

        PLUS = icVar.PLUS
        # header
        version     = pp.Group("VERSION" + icVar.floatNum + icVar.SEMICOLON)
        dividerchar = pp.Group("DIVIDERCHAR" + pp.delimitedList(icVar.dquotes) + icVar.SEMICOLON)
        busbitchars = pp.Group("BUSBITCHARS" + pp.delimitedList(icVar.dquotes) + icVar.SEMICOLON)
        designName =  pp.Group("DESIGN" + icVar.flatName + icVar.SEMICOLON)
        technology =  pp.Group("TECHNOLOGY" + icVar.flatName + icVar.SEMICOLON)
        unit       =  pp.Group("UNITS DISTANCE MICRONS" + icVar.intNum + icVar.SEMICOLON)
        history    =  pp.Group("HISTORY" + icVar.flatName + icVar.SEMICOLON)
        property =    pp.Group("PROPERTYDEFINITIONS" + icVar.objectType + icVar.flatName + icVar.propType + icVar.flatName + "END PROPERTYDEFINITIONS ")
        die_area = pp.Group("DIEAREA" + icVar.polygon + icVar.SEMICOLON)
        compMaskShift = pp.Group(pp.oneOf("COMPONENTMASKSHIFT ") + pp.OneOrMore(icVar.layerName))
        maskShift = pp.Group("MASKSHIFT" + icVar.intNum)

        #COMMON
        #propDefine = pp.Group(self.PLUS + "PROPERTY" + pp.OneOrMore(   LBRACE + propName + propVal + RBRACE) )
        propDefine = pp.Group(PLUS + "PROPERTY" + pp.OneOrMore(pp.delimitedList(icVar.braces)))
        # ROW
        
        row = pp.Group("ROW" + rowName + siteName + icVar.orig + icVar.orient +
                       pp.Optional("DO" + icVar.intNum + "BY" + icVar.intNum + pp.Optional("STEP" + icVar.intNum + icVar.intNum)) +
                       pp.Optional(PLUS + "PROPERTY" + pp.OneOrMore(pp.delimitedList(icVar.braces))) + icVar.SEMICOLON)
        rows = pp.Group(pp.OneOrMore(row))

        # TRACK SECTION
        track = pp.Group("TRACKS" + icVar.routeDir + icVar.intNum + "DO" + icVar.intNum + "STEP" + icVar.intNum +
                          pp.Optional("MASK" + icVar.intNum + pp.Optional("SAMEMASK")) +
                          pp.Optional("LAYER"+ icVar.layerName) + ';')
        tracks = pp.Group(pp.OneOrMore(track))

        # VIA SECTION
        viaRule = pp.Group(PLUS + "VIARULE" + icVar.flatName +
                                    PLUS + "CUTSIZE" + icVar.intNum + icVar.intNum +
                                    PLUS + "LAYERS" + icVar.metalName + icVar.cutName + icVar.metalName +
                                    PLUS + "CUTSPACING" + icVar.intNum + icVar.intNum +
                                    PLUS + "ENCLOSE" + icVar.intNum + icVar.intNum + icVar.intNum + icVar.intNum +
                                    pp.Optional(PLUS + "ROWCOL" + icVar.intNum + icVar.intNum) +
                                    pp.Optional(PLUS + "ORIGIN" + icVar.intNum + icVar.intNum) +
                                    pp.Optional(PLUS + "OFFSET" + icVar.intNum + icVar.intNum + icVar.intNum + icVar.intNum) +
                                    pp.Optional(PLUS + "PATTERN" + icVar.flatName)
                        )
        viaRect   = pp.Group(PLUS + "RECT"    + icVar.layerName + pp.Optional(PLUS + "MASK" + icVar.intNum ) + icVar.rectangle)
        viaPoly   = pp.Group(PLUS + "icVar.polygon" + icVar.layerName + pp.Optional(PLUS + "MASK" + icVar.intNum) +  icVar.polygon)
        viaDefine = pp.Group(icVar.DASH + viaName + pp.Optional(viaRule) + pp.ZeroOrMore(viaRect) + pp.ZeroOrMore(viaPoly) + icVar.SEMICOLON )
        viaSect   = pp.Group("VIAS" + icVar.intNum + icVar.SEMICOLON + pp.OneOrMore(viaDefine) + "END VIAS")

        #NonDefault rule
        ndrLayer = pp.Group(PLUS + "LAYER" + icVar.layerName + "WIDTH" + icVar.intNum +
                                            pp.Optional("DIAGWIDTH" + icVar.intNum) +
                                            pp.Optional("SPACING"   + icVar.intNum) +
                                            pp.Optional("WIREEXT"   +  icVar.flatName) )


        ndrDefine  = pp.Group(icVar.DASH + icVar.flatName +
                            pp.Optional(PLUS + "HARDSPACING") +
                            pp.OneOrMore(ndrLayer) +
                            pp.Optional(PLUS + "VIA" + viaName) +
                            pp.Optional(PLUS + "VIARULE" + icVar.flatName) +
                            pp.ZeroOrMore(PLUS + "MINCUTS" + icVar.cutName + icVar.intNum) +
                            pp.ZeroOrMore(propDefine) +
                            icVar.SEMICOLON)
        ndrSect    = pp.Group("NONDEFAULTRULES" + icVar.intNum + icVar.SEMICOLON + pp.OneOrMore(ndrDefine) + "END NONDEFAULTRULES" )

        # REGION SECTION
        regionDefine = pp.Group(icVar.DASH + icVar.flatName + icVar.polygon +
                                pp.Optional(PLUS + "TYPE" + pp.oneOf("FENCE GUIDE")) +
                                pp.ZeroOrMore(propDefine) +
                                icVar.SEMICOLON)
        regionSect  = pp.Group("REGIONS" + icVar.intNum + icVar.SEMICOLON + pp.OneOrMore(regionDefine) + "END REGIONS")

        # COMPONENTS
        cellLoc  = pp.Group(PLUS + pp.oneOf("FIXED COVER PLACED UNPLACED") + pp.Optional(icVar.orig)  + pp.Optional(icVar.orient) )
        compDefine = pp.Group(icVar.DASH + icVar.hierName + icVar.flatName +
                              pp.Optional(PLUS + "EEQMASTER" + icVar.flatName) +
                              pp.Optional(PLUS + "SOURCE" + pp.oneOf("NETLIST DIST USER TIMING")) +
                              pp.Optional(cellLoc) +
                              pp.Optional(PLUS + maskShift) +
                              pp.Optional(PLUS + "HALO" + pp.Optional("SOFT") + icVar.rectangle) +
                              pp.Optional(PLUS + "ROUTEHALO" + icVar.intNum + icVar.layerName + icVar.layerName) +
                              pp.Optional(PLUS + "WEIGHT" + icVar.intNum) +
                              pp.Optional(PLUS + "REGION" + icVar.flatName) +
                              pp.Optional(propDefine) +
                              icVar.SEMICOLON
                              )
        compSect = pp.Group("COMPONENTS" + icVar.intNum  + icVar.SEMICOLON + pp.OneOrMore(compDefine) + "END COMPONENTS")

        ##pin section
        portLayerDefine = pp.Group(PLUS + "layer" + icVar.metalName +
                                  pp.Optional("MASK" + intNum) +
                                  pp.Optional("SPACING" + intNum ) +
                                  pp.Optional("DESIGNRULEWIDTH" + intNum) +
                                  icVar.rectangle
                               )
        portPolygonDefine = pp.Group(PLUS + "POLYGEN" + icVar.metalName +
                                     pp.Optional("MASK" + icVar.intNum) +
                                     pp.Optional("SPACING" + icVar.intNum ) +
                                     pp.Optional("DESIGNRULEWIDTH" + icVar.intNum) +
                                     icVar.polygon
                                     )
        portViaDefine = pp.Group(PLUS + "VIA" + viaName +
                                 pp.Optional("MASK" + icVar.intNum) +
                                 icVar.orig
                                 )


        portDefine = pp.Group(PLUS + "PORT" +
                              portLayerDefine +
                              portPolygonDefine +
                              portViaDefine
                              )
        portAttrDefine = pp.Group(PLUS + "SPECIAL" +
                                  PLUS + "DIRECTION" + icVar.pinDir +
                                  PLUS + "NETEXPR" + pp.delimitedList(icVar.dquotes) +
                                  PLUS + "SUPPLYSENSITIVITY" + pinName +
                                  PLUS + "GROUNDSENSITIVITY" + pinName +
                                  PLUS + "USE" + pp.oneOf("SIGNAL POWER GROUND CLOCK TIEOFF ANALOG SCAN RESET") +
                                  PLUS + "ANTENNAPINPARTIALMETALAREA"   + float + pp.Optional("LAYER" + icVar.metalName) +
                                  PLUS + "ANTENNAPINPARTIALMETALSIDEAREA" +  float + pp.Optional("LAYER" + icVar.metalName) +
                                  PLUS + "ANTENNAPINPARTIALCUTAREA" +  float + pp.Optional("LAYER" + icVar.metalName) +
                                  PLUS + "ANTENNAPINDIFFAREA" + float + pp
                                  )
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
            rst = viaSect.searchString(rpt_string)
            print len(rst) , rst
            #rst = ndrLayer.searchString(rpt_string)
            #rst = ndrDefine.searchString(rpt_string)
            #rst = ndrSect.searchString(rpt_string)
            #self.viaSect = viaSect.searchString(rpt_string)
            #rst = regionDefine.searchString(rpt_string)
            #rst  = regionSect.searchString(rpt_string)
            #rst = compDefine.searchString(rpt_string)
            #rst = compSect.searchString(rpt_string)
            print len(rst) , rst

