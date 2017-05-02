import sys
import os
import shutil
import re
import gzip
import pyparsing as pp
import icComVar


class parse_def(icComVar):
    def __init__(self, def_file):
        self.def_file = def_file
        self.designName = "None"
        self.viaSect = []
        print "parsing" , self.def_file

    def read_def(self):

        delimPair = pp.Word("[" + "]")
        pinName =  self.hierName
        instName = self.hierName
        net_name = self.hierName
        propName = self.flatName
        propVal  = self.flatName

        rowName  = self.flatName
        siteName = self.flatName
        viaName  = self.flatName
        ndrName  = self.flatName

        # header
        version     = pp.Group("VERSION" + self.float + self.SEMICOLON)
        dividerchar = pp.Group("DIVIDERCHAR" + DQUOTA + flatName + DQUOTA + self.SEMICOLON)
        busbitchars = pp.Group("BUSBITCHARS" + DQUOTA + delimPair + self.SEMICOLON)
        designName =  pp.Group("DESIGN" + flatName + self.SEMICOLON)
        technology =  pp.Group("TECHNOLOGY" + flatName + self.SEMICOLON)
        unit =        pp.Group("UNITS DISTANCE MICRONS" + int + self.SEMICOLON)
        history =     pp.Group("HISTORY" + flatName + self.SEMICOLON)
        property =    pp.Group("PROPERTYDEFINITIONS" + objectType + flatName + propType + flatName + "END PROPERTYDEFINITIONS ")
        die_area = pp.Group("DIEAREA" + polygon + self.SEMICOLON)
        compMaskShift = pp.Group(pp.oneOf("COMPONENTMASKSHIFT ") + pp.OneOrMore(layerName))
        maskShift = pp.Group("MASKSHIFT" + int)

        #COMMON
        propDefine = pp.Group(self.PLUS + "PROPERTY" + pp.OneOrMore(LBRACE + propName + propVal + RBRACE) )
        # ROW
        
        row = pp.Group("ROW" + rowName + siteName + orig + orient +
                       pp.Optional("DO" + int + "BY" + int + pp.Optional("STEP" + int + int)) +
                       pp.Optional(PLUS + "PROPERTY" + pp.OneOrMore(LBRACE + flatName + flatName + RBRACE)) + self.SEMICOLON)
        rows = pp.Group(pp.OneOrMore(row))

        # TRACK SECTION
        track = pp.Group("TRACKS" + routeDir + int + "DO" + int + "STEP" + int +
                          pp.Optional("MASK" + int + pp.Optional("SAMEMASK")) +
                          pp.Optional("LAYER"+ layerName) + self.SEMICOLON)
        tracks = pp.Group(pp.OneOrMore(track))

        # VIA SECTION
        viaRule = pp.Group(PLUS + "VIARULE" + flatName +
                                    PLUS + "CUTSIZE" + int + int +
                                    PLUS + "LAYERS" + matalName + cutName + matalName +
                                    PLUS + "CUTSPACING" + int + int +
                                    PLUS + "ENCLOSE" + int + int + int + int +
                                    pp.Optional(PLUS + "ROWCOL" + int + int) +
                                    pp.Optional(PLUS + "ORIGIN" + int + int) +
                                    pp.Optional(PLUS + "OFFSET" + int + int + int + int) +
                                    pp.Optional(PLUS + "PATTERN" + flatName)
                        )
        viaRect   = pp.Group(PLUS + "RECT"    + layerName + pp.Optional(PLUS + "MASK" + int ) + rectangle)
        viaPoly   = pp.Group(PLUS + "POLYGON" + layerName + pp.Optional(PLUS + "MASK" + int) +  polygon)
        viaDefine = pp.Group(DASH + viaName + pp.Optional(viaRule) + pp.ZeroOrMore(viaRect) + pp.ZeroOrMore(viaPoly) + self.SEMICOLON )
        viaSect   = pp.Group("VIAS" + int + self.SEMICOLON + pp.OneOrMore(viaDefine) + "END VIAS")

        #NonDefault rule
        ndrLayer = pp.Group(PLUS + "LAYER" + layerName + "WIDTH" + int +
                                            pp.Optional("DIAGWIDTH" + int) +
                                            pp.Optional("SPACING" + int) +
                                            pp.Optional("WIREEXT" +  flatName) )


        ndrDefine  = pp.Group(DASH + flatName +
                            pp.Optional(PLUS + "HARDSPACING") +
                            pp.OneOrMore(ndrLayer) +
                            pp.Optional(PLUS + "VIA" + viaName) +
                            pp.Optional(PLUS + "VIARULE" + flatName) +
                            pp.ZeroOrMore(PLUS + "MINCUTS" + cutName + int) +
                            pp.ZeroOrMore(propDefine) +
                            self.SEMICOLON)
        ndrSect    = pp.Group("NONDEFAULTRULES" + int + self.SEMICOLON + pp.OneOrMore(ndrDefine) + "END NONDEFAULTRULES" )

        # REGION SECTION
        regionDefine = pp.Group(DASH + flatName + polygon +
                                pp.Optional(PLUS + "TYPE" + pp.oneOf("FENCE GUIDE")) +
                                pp.ZeroOrMore(propDefine) +
                                self.SEMICOLON)
        regionSect  = pp.Group("REGIONS" + int + self.SEMICOLON + pp.OneOrMore(regionDefine) + "END REGIONS")

        # COMPONENTS
        cellLoc  = pp.Group(PLUS + pp.oneOf("FIXED COVER PLACED UNPLACED") + pp.Optional(orig)  + pp.Optional(orient) )
        compDefine = pp.Group(DASH + hierName + flatName +
                              pp.Optional(PLUS + "EEQMASTER" + flatName) +
                              pp.Optional(PLUS + "SOURCE" + pp.oneOf("NETLIST DIST USER TIMING")) +
                              pp.Optional(cellLoc) +
                              pp.Optional(PLUS + maskShift) +
                              pp.Optional(PLUS + "HALO" + pp.Optional("SOFT") + rectangle) +
                              pp.Optional(PLUS + "ROUTEHALO" + int + layerName + layerName) +
                              pp.Optional(PLUS + "WEIGHT" + int) +
                              pp.Optional(PLUS + "REGION" + flatName) +
                              pp.Optional(propDefine) +
                              self.SEMICOLON
                              )
        compSect = pp.Group("COMPONENTS" + int  + self.SEMICOLON + pp.OneOrMore(compDefine) + "END COMPONENTS")

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



