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
   'GEQ',
   'LEQ',
   'GT',
   'LT',
   'EQ',
   'NUMBER'
)

reserved = {
	'if'   : 'IF',
	'then' : 'THEN',
	'else' : 'ELSE',
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
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_GEQ = r'>='
t_LEQ = r'<='
t_GT = r'>'
t_LT = r'<'
t_EQ = r'=='

def t_NAME(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	if t.value in reserved:
		t.type = reserved[t.value]
	return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
	r'\"(.)*?\"'
	t.value = t.value.replace('"','')
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
if remain >= 1
	then fill (find "#netid") "yutang2"
	else 
'''
lexer.input(data)

# Tokenize
while True:
	tok = lexer.token()
	if not tok: 
		break      # No more input
	print(tok)

names = {}

class Expr: pass
'''
class FindOp(Expr):
	def __init__(self, )


class BinOp(Expr):
    def __init__(self,left,op,right):
        self.type = "binop"
        self.left = left
        self.right = right
        self.op = op

class Number(Expr):
    def __init__(self,value):
        self.type = "number"
        self.value = value

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''

    p[0] = BinOp(p[1],p[2],p[3])
'''

class Node:
    def __init__(self,type,children=None,leaf=None):
         self.type = type
         if children:
              self.children = children
         else:
              self.children = [ ]
         self.leaf = leaf
	 
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''

    p[0] = Node("binop", [p[1],p[3]], p[2])


def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = Number(p[1])


def p_statement_assign(p):
    'statement : NAME ASSIGN expression'
    names[p[1]] = p[3]
def p_expression(p):
	'''expression : elementexpr
				  | stringexpr'''
	p[0] = p[1]

def p_expression_paren(p):
	'expression : LPAREN expression RPAREN'
	p[0] = p[2]

def p_statement_find(p):
	'elementexpr : FIND STRING'


def p_statement_fill(p):
    'statement : FILL elementexpr stringexpr'
    p[2].send_keys(p[3])

def p_expression_string_concat(p):
	'stringexpr : STRING PLUS STRING'
	p[0] = p[1] + p[3]


yacc.yacc()