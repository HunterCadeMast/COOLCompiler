# Hunter Mast / hunter.c.mast@vanderbilt.edu
# Referenced code from Dr. Leach's video on PA3.

import sys
import ply.lex as lex
import ply.yacc as yacc

# We start out by getting all of the information from our '.cl-lex' file and create an AST file.
input_filename = sys.argv[1]
# This section will remove the '.cl-lex' section and replace it with '.cl-ast', unless it does not have '.cl-lex' and it will just add '.cl-ast'.
if input_filename.endswith('.cl-lex'):
    output_filename = input_filename[:-len('.cl-lex')] + '.cl-ast'
else:
    output_filename = input_filename + '.cl-ast'
# Here, we read every line from our lexed file and place it into a list.
input_lines = []
with open(input_filename) as f:
    input_lines = [x[:-1] if x.endswith('\n') else x for x in f.readlines()]
# This will access the total number of classes in our COOL program.
class_count = 0

# Here, we get information from our lex file that we will eventually send from LEX to YACC.
class PA2Lexer(object):
    def token(self):
        # We return 'None' if the file is empty.
        global input_lines
        if len(input_lines) == 0:
            return None
        # The format of a lexed file is [line number, type, and lexme token].
        # We get all of this info and place it into our 'input_lines' list.
        line_number = input_lines.pop(0)
        token_type = input_lines.pop(0)
        token_lexme = ""
        if token_type in ['type', 'identifier', 'string', 'integer']:
            token_lexme = input_lines.pop(0)
        # We get our list of tokens that we return here with all the information we need on it.
        return_token = lex.LexToken()
        return_token.lineno = int(line_number)
        return_token.value = token_lexme
        return_token.type = token_type.upper()
        return_token.lexpos = 0
        # The comment below was used for debugging:
        # print(f"Token: {return_token.type} at line {return_token.lineno}")
        return return_token

# List of all tokens.
tokens = [
    "AT",
    "CASE",
    "CLASS",
    "COLON",
    "COMMA",
    "DIVIDE",
    "DOT",
    "ELSE",
    "EQUALS", 
    "ESAC",
    "FALSE",
    "FI",
    "IDENTIFIER",
    "IF",
    "IN",
    "INHERITS",
    "INTEGER", 
    "ISVOID",
    "LARROW",
    "LBRACE",
    "LE",
    "LET",
    "LOOP",
    "LPAREN",
    "LT",
    "MINUS", 
    "NEW",
    "NOT",
    "OF",
    "PLUS",
    "POOL",
    "RARROW",
    "RBRACE",
    "RPAREN",
    "SEMI", 
    "STRING",
    "THEN",
    "TILDE",
    "TIMES",
    "TRUE",
    "TYPE",
    "WHILE"
]

