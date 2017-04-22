import sys
import os
import shutil
import re
import gzip
import pyparsing as pp


class parse_def():
    def __init__(self, def_file):
        self.def_file = def_file
        self.designName = "None"
        self.viaSect = []
        print "parsing" , self.def_file

    def read_def(self):
        COLON, LBRACK, RBRACK, LBRACE, RBRACE, TILDE, CARAT,COMMA = map(pp.Literal, ":[]{}~^,")
        UNDERSCORE, DOT, BSLASH, SLASH = map(pp.Literal, '_./\\')
        PLUS, DASH = map(pp.Suppress, "+-")
        LPAR, RPAR = map(pp.Suppress, "()")
        SEMICOLON, DQUOTA = map(pp.Suppress, ';"')

        #character = pp.Word(pp.alphanums + BSLASH + UNDERSCORE + LBRACE + RBRACE)
        character = pp.Word(pp.alphanums + "/" + "_" + "[" +"]")
        delimPair = pp.Word("[" + "]")

        float = pp.Word(pp.nums + '.' + "_")
        integer = pp.Word(pp.nums + '-')
        flatName = pp.Word(pp.alphanums + "_")
        hierName = pp.Word(pp.alphanums + '/' + '_' + '[' + ']')
        pinName = hierName
        instName = hierName
        net_name = hierName
        propName = flatName
        propVal  = flatName

        libCellName = pp.Word(pp.alphas.upper() + pp.nums + "_")

        orient = pp.Word('N' + 'E' + 'W' + 'S' + 'FN' + 'FE' + 'FW' + 'FS')
        routeDir = pp.Word('X' + 'Y')
        layerName = pp.Word('M0' + 'M1' + 'M2' + 'M3' + 'M4' + 'M5' + 'M6' + 'M7' + 'M8' + 'M10' + 'M11' + 'M12' +
                              'VIA0' + 'VIA1' + 'VIA2' + 'VIA3' + 'VIA4' + 'VIA5' + 'VIA6' + 'VIA7' + 'VIA8' + 'VIA10' + 'VIA11' + 'VIA12'
                              )
        metalLayerName = pp.Word('M0' + 'M1' + 'M2' + 'M3' + 'M4' + 'M5' + 'M6' + 'M7' + 'M8' + 'M10' + 'M11' + 'M12')
        cutLayerName = pp.Word('VIA0' + 'VIA1' + 'VIA2' + 'VIA3' + 'VIA4' + 'VIA5' + 'VIA6' + 'VIA7' + 'VIA8' + 'VIA10' + 'VIA11' + 'VIA12')

        placeStatus = pp.Word('PLACED' + "FIXED" + "COVER")
        pinDir = pp.Word('INPUT' + "OUTPUT" + "INOUT")
        pinUse = pp.Word('SIGNAL' + "POWER" + "GROUND" + "CLOCK")
        PropType = pp.Word('INTERGER' + 'REAL' + 'STRING')
        ObjectType = pp.Word("DESIGN" + "COMPONENT" + "NET" + "SPECIALNET" + "GROUP" + "ROW" + "COMPONENTPIN" + "REGION")

        origX = pp.Word(pp.nums + "*" + "-")
        origY = pp.Word(pp.nums + "*" + "-")
        orig = pp.Group(pp.Optional(LPAR) + origX + origY + pp.Optional(RPAR))
        rectangle = pp.Group( orig + orig)
        polygon = pp.Group(orig + orig + pp.OneOrMore(orig))
        rowName = pp.Word(pp.alphanums + '_')
        siteName = rowName
        viaName = flatName
        ndrName = flatName
        

        # header
        version = pp.Group("VERSION" + float + SEMICOLON)
        dividerchar = pp.Group("DIVIDERCHAR" + DQUOTA + flatName + DQUOTA + SEMICOLON)
        busbitchars = pp.Group("BUSBITCHARS" + DQUOTA + delimPair + SEMICOLON)
        designName = pp.Group("DESIGN" + flatName + SEMICOLON)
        technology = pp.Group("TECHNOLOGY" + flatName + SEMICOLON)
        unit = pp.Group("UNITS DISTANCE MICRONS" + integer + SEMICOLON)
        history = pp.Group("HISTORY" + character + SEMICOLON)
        property = pp.Group(
            "PROPERTYDEFINITIONS" + ObjectType + flatName + PropType + flatName + "END PROPERTYDEFINITIONS ")
        die_area = pp.Group("DIEAREA" + polygon + SEMICOLON)
        compMaskShift = pp.Group("COMPONENTMASKSHIFT" + pp.OneOrMore(layerName))

        #COMMON
        propDefine = pp.Group(PLUS + "PROPERTY" + pp.OneOrMore(LBRACE + propName + propVal + RBRACE) )
        # ROW
        
        row = pp.Group("ROW" + rowName + siteName + orig + orient +
                       pp.Optional("DO" + integer + "BY" + integer + pp.Optional("STEP" + integer + integer)) +
                       pp.Optional(PLUS + "PROPERTY" + pp.OneOrMore(LBRACE + flatName + flatName + RBRACE)) + SEMICOLON)
        rows = pp.Group(pp.OneOrMore(row))

        # TRACK SECTION
        track = pp.Group("TRACKS" + routeDir + integer + "DO" + integer + "STEP" + integer +
                          pp.Optional("MASK" + integer + pp.Optional("SAMEMASK")) +
                          pp.Optional("LAYER"+ layerName) + SEMICOLON)
        tracks = pp.Group(pp.OneOrMore(track))

        # VIA SECTION
        viaRule = pp.Group(PLUS + "VIARULE" + flatName +
                                    PLUS + "CUTSIZE" + integer + integer +
                                    PLUS + "LAYERS" + metalLayerName + cutLayerName + metalLayerName +
                                    PLUS + "CUTSPACING" + integer + integer +
                                    PLUS + "ENCLOSE" + integer + integer + integer + integer +
                                    pp.Optional(PLUS + "ROWCOL" + integer + integer) +
                                    pp.Optional(PLUS + "ORIGIN" + integer + integer) +
                                    pp.Optional(PLUS + "OFFSET" + integer + integer + integer + integer) +
                                    pp.Optional(PLUS + "PATTERN" + flatName)
                        )
        viaRect   = pp.Group(PLUS + "RECT"    + layerName + pp.Optional(PLUS + "MASK" + integer ) + rectangle)
        viaPoly   = pp.Group(PLUS + "POLYGON" + layerName + pp.Optional(PLUS + "MASK" + integer) +  polygon)
        viaDefine = pp.Group(DASH + viaName + pp.Optional(viaRule) + pp.ZeroOrMore(viaRect) + pp.ZeroOrMore(viaPoly) + SEMICOLON )
        viaSect   = pp.Group("VIAS" + integer + SEMICOLON + pp.OneOrMore(viaDefine) + "END VIAS")

        #NonDefault rule
        ndrLayer = pp.Group(PLUS + "LAYER" + layerName + "WIDTH" + integer +
                                            pp.Optional("DIAGWIDTH" + integer) +
                                            pp.Optional("SPACING" + integer) +
                                            pp.Optional("WIREEXT" +  flatName))


        ndrDefine  = pp.Group(DASH + flatName +
                            pp.Optional(PLUS + "HARDSPACING") +
                            pp.OneOrMore(ndrLayer) +
                            pp.Optional(PLUS + "VIA" + viaName) +
                            pp.Optional(PLUS + "VIARULE" + flatName) +
                            pp.ZeroOrMore(PLUS + "MINCUTS" + cutLayerName + integer) +
                            propDefine +
                            SEMICOLON)
        ndrSect    = pp.Group("NONDEFAULTRULES" + integer + SEMICOLON + pp.OneOrMore(ndrDefine) + "END NONDEFAULTRULES" )

        # REGION SECTION
        regionDefine = pp.Group(DASH + flatName + polygon +
                                pp.Optional(PLUS + "TYPE" + LBRACE +  pp.oneOf("FENCE GUIDE" ) + RBRACE) +
                                pp.OneOrMore(PLUS + propDefine) +
                                SEMICOLON)
        regionSect  = pp.Group("REGIONS" + integer + SEMICOLON + pp.OneOrMore(regionDefine) + "END REGIONS")

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
            rst = ndrSect.searchString(rpt_string)
            #self.viaSect = viaSect.searchString(rpt_string)
            print len(rst) , rst



