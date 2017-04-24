# http://www.dabeaz.com/ply/ply.html 의 PLY 예시 소스코드를 참조하여 수정하였습니다.

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