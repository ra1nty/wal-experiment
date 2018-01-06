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
   'NUMBER',
   'WS',
   'NEWLINE',
   'COLON'
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
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COLON = r':'
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
    r'(\d+(\.\d*)?|\.\d+)([eE][-+]? \d+)?'
    t.value = decimal.Decimal(t.value)
    return t

def t_STRING(t):
	r'\"(.)*?\"'
	t.value = t.value.replace('"','')
	return t

#t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.type = "NEWLINE"
    if t.lexer.paren_count == 0:
        return t


def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

def find_column(input,token):
	last_cr = input.rfind('\n',0,token.lexpos)
	if last_cr < 0:
		last_cr = 0
	column = (token.lexpos - last_cr) + 1
	return column

def t_WS(t):
    r' [ ]+ '
    if t.lexer.at_line_start and t.lexer.paren_count == 0:
        return t

def t_LBRACE(t):
    r'\('
    t.lexer.paren_count += 1
    return t

def t_RPAREN(t):
    r'\)'
    # check for underflow?  should be the job of the parser
    t.lexer.paren_count -= 1
    return t

NO_INDENT = 0
MAY_INDENT = 1
MUST_INDENT = 2

def track_tokens_filter(lexer, tokens):
    lexer.at_line_start = at_line_start = True
    indent = NO_INDENT
    saw_colon = False
    for token in tokens:
        token.at_line_start = at_line_start

        if token.type == "COLON":
            at_line_start = False
            indent = MAY_INDENT
            token.must_indent = False

        elif token.type == "NEWLINE":
            at_line_start = True
            if indent == MAY_INDENT:
                indent = MUST_INDENT
            token.must_indent = False

        elif token.type == "WS":
            assert token.at_line_start == True
            at_line_start = True
            token.must_indent = False

        else:
            # A real token; only indent after COLON NEWLINE
            if indent == MUST_INDENT:
                token.must_indent = True
            else:
                token.must_indent = False
            at_line_start = False
            indent = NO_INDENT

        yield token
        lexer.at_line_start = at_line_start

def _new_token(type, lineno):
    tok = lex.LexToken()
    tok.type = type
    tok.value = None
    tok.lineno = lineno
    return tok

def DEDENT(lineno):
    return _new_token("DEDENT", lineno)

def INDENT(lineno):
    return _new_token("INDENT", lineno)

def indentation_filter(tokens):
    # A stack of indentation levels; will never pop item 0
    levels = [0]
    token = None
    depth = 0
    prev_was_ws = False
    for token in tokens:
        print "Process", token,
        if token.at_line_start:
        	print "at_line_start",
        if token.must_indent:
        	print "must_indent",
        
        # WS only occurs at the start of the line
        # There may be WS followed by NEWLINE so
        # only track the depth here.  Don't indent/dedent
        # until there's something real.
        if token.type == "WS":
            assert depth == 0
            depth = len(token.value)
            prev_was_ws = True
            # WS tokens are never passed to the parser
            continue

        if token.type == "NEWLINE":
            depth = 0
            if prev_was_ws or token.at_line_start:
                # ignore blank lines
                continue
            # pass the other cases on through
            yield token
            continue

        # then it must be a real token (not WS, not NEWLINE)
        # which can affect the indentation level

        prev_was_ws = False
        if token.must_indent:
            # The current depth must be larger than the previous level
            if not (depth > levels[-1]):
                raise IndentationError("expected an indented block")

            levels.append(depth)
            yield INDENT(token.lineno)

        elif token.at_line_start:
            # Must be on the same level or one of the previous levels
            if depth == levels[-1]:
                # At the same level
                pass
            elif depth > levels[-1]:
                raise IndentationError(
                    "indentation increase but not in new block")
            else:
                # Back up; but only if it matches a previous level
                try:
                    i = levels.index(depth)
                except ValueError:
                    raise IndentationError("inconsistent indentation")
                for _ in range(i + 1, len(levels)):
                    yield DEDENT(token.lineno)
                    levels.pop()

        yield token
    ### Finished processing ###

    # Must dedent any remaining levels
    if len(levels) > 1:
        assert token is not None
        for _ in range(1, len(levels)):
            yield DEDENT(token.lineno)






lexer = lex.lex()

data = '''
url <- "http://uiuc.edu"
open url
fill (find "#netid") "yutang2"
fill (find "#easpass") "19970202"
click (find ".bttn")
if remain >= 1:
	fill (find "#netid") "yutang2"
'''
lexer.input(data)

# Tokenize
while True:
	tok = lexer.token()
	if not tok: 
		break      # No more input
	print(tok)