'''





        cell_place = pp.Group(DASH + instName + libCellName + PLUS + placeStatus + orig + orient + SEMICOLON)
        componets_section = pp.Group("COMPONENTS" + integer + SEMICOLON + pp.OneOrMore(cell_place) + "END COMPONENTS")

        pin_shape = pp.Group("PORT" + PLUS + "LAYER" + layerName + polygon + PLUS + placeStatus +  orig  + orient )
        pin_shapes = pp.Group(pp.ZeroOrMore(pin_shape))
        pin_define = pp.Group(DASH + pinName + PLUS + "NET" + net_name + "DIRECTION" + pinDir + "USE" + pinUse + pin_shapes + SEMICOLON)
        pin_section = pp.Group("PIN" + integer + SEMICOLON + pp.OneOrMore(pin_define) + "END PINS")


        place_bkg = pp.Group(DASH + "PLACEMENT" + "RECT" + polygon + SEMICOLON)
        place_bkgs = pp.OneOrMore(place_bkg)

        bkg_spacing = pp.Group("SPACING" + integer)
        route_bkg = pp.Group(DASH + "LAYER" + layerName + PLUS + pp.ZeroOrMore(bkg_spacing) + "POLYGON" +polygon + SEMICOLON
        route_bkgs = pp.OneOrMore(route_bkg)
        bkg_section = pp.Group("BLOCKAGES" + integer + place_bkgs + route_bkgs + SEMICOLON)
'''