'''





        cell_place = pp.Group(DASH + instName + libCellName + PLUS + placeStatus + orig + orient + self.SEMICOLON)
        componets_section = pp.Group("COMPONENTS" + int + self.SEMICOLON + pp.OneOrMore(cell_place) + "END COMPONENTS")

        pin_shape = pp.Group("PORT" + PLUS + "LAYER" + layerName + polygon + PLUS + placeStatus +  orig  + orient )
        pin_shapes = pp.Group(pp.ZeroOrMore(pin_shape))
        pin_define = pp.Group(DASH + pinName + PLUS + "NET" + net_name + "DIRECTION" + pinDir + "USE" + pinUse + pin_shapes + self.SEMICOLON)
        pin_section = pp.Group("PIN" + int + self.SEMICOLON + pp.OneOrMore(pin_define) + "END PINS")


        place_bkg = pp.Group(DASH + "PLACEMENT" + "RECT" + polygon + self.SEMICOLON)
        place_bkgs = pp.OneOrMore(place_bkg)

        bkg_spacing = pp.Group("SPACING" + int)
        route_bkg = pp.Group(DASH + "LAYER" + layerName + PLUS + pp.ZeroOrMore(bkg_spacing) + "POLYGON" +polygon + self.SEMICOLON
        route_bkgs = pp.OneOrMore(route_bkg)
        bkg_section = pp.Group("BLOCKAGES" + int + place_bkgs + route_bkgs + self.SEMICOLON)
'''

