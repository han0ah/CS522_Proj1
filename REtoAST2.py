# http://www.dabeaz.com/ply/ply.html 의 PLY 예시 소스코드를 참조하여 수정하였습니다.
import ply.lex as lex

######################### lex에 대한 정의 ###########################
# List of token names.   This is always required
tokens = (
   'SYMBOL',
   'PLUS',
   'STAR',
   'LPAREN',
   'RPAREN',
)

# Regular expression rules for simple tokens
t_SYMBOL  = r'[a-zA-z0-9_\u3131-\u3163]'
t_PLUS    = r'\+'
t_STAR   = r'\*'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

####### Parsing 시 호출되며 구성하기 위한 AST에 대한 정의 #######
# AST의 node 하나를 나타내는 class
class NodeInAST():
    def __init__(self,tag):
        self.tag = tag
        self.left_child = None
        self.right_child = None

# F -> F*
def get_star_value(p):
    newNode = NodeInAST('*')
    newNode.left_child = p[0]
    return newNode

# T -> TF
def get_concate_value(p):
    newNode = NodeInAST('.')
    newNode.left_child = p[0]
    newNode.right_child = p[1]
    return newNode

# E -> E+T
def get_plus_value(p):
    newNode = NodeInAST('+')
    newNode.left_child = p[0]
    newNode.right_child = p[2]
    return newNode

# P -> (E)
def get_paren_value(p):
    return p[1]

# P -> Symbol
def get_symbol_value(p):
    return NodeInAST(p[0])


######################### Parsing 구현 ###########################

# Stack에 들어가는 옵션 'P', 'T', 'F', 'E'
parse_stack = []

rules = []

# regular expression의 기본 rule
# 0(symbol), 1(parenthe), 2, 3(star), 4, 5(plus), 6
rules.append([(['SYMBOL'], 'P'),(['LPAREN','E','RPAREN'], 'P'),
            (['P','F']), (['F','STAR'], 'F'),
            (['T','F'], 'T'),
            (['E','PLUS','T'], 'E')])
# stack에서 함부로 사용할 수 없는 rule
rules.append([(['F'],'T')])
rules.append([(['T'],'E')])


def updateStackTop(useRule1=True, useRule2=False, useRule3=False):
    global parse_stack

    if (len(parse_stack) == 0):
        return False

    for ruleNum in range(3):
        if (ruleNum == 0 and useRule1 == False):
            continue
        if (ruleNum == 1 and useRule2 == False):
            continue
        if (ruleNum == 2 and useRule3 == False):
            continue
        for rule in rules[ruleNum]:
            rulelen = len(rule[0])
            if (rulelen > len(parse_stack)):
                continue

            # 현재 Rule과 같은 Patter인지 판별한다.
            same_pattern = True
            for i in range(1,rulelen+1):
                if (parse_stack[-1*i][0] != rule[0][-1*i]):
                    same_pattern=False
                    break

            params = []
            if( same_pattern ):
                for i in range(rulelen):
                    t=parse_stack.pop()
                    params.append(t[1])
                params.reverse()

                # stack top을 보면서 rule 변환에 따르는 알맞은 AST 생성(조합) 값을 설정해준다.
                if (rule[0][0] == 'SYMBOL'):
                    new_value = get_symbol_value(params)
                elif (rule[0][0] == 'LPAREN'):
                    new_value = get_paren_value(params)
                elif (rulelen > 1 and rule[0][0] == 'F' and rule[0][1] == 'STAR'):
                    new_value = get_star_value(params)
                elif (rulelen > 1 and rule[0][0] == 'E' and rule[0][1] == 'PLUS'):
                    new_value = get_plus_value(params)
                elif (rulelen > 1 and rule[0][0] == 'T' and rule[0][1] == 'F'):
                    new_value = get_concate_value(params)
                else:
                    new_value = params[0]

                parse_stack.append((rule[1], new_value))
                return True

    return False



def getASTfromRegExpStr(regExpStr):
    lexer.input(regExpStr)

    # 반복문을 돌면서 Token을 하나씩 소비한다.
    while True:
        tok = lexer.token()
        if not tok:
            break

        # Stack에 Special Rule 적용
        if(len(parse_stack) > 0):
            if (parse_stack[-1][0] == 'F'): # T -> F Rule 적용 ( stack 에서는 F 가 T로 변함 )
                if (tok.type != 'STAR'):
                    updateStackTop(useRule2=True)
            if (parse_stack[-1][0] == 'T'): # E -> T Rule 적용 ( stack 에서는 T 가 E로 변함 )
                if (tok.type == 'RPAREN' or tok.type == 'PLUS'):
                    updateStackTop(useRule3=True)

        parse_stack.append((tok.type, tok.value))

        while(updateStackTop()):
            pass

    while(updateStackTop(useRule2=True, useRule3=True)):
        pass

    if (len(parse_stack) == 1 and parse_stack[0][0] == 'E'):
        return parse_stack[0][1]
    return None