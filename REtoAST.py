# http://www.dabeaz.com/ply/ply.html 의 PLY 예시 소스코드를 참조하여 수정하였습니다.

# Yacc example

import ply.yacc as yacc
# Get the token map from the lexer.  This is required.
from regexplex import tokens


# AST의 node 하나를 나타내는 class
class NodeInAST():
    def __init__(self,tag):
        self.tag = tag
        self.left_child = None
        self.right_child = None

precedence = (
    ('left', 'CONCAT'),
    ('left', 'STAR'),
)

# E -> E*
def p_expression_star(p):
    'expression : expression STAR'
    newNode = NodeInAST('*')
    newNode.left_child = p[1]
    p[0] = newNode

# E -> EE
def p_expression_concate(p):
    'expression : expression expression %prec CONCAT'
    newNode = NodeInAST('.')
    newNode.left_child = p[1]
    newNode.right_child = p[2]
    p[0] = newNode

# E -> E+E
def p_expression_plus(p):
    'expression : expression PLUS expression'
    newNode = NodeInAST('+')
    newNode.left_child = p[1]
    newNode.right_child = p[3]
    p[0] = newNode

# E -> (E)
def p_expression_in_parenthesis(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

# E -> V
def p_expression_symbol(p):
    'expression : SYMBOL'
    p[0] = NodeInAST(p[1])


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# RegularExpression 문자열로 부터 AST를 얻는다.
'''
def getASTfromRegExpStr(s):
    parser = yacc.yacc()
    return parser.parse(s)
'''