# List of precedence and associativity.
precedence = (
    ('right', 'LARROW'),
    ('nonassoc', 'EQUALS', 'LT', 'LE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'ISVOID', 'TILDE', 'NOT'),
    ('left', 'DOT', 'AT'),
    ('nonassoc', 'LPAREN', 'RPAREN'),
    ('nonassoc', 'LBRACE', 'RBRACE')
)

class ASTNode(object):
    pass

# Class nodes.
class ClassList(ASTNode):
    def __init__ (self, children):
        self.children = children

# ClassNoInherits and ClassInherits both check if each class matches certain criteria and will print with it's features, as long as the class is not empty.
class ClassNoInherits(ASTNode):
    def __init__ (self, lineno, typename, featurelist):
        self.lineno = lineno
        self.typename = typename
        self.featurelist = featurelist

    def __repr__ (self):
        features = "\n".join(str(feature) for feature in self.featurelist)
        if features:
            return f"{self.lineno}\n{self.typename}\nno_inherits\n{len(self.featurelist)}\n{features}"
        else:
            return f"{self.lineno}\n{self.typename}\nno_inherits\n{len(self.featurelist)}"

class ClassInherits(ASTNode):
    def __init__ (self, lineno, typename, featurelist, inheritsfrom):
        self.lineno = lineno
        self.typename = typename
        self.featurelist = featurelist
        self.inheritsfrom = inheritsfrom

    def __repr__ (self):
        features = "\n".join(str(feature) for feature in self.featurelist)
        if features:
            return f"{self.lineno}\n{self.typename}\ninherits\n{self.lineno}\n{self.inheritsfrom}\n{len(self.featurelist)}\n{features}"
        else:
            return f"{self.lineno}\n{self.typename}\ninherits\n{self.lineno}\n{self.inheritsfrom}\n{len(self.featurelist)}"

# Feature nodes.
class Attribute(ASTNode):
    def __init__(self, lineno, name, typename, init_expr = None):
        self.lineno = lineno
        self.name = name
        self.typename = typename
        self.init_expr = init_expr

    def __repr__(self):
        if self.init_expr:
            return f"attribute_init\n{self.lineno}\n{self.name}\n{self.lineno}\n{self.typename}\n{self.init_expr}"
        else:
            return f"attribute_no_init\n{self.lineno}\n{self.name}\n{self.lineno}\n{self.typename}"

# With Method, we make sure to check the list of formals (Parameters) are zero or not.
# We also use '.join' so that we print our list of formals as a string, not just a list.
class Method(ASTNode):
    def __init__(self, lineno, name, formals, return_type, body):
        self.lineno = lineno
        self.name = name
        self.formals = formals
        self.return_type = return_type
        self.body = body

    def __repr__(self):
        formal_List = "\n".join(str(formal) for formal in self.formals)
        if len(self.formals) <= 0:
            return f"method\n{self.lineno}\n{self.name}\n{len(self.formals)}\n{self.lineno}\n{self.return_type}\n{self.body}"
        else:
            return f"method\n{self.lineno}\n{self.name}\n{len(self.formals)}\n{formal_List}\n{self.lineno}\n{self.return_type}\n{self.body}"

class Formal(ASTNode):
    def __init__(self, lineno, name, typename, init_expr = None):
        self.lineno = lineno
        self.name = name
        self.typename = typename
        self.init_expr = init_expr

    def __repr__(self):
        if self.init_expr:
            return f"{self.lineno}\n{self.name}\n{self.lineno}\n{self.typename}\n{self.init_expr}"
        else:
            return f"{self.lineno}\n{self.name}\n{self.lineno}\n{self.typename}"

    # This is used to check if formals are present and initialized or not (Specifically LET conditions).
    def init_flag(self):
        return self.init_expr is not None

# Expression nodes.
class Dynamic_Dispatch(ASTNode):
    def __init__(self, lineno, obj, method, formals):
        self.lineno = lineno
        self.obj = obj
        self.method = method
        self.formals = formals

    def __repr__(self):
        formal_list = "\n".join(str(formal) for formal in self.formals)
        # With dispatch, we need to check and make sure that if the object is self dispatch, we recognize that.
        if self.obj == "self":
            if len(self.formals) <= 0:
                return f"{self.lineno}\nself_dispatch\n{self.lineno}\n{self.method}\n{len(self.formals)}"
            else:
                return f"{self.lineno}\nself_dispatch\n{self.lineno}\n{self.method}\n{len(self.formals)}\n{formal_list}"
        else:
            if len(self.formals) <= 0:
                return f"{self.lineno}\ndynamic_dispatch\n{self.obj}\n{self.lineno}\n{self.method}\n{len(self.formals)}"
            else:
                return f"{self.lineno}\ndynamic_dispatch\n{self.obj}\n{self.lineno}\n{self.method}\n{len(self.formals)}\n{formal_list}"

class Static_Dispatch(ASTNode):
    def __init__(self, lineno, obj, type_name, method, formals):
        self.lineno = lineno
        self.obj = obj
        self.type_name = type_name
        self.method = method
        self.formals = formals

    def __repr__(self):
        formal_list = "\n".join(str(formal) for formal in self.formals)
        if self.obj == "self":
            if len(self.formals) <= 0:
                return f"{self.lineno}\nself_dispatch\n{self.lineno}\n{self.method}\n{len(self.formals)}"
            else:
                return f"{self.lineno}\nself_dispatch\n{self.lineno}\n{self.method}\n{len(self.formals)}\n{formal_list}"
        else:
            if len(self.formals) <= 0:
                return f"{self.lineno}\nstatic_dispatch\n{self.obj}\n{self.lineno}\n{self.type_name}\n{self.lineno}\n{self.method}\n{len(self.formals)}"
            else:
                return f"{self.lineno}\nstatic_dispatch\n{self.obj}\n{self.lineno}\n{self.type_name}\n{self.lineno}\n{self.method}\n{len(self.formals)}\n{formal_list}"

# Most classes here follow this format of just passing a string with all of the information needed for that token.
class Assignment(ASTNode):
    def __init__(self, lineno, name, expr):
        self.lineno = lineno
        self.name = name
        self.expr = expr

    def __repr__(self):
        return f"{self.lineno}\nassign\n{self.lineno}\n{self.name}\n{self.expr}"

class If(ASTNode):
    def __init__(self, lineno, if_expr, then_expr, else_expr):
        self.lineno = lineno
        self.if_expr = if_expr
        self.then_expr = then_expr
        self.else_expr = else_expr

    def __repr__(self):
        return f"{self.lineno}\nif\n{self.if_expr}\n{self.then_expr}\n{self.else_expr}"

class While(ASTNode):
    def __init__(self, lineno, expr, body):
        self.lineno = lineno
        self.expr = expr
        self.body = body

    def __repr__(self):
        return f"{self.lineno}\nwhile\n{self.expr}\n{self.body}"

class Block(ASTNode):
    def __init__(self, lineno, exprlist):
        self.lineno = lineno
        self.exprlist = exprlist

    def __repr__(self):
        expression_list = "\n".join(str(expr) for expr in self.exprlist)
        return f"{self.lineno}\nblock\n{len(self.exprlist)}\n{expression_list}"

class Parentheses(ASTNode):
    def __init__(self, lineno, exprlist):
        self.lineno = lineno
        self.exprlist = exprlist

    def __repr__(self):
        expression_list = "\n".join(str(expr) for expr in self.exprlist)
        # Since RPAREN and LPAREN are not labeled in our '.cl-ast' file, we just send the expression list as a string inside of the parentheses.
        return f"{expression_list}"

class Let(ASTNode):
    def __init__(self, lineno, variables, body):
        self.lineno = lineno
        self.variables = variables
        self.body = body

    def __repr__(self):
        # Here, we are checking if the LET condition is empty.
        # The CASE condition is the same way, but for some reason I was not able to use a list when checking if 'self.variables' is empty.
        # My solution is instead pass it as a string and if it does not have anything, have it throw an error.
        if "" in self.variables:
            print(f"ERROR: {self.lineno}: Parser: Empty LET!")
            exit(1)
        # Each LET condition needs to print if it is 'let_binding_init' or 'let_binding_no_init', so I added this to a list that I would then join with newlines and then turn into a string.
        variable_list = []
        for variable in self.variables:
            if variable.init_flag():
                variable_list.append(f"let_binding_init\n{variable}")
            else:
                variable_list.append(f"let_binding_no_init\n{variable}")
        full_variable_list = "\n".join(str(variable) for variable in variable_list)
        return f"{self.lineno}\nlet\n{len(self.variables)}\n{full_variable_list}\n{self.body}"

class Case(ASTNode):
    def __init__(self, lineno, expr, actions):
        self.lineno = lineno
        self.expr = expr
        self.actions = actions

    def __repr__(self):
        # We throw an error if the CASE condition is empty.
        if not self.actions:
            print(f"ERROR: {self.lineno}: Parser: Empty CASE!")
            exit(1)
        action = "\n".join(str(action) for action in self.actions)
        return f"{self.lineno}\ncase\n{self.expr}\n{len(self.actions)}\n{action}"

class CaseCondition(ASTNode):
    def __init__(self, lineno, variable, typename, body):
        self.lineno = lineno
        self.variable = variable
        self.typename = typename
        self.body = body

    def __repr__(self):
        return f"{self.lineno}\n{self.variable}\n{self.lineno}\n{self.typename}\n{self.body}"

class BinaryOperation(ASTNode):
    def __init__(self, lineno, left_expr, operation, right_expr):
        self.lineno = lineno
        self.left_expr = left_expr
        self.operation = operation
        self.right_expr = right_expr

    def __repr__(self):
        return f"{self.lineno}\n{self.operation}\n{self.left_expr}\n{self.right_expr}"

class Not(ASTNode):
    def __init__(self, lineno, expr):
        self.lineno = lineno
        self.expr = expr

    def __repr__(self):
        return f"{self.lineno}\nnot\n{self.expr}"

class IsVoid(ASTNode):
    def __init__(self, lineno, expr):
        self.lineno = lineno
        self.expr = expr

    def __repr__(self):
        return f"{self.lineno}\nisvoid\n{self.expr}"

class Tilde(ASTNode):
    def __init__(self, lineno, expr):
        self.lineno = lineno
        self.expr = expr

    def __repr__(self):
        return f"{self.lineno}\nnegate\n{self.expr}"

class Integer(ASTNode):
    def __init__(self, lineno, integer_value):
        self.lineno = lineno
        self.integer_value = integer_value

    def __repr__(self):
        return f"{self.lineno}\ninteger\n{self.integer_value}"

class String(ASTNode):
    def __init__(self, lineno, string_value):
        self.lineno = lineno
        self.string_value = string_value

    def __repr__(self):
        return f'{self.lineno}\nstring\n{self.string_value}'

class Boolean(ASTNode):
    def __init__(self, lineno, boolean_value):
        self.lineno = lineno
        self.boolean_value = boolean_value

    def __repr__(self):
        return f'{self.lineno}\n{self.boolean_value}'

class NewObject(ASTNode):
    def __init__(self, lineno, typename):
        self.lineno = lineno
        self.typename = typename

    def __repr__(self):
        return f"{self.lineno}\nnew\n{self.lineno}\n{self.typename}"

class Identifier(ASTNode):
    def __init__(self, lineno, name):
        self.lineno = lineno
        self.name = name

    def __repr__(self):
        return f"{self.lineno}\nidentifier\n{self.lineno}\n{self.name}"

# Class structure.
def p_program(p):
    'program : classlist'
    p[0] = p[1]

def p_classlist(p):
    '''classlist : classlist_some
                 | classlist_none'''
    p[0] = p[1]

def p_classlist_some(p):
    'classlist_some : classdef classlist'
    p[0] = [p[1]] + p[2]

def p_class_no_inherits(p):
    'classdef : CLASS TYPE LBRACE featurelist RBRACE SEMI'
    # Class count is incremented when a new class is encountered.
    global class_count
    class_count += 1
    p[0] = ClassNoInherits(p.lineno(1), p[2], p[4])

def p_class_inherits(p):
    'classdef : CLASS TYPE INHERITS TYPE LBRACE featurelist RBRACE SEMI'
    global class_count
    class_count += 1
    p[0] = ClassInherits(p.lineno(1), p[2], p[6], p[4])

def p_classlist_none(p):
    'classlist_none : '
    p[0] = []

# Feature structure.
def p_featurelist(p):
    '''featurelist : featurelist_some
                   | featurelist_none'''
    p[0] = p[1]

def p_featurelist_some(p):
    'featurelist_some : featuredef SEMI featurelist'
    p[0] = [p[1]] + p[3]

def p_featurelist_none(p):
    'featurelist_none : '
    p[0] = []

def p_feature_no_init(p):
    'featuredef : IDENTIFIER COLON TYPE'
    p[0] = Attribute(p.lineno(1), p[1], p[3])

def p_feature_init(p):
    'featuredef : IDENTIFIER COLON TYPE LARROW expr'
    p[0] = Attribute(p.lineno(1), p[1], p[3], p[5])

def p_feature_method(p):
    '''featuredef : IDENTIFIER LPAREN formal_list RPAREN COLON TYPE LBRACE expr RBRACE
                    | IDENTIFIER LPAREN formal_list_none RPAREN COLON TYPE LBRACE expr RBRACE'''
    p[0] = Method(p.lineno(1), p[1], p[3], p[6], p[8])

# Formal strucutre.
def p_formal_list(p):
    '''formal_list : formaldef COMMA formal_list
                   | formaldef'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2:
        p[0] = [p[1]]

def p_formal_no_init(p):
    'formaldef : IDENTIFIER COLON TYPE'
    p[0] = Formal(p.lineno(1), p[1], p[3])

def p_formal_init(p):
    'formaldef : IDENTIFIER COLON TYPE LARROW expr'
    p[0] = Formal(p.lineno(1), p[1], p[3], p[5])

# Passes a string as passing a list led to issues with the Let class.
def p_formal_list_none(p):
    'formal_list_none : '
    p[0] = ""

# Expression structure.
def p_exprlist(p):
    '''exprlist : expr SEMI exprlist
                | expr COMMA exprlist
                | expr SEMI
                | expr'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_expr_block(p):
    'expr : LBRACE exprlist RBRACE'
    p[0] = Block(p.lineno(1), p[2])

def p_expr_parentheses(p):
    'expr : LPAREN exprlist RPAREN'
    p[0] = Parentheses(p.lineno(1), p[2])

def p_expr_assignment(p):
    'expr : IDENTIFIER LARROW expr'
    p[0] = Assignment(p.lineno(1), p[1], p[3])

def p_expr_if(p):
    'expr : IF expr THEN expr ELSE expr FI'
    p[0] = If(p.lineno(1), p[2], p[4], p[6])

def p_expr_while(p):
    'expr : WHILE expr LOOP expr POOL'
    p[0] = While(p.lineno(1), p[2], p[4])

def p_expr_let(p):
    'expr : LET formal_list IN expr'
    p[0] = Let(p.lineno(1), p[2], p[4])

def p_expr_case(p):
    'expr : CASE expr OF case_condition_list ESAC'
    p[0] = Case(p.lineno(1), p[2], p[4])

def p_case_action_list(p):
    '''case_condition_list : case_condition_some SEMI case_condition_list
                        | case_condition_none'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = []

def p_case_condition_some(p):
    'case_condition_some : IDENTIFIER COLON TYPE RARROW expr'
    p[0] = CaseCondition(p.lineno(1), p[1], p[3], p[5])

def p_case_condition_none(p):
    'case_condition_none : '
    p[0] = []

# Expressions with ambiguity had the smaller expression first so it would always be seen first and if it did not match, then the longer one would possibly.
def p_expr_method_dispatch(p):
    '''expr : expr AT TYPE DOT IDENTIFIER LPAREN RPAREN
            | expr AT TYPE DOT IDENTIFIER LPAREN exprlist RPAREN
            | expr DOT IDENTIFIER LPAREN RPAREN
            | expr DOT IDENTIFIER LPAREN exprlist RPAREN
            | IDENTIFIER LPAREN RPAREN
            | IDENTIFIER LPAREN exprlist RPAREN'''
    if len(p) == 9:
        p[0] = Static_Dispatch(p.lineno(2), p[1], p[3], p[5], p[7])
    if len(p) == 8:
        p[0] = Static_Dispatch(p.lineno(2), p[1], p[3], p[5], [])
    elif len(p) == 7:
        p[0] = Dynamic_Dispatch(p.lineno(2), p[1], p[3], p[5])
    elif len(p) == 6:
        p[0] = Dynamic_Dispatch(p.lineno(2), p[1], p[3], [])
    elif len(p) == 5:
        p[0] = Dynamic_Dispatch(p.lineno(2), "self", p[1], p[3])
    elif len(p) == 4:
        p[0] = Dynamic_Dispatch(p.lineno(2), "self", p[1], [])

# These few for binary operations directly passed what token should be printed as when trying to pass p[2], they would print blank.
# These added more structures here, but saved on classes above (Unary operations could most likely have also been condensed).
def p_expr_plus(p):
    'expr : expr PLUS expr'
    p[0] = BinaryOperation(p.lineno(2), p[1], 'plus', p[3])

def p_expr_minus(p):
    'expr : expr MINUS expr'
    p[0] = BinaryOperation(p.lineno(2), p[1], 'minus', p[3])

def p_expr_times(p):
    'expr : expr TIMES expr'
    p[0] = BinaryOperation(p.lineno(2), p[1], 'times', p[3])

def p_expr_divide(p):
    'expr : expr DIVIDE expr'
    p[0] = BinaryOperation(p.lineno(2), p[1], 'divide', p[3])

def p_expr_lt(p):
    'expr : expr LT expr'
    p[0] = BinaryOperation(p.lineno(2), p[1], 'lt', p[3])

def p_expr_le(p):
    'expr : expr LE expr'
    p[0] = BinaryOperation(p.lineno(2), p[1], 'le', p[3])

def p_expr_equals(p):
    'expr : expr EQUALS expr'
    p[0] = BinaryOperation(p.lineno(2), p[1], 'eq', p[3])

def p_expr_isvoid(p):
    'expr : ISVOID expr'
    p[0] = IsVoid(p.lineno(1), p[2])

def p_expr_tilde(p):
    'expr : TILDE expr'
    p[0] = Tilde(p.lineno(1), p[2])

def p_expr_not(p):
    'expr : NOT expr'
    p[0] = Not(p.lineno(1), p[2])

def p_expr_integer(p):
    'expr : INTEGER'
    p[0] = Integer(p.lineno(1), int(p[1]))

def p_expr_string(p):
    'expr : STRING'
    p[0] = String(p.lineno(1), p[1])

def p_expr_true(p):
    'expr : TRUE'
    p[0] = Boolean(p.lineno(1), 'true')

def p_expr_false(p):
    'expr : FALSE'
    p[0] = Boolean(p.lineno(1), 'false')

def p_expr_new_object(p):
    'expr : NEW TYPE'
    p[0] = NewObject(p.lineno(1), p[2])

def p_expr_identifier(p):
    'expr : IDENTIFIER'
    p[0] = Identifier(p.lineno(1), p[1])

# Errors are printed along with what the token type was near said error.
def p_error(p):
    if p:
        print(f"ERROR: {p.lineno}: Parser: Syntax error near '{p.type}'!")
    else:
        # If the end of file was reached with such an error, we printed 'EOF' or 'End of File'.
        print(f"ERROR: EOF: Parser: EOF")
    exit(1)

# Here, we set up our parser using YACC from our lexer.
pa2lexer = PA2Lexer()
parser = yacc.yacc()
ast = parser.parse(lexer = pa2lexer)

# With out AST tree created, we write this all to our AST file.
with open(output_filename, 'w', encoding = 'utf-8') as file:
    file.write(str(class_count) + '\n')
    for node in ast:
            file.write(str(node) + '\n')