import sys
import os
import shutil
import re
import gzip
import pyparsing as pp
import icComVar as icVar
import fileinput as fi
import numpy as np
from multiprocessing import Pool
from multiprocessing import process

class parse_def():
    '''
    defHeader
    defRow
    defTrack
    defVia
    defNDR
    defRegion
    defComp
    defPin
    defBkg
    '''
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
        compMaskShift   =  pp.Group("COMPONENTMASKSHIFT " + pp.OneOrMore(icVar.layerName))
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
        cellLoc  = pp.Group(icVar.PLUS + icVar.placeStatus + pp.Optional(icVar.orig)  + pp.Optional(icVar.orient) )
        compDefine = pp.Group(icVar.DASH + icVar.hierName + icVar.hierName +
                              pp.Optional(icVar.PLUS + "EEQMASTER" + icVar.hierName) +
                              pp.Optional(icVar.PLUS + "SOURCE" + pp.oneOf("NETLIST DIST USER TIMING")) +
                              pp.Optional(cellLoc) +
                              pp.Optional(icVar.PLUS + maskShift) +
                              pp.Optional(icVar.PLUS + "HALO" + pp.Optional("SOFT") + icVar.rectangle) +
                              pp.Optional(icVar.PLUS + "ROUTEHALO" + icVar.intNum + icVar.layerName + icVar.layerName) +
                              pp.Optional(icVar.PLUS + "WEIGHT" + icVar.intNum) +
                              pp.Optional(icVar.PLUS + "REGION" + icVar.hierName) +
                              pp.Optional(icVar.propDefine) +
                              icVar.SEMICOLON
                              )
        compSect = pp.Group("COMPONENTS" + icVar.intNum  + icVar.SEMICOLON + pp.OneOrMore(compDefine) + "END COMPONENTS")

    def get_values(self,lVals):
        for val in lVals:
            if isinstance(val,list):
                self.get_values(val)
            else:
                #print "list element",len(val),type(val),val
                self.result.append(val)
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
        portStatDefine = pp.Group(icVar.placeStatus + icVar.orig + icVar.orient)

        portDefine = pp.Group(pp.Optional(icVar.PLUS + "PORT") +
                              pp.Optional(portLayerDefine) +
                              pp.Optional(portPolygonDefine) +
                              pp.Optional(portViaDefine) +
                              pp.Optional(portStatDefine)
                              )
        pinAttr        = pp.Group(icVar.PLUS + icVar.pinAttr + pp.Optional(icVar.hierName))
        portAttrDefine = pp.Group(icVar.PLUS + "NET" + icVar.hierName +
                                  pp.ZeroOrMore(pinAttr)
                                  )

        pinDefine = pp.Group(icVar.DASH + icVar.hierName +
                             portAttrDefine +
                             pp.Optional(portDefine)
                             )
        defFile = fi.FileInput(self.defFile, openhook=fi.hook_compressed)
        for line0 in defFile:
            if line0.find('PINS') == 0:
                allPin = []
                singlePin = []
                for line1 in defFile:
                    if line1.find('END PINS') == 0:
                        str1 = ''.join(allPin)
                        #result = pinDefine.searchString(str1)
                        #print str1
                        break
                    else:
                        if line1.find(';') > -1:
                            singlePin.append(line1)
                            singlePinString =''.join(singlePin)
                            allPin.append(singlePinString)
                            #result = self.pattern_match(pinDefine,singlePinString)
                            #self.result = []
                            #self.get_values(result)
                            #print "pin:",len(singlePinString),type(result),self.result
                            #print defFile.lineno(),self.result
                            #print singlePinString
                            singlePin = []
                        else:
                            singlePin.append(line1)
                results = self.MP_pattern_match(pinDefine,allPin)
                #output = [pt.get() for pt in results]
                print type(results),len(results)
                for pt in results:
                    print type(pt)
            #else:
            #    print "finished", line0.strip()
        #print "complete read the", rpt_file
        return results


    def defBkg(self):
        #blockage
        layerBkg = pp.Group(icVar.DASH + "LAYER" + icVar.layerName +
                            pp.Optional(icVar.routeBkgAttr + pp.Optional(icVar.hierName)) +
                            pp.OneOrMore(pp.oneOf("RECT POLYGON") + icVar.polygon) +
                            icVar.SEMICOLON
                            )
        cellBkg  = pp.Group(icVar.DASH + "PLACEMENT" +
                            pp.Optional(icVar.cellBkgAttr + pp.Optional(icVar.hierName)) +
                            pp.OneOrMore("RECT" + icVar.polygon) +
                            icVar.SEMICOLON
                            )
        bkgSect = pp.Group( "BLOCKAGES" + icVar.intNum +
                            pp.ZeroOrMore(layerBkg) +
                            pp.ZeroOrMore(cellBkg)
                           )

        defFile = fi.FileInput(self.defFile, openhook=fi.hook_compressed)
        for line0 in defFile:
            if line0.find('BLOCKAGES') == 0:
                allPin = []
                singlePin = []
                for line1 in defFile:
                    if line1.find('END BLOCKAGES') == 0:
                        str1 = ''.join(allPin)
                        # result = pinDefine.searchString(str1)
                        # print str1
                        break
                    else:
                        if line1.find(';') > -1:
                            singlePin.append(line1)
                            singlePinString = ''.join(singlePin)
                            allPin.append(singlePinString)
                            # result = self.pattern_match(pinDefine,singlePinString)
                            # self.result = []
                            # self.get_values(result)
                            # print "pin:",len(singlePinString),type(result),self.result
                            # print defFile.lineno(),self.result
                            # print singlePinString
                            singlePin = []
                        else:
                            singlePin.append(line1)
                results = self.MP_pattern_match(cellBkg, allPin)
                # output = [pt.get() for pt in results]
                print type(results), len(results)
                for pt in results:
                    print type(pt)
                    # else:
                    #    print "finished", line0.strip()
        # print "complete read the", rpt_file
        return results

    def pattern_match(self,pattern,target_string):
        #print "pattern:", pattern
        #print "target:", target_string
        result = pattern.searchString(target_string).asList()
        #print "result:", result
        return result
    def MP_pattern_match(self,pattern,target_list):
        #print('Run task %s (%s)...' % (name, os.getpid()))
        #start = time.time()
        p = Pool(4)
        results = [p.apply_async(self.pattern_match, args=(pattern, target_list[i])) for i in range(1, len(target_list))]
        #end = time.time()
        #print('Task %s runs %0.2f seconds.' % (name, (end - start)))
        #print
        return results
