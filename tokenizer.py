from ply import lex as lex

tokens = (
   'ADD',
   'EQUAL',
   'ASSIGN',
   'STRING',
   'NAME',
   'DQUOTE',
   'SQUOTE',
   'LPAREN',
   'RPAREN',
   'LBRACE',
   'RBRACE',
)

reserved = {
    'fill' : 'FILL',
    'open' : 'OPEN',
    'click': 'CLICK',
    'find' : 'FIND'
}

tokens += tuple(reserved.values())

t_EQUAL  = r'='
t_ASSIGN = r'<-'
t_ADD = r'\+'
t_DQUOTE = r'\"'
t_SQUOTE = r'\''
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_STRING = r'\"(.)*?\"'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

def t_NAME(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	if t.value in reserved:
		t.type = reserved[t.value]
	return t

t_ignore = ' \t'

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

def find_column(input,token):
	last_cr = input.rfind('\n',0,token.lexpos)
	if last_cr < 0:
		last_cr = 0
	column = (token.lexpos - last_cr) + 1
	return column



lexer = lex.lex()

data = '''
url <- "http://uiuc.edu"
open url
fill (find "#netid") "yutang2"
fill (find "#easpass") "19970202"
click (find ".bttn")
'''
lexer.input(data)

# Tokenize
while True:
	tok = lexer.token()
	if not tok: 
		break      # No more input
	print(tok)

