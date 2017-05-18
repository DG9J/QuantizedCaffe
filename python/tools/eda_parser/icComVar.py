import pyparsing as pp

#Define the special variables
PLUS, DASH = map(pp.Suppress, "+-")
COLON, LBRACK, RBRACK, LBRACE, RBRACE, TILDE, CARAT, COMMA = map(pp.Suppress, ":[]{}~^,")
UNDERSCORE, DOT, BSLASH, SLASH = map(pp.Literal, '_./\\')
LPAR, RPAR = map(pp.Suppress, "()")
SEMICOLON, DQUOTA = map(pp.Suppress, ';"')
SQUOTA = map(pp.Suppress, "'")
STAR = map(pp.Literal, '*')

dashLine = pp.Suppress(pp.Group(pp.OneOrMore('-')))
starLine = pp.Suppress(pp.Group(pp.OneOrMore('*')))
date     = pp.Word(pp.alphanums + " " + ":")

##quota define
squotes     = pp.QuotedString("'")
dquotes     = pp.QuotedString('"')
stars  = pp.QuotedString('*')
eques    = pp.QuotedString('=')
tildes = pp.QuotedString('~')
angles = pp.QuotedString('<', endQuoteChar='>')
braces = pp.QuotedString('{', endQuoteChar='}')
bracks = pp.QuotedString('[', endQuoteChar=']')
paras   = pp.QuotedString('(', endQuoteChar=')')


#Define the name rule
floatNum       = pp.Word(pp.nums + '.' + "_" + "-")
floatZero      = pp.Word("0" + '.')
intNum         = pp.Word(pp.nums + '-')
flatName       = pp.Word(pp.alphanums + "_")
hierName       = pp.Word(pp.alphanums + '/' + '_' + '[' + ']')
libCellName    = pp.Word(pp.alphas.upper() + pp.nums + "_")

#Timing related
toggleType  = pp.Word("r" + "f" + "rise" + "fall")
pathType    = pp.Word("min" + "max" + "Min" + "Max")
pathCol     = pp.Word("Fanout" + "Cap" + "Trans" + "Incr" + "Path")
clkType     = pp.Word("ideal" + "propagated")
annoType    = pp.Word("&" + "*")
pathGroup   = pp.Word(pp.alphanums + '\*' + '_' + "'")
scenarioName= pp.Word(pp.alphanums + "_" + "'")

#DEF varible
orient          = pp.oneOf('N' + 'E' + 'W' + 'S' + 'FN' + 'FE' + 'FW' + 'FS')
routeDir        = pp.oneOf('X' + 'Y')
placeStatus     = pp.oneOf('PLACED' + "FIXED" + "COVER" + "UNPLACED")
oxide           = pp.oneOf("OXIDE1" + "OXIDE2" + "OXIDE3" + "OXIDE4")
pinDir          = pp.oneOf('INPUT' + "OUTPUT" + "INOUT")
pinUse          = pp.oneOf("SIGNAL"+ "POWER" + "GROUND" + "CLOCK" + "TIEOFF" + "ANALOG" + "SCAN" + "RESET")
propType        = pp.oneOf('INTERGER' + 'REAL' + 'STRING')
objectType      = pp.oneOf("DESIGN" + "COMPONENT" + "NET" + "SPECIALNET" + "GROUP" + "ROW" + "COMPONENT" + "REGION")
pinAttr         = pp.oneOf("SPECIA DIRECTION  NETEXPR SUPPLYSENSITIVITY GROUNDSENSITIVITY USE ANTENNAPINMAXAREACAR ANTENNAPINMAXCUTCAR ANTENNAPINDIFFAREA ANTENNAMODEL ANTENNAPINGATEAREA ANTENNAPINPARTIALMETALAREA ANTENNAPINPARTIALMETALAREA ANTENNAPINPARTIALCUTAREA")
routeBkgAttr    = pp.oneOf("SLOTS FILLS PUSHDOWN EXCEPTPGNET COMPONENT SPACING DESIGNRULEWIDTH MASK")
cellBkgAttr     = pp.oneOf("SOFT PARTIAL COMPONENT PUSHDOWN")

# polygon
origX        = pp.Word(pp.nums + "*" + "-")
origY        = pp.Word(pp.nums + "*" + "-")
orig         = pp.Group(pp.Optional(LPAR) + origX + origY + pp.Optional(RPAR))
rectangle    = pp.Group(orig + orig)
polygon      = pp.Group(orig + pp.OneOrMore(orig))

# Process Varible
layerName    = pp.oneOf('M0' + 'M1' + 'M2' + 'M3' + 'M4' + 'M5' + 'M6' + 'M7' + 'M8' + 'M10' + 'M11' + 'M12' +
                      'VIA0' + 'VIA1' + 'VIA2' + 'VIA3' + 'VIA4' + 'VIA5' + 'VIA6' + 'VIA7' + 'VIA8' + 'VIA10' + 'VIA11' + 'VIA12')
metalName    = pp.oneOf('M0' + 'M1' + 'M2' + 'M3' + 'M4' + 'M5' + 'M6' + 'M7' + 'M8' + 'M10' + 'M11' + 'M12')
cutName = pp.oneOf('VIA0' + 'VIA1' + 'VIA2' + 'VIA3' + 'VIA4' + 'VIA5' + 'VIA6' + 'VIA7' + 'VIA8' + 'VIA10' + 'VIA11' + 'VIA12')



