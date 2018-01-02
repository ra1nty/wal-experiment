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