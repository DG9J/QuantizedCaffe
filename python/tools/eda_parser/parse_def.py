import sys
import os
import shutil
import re
import gzip
import pyparsing as pp
import icComVar as icVar
import fileinput as fi
import numpy as np

class parse_def():
    def __init__(self, defFile):
        self.defFile = defFile
        self.designName = "None"
        print "parsing ", self.defFile

    def defHeader(self):
        # header
        version         =  pp.Group("VERSION" + icVar.floatNum + icVar.SEMICOLON)
        dividerchar     =  pp.Group("DIVIDERCHAR" + pp.delimitedList(icVar.dquotes) + icVar.SEMICOLON)
        busbitchars     =  pp.Group("BUSBITCHARS" + pp.delimitedList(icVar.dquotes) + icVar.SEMICOLON)
        designName      =  pp.Group("DESIGN" + icVar.hierName + icVar.SEMICOLON)
        technology      =  pp.Group("TECHNOLOGY" + icVar.hierName + icVar.SEMICOLON)
        unit            =  pp.Group("UNITS DISTANCE MICRONS" + icVar.intNum + icVar.SEMICOLON)
        history         =  pp.Group("HISTORY" + icVar.hierName + icVar.SEMICOLON)
        property        =  pp.Group("PROPERTYDEFINITIONS" + icVar.objectType + icVar.hierName + icVar.propType + icVar.hierName + "END PROPERTYDEFINITIONS ")
        die_area        =  pp.Group("DIEAREA" + icVar.polygon + icVar.SEMICOLON)
        compMaskShift   =  pp.Group(pp.oneOf("COMPONENTMASKSHIFT ") + pp.OneOrMore(icVar.layerName))
        maskShift       =  pp.Group("MASKSHIFT" + icVar.intNum)

        #COMMON
        #propDefine = pp.Group(self.icVar.PLUS + "PROPERTY" + pp.OneOrMore(   LBRACE + icVar.hierName + icVar.hierName + RBRACE) )
        propDefine = pp.Group(icVar.PLUS + "PROPERTY" + pp.OneOrMore(pp.delimitedList(icVar.braces)))

    def defRow(self):
        # ROW
        row = pp.Group("ROW" + icVar.hierName + icVar.hierName + icVar.orig + icVar.orient +
                       pp.Optional("DO" + icVar.intNum + "BY" + icVar.intNum + pp.Optional("STEP" + icVar.intNum + icVar.intNum)) +
                       pp.Optional(icVar.PLUS + "PROPERTY" + pp.OneOrMore(pp.delimitedList(icVar.braces))) + icVar.SEMICOLON)
        rows = pp.Group(pp.OneOrMore(row))
    def defTrack(self):
        # TRACK SECTION
        track = pp.Group("TRACKS" + icVar.routeDir + icVar.intNum + "DO" + icVar.intNum + "STEP" + icVar.intNum +
                          pp.Optional("MASK" + icVar.intNum + pp.Optional("SAMEMASK")) +
                          pp.Optional("LAYER"+ icVar.layerName) + ';')
        tracks = pp.Group(pp.OneOrMore(track))


    def defVia(self):
        # VIA SECTION
        viaRule = pp.Group(icVar.PLUS + "VIARULE" + icVar.hierName +
                                    icVar.PLUS + "CUTSIZE" + icVar.intNum + icVar.intNum +
                                    icVar.PLUS + "LAYERS" + icVar.metalName + icVar.cutName + icVar.metalName +
                                    icVar.PLUS + "CUTSPACING" + icVar.intNum + icVar.intNum +
                                    icVar.PLUS + "ENCLOSE" + icVar.intNum + icVar.intNum + icVar.intNum + icVar.intNum +
                                    pp.Optional(icVar.PLUS + "ROWCOL" + icVar.intNum + icVar.intNum) +
                                    pp.Optional(icVar.PLUS + "ORIGIN" + icVar.intNum + icVar.intNum) +
                                    pp.Optional(icVar.PLUS + "OFFSET" + icVar.intNum + icVar.intNum + icVar.intNum + icVar.intNum) +
                                    pp.Optional(icVar.PLUS + "PATTERN" + icVar.hierName)
                        )
        viaRect   = pp.Group(icVar.PLUS + "RECT"    + icVar.layerName + pp.Optional(icVar.PLUS + "MASK" + icVar.intNum ) + icVar.rectangle)
        viaPoly   = pp.Group(icVar.PLUS + "icVar.polygon" + icVar.layerName + pp.Optional(icVar.PLUS + "MASK" + icVar.intNum) +  icVar.polygon)
        viaDefine = pp.Group(icVar.DASH + icVar.hierName + pp.Optional(viaRule) + pp.ZeroOrMore(viaRect) + pp.ZeroOrMore(viaPoly) + icVar.SEMICOLON )
        viaSect   = pp.Group("VIAS" + icVar.intNum + icVar.SEMICOLON + pp.OneOrMore(viaDefine) + "END VIAS")

    def defNDR(self):
        # NonDefault rule
        ndrLayer = pp.Group(icVar.PLUS + "LAYER" + icVar.layerName + "WIDTH" + icVar.intNum +
                                            pp.Optional("DIAGWIDTH" + icVar.intNum) +
                                            pp.Optional("SPACING"   + icVar.intNum) +
                                            pp.Optional("WIREEXT"   +  icVar.hierName) )


        ndrDefine  = pp.Group(icVar.DASH + icVar.hierName +
                            pp.Optional(icVar.PLUS + "HARDSPACING") +
                            pp.OneOrMore(ndrLayer) +
                            pp.Optional(icVar.PLUS + "VIA" + icVar.hierName) +
                            pp.Optional(icVar.PLUS + "VIARULE" + icVar.hierName) +
                            pp.ZeroOrMore(icVar.PLUS + "MINCUTS" + icVar.cutName + icVar.intNum) +
                            pp.ZeroOrMore(propDefine) +
                            icVar.SEMICOLON)
        ndrSect    = pp.Group("NONDEFAULTRULES" + icVar.intNum + icVar.SEMICOLON + pp.OneOrMore(ndrDefine) + "END NONDEFAULTRULES" )
    def defRegion(self):
        # REGION SECTION
        regionDefine = pp.Group(icVar.DASH + icVar.hierName + icVar.polygon +
                                pp.Optional(icVar.PLUS + "TYPE" + pp.oneOf("FENCE GUIDE")) +
                                pp.ZeroOrMore(propDefine) +
                                icVar.SEMICOLON)
        regionSect  = pp.Group("REGIONS" + icVar.intNum + icVar.SEMICOLON + pp.OneOrMore(regionDefine) + "END REGIONS")
    def defComp(self):
        # COMPONENTS
        cellLoc  = pp.Group(icVar.PLUS + pp.oneOf("FIXED COVER PLACED UNPLACED") + pp.Optional(icVar.orig)  + pp.Optional(icVar.orient) )
        compDefine = pp.Group(icVar.DASH + icVar.hierName + icVar.hierName +
                              pp.Optional(icVar.PLUS + "EEQMASTER" + icVar.hierName) +
                              pp.Optional(icVar.PLUS + "SOURCE" + pp.oneOf("NETLIST DIST USER TIMING")) +
                              pp.Optional(cellLoc) +
                              pp.Optional(icVar.PLUS + maskShift) +
                              pp.Optional(icVar.PLUS + "HALO" + pp.Optional("SOFT") + icVar.rectangle) +
                              pp.Optional(icVar.PLUS + "ROUTEHALO" + icVar.intNum + icVar.layerName + icVar.layerName) +
                              pp.Optional(icVar.PLUS + "WEIGHT" + icVar.intNum) +
                              pp.Optional(icVar.PLUS + "REGION" + icVar.hierName) +
                              pp.Optional(propDefine) +
                              icVar.SEMICOLON
                              )
        compSect = pp.Group("COMPONENTS" + icVar.intNum  + icVar.SEMICOLON + pp.OneOrMore(compDefine) + "END COMPONENTS")

        ##pin section
    def defPin(self):
        portLayerDefine = pp.Group(icVar.PLUS + "LAYER" + icVar.layerName +
                                  pp.Optional("MASK" + icVar.intNum) +
                                  pp.Optional("SPACING" + icVar.intNum) +
                                  pp.Optional("DESIGNRULEWIDTH" + icVar.intNum) +
                                  icVar.rectangle
                               )
        portPolygonDefine = pp.Group(icVar.PLUS + "POLYGON" + icVar.layerName +
                                     pp.Optional("MASK" + icVar.intNum) +
                                     pp.Optional("SPACING" + icVar.intNum ) +
                                     pp.Optional("DESIGNRULEWIDTH" + icVar.intNum) +
                                     icVar.polygon)
        portViaDefine = pp.Group(icVar.PLUS + "VIA" + icVar.hierName +
                                 pp.Optional("MASK" + icVar.intNum) +
                                 icVar.orig
                                 )
        portStatDefine = pp.Group(pp.oneOf("COVER PLACED FIXED") + icVar.orig + icVar.orient)

        portDefine = pp.Group(icVar.PLUS + "PORT" +
                              pp.Optional(portLayerDefine) +
                              pp.Optional(portPolygonDefine) +
                              pp.Optional(portViaDefine) +
                              pp.Optional(portStatDefine)
                              )
        portAttrDefine = pp.Group(pp.Optional(icVar.PLUS + "SPECIAL") +
                                  pp.Optional(icVar.PLUS + "DIRECTION" + icVar.pinDir) +
                                  pp.Optional(icVar.PLUS + "NETEXPR" + pp.delimitedList(icVar.dquotes)) +
                                  pp.Optional(icVar.PLUS + "SUPPLYSENSITIVITY" + icVar.hierName) +
                                  pp.Optional(icVar.PLUS + "GROUNDSENSITIVITY" + icVar.hierName) +
                                  pp.Optional(icVar.PLUS + "USE" + icVar.pinUse) +
                                  pp.ZeroOrMore(icVar.PLUS + "ANTENNAPINPARTIALMETALAREA"   + icVar.floatNum + pp.Optional("LAYER" + icVar.metalName)) +
                                  pp.ZeroOrMore(icVar.PLUS + "ANTENNAPINPARTIALMETALSIDEAREA" +  icVar.floatNum + pp.Optional("LAYER" + icVar.metalName)) +
                                  pp.ZeroOrMore(icVar.PLUS + "ANTENNAPINPARTIALCUTAREA" +  icVar.floatNum + pp.Optional("LAYER" + icVar.metalName)) +
                                  pp.ZeroOrMore(icVar.PLUS + "ANTENNAPINDIFFAREA" + icVar.floatNum + pp.Optional("LAYER" + icVar.layerName )) +
                                  pp.ZeroOrMore(icVar.PLUS + "ANTENNAMODEL" + pp.oneOf("OXIDE1 OXIDE2 OXIDE3 OXIDE4")) +
                                  pp.ZeroOrMore(icVar.PLUS + "ANTENNAPINGATEAREA"  +   icVar.floatNum + pp.Optional("LAYER" + icVar.layerName)) +
                                  pp.ZeroOrMore(icVar.PLUS + "ANTENNAPINMAXAREACAR"  +  icVar.floatNum + pp.Optional("LAYER" + icVar.layerName)) +
                                  pp.ZeroOrMore(icVar.PLUS + "ANTENNAPINMAXCUTCAR" + icVar.floatNum + pp.Optional("LAYER" + icVar.layerName))
                                  )

        pinDefine = pp.Group(icVar.DASH + icVar.hierName + icVar.PLUS + "NET" + icVar.hierName +
                             portAttrDefine +
                             portDefine)
        pinSection = pp.Group("PINS" + icVar.intNum + icVar.SEMICOLON +
                              pp.ZeroOrMore(pinDefine) +
                              "END PINS")
        defFile = fi.FileInput(self.defFile, openhook=fi.hook_compressed)
        for line0 in defFile:
            if line0.find('PINS') == 0:
                pinSect = []
                for line1 in defFile:
                    if line1.find('END PINS') == 0:

                        str1 = ''.join(pinSect)
                        #print line1, str1
                        result = pinDefine.searchString(str1)
                        break
                    else:
                        pinSect.append(line1)
            #else:
            #    print "finished", line0.strip()
        #print "complete read the", rpt_file
        return result

        #self.designName = designName.searchString(rpt_string)
        #print rpt_string
        #rst = rows.searchString(rpt_string)
        #rst = tracks.searchString(rpt_string)
        #rst = viaSect.searchString(rpt_string)
        #print len(rst) , rst
        #rst = ndrLayer.searchString(rpt_string)
        #rst = ndrDefine.searchString(rpt_string)
        #rst = ndrSect.searchString(rpt_string)
        #self.viaSect = viaSect.searchString(rpt_string)
        #rst = regionDefine.searchString(rpt_string)
        #rst  = regionSect.searchString(rpt_string)
        #rst = compDefine.searchString(rpt_string)
        #rst = compSect.searchString(rpt_string)

        #rst =  portLayerDefine.searchString(rpt_string)
        #rst = portPolygonDefine.searchString(rpt_string)
        #rst = portViaDefine.searchString(rpt_string)
        #rst = portStatDefine.searchString(rpt_string)
        #rst = portDefine.searchString(rpt_string)
        #rst = portAttrDefine.searchString(rpt_string)
        #rst = pinQuota.searchString(rpt_string)
        #return rst

