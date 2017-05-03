from pyparsing import *

text = '''
a = 10
a_2=100
pi=3.14159
goldenRatio = 1.61803
E = mc2
'''

identifier = Word(alphas, alphanums+'_')
number = Word(nums+".")
assignmentExpr = identifier + "=" + (identifier | number)

assignmentTokens = assignmentExpr.parseString(text)
print assignmentTokens
assignmentExpr = identifier.setResultsName("lhs") + "=" + \
(identifier | number).setResultsName("rhs")
assignmentTokens = assignmentExpr.parseString( text )
print assignmentTokens.rhs, "is assigned to", assignmentTokens.lhs

tests = "Hi, Mom! Good morning, Miss Crabtree!
Yo, Adrian!
Whattup, G?
How's it goin', Dude?
Hey, Jude!
Goodbye, Mr. Chips!
"
word = Word(alphas+"'.")
salutation = OneOrMore(word)
comma = Literal(",")
greetee = OneOrMore(word)
endpunc = oneOf("! ?")
greeting = salutation + comma + greetee + endpunc

for t in tests:
    print t
    results = greeting.parseString(t)
    salutation = []
    for token in results:
        if token == ",": break
        salutation.append(token)
    print salutation