# http://www.dabeaz.com/ply/ply.html 의 PLY 예시 소스코드를 참조하여 수정하였습니다.
# http://matt.might.net/articles/parsing-regex-with-recursive-descent/ 참조
import ply.lex as lex

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

regExpStr = '((a+bc+c)(t+ry))*'
lexer.input(regExpStr)

# Stack에 들어가는 옵션 'P', 'T', 'F', 'E'
parse_stack = []

rules = []

# regular expression의 기본 rule
rules.append([(['SYMBOL'], 'P'),(['LPAREN','E','RPAREN'], 'P'),
            (['P','F']), (['F','STAR'], 'F'),
            (['T','F'], 'T'),
            (['E','PLUS','T'], 'E'), (['T'], 'E')])
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

            if( same_pattern ):
                for i in range(rulelen):
                    parse_stack.pop()
                parse_stack.append((rule[1], 'Some_Value'))
                return True

            debug = 1
    return False


updateStackTop()
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
    print(tok)

while(updateStackTop(useRule2=True, useRule3=True)):
    pass

debug = 1