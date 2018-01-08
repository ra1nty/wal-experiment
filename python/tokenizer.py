names = {}

class Node:
    def __init__(self,type,children=None,leaf=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = []
        self.leaf = leaf

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''

    p[0] = Node("binop", [p[1],p[3]], p[2])


def p_expression_paren(p):
    'expression : LPAREN expression RPAREN'
    p[0] = Node("paren", [p[2]])

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = Node("number", [], p[1])

def p_statement_assign(p):
    'statement : NAME ASSIGN expression'
    names[p[1]] = p[3]

def p_expression(p):
	'''expression : elementexpr
				  | stringexpr'''
	p[0] = p[1]

def p_statement_find(p):
	'elementexpr : FIND STRING'
    p[0] = Node("find", [], p[2])

def p_statement_fill(p):
    'statement : FILL expression stringexpr'
    p[0] = Node("fill", [p[2]], p[3])

def p_expression_string(p):
    'stringexpr : STRING'
    p[0] = p[1]

def p_expression_string_concat(p):
	'stringexpr : STRING PLUS STRING'
	p[0] = p[1] + p[3]

# Catch catastrophic error, return nothing
def p_program_error(p):
    '''program : error'''
    p[0] = None
    p.parser.error = 1

# Empty
def p_empty(p):
    '''empty : '''

# Catastrophic error handler
def p_error(p):
    if not p:
        print("SYNTAX ERROR AT EOF")

walParser = yacc.yacc()

def parse(data, debug=0):
    walParser.error = 0
    p = walParser.parse(data, debug=debug)
    if walParser.error:
        return None
    return p