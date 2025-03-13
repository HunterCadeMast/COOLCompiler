# Hunter Mast / hunter.c.mast@vanderbilt.edu
# Resources used were PA4Starter.py file given and Dr. Leach's videos.
import sys

tabs = 0
ast_lines = []
class_list = []

# Here are all of our classes that we format our parsed code intto something the type checker can recognize
# The Class class has the class name, class it inherits, attribute names, method names, and features.
class Class(object):
    name_iden = None
    inherits_iden = None
    attributes = []
    methods = []
    features = []

    def __init__(self, _name_iden, _inherits_iden, _attributes, _methods, _features):
        self.name_iden = _name_iden
        self.inherits_iden = _inherits_iden
        self.attributes = _attributes
        self.methods = _methods
        self.features = _features
        self.inherits_object = False

    def __str__(self):
        global tabs
        ret = ""
        ret += "\n"
        for i in range(tabs):
            ret += "\t"
        ret += "Class( "
        tabs += 1
        ret += str(self.name_iden)
        ret += ", "
        if self.inherits_iden != Identifier(0, "Object"):
            ret += "inherits"
            ret += ", "
            ret += str(self.inherits_iden)
            ret += ", "
        else:
            ret += "no_inherits"
            ret += ", "
        ret += str(len(self.attributes))
        ret += ", "
        for attribute in self.attributes:
            ret += str(attribute)
            ret += ", "
        ret += str(len(self.methods))
        ret += ", "
        for method in self.methods:
            ret += str(method)
            ret += ", "
        ret += str(len(self.features))
        ret += ", "
        for feature in self.features:
            ret += str(feature)
            ret += ", "
        ret = ret.rstrip(", ")
        ret += " )"
        tabs -= 1
        return ret

    def __repr__(self):
        return str(self)

# Attribute class has name, type, and if it is initialized.
class Attribute(Class):
    def __init__(self, _feature_kind, _feature_name, _feature_type, _feature_init = None):
        self.feature_kind = _feature_kind
        self.feature_name = _feature_name
        self.feature_type = _feature_type
        self.feature_init = _feature_init

    def __str__(self):
        global tabs
        ret = ""
        ret += "\n"
        for i in range(tabs):
            ret += "\t"
        ret += "Attribute( "
        tabs += 1
        ret += str(self.feature_kind)
        ret += ", "
        ret += str(self.feature_name)
        ret += ", "
        ret += str(self.feature_type)
        if self.feature_init is not None:
            ret += ", "
            ret += str(self.feature_init)
        ret += " )"
        tabs -= 1
        return ret

# Method class has name, list of parameters, type, the body, and a check for for if it is from an internal class or not.
class Method(Class):
    def __init__(self, _feature_name, _formals_list, _feature_type, _feature_body, _internal_check = False):
        self.feature_name = _feature_name
        self.formals_list = _formals_list
        self.feature_type = _feature_type
        self.feature_body = _feature_body
        self.internal_check = _internal_check

    def __str__(self):
        global tabs
        ret = ""
        ret += "\n"
        for i in range(tabs):
            ret += "\t"
        ret += "Method( "
        tabs += 1
        ret += str(self.feature_name)
        ret += ", "
        for formal in self.formals_list:
            ret += str(formal)
            ret += ", "
        ret += str(self.feature_type)
        ret += ", "
        ret += str(self.feature_body)
        ret += " )"
        tabs -= 1
        return ret

# All expressions expand on this class, all also including expression type name, expression type exactly, and the line number.
class Expression(object):
    def __str__ (self):
        return "Expression()"

# This gets the formal name and type.
class Formal(Expression):
    def __init__(self, _formal_name, _formal_type):
        self.formal_name = _formal_name
        self.formal_type = _formal_type
        self.exp_type = None

    def __str__(self):
        global tabs
        ret = ""
        ret += "\n"
        for i in range(tabs):
            ret += "\t"
        ret += "Formal( "
        tabs += 1
        ret += str(self.formal_name)
        ret += ", "
        ret += str(self.formal_type)
        ret += " )"
        tabs -= 1
        return ret

# This gets the assignee and right hand side.
class Assign(Expression):
    def __init__(self, _line_number, _assignee, _rhs):
        self.line_number = _line_number
        self.assignee = _assignee
        self.rhs = _rhs
        self.expression_type = "assign"
        self.exp_type = None

    def __str__(self):
        global tabs
        ret = ""
        ret += "\n"
        for i in range(tabs):
            ret += "\t"
        ret += "Assign( "
        tabs += 1
        ret += str(self.assignee)
        ret += ", "
        ret += str(self.rhs)
        ret += " )"
        tabs -= 1
        return ret

# It gets the class name, method name, and arguments.
class Dynamic_Dispatch(Expression):
    def __init__(self, _line_number, _obj_name, _method_name, _args):
        self.line_number = _line_number
        self.obj_name = _obj_name
        self.method_name = _method_name
        self.args = _args
        self.expression_type = "dynamic_dispatch"
        self.exp_type = None

    def __str__(self):
        global tabs
        ret = ""
        ret += "\n"
        for i in range(tabs):
            ret += "\t"
        ret += "Dynamic_Dispatch( "
        tabs += 1
        ret += str(self.obj_name)
        ret += ", "
        ret += str(self.method_name)
        ret += ", "
        for arg in self.args:
            ret += str(arg)
            ret += ", "
        ret = ret.rstrip(", ")
        ret += " )"
        tabs -= 1
        return ret

# This has class name, type name, method name, and arguments.
class Static_Dispatch(Expression):
    def __init__(self, _line_number, _obj_name, _type_name, _method_name, _args):
        self.line_number = _line_number
        self.obj_name = _obj_name
        self.type_name = _type_name
        self.method_name = _method_name
        self.args = _args
        self.expression_type = "static_dispatch"
        self.exp_type = None

    def __str__(self):
        global tabs
        ret = ""
        ret += "\n"
        for i in range(tabs):
            ret += "\t"
        ret += "Static_Dispatch( "
        tabs += 1
        ret += str(self.obj_name)
        ret += ", "
        ret += str(self.type_name)
        ret += ", "
        ret += str(self.method_name)
        ret += ", "
        for arg in self.args:
            ret += str(arg)
            ret += ", "
        ret = ret.rstrip(", ")
        ret += " )"
        tabs -= 1
        return ret

# This has the method name and arguments.
class Self_Dispatch(Expression):
    def __init__(self, _line_number, _method_name, _args):
        self.line_number = _line_number
        self.method_name = _method_name
        self.args = _args
        self.expression_type = "self_dispatch"
        self.exp_type = None

    def __str__(self):
        global tabs
        ret = ""
        ret += "\n"
        for i in range(tabs):
            ret += "\t"
        ret += "Self_Dispatch( "
        tabs += 1
        ret += str(self.method_name)
        ret += ", "
        for arg in self.args:
            ret += str(arg)
            ret += ", "
        ret = ret.rstrip(", ")
        ret += " )"
        tabs -= 1
        return ret

# This has the if-statement predicate, then body, and else body.
class If(Expression):
    def __init__(self, _line_number, _predicate, _then_body, _else_body):
        self.line_number = _line_number
        self.predicate = _predicate
        self.then_body = _then_body
        self.else_body = _else_body
        self.expression_type = "if"
        self.exp_type = None

    def __str__(self):
        global tabs
        ret = ""
        ret += "\n"
        for i in range(tabs):
            ret += "\t"
        ret += "If( "
        tabs += 1
        ret += str(self.predicate)
        ret += ", "
        ret += str(self.then_body)
        ret += ", "
        ret += str(self.else_body)
        ret += " )"
        tabs -= 1
        return ret

# This has the while-statement predicate and body expression.
class While(Expression):
    def __init__(self, _line_number, _predicate, _body_exp):
        self.line_number = _line_number
        self.predicate = _predicate
        self.body_exp = _body_exp
        self.expression_type = "while"
        self.exp_type = None

    def __str__(self):
        global tabs
        ret = ""
        ret += "\n"
        for i in range(tabs):
            ret += "\t"
        ret += "While( "
        tabs += 1
        ret += str(self.predicate)
        ret += ", "
        ret += str(self.body_exp)
        ret += " )"
        tabs -= 1
        return ret

# This has a block of expressions.
class Block(Expression):
    def __init__(self, _line_number, _exps):
        self.line_number = _line_number
        self.exps = _exps
        self.expression_type = "block"
        self.exp_type = None

    def __str__(self):
        global tabs
        ret = ""
        ret += "\n"
        for i in range(tabs):
            ret += "\t"
        ret += "Block( "
        tabs += 1
        for expression in self.exps:
            ret += str(expression)
            ret += ", "
        ret = ret.rstrip(", ")
        ret += " )"
        tabs -= 1
        return ret

# This has just the expression to new.
class New(Expression):
    def __init__(self, _line_number, _exp):
        self.line_number = _line_number
        self.exp = _exp
        self.expression_type = "new"
        self.exp_type = None

    def __str__(self):
        global tabs
        ret = ""
        ret += "\n"
        for i in range(tabs):
            ret += "\t"
        ret += "New( "
        tabs += 1
        ret += str(self.exp)
        ret += " )"
        tabs -= 1
        return ret

# This has just the expression to void.
class IsVoid(Expression):
    def __init__(self, _line_number, _exp):
        self.line_number = _line_number
        self.exp = _exp
        self.expression_type = "isvoid"
        self.exp_type = None

    def __str__(self):
        global tabs
        ret = ""
        ret += "\n"
        for i in range(tabs):
            ret += "\t"
        ret += "IsVoid( "
        tabs += 1
        ret += str(self.exp)
        ret += " )"
        tabs -= 1
        return ret

# This has the left side expression and right side.
class Plus(Expression):
    def __init__(self, _line_number, _e1, _e2):
        self.line_number = _line_number
        self.e1 = _e1
        self.e2 = _e2
        self.expression_type = "plus"
        self.exp_type = None

    def __str__(self):
        global tabs
        ret = ""
        ret += "\n"
        for i in range(tabs):
            ret += "\t"
        ret += "Plus( "
        tabs += 1
        ret += str(self.e1)
        ret += ", "
        ret += str(self.e2)
        ret += " )"
        tabs -= 1
        return ret

# This has the left side expression and right side.
class Minus(Expression):
    def __init__(self, _line_number, _e1, _e2):
        self.line_number = _line_number
        self.e1 = _e1
        self.e2 = _e2
        self.expression_type = "minus"
        self.exp_type = None

    def __str__(self):
        global tabs
        ret = ""
        ret += "\n"
        for i in range(tabs):
            ret += "\t"
        ret += "Minus( "
        tabs += 1
        ret += str(self.e1)
        ret += ", "
        ret += str(self.e2)
        ret += " )"
        tabs -= 1
        return ret

# This has the left side expression and right side.
class Times(Expression):
    def __init__(self, _line_number, _e1, _e2):
        self.line_number = _line_number
        self.e1 = _e1
        self.e2 = _e2
        self.expression_type = "times"
        self.exp_type = None

    def __str__(self):
        global tabs
        ret = ""
        ret += "\n"
        for i in range(tabs):
            ret += "\t"
        ret += "Times( "
        tabs += 1
        ret += str(self.e1)
        ret += ", "
        ret += str(self.e2)
        ret += " )"
        tabs -= 1
        return ret

# This has the left side expression and right side.
class Divide(Expression):
    def __init__(self, _line_number, _e1, _e2):
        self.line_number = _line_number
        self.e1 = _e1
        self.e2 = _e2
        self.expression_type = "divide"
        self.exp_type = None

    def __str__(self):
        global tabs
        ret = ""
        ret += "\n"
        for i in range(tabs):
            ret += "\t"
        ret += "Divide( "
        tabs += 1
        ret += str(self.e1)
        ret += ", "
        ret += str(self.e2)
        ret += " )"
        tabs -= 1
        return ret

# This has the left side expression and right side.
class Lt(Expression):
    def __init__(self, _line_number, _e1, _e2):
        self.line_number = _line_number
        self.e1 = _e1
        self.e2 = _e2
        self.expression_type = "lt"
        self.exp_type = None

    def __str__(self):
        global tabs
        ret = ""
        ret += "\n"
        for i in range(tabs):
            ret += "\t"
        ret += "Lt( "
        tabs += 1
        ret += str(self.e1)
        ret += ", "
        ret += str(self.e2)
        ret += " )"
        tabs -= 1
        return ret

# This has the left side expression and right side.
class Le(Expression):
    def __init__(self, _line_number, _e1, _e2):
        self.line_number = _line_number
        self.e1 = _e1
        self.e2 = _e2
        self.expression_type = "le"
        self.exp_type = None

    def __str__(self):
        global tabs
        ret = ""
        ret += "\n"
        for i in range(tabs):
            ret += "\t"
        ret += "Le( "
        tabs += 1
        ret += str(self.e1)
        ret += ", "
        ret += str(self.e2)
        ret += " )"
        tabs -= 1
        return ret

# This has the left side expression and right side.
class Eq(Expression):
    def __init__(self, _line_number, _e1, _e2):
        self.line_number = _line_number
        self.e1 = _e1
        self.e2 = _e2
        self.expression_type = "eq"
        self.exp_type = None

    def __str__(self):
        global tabs
        ret = ""
        ret += "\n"
        for i in range(tabs):
            ret += "\t"
        ret += "Eq( "
        tabs += 1
        ret += str(self.e1)
        ret += ", "
        ret += str(self.e2)
        ret += " )"
        tabs -= 1
        return ret

# This has the expression that is not.
class Not(Expression):
    def __init__(self, _line_number, _e):
        self.line_number = _line_number
        self.e = _e
        self.expression_type = "not"
        self.exp_type = None

    def __str__(self):
        global tabs
        ret = ""
        ret += "\n"
        for i in range(tabs):
            ret += "\t"
        ret += "Not( "
        tabs += 1
        ret += str(self.e)
        ret += " )"
        tabs -= 1
        return ret

# This has the expression that is negated.
class Negate(Expression):
    def __init__(self, _line_number, _e):
        self.line_number = _line_number
        self.e = _e
        self.expression_type = "negate"
        self.exp_type = None

    def __str__(self):
        global tabs
        ret = ""
        ret += "\n"
        for i in range(tabs):
            ret += "\t"
        ret += "Negate( "
        tabs += 1
        ret += str(self.e)
        ret += " )"
        tabs -= 1
        return ret

# This has the type of bind the let statement is, the body, and the bind itself being broken up into identifier name, type name, and value.
class Let(Expression):
    def __init__(self, _line_number, _binds, _body):
        self.line_number = _line_number
        self.binds = _binds
        self.body = _body
        self.expression_type = "let"
        self.exp_type = None
    
    def __str__(self):
        global tabs
        ret = ""
        ret += "Let( "
        for binding in self.binds:
            ident, type_name, value = binding
            if value is None:
                ret += str(ident)
                ret += ", "
                ret += str(type_name)
                ret += ", "
            else:
                ret += str(ident)
                ret += ", "
                ret += str(type_name)
                ret += ", "
                ret += str(value)
                ret += ", "
        ret = ret.rstrip(", ")
        ret += " in \n"
        tabs += 1
        for i in range(tabs):
            ret += "\t"
        ret += str(self.body)
        ret += " )"
        return ret

# This has the case of what expression, and is also broken into identifier name, type name, and body of the case expression.
class Case(Expression):
    def __init__(self, _line_number, _case, _exp):
        self.line_number = _line_number
        self.case = _case
        self.exp = _exp
        self.expression_type = "case"
        self.exp_type = None
    
    def __str__(self):
        global tabs
        ret = ""
        ret += "Case( "
        ret += str(self.case)
        ret += " of \n"
        tabs += 1
        for i in range(tabs):
            ret += "\t"
        for ident, type_name, body in self.exp:
            ret += str(ident)
            ret += ", "
            ret += str(type_name)
            ret += ", "
            ret += str(body)
            ret += ", "
        ret = ret.rstrip(", ")
        ret += " )"
        return ret

# This has the integer value.
class Integer(Expression):
    def __init__(self, _line_number, int_val):
        self.exp_type = "Int"
        self.line_number = _line_number
        self.int_val = int_val
        self.expression_type = "integer"

    def __str__(self):
        return "Integer( " + str(self.int_val) + " )"

# This has the string value.
class String(Expression):
    def __init__(self, _line_number, str_val):
        self.exp_type = "String"
        self.line_number = _line_number
        self.str_val = str_val
        self.expression_type = "string"

    def __str__(self):
        return "String( " + str(self.str_val) + " )"

# This has the identifier value.
class Identifier(Expression):
    def __init__(self, _line_number, _ident_name):
        self.line_number = _line_number
        self.ident_name = _ident_name
        self.expression_type = "identifier"
        self.exp_type = None
        
    def __str__(self):
        ret = "Identifier( " + str(self.ident_name) + " )"
        return ret

# This has the bool value.
class Bool(Expression):
    def __init__(self, _line_number, bool_val):
        self.exp_type = "Bool"
        self.line_number = _line_number
        self.bool_val = bool_val
        self.expression_type = None

    def __str__(self):
        return "Bool( " + str(self.bool_val) + " )"

# This gets the next line from the parsed AST file.
def get_line():
    global ast_lines
    line = ast_lines.pop(0)
    return line

# This is called a lot and ties an identifier name to a line number.
def read_identifier():
    line_num = get_line()
    ident_name = get_line()
    return Identifier(line_num, ident_name)

# This creates from our classes formals binded with name and type.
def read_formal():
    formal_name = read_identifier()
    formal_type = read_identifier()
    return Formal(formal_name, formal_type)

# This whole section is reading expressions and formatting them using the classes above and the expression name inside our parsed AST file.
def read_exp():
    line_number = get_line()
    exp_name = get_line()
    if exp_name == "assign":
        assignee = read_identifier()
        rhs = read_exp()
        return Assign(line_number, assignee, rhs)
    elif exp_name == "dynamic_dispatch":
        obj_name = read_exp()
        method_name = read_identifier()
        num_args = int(get_line())
        args = []
        for i in range(num_args):
            args.append(read_exp())
        return Dynamic_Dispatch(line_number, obj_name, method_name, args)
    elif exp_name == "static_dispatch":
        obj_name = read_exp()
        type_name = read_identifier()
        method_name = read_identifier()
        num_args = int(get_line())
        args = []
        for i in range(num_args):
            args.append(read_exp())
        return Static_Dispatch(line_number, obj_name, type_name, method_name, args)
    elif exp_name == "self_dispatch":
        method_name = read_identifier()
        num_args = int(get_line())
        args = []
        for i in range(num_args):
            args.append(read_exp())
        return Self_Dispatch(line_number, method_name, args)
    elif exp_name == "if":
        predicate = read_exp()
        then_body = read_exp()
        else_body = read_exp()
        return If(line_number, predicate, then_body, else_body)
    elif exp_name == "while":
        predicate = read_exp()
        body_exp = read_exp()
        return While(line_number, predicate, body_exp)
    elif exp_name == "block":
        num_exps = int(get_line())
        exps = []
        for i in range(num_exps):
            exps.append(read_exp())
        return Block(line_number, exps)
    elif exp_name == "new":
        return New(line_number, read_identifier())
    elif exp_name == "isvoid":
        return IsVoid(line_number, read_exp())
    elif exp_name == "plus":
        return Plus(line_number, read_exp(), read_exp())
    elif exp_name == "minus":
        return Minus(line_number, read_exp(), read_exp())
    elif exp_name == "times":
        return Times(line_number, read_exp(), read_exp())
    elif exp_name == "divide":
        return Divide(line_number, read_exp(), read_exp())
    elif exp_name == "lt":
        return Lt(line_number, read_exp(), read_exp())
    elif exp_name == "le":
        return Le(line_number, read_exp(), read_exp())
    elif exp_name == "eq":
        return Eq(line_number, read_exp(), read_exp())
    elif exp_name == "not":
        return Not(line_number, read_exp())
    elif exp_name == "negate":
        return Negate(line_number, read_exp())
    elif exp_name == "integer":
        return Integer(line_number, int(get_line()))
    elif exp_name == "string":
        return String(line_number, get_line())
    elif exp_name == "identifier":
        return read_identifier()
    elif exp_name == "true":
        return Bool(line_number, exp_name)
    elif exp_name == "false":
        return Bool(line_number, exp_name)
    elif exp_name == "let":
        num_binds = int(get_line())
        binds = []
        for i in range(num_binds):
            binding_type = get_line()
            if binding_type == "let_binding_no_init":
                ident = read_identifier()
                type_name = read_identifier()
                binds.append((ident, type_name, None))
            elif binding_type == "let_binding_init":
                ident = read_identifier()
                type_name = read_identifier()
                binds.append((ident, type_name, read_exp()))
        return Let(line_number, binds, read_exp())
    elif exp_name == "case":
        case_exp = read_exp()
        num_exps = int(get_line())
        exps = []
        for i in range(num_exps):
            ident = read_identifier()
            type_name = read_identifier()
            exps.append((ident, type_name, read_exp()))
        return Case(line_number, case_exp, exps)

# This section speficically goes through and sorts attributes and methods.
def read_feature():
    feature_kind = get_line()
    if feature_kind == "attribute_no_init":
        feature_name = read_identifier()
        feature_type = read_identifier()
        return Attribute(feature_kind, feature_name, feature_type)
    elif feature_kind == "attribute_init":
        feature_name = read_identifier()
        feature_type = read_identifier()
        feature_init = read_exp()
        return Attribute(feature_kind, feature_name, feature_type, feature_init)
    elif feature_kind == "method":
        feature_name = read_identifier()
        formals_list = []
        num_formals = int(get_line())
        for i in range(num_formals):
            formals_list.append(read_formal())
        feature_type = read_identifier()
        feature_body = read_exp()
        return Method(feature_name, formals_list, feature_type, feature_body)

# Here, we go through and get each line and add names, inheritance, and different aspects of each class from our parsed file.
def read_class():
    class_info = read_identifier()
    check_inherits = get_line()
    parent = None
    if check_inherits == "inherits":
        parent = read_identifier()
    num_features = int(get_line())
    attr_list = []
    method_list = []
    feature_list = []
    for i in range(num_features):
        feature_list.append(read_feature())
    for feature in feature_list:
        if isinstance(feature, Attribute):
            attr_list.append(feature)
        elif isinstance(feature, Method):
            method_list.append(feature)
    return Class(class_info, parent, attr_list, method_list, feature_list)

# Here, we get the number of classes from the first line and then read info from them all to append to the class list.
def read_ast():
    global class_list
    # We create all of our internal classes and append them to our overall class list.
    class_list.append(Class(Identifier(0, "Object"), None, [], [Method(Identifier(0, "abort"), [], Identifier(0, "Object"), None, True), Method(Identifier(0, "copy"), [], Identifier(0, "SELF_TYPE"), None, True), Method(Identifier(0, "type_name"), [], Identifier(0, "String"), None, True)], []))
    class_list.append(Class(Identifier(0, "IO"), Identifier(0, "Object"), [], [Method(Identifier(0, "in_int"), [], Identifier(0, "Int"), None, True), Method(Identifier(0, "in_string"), [], Identifier(0, "String"), None, True), Method(Identifier(0, "out_int"), [Formal(Identifier(0, "x"), Identifier(0, "Int"))], Identifier(0, "SELF_TYPE"), None, True), Method(Identifier(0, "out_string"), [Formal(Identifier(0, "x"), Identifier(0, "String"))], Identifier(0, "SELF_TYPE"), None, True)], []))
    class_list.append(Class(Identifier(0, "Int"), Identifier(0, "Object"), [], [], []))
    class_list.append(Class( Identifier(0, "String"), Identifier(0, "Object"), [], [Method(Identifier(0, "concat"), [Formal(Identifier(0, "s"), Identifier(0, "String"))], Identifier(0, "String"), None, True), Method(Identifier(0, "length"), [], Identifier(0, "Int"), None, True), Method(Identifier(0, "substr"), [Formal(Identifier(0, "i"), Identifier(0, "Int")), Formal(Identifier(0, "l"), Identifier(0, "Int"))], Identifier(0, "String"), None, True)],[]))
    class_list.append(Class(Identifier(0, "Bool"), Identifier(0, "Object"), [], [], []))
    num_classes = int(get_line())
    for i in range(num_classes):
        class_list.append(read_class())
    return class_list

# We initialize the symbol table as a global variable here.
symbol_table = {
    "classes": {}
}
# Here is where all of the type checking for feature bodies and expressions are implemented.
def typeCheck(astnode):
    global symbol_table
    # Here, we need to clarify that we are not getting attributes or methods as errors kept occuring if I did not.
    # We mostly jsut setting up our classes and symbol table.
    if isinstance(astnode, Class) and not (isinstance(astnode, Attribute) or isinstance(astnode, Method)):
        if str(astnode.inherits_iden) is not None:
            parent_class = astnode.inherits_iden.ident_name
        else:
            parent_class = "Object"
        symbol_table["current_class"] = astnode.name_iden.ident_name
        symbol_table[astnode.name_iden.ident_name] = {
            'inherits': parent_class,
            'attributes': {},
            'methods': {}
        }
        if astnode.name_iden.ident_name not in symbol_table["classes"]:
            symbol_table["classes"][astnode.name_iden.ident_name] = {
                "inherits": parent_class,
                "attributes": {},
                "methods": {}
            }
        # Here, we get the type for our attribute and method and format our symbol table with all of this information.
        for attribute in astnode.attributes:
            # This is how we start reading attribute feature bodies.
            attribute_type = typeCheck(attribute)
            # We check the feature initialization and make sure that it's type matches the attribute's type.
            if attribute.feature_init is not None:
                feature_init_type = typeCheck(attribute.feature_init)
                if feature_init_type == "SELF_TYPE":
                    feature_init_type = symbol_table["current_class"]
                if feature_init_type != str(attribute.feature_type.ident_name):
                    if str(attribute.feature_type.ident_name) != "SELF_TYPE" and feature_init_type != symbol_table["current_class"]:
                        print(f"ERROR: {attribute.feature_name.line_number}: Type-Check: Type, {feature_init_type}, does not match type, {attribute.feature_type.ident_name}, for attribute, {attribute.feature_name.ident_name}!")
                        exit(1)
            symbol_table["classes"][astnode.name_iden.ident_name]["attributes"][attribute.feature_name.ident_name] = attribute_type
        for method in astnode.methods:
            # This is how we start reading method feature bodies.
            method_type = typeCheck(method)
            symbol_table["classes"][astnode.name_iden.ident_name]["methods"][method.feature_name.ident_name] = {
                "return_type": method_type,
                "formals": {formal.formal_name.ident_name: formal.formal_type.ident_name for formal in method.formals_list},
                "line_number": method.feature_name.line_number
            }
        return "Class"
    # Here, we check each attribute and start type checking each expression in the body.
    elif isinstance(astnode, Attribute):
        class_name = symbol_table["current_class"]
        parent_class = symbol_table["classes"][class_name]["inherits"]
        # Attribute cannot be named 'self'.
        if astnode.feature_name.ident_name == "self":
            print(f"ERROR: {astnode.feature_name.line_number}: Type-Check: The class, {class_name}, cannot have an attribute named 'self'!")
            exit(1)
        # We cannot override an attribute.
        while parent_class is not None:
            if astnode.feature_name.ident_name in symbol_table["classes"][parent_class]["attributes"]:
                print(f"ERROR: {astnode.feature_name.line_number}: Type-Check: The attribute, {astnode.feature_name.ident_name}, in the class, {class_name}, cannot be overridden from the inherited class, {parent_class}!")
                exit(1)
            parent_class = symbol_table["classes"][parent_class].get("inherits")
        # We add the attribute type to the symbol table.
        symbol_table[class_name]['attributes'][astnode.feature_name.ident_name] = astnode.feature_type.ident_name
        # We return what our feature type should be.
        return astnode.feature_type.ident_name
    # Here, we check each mehtod and then start type checking each expression in the body.
    elif isinstance(astnode, Method):
        current_class = symbol_table.get("current_class")
        # We start by checking to make sure none of the method formals are 'SELF_TYPE'.
        for i, formal in enumerate(astnode.formals_list):
            if str(formal.formal_type.ident_name) == "SELF_TYPE":
                print(f"ERROR: {astnode.feature_name.line_number}: Type-Check: The method, {astnode.feature_name.ident_name}, should not have type, 'SELF_TYPE'!")
                exit(1)
        # We then iterate through all of our inherited methods to make sure we do not redefine any method.
        if current_class is not None:
            parent_class = symbol_table["classes"][current_class].get("inherits", None)
            if isinstance(parent_class, Identifier):
                parent_class = parent_class.ident_name
            while parent_class is not None:
                if astnode.feature_name.ident_name in symbol_table["classes"][parent_class]["methods"]:
                    parent_method_info = symbol_table["classes"][parent_class]["methods"][astnode.feature_name.ident_name]
                    if len(parent_method_info["formals"]) != len(astnode.formals_list):
                        print(f"ERROR: {astnode.feature_name.line_number}: Type-Check: The class, {current_class}, redefines the method, {astnode.feature_name.ident_name}!")
                        exit(1)
                    break
                parent_class = symbol_table["classes"][parent_class].get("inherits", None)
                if isinstance(parent_class, Identifier):
                    parent_class = parent_class.ident_name
        # If we have a method named the same as one of our predefined internal methods, we throw an error.
        if astnode.feature_name.ident_name in ["abort", "type_name", "copy", "in_int", "in_string", "out_int", "out_string", "concat", "length", "substr"]:
            print(f"ERROR: {astnode.feature_name.line_number}: Type-Check: The internal method, {astnode.feature_name.ident_name}, in the class, {current_class}, cannot be overridden!")
            exit(1)
        # If we cannot find the class the method exists in, we throw an error.
        if current_class is None:
            print(f"ERROR: {astnode.feature_name.line_number}: Type-Check: No class information on method, {astnode.feature_name}!")
            exit(1)
        symbol_table["self"] = current_class
        seen_formals = set()
        # Here, we go through and make sure there are no duplicate formals by keeping track of ones we see or, again, each method formal is not self or SELF_TYPE.
        for formal in astnode.formals_list:
            if str(formal.formal_name) in seen_formals:
                print(f"ERROR: {formal.formal_name.line_number}: Type-Check: The method, {astnode.feature_name.ident_name}, has duplicate formals, {formal.formal_name.ident_name}!")
                exit(1)
            if formal.formal_name.ident_name == "self" or formal.formal_name.ident_name == "SELF_TYPE":
                print(f"ERROR: {formal.formal_name.line_number}: Type-Check: The method formal cannot be {formal.formal_name.ident_name}!")
                exit(1)
            symbol_table[formal.formal_name.ident_name] = formal.formal_type.ident_name
            seen_formals.add(str(formal.formal_name))
        # If all of that passes, we check the method's body.
        typeCheck(astnode.feature_body)
        return astnode.feature_type.ident_name
    # Here, we deal with assigning values and identifiers to each other.
    elif isinstance(astnode, Assign):
        # We make sure that we are not assigning to self.
        if str(astnode.assignee.ident_name) == "self":
            print(f"ERROR: {astnode.assignee.line_number}: Type-Check: The variable, {astnode.assignee.ident_name}, cannot be assigned!")
            exit(1)
        # If we have the identifier in our symbol table, we use that as t1.
        if astnode.assignee.ident_name in symbol_table:
            t1 = symbol_table[astnode.assignee.ident_name]
        else:
            # If we do not have t1, we search the class to make sure that the value has been declared somewhere with inheritance or in the class.
            class_name = symbol_table.get("current_class")
            if class_name and astnode.assignee.ident_name in symbol_table[class_name]['attributes']:
                t1 = symbol_table[class_name]['attributes'][astnode.assignee.ident_name]
            else:
                parent_class = symbol_table['classes'][class_name].get('inherits')
                while parent_class:
                    if astnode.assignee.ident_name in symbol_table['classes'][parent_class]['attributes']:
                        t1 = symbol_table['classes'][parent_class]['attributes'][astnode.assignee.ident_name]
                        break
                    parent_class = symbol_table['classes'][parent_class].get('inherits')
                else:
                    print(f"ERROR: {astnode.assignee.line_number}: Type-Check: The variable, {astnode.assignee.ident_name}, has not been declared!")
                    exit(1)
        # We get the right-hand side's type for t2.
        t2 = typeCheck(astnode.rhs)
        # If they are the same identifiers, we say we cannot assign something to itself.
        if astnode.assignee == astnode.rhs:
            print(f"ERROR: {astnode.assignee.line_number}: Type-Check: {astnode.assignee.ident_name} cannot be assigned to itself!")
            exit(1)
        # If they are the same, return it's type.
        if t1 == t2:
            astnode.exp_type = t2
            return t2
        else:
            # If they are not the same, we check if the values can conform to one another and if not, we throw an error.
            left_info = symbol_table["classes"].get(t1)
            right_info = symbol_table["classes"].get(t2)
            conform_check = False
            while right_info:
                if right_info['inherits'] == t1:
                    conform_check = True
                    break
                right_info = symbol_table["classes"].get(right_info['inherits'])
            if not conform_check:
                print(f"ERROR: {astnode.line_number}: Type-Check: Assigning {t2} to {t1} does not conform!")
                exit(1)
        astnode.exp_type = t2
        return t2
    # Here, we deal with method calls from dynamic dispatch.
    elif isinstance(astnode, Dynamic_Dispatch):
        # We get the object type and make sure that it exists as one of our classes.
        object_type = typeCheck(astnode.obj_name)
        if str(object_type) not in symbol_table["classes"]:
            print(f"ERROR: {astnode.line_number}: Type-Check: The class, {astnode.obj_name.ident_name}, was not found!")
            exit(1)
        # We then go through and get information about the method we are calling.
        method_info = None
        class_to_check = object_type
        while class_to_check is not None:
            if astnode.method_name.ident_name in symbol_table["classes"][class_to_check]["methods"]:
                method_info = symbol_table["classes"][class_to_check]["methods"][astnode.method_name.ident_name]
                break
            class_to_check = symbol_table["classes"][class_to_check].get("inherits", None)
            if isinstance(class_to_check, Identifier):
                class_to_check = class_to_check.ident_name
        # If the method does not exist, we throw an error.
        if method_info is None:
            print(f"ERROR: {astnode.line_number}: Type-Check: The method, {astnode.method_name.ident_name}, was not found in the class, {object_type}!")
            exit(1)
        method_formals = method_info["formals"]
        method_return_type = method_info["return_type"]
        # We check to make sure the number of method arguments are correct.
        if len(astnode.args) != len(method_formals):
            argument_line_number = method_info["line_number"]
            print(f"ERROR: {argument_line_number}: Type-Check: The method, {astnode.method_name.ident_name}, only received {len(astnode.args)} arguments, but needed {len(method_formals)}!")
            exit(1)
        # This section was supposed to check through arguments for bad arguments, but it caused too many errors I removed it.
        for i, arg in enumerate(astnode.args):
            argument_check = False
            arg_type = typeCheck(arg)
            formal_name, formal_type = list(method_formals.items())[i]
            if arg_type == "SELF_TYPE" or arg_type == formal_type:
                argument_check = True
                arg_type = symbol_table["current_class"]
            current_class = arg_type
            while current_class is not None:
                if current_class == formal_name:
                    argument_check = True
                    break
                current_class = symbol_table["classes"].get(current_class, {}).get("inherits", None)
                if isinstance(current_class, Identifier):
                    current_class = current_class.ident_name
        # We return the type of class we dispatched from.
        if method_return_type == "SELF_TYPE":
            method_return_type = object_type
        astnode.exp_type = method_return_type
        return method_return_type
    # This section goes through static dispatch and checks for bad arguments and sends back the method call type
    elif isinstance(astnode, Static_Dispatch):
        # We get the object type and make sure that it exists as one of our classes.
        obj_type = typeCheck(astnode.obj_name)
        # We also make sure that object type conforms to the static class name.
        static_class_name = astnode.type_name.ident_name
        conform_check = False
        while obj_type is not None:
            if obj_type == static_class_name:
                conform_check = True
            obj_type = symbol_table["classes"].get(obj_type, {}).get("inherits", None)
        if not conform_check:
            print(f"ERROR: {astnode.line_number}: Type-Check: The type, {obj_type}, does not conform to the class, {static_class_name}!")
            exit(1)
        # We then go through and get information about the method we are calling.
        method_info = None
        class_to_check = static_class_name
        actual_method_class = None
        while class_to_check is not None:
            if astnode.method_name.ident_name in symbol_table["classes"][class_to_check]["methods"]:
                method_info = symbol_table["classes"][class_to_check]["methods"][astnode.method_name.ident_name]
                actual_method_class = class_to_check
                break
            class_to_check = symbol_table["classes"][class_to_check].get("inherits", None)
            if isinstance(class_to_check, Identifier):
                class_to_check = class_to_check.ident_name
        # If the method does not exist, we throw an error.
        if method_info is None:
            print(f"ERROR: {astnode.line_number}: Type-Check: The method, {astnode.method_name.ident_name}, was not found in the class, {static_class_name}!")
            exit(1)
        # We check to make sure the number of method arguments are correct.
        method_formals = method_info["formals"]
        if len(astnode.args) != len(method_formals):
            argument_line_number = method_info["line_number"]
            print(f"ERROR: {argument_line_number}: Type-Check: The method, {astnode.method_name.ident_name}, only received {len(astnode.args)} arguments, but needed {len(method_formals)}!")
            exit(1)
        # This section was supposed to check through arguments for bad arguments, but it caused too many errors I removed it.
        for i, arg in enumerate(astnode.args):
            argument_check = False
            arg_type = typeCheck(arg)
            formal_name, formal_type = list(method_formals.items())[i]
            if arg_type == "SELF_TYPE" or arg_type == formal_type:
                argument_check = True
                arg_type = symbol_table["current_class"]
            current_class = arg_type
            while current_class is not None:
                if current_class == formal_name:
                    argument_check = True
                    break
                current_class = symbol_table["classes"].get(current_class, {}).get("inherits", None)
                if isinstance(current_class, Identifier):
                    current_class = current_class.ident_name
        # We return the type of class we dispatched from.
        method_return_type = method_info["return_type"]
        if method_return_type == "SELF_TYPE":
            astnode.exp_type = obj_type
        else:
            astnode.exp_type = method_return_type
        return astnode.exp_type
    # This section is like dynamic dispatch, except it only cares about the method name.
    elif isinstance(astnode, Self_Dispatch):
        method_name = astnode.method_name.ident_name if isinstance(astnode.method_name, Identifier) else astnode.method_name
        class_to_check = symbol_table.get("current_class")
        # We then go through and get information about the method we are calling.
        method_info = None
        while class_to_check is not None:
            if method_name in symbol_table["classes"][class_to_check]["methods"]:
                method_info = symbol_table["classes"][class_to_check]["methods"][method_name]
                break
            class_to_check = symbol_table["classes"][class_to_check].get("inherits", None)
            if isinstance(class_to_check, Identifier):
                class_to_check = class_to_check.ident_name
         # If the method does not exist, we throw an error.
        if method_info is None:
            print(f"ERROR: {astnode.line_number}: Type-Check: The method, {method_name}, was not found in {class_to_check}!")
            available_methods = []
            temp_class = symbol_table.get("current_class")
            while temp_class is not None:
                available_methods.extend(symbol_table["classes"][temp_class]["methods"].keys())
                temp_class = symbol_table["classes"][temp_class].get("inherits", None)
                if isinstance(temp_class, Identifier):
                    temp_class = temp_class.ident_name
            exit(1)
        method_formals = method_info["formals"]
        method_return_type = method_info["return_type"]
        # We check to make sure the number of method arguments are correct.
        if len(astnode.args) != len(method_formals):
            argument_line_number = method_info["line_number"]
            print(f"ERROR: {argument_line_number}: Type-Check: The method, {astnode.method_name.ident_name}, only received {len(astnode.args)} arguments, but needed {len(method_formals)}!")
            exit(1)
        # This section was supposed to check through arguments for bad arguments, but it caused too many errors I removed it.
        for i, arg in enumerate(astnode.args):
            argument_check = False
            arg_type = typeCheck(arg)
            formal_name, formal_type = list(method_formals.items())[i]
            if arg_type == "SELF_TYPE" or arg_type == formal_type:
                argument_check = True
                arg_type = symbol_table["current_class"]
            current_class = arg_type
            while current_class is not None:
                if current_class == formal_name:
                    argument_check = True
                    break
                current_class = symbol_table["classes"].get(current_class, {}).get("inherits", None)
                if isinstance(current_class, Identifier):
                    current_class = current_class.ident_name
        # We return the type of class we dispatched from.
        if method_return_type == "SELF_TYPE":
            astnode.exp_type = "SELF_TYPE"
        else:
            astnode.exp_type = method_return_type
        return method_return_type
    # Here, we deal with checking the predicate, then type, and else type.
    elif isinstance(astnode, If):
        predicate_type = typeCheck(astnode.predicate)
        # We check if the predicate is of type Bool and throw an error if not.
        if predicate_type != "Bool":
            print(f"ERROR: {astnode.line_number}: Type-Check: Predicate for If-statement should be type 'Bool', not '{predicate_type}'!")
            exit(1)
        then_type = typeCheck(astnode.then_body)
        # We might not have else section, we so may have to skip that.
        else_type = None
        if astnode.else_body is not None:
            else_type = typeCheck(astnode.else_body)
        else:
            else_type = "Object"
        result_type = None
        # We compare the then and else types and give the resulting type.
        if then_type == else_type:
            result_type = then_type
        else:
            result_type = "Object"
        astnode.exp_type = result_type
        return result_type
        # Here, we check the while statement's predicate and body.
    elif isinstance(astnode, While):
        predicate_type = typeCheck(astnode.predicate)
        # If the predicate is not type Bool, we throw an error.
        if predicate_type != "Bool":
            print(f"ERROR: {astnode.line_number}: Type-Check: Predicate for While-statement should be type 'Bool', not '{predicate_type}'")
            exit(1)
        # If the body is SELF_TYPE, we throw an error.
        body_type = typeCheck(astnode.body_exp)
        if body_type == "SELF_TYPE":
            print(f"ERROR: {astnode.line_number}: Type-Check: Body for While-statement should not be 'SELF_TYPE'!")
            exit(1)
        # The while statement is always the type Object.
        astnode.exp_type = "Object"
        return "Object"
    # Here, we go through the block expression and return the type of the last expression.
    elif isinstance(astnode, Block):
        block_type = None
        for exp in astnode.exps:
            block_type = typeCheck(exp)
        astnode.exp_type = block_type
        return block_type
    # New returns the identifier of it's expression.
    elif isinstance(astnode, New):
        astnode.exp_type = astnode.exp.ident_name
        return astnode.exp.ident_name
    # IsVoid will always return Bool.
    elif isinstance(astnode, IsVoid):
        exp_type = typeCheck(astnode.exp)
        astnode.exp_type = "Bool"
        return "Bool"
    # Plus, Minus, Multiply, and Divide are all the same with checking both expressions are ints.
    elif isinstance(astnode, Plus):
        t1 = typeCheck(astnode.e1)
        t2 = typeCheck(astnode.e2)
        if (t1 == "Int" and t2 == "Int"):
            astnode.exp_type = "Int"
            return "Int"
        else:
            print(f"ERROR: {astnode.line_number}: Type-Check: Adding {t1} to {t2}!")
            exit(1)
    elif isinstance(astnode, Minus):
        t1 = typeCheck(astnode.e1)
        t2 = typeCheck(astnode.e2)
        if (t1 == "Int" and t2 == "Int"):
            astnode.exp_type = "Int"
            return "Int"
        else:
            print(f"ERROR: {astnode.line_number}: Type-Check: Subtracting {t1} to {t2}!")
            exit(1)
    elif isinstance(astnode, Times):
        t1 = typeCheck(astnode.e1)
        t2 = typeCheck(astnode.e2)
        if (t1 == "Int" and t2 == "Int"):
            astnode.exp_type = "Int"
            return "Int"
        else:
            print(f"ERROR: {astnode.line_number}: Type-Check: Multiplying {t1} to {t2}!")
            exit(1)
    elif isinstance(astnode, Divide):
        t1 = typeCheck(astnode.e1)
        t2 = typeCheck(astnode.e2)
        if (t1 == "Int" and t2 == "Int"):
            astnode.exp_type = "Int"
            return "Int"
        else:
            print(f"ERROR: {astnode.line_number}: Type-Check: Dividing {t1} to {t2}!")
            exit(1)
    # Lt and Le check that both of the expressions are of type Int and throw an error if not (Returns a Bool type).
    elif isinstance(astnode, Lt):
        t1 = typeCheck(astnode.e1)
        t2 = typeCheck(astnode.e2)
        if str(t1) != "Int" or str(t2) != "Int":
            print(f"ERROR: {astnode.line_number}: Type-Check: {t1} and {t2} cannot be compared with less-than-statement!")
            exit(1)
        astnode.exp_type = "Bool"
        return "Bool"
    elif isinstance(astnode, Le):
        t1 = typeCheck(astnode.e1)
        t2 = typeCheck(astnode.e2)
        if str(t1) != "Int" or str(t2) != "Int":
            print(f"ERROR: {astnode.line_number}: Type-Check: {t1} and {t2} cannot be compared with less-than-statement!")
            exit(1)
        astnode.exp_type = "Bool"
        return "Bool"
    # Here, we are making sure the values are objects of some sort and then if they are not equal types, we throw an error.
    elif isinstance(astnode, Eq):
        t1 = typeCheck(astnode.e1)
        t2 = typeCheck(astnode.e2)
        if (t1 in ["Int", "Bool", "String"]) and (t2 in ["Int", "Bool", "String"]):
            if t1 != t2:
                print(f"ERROR: {astnode.line_number}: Type-Check: {t1} and {t2} cannot be compared with equal-to-statement!")
                exit(1)
        # Types can be void, so it makes sure they match one another.
        elif t1 == "void" or t2 == "void":
            if t1 == "void" and t2 != "void":
                print(f"ERROR: {astnode.line_number}: Type-Check: The type, {t2}, must match void!")
                exit(1)
            if t2 == "void" and t1 != "void":
                print(f"ERROR: {astnode.line_number}: Type-Check: The type, {t1}, must match void!")
                exit(1)
        astnode.exp_type = "Bool"
        return "Bool"
    # Not checks if the expression is Bool and if not, throws an error.
    elif isinstance(astnode, Not):
        t1 = typeCheck(astnode.e)
        if t1 != "Bool":
            print(f"ERROR: {astnode.line_number}: Type-Check: Type, '{t1}', must be type, 'Bool', to use not-statement!")
            exit(1)
        astnode.exp_type = "Bool"
        return "Bool"
    # Negate checks if the expression is Int and if not, throws an error.
    elif isinstance(astnode, Negate):
        t1 = typeCheck(astnode.e)
        if t1 == "Int":
            astnode.exp_type = "Int"
            return "Int"
        else:
            print(f"ERROR: {astnode.line_number}: Type-Check: Type, '{t1}', must be type, 'Int', to use negate-statement!")
            exit(1)
    # Here, we make a copy of the symbol table and check through the let bindings to complete the let statement.
    elif isinstance(astnode, Let):
        let_symbol_table = symbol_table.copy()
        # Go through binding and check identifier, type, and value.
        for (ident, type_name, value) in astnode.binds:
            # If the identifier is named self, then return an error.
            if ident.ident_name == "self":
                print(f"ERROR: {astnode.line_number}: Type-Check:The variable, self, cannot be used!")
                exit(1)
            # if the value is exists, then we go through and get the value's type.
            if value is not None:
                let_type = typeCheck(value)
                # If the type does not match the type given that we are assigning to, then we throw an error.
                if let_type != type_name.ident_name:
                    print(f"ERROR: {astnode.line_number}: Type-Check: The type, {let_type}, does not match {type_name.ident_name} for {ident.ident_name}!")
                    exit(1)
                # We throw an error speifically for object assignment.
                elif let_type == "Object" and type_name.ident_name != "Object":
                    print(f"ERROR: {astnode.line_number}: Type-Check: Cannot assign 'Object' type to {ident.ident_name} with type, {type_name.ident_name}'!")
                    exit(1)
            # We register the type to the symbol table.
            symbol_table[ident.ident_name] = type_name.ident_name
        # We then get the body's type and assign that to our let statement.
        body_type = typeCheck(astnode.body)
        astnode.exp_type = body_type
        # We revert the symbol table back to how it originally was.
        symbol_table = let_symbol_table.copy()
        return body_type
    # Here, we go through our Case expression to unpack our expression and go through our options.
    elif isinstance(astnode, Case):
        typeCheck(astnode.case)
        case_types = []
        seen_types = set()
        # We copy the symbol table for scope.
        case_symbol_table = symbol_table.copy()
        # With the expression, we go through and make sure we only see each type once.
        for ident, type_name, body in astnode.exp:
            if str(type_name.ident_name) in seen_types:
                print(f"ERROR: {ident.line_number}: Type-Check: {type_name.ident_name} is already a case expression!")
                exit(1)
            else:
                seen_types.add(str(type_name.ident_name))
            # THe type can also not be SELF_TYPE
            if type_name.ident_name == "SELF_TYPE":
                print(f"ERROR: {type_name.line_number}: Type-Check: Case expression cannot be 'SELF_TYPE'!")
                exit(1)
            symbol_table[ident.ident_name] = type_name.ident_name
            # Here, we go through each body and add that to our possible types.
            expression_type = typeCheck(body)
            case_types.append(expression_type)
        symbol_table = case_symbol_table.copy()
        # Depending on the value of all the types, if they are not like the first we return Object.
        if not case_types:
            print(f"ERROR: {astnode.line_number}: Type-Check: No case expressions!")
            exit(1)
        result_type = case_types[0]
        for case_type in case_types[1:]:
            if case_type != result_type:
                result_type = "Object"
        astnode.exp_type = result_type
        return result_type
    # This returns the type as Int.
    elif isinstance(astnode, Integer):
        astnode.exp_type = "Int"
        return astnode.exp_type
    # This returns the type as String.
    elif isinstance(astnode, String):
        astnode.exp_type = "String"
        return astnode.exp_type
    # Here, we do a lot of checks to make sure we get our identifier and assign the right type..
    elif isinstance(astnode, Identifier):
        # We make sure to specifically assign self and SELF_TYPE as such.
        if str(astnode.ident_name) == "self" or str(astnode.ident_name) == "SELF_TYPE":
            astnode.exp_type = "SELF_TYPE"
            return "SELF_TYPE"
        # If our value is in the table, we assign that value.
        if astnode.ident_name in symbol_table:
            astnode.exp_type = symbol_table[astnode.ident_name]
            return symbol_table[astnode.ident_name]
        # If the class name is not gone, we start to check all of the methods and attributes to assign the right type, depending on what our value is.
        class_name = symbol_table.get("current_class")
        if class_name is not None:
            if astnode.ident_name in symbol_table["classes"][class_name]['attributes']:
                astnode.exp_type = symbol_table["classes"][class_name]['attributes'][astnode.ident_name]
                return symbol_table["classes"][class_name]['attributes'][astnode.ident_name]
            if astnode.ident_name in symbol_table["classes"][class_name]['methods']:
                astnode.exp_type = symbol_table["classes"][class_name]['methods'][astnode.ident_name]['return_type']
                return symbol_table["classes"][class_name]['methods'][astnode.ident_name]['return_type']
            parent_class = symbol_table["classes"][class_name].get('inherits')
            while parent_class is not None:
                if astnode.ident_name in symbol_table["classes"][parent_class]['attributes']:
                    astnode.exp_type = symbol_table["classes"][parent_class]['attributes'][astnode.ident_name]
                    return symbol_table["classes"][parent_class]['attributes'][astnode.ident_name]
                if astnode.ident_name in symbol_table["classes"][parent_class]['methods']:
                    astnode.exp_type = symbol_table["classes"][parent_class]['methods'][astnode.ident_name]['return_type']
                    return symbol_table["classes"][parent_class]['methods'][astnode.ident_name]['return_type']
                parent_class = symbol_table["classes"][parent_class].get('inherits')
        # Should return an error if value is not found.
        print(f"ERROR: {astnode.line_number}: Type-Check: The identifier, {astnode.ident_name}, is out of scope or not found!")
        exit(1)
    # This returns the type as Bool.
    elif isinstance(astnode, Bool):
        astnode.exp_type = "Bool"
        return "Bool"
    # This is if none of the other types are found at all.
    else:
        print(f"ERROR: {astnode.line_number}: Type-Check: Unknown type for expression, {astnode}!")
        exit(1)

# This method is called to gather all of the attributes inherited by each class.
def collect_parent_attributes(class_name, classes):
    attribute_list = {}
    if class_name.inherits_iden is not None:
        parent_classes = []
        current_class = class_name
        # We continue to look at each class and check if we inherit the class.
        while current_class.inherits_iden is not None:
            parent_class = None
            for check_class in classes:
                if str(check_class.name_iden.ident_name) == str(current_class.inherits_iden.ident_name):
                    parent_class = check_class
                    break
            if parent_class:
                parent_classes.append(parent_class)
                current_class = parent_class
            else:
                break
        parent_classes.reverse()
        # We then go through each parent class we inherit and add each attribute to a list of our classes total amount of attributes.
        # We make sure to keep the most recent ones that may override inherited attributes.
        for parent_class in parent_classes:
            for attribute in parent_class.attributes:
                attribute_list[attribute.feature_name.ident_name] = (attribute, parent_class)
    for attribute in class_name.attributes:
            attribute_list[attribute.feature_name.ident_name] = (attribute, class_name)
    for current_class in classes:
        if str(current_class.name_iden.ident_name) == "Object":
            for attribute in current_class.attributes:
                attribute_list[attribute.feature_name.ident_name] = (attribute, current_class)
    return attribute_list

# This method is called to gather all of the methods inherited by each class and is exactly like the function above.
# I decided to seperate them up here to make reading the code below where these are called a bit more visable.
def collect_parent_methods(class_name, classes):
    method_list = {}
    if class_name.inherits_iden is not None:
        parent_classes = []
        current_class = class_name
        # We continue to look at each class and check if we inherit the class.
        while current_class.inherits_iden is not None:
            parent_class = None
            for check_class in classes:
                if str(check_class.name_iden.ident_name) == str(current_class.inherits_iden.ident_name):
                    parent_class = check_class
                    break
            if parent_class:
                parent_classes.append(parent_class)
                current_class = parent_class
            else:
                break
        parent_classes.reverse()
        # We then go through each parent class we inherit and add each method to a list of our classes total amount of methods.
        # We make sure to keep the most recent ones that may override inherited methods.
        for parent_class in parent_classes:
            for method in parent_class.methods:
                method_list[method.feature_name.ident_name] = (method, parent_class)
    for method in class_name.methods:
        method_list[method.feature_name.ident_name] = (method, class_name)
    for current_class in classes:
        if str(current_class.name_iden.ident_name) == "Object":
            for method in current_class.methods:
                method_list[method.feature_name.ident_name] = (method, current_class)
    return method_list

# Here, we format how we write each internal method to the written file, depending on certain conditions and information needed.
def serialize_internal(class_name, method, inherits, file):
    file.write(f"{method.feature_name.ident_name}\n")
    if method.formals_list is not None:
        file.write(f"{len(method.formals_list)}\n")
        for formal in method.formals_list:
            file.write(f"{formal.formal_name.ident_name}\n")
    else:
        file.write("0\n")
    if inherits is not None:
        file.write(f"{inherits}\n")
        file.write("0\n")
    file.write(f"{method.feature_type.ident_name}\n")
    file.write("internal\n")
    if inherits is not None:
        file.write(f"{inherits}.{method.feature_name.ident_name}\n")

# Here, we format how we write each expression to the written file, depending on certain conditions and information needed.
# We call this multiple times, so it is better to have it as a single method we can call on.
# Nothing about this is that specical, we just recursively will keep calling the function to make sure every expression in each body is written correctly.
def serialize_expression(expression, file):
    # This is the only unique instance where if it is an identifier, we need ot write "identifier" and provide a different format, depending on expression.exp_type.
    if isinstance(expression, Identifier):
        file.write(f"{expression.line_number}\n")
        # THIS MAY NEED TO CHANGE TO JUST HAVING expression.exp_type = "SELF_TYPE"
        if expression.ident_name == "self":
            expression.exp_type = "SELF_TYPE"
        if expression.exp_type is not None:
            file.write(f"{expression.exp_type}\n")
            file.write(f"identifier\n")
            file.write(f"{expression.line_number}\n")
            file.write(f"{expression.ident_name}\n")
        else:
            file.write(f"{expression.ident_name}\n")
    else:
        file.write(f"{expression.line_number}\n")
        if expression.exp_type is not None:
            file.write(f"{expression.exp_type}\n")
        if expression.expression_type is not None:
            file.write(f"{expression.expression_type}\n")
    if isinstance(expression, Assign):
        serialize_expression(expression.assignee, file)
        serialize_expression(expression.rhs, file)
    elif isinstance(expression, Dynamic_Dispatch):
        serialize_expression(expression.obj_name, file)
        serialize_expression(expression.method_name, file)
        file.write(f"{len(expression.args)}\n")
        for argument in expression.args:
            serialize_expression(argument, file)
    elif isinstance(expression, Static_Dispatch):
        serialize_expression(expression.obj_name, file)
        serialize_expression(expression.type_name, file)
        serialize_expression(expression.method_name, file)
        file.write(f"{len(expression.args)}\n")
        for argument in expression.args:
            serialize_expression(argument, file)
    elif isinstance(expression, Self_Dispatch):
        serialize_expression(expression.method_name, file)
        file.write(f"{len(expression.args)}\n")
        for argument in expression.args:
            serialize_expression(argument, file)
    elif isinstance(expression, If):
        serialize_expression(expression.predicate, file)
        serialize_expression(expression.then_body, file)
        serialize_expression(expression.else_body, file)
    elif isinstance(expression, While):
        serialize_expression(expression.predicate, file)
        serialize_expression(expression.body_exp, file)
    elif isinstance(expression, Block):
        file.write(f"{len(expression.exps)}\n")
        for exp in expression.exps:
            serialize_expression(exp, file)
    elif isinstance(expression, New):
        serialize_expression(expression.exp, file)
    elif isinstance(expression, IsVoid):
        serialize_expression(expression.exp, file)
    elif isinstance(expression, Plus):
        serialize_expression(expression.e1, file)
        serialize_expression(expression.e2, file)
    elif isinstance(expression, Minus):
        serialize_expression(expression.e1, file)
        serialize_expression(expression.e2, file)
    elif isinstance(expression, Times):
        serialize_expression(expression.e1, file)
        serialize_expression(expression.e2, file)
    elif isinstance(expression, Divide):
        serialize_expression(expression.e1, file)
        serialize_expression(expression.e2, file)
    elif isinstance(expression, Lt):
        serialize_expression(expression.e1, file)
        serialize_expression(expression.e2, file)
    elif isinstance(expression, Le):
        serialize_expression(expression.e1, file)
        serialize_expression(expression.e2, file)
    elif isinstance(expression, Eq):
        serialize_expression(expression.e1, file)
        serialize_expression(expression.e2, file)
    elif isinstance(expression, Not):
        serialize_expression(expression.e, file)
    elif isinstance(expression, Negate):
        serialize_expression(expression.e, file)
    # For Let and Case, we need to unbind each of our binds by identifier name, type name, and value.
    elif isinstance(expression, Let):
        file.write(f"{len(expression.binds)}\n")
        for (ident, type_name, value) in expression.binds:
            if value is None:
                file.write("let_binding_no_init\n")
            else:
                file.write("let_binding_init\n")
            serialize_expression(ident, file)
            serialize_expression(type_name, file)
            if value is not None:
                serialize_expression(value, file)
        serialize_expression(expression.body, file)
    elif isinstance(expression, Case):
        serialize_expression(expression.case, file)
        file.write(f"{len(expression.exp)}\n")
        for (ident, type_name, case) in expression.exp:
            serialize_expression(ident, file)
            serialize_expression(type_name, file)
            serialize_expression(case, file)
    if isinstance(expression, Integer):
        file.write(f"{expression.int_val}\n")
    elif isinstance(expression, String):
        file.write(f"{expression.str_val}\n")
    elif isinstance(expression, Bool):
        file.write(f"{expression.bool_val}\n")

# We perform our depth first search here and if we cannot find it has a parent class it inherits, we then recursively check for that one until we find a cycle or not.
def depth_first_search(cls, visited_list, classes):
        if visited_list[cls.name_iden.ident_name] == 1:
            print(f"ERROR: 0: Type-Check: The class, {cls.name_iden.ident_name}, was detected inside of a cycle!")
            return True
        if visited_list[cls.name_iden.ident_name] == 2:
            return False
        visited_list[cls.name_iden.ident_name] = 1
        if cls.inherits_iden is not None:
            parent_class = None
            for class_name in classes:
                if str(cls.inherits_iden) == str(class_name.name_iden):
                    parent_class = class_name
                if parent_class is not None:
                    if depth_first_search(parent_class, visited_list, classes):
                        return True
        visited_list[cls.name_iden.ident_name] = 2
        return False

# We keep track of visited classes and continue to call depth first search on each class.
def cycle_check(classes):
    visited_list = {}
    for cls in classes:
        visited_list[cls.name_iden.ident_name] = 0
    for cls in classes:
        if visited_list[cls.name_iden.ident_name] == 0:
            if depth_first_search(cls, visited_list, classes):
                exit(1)

def main():
    # Here, we start by reading our input file and formatting our AST.
    global ast_lines
    if len(sys.argv) < 2:
        print("Specify .cl-ast input file.\n")
        exit(1)
    input_filename = sys.argv[1]
    if input_filename.endswith('.cl-ast'):
        output_filename = input_filename[:-len('.cl-ast')] + '.cl-type'
    else:
        output_filename = input_filename + '.cl-type'
    with open(input_filename) as f:
        ast_lines = [x[:-1] if x.endswith('\n') else x for x in f.readlines()]
    ast = read_ast()
    for cls in ast:
        if cls.inherits_iden is not None:
            if str(cls.inherits_iden.ident_name) == "Object":
                cls.inherits_object = True
        elif cls.name_iden.ident_name != "Object":
            cls.inherits_iden = Identifier(0, "Object")
    # We check for class inheritance cycles now.
    cycle_check(ast)
    # This first section for type checking goes through all of the class names and makes sure that they are not defined multiple times.
    class_names = set()
    for cls in ast:
        if f"Identifier( {cls.name_iden.ident_name} )" in class_names:
            print(f"ERROR: {cls.name_iden.line_number}: Type-Check: The class, {cls.name_iden.ident_name}, is defined multiple times!\n")
            exit(1)
        class_names.add(f"Identifier( {cls.name_iden.ident_name} )")
    class_to_check = "Main"
    main_method_check = False
    parents_class_name = None
    for cls in ast:
        if cls.name_iden.ident_name == class_to_check:
            while cls is not None:
                for feature in cls.methods:
                    if isinstance(feature, Method) and str(feature.feature_name.ident_name) == "main":
                        main_method_check = True
                        break
                if main_method_check:
                    break
                if cls.inherits_iden is not None:
                    parent_class_name = cls.inherits_iden.ident_name
                cls = next((class_name for class_name in ast if class_name.name_iden.ident_name == parent_class_name), None)
    # If the Main class exists and does not have the main method inherited or inside of itself, throw an error.
    if not main_method_check:
        print(f"ERROR: 0: Type-Check: The class, Main, or any inherited class are missing the method, main!")
        exit(1)
    # If the Main class does not exist, we throw an error.
    if "Identifier( Main )" not in class_names:
        print("ERROR: 0: Type-Check: The class, Main, does not exist!")
        exit(1)
    for cls in ast:
        if cls.inherits_iden is not None:
            # Here, we go through and check inherits to make sure we are not inheriting Ints, Strings, or Bools.
            if str(cls.inherits_iden) in ["Identifier( Int )", "Identifier( String )", "Identifier( Bool )"]:
                print(f"ERROR: {cls.inherits_iden.line_number}: Type-Check: The type, '{cls.inherits_iden.ident_name}', cannot be inherited from!\n")
                exit(1)
            # If we do not inherit from something that is a classname, we throw an error.
            if str(cls.inherits_iden) not in class_names:
                print(f"ERROR: {cls.inherits_iden.line_number}: Type-Check: The class, '{cls.inherits_iden.ident_name}', cannot be inherited from as it does not exist!\n")
                exit(1)
    # Here, we go through and check basic types for each attribute or method.
    for cls in ast:
        parent_names = set()
        for feature in cls.features:
            # We go through to make sure that if an attribute or method type is not from a class or not Int, String, Bool, or SELF_TYPE, we throw an error.
            if isinstance(feature, Attribute):
                if str(feature.feature_type) not in class_names and str(feature.feature_type.ident_name) not in ["Int", "String", "Bool", "SELF_TYPE"]:
                    print(f"ERROR: {feature.feature_name.line_number}: Type-Check: The attribute, {feature.feature_name.ident_name}, does not have return type, {feature.feature_type.ident_name}!\n")
                    exit(1)
            elif isinstance(feature, Method):
                if str(feature.feature_type) not in class_names and str(feature.feature_type.ident_name) not in ["Int", "String", "Bool", "SELF_TYPE"]:
                    print(f"ERROR: {feature.feature_name.line_number}: Type-Check: The method, {feature.feature_name.ident_name}, does not have return type, {feature.feature_type.ident_name}!\n")
                    exit(1)
                # With method, it's a bit more complicated. We need to also check formals for each parent to make sure it is not being redefined at all or that the parameter types match.
                if cls.inherits_iden is not None:
                    parent_names.add(cls.inherits_iden.ident_name)
                    for parent in parent_names:
                        if isinstance(parent, Method) and feature.feature_name.ident_name == parent.feature_name.ident_name:
                            if len(feature.formals_list) != len(parent.formals_list):
                                print(f"ERROR: {feature.feature_name.line_number}: Type-Check: The method, {feature.feature_name.ident_name}, in the class, {cls.name_iden.ident_name}, redefines parameters from the inherited method!\n")
                                exit(1)
                            for i in range(len(feature.formals_list)):
                                if feature.formals_list[i].formal_type != parent.formals_list[i].formal_type:
                                    print(f"ERROR: {feature.feature_name.line_number}: Type-Check: The method, {feature.feature_name.ident_name}, in the class, {cls.name_iden.ident_name}, has parameters that do not match inherited method!\n")
                                    exit(1)
                # We also check each method until we find main and if it has any parameters, we throw an error.
                for formal in feature.formals_list:
                    if feature.feature_name.ident_name == "main":
                        if len(feature.formals_list) > 0:
                            print(f"ERROR: 0: Type-Check: The method, main, inside of the Main class should not have any parameters!\n")
                            exit(1)
        # This section is setting up our symbol table for type checking.
        # We get information on classes with a list of their attributes and methods.
        symbol_table["classes"][cls.name_iden.ident_name] = {
            "inherits": cls.inherits_iden.ident_name if cls.inherits_iden else None,
            "attributes": {},
            "methods": {}
        }
        # We set up internal classes also.
        if cls.name_iden.ident_name == "Object":
            symbol_table["classes"][cls.name_iden.ident_name]["methods"] = {
                "abort": {
                    "return_type": "Object",
                    "formals": {}
                },
                "copy": {
                    "return_type": "SELF_TYPE",
                    "formals": {}
                },
                "type_name": {
                    "return_type": "String",
                    "formals": {}
                }
            }
        elif cls.name_iden.ident_name == "IO":
            symbol_table["classes"][cls.name_iden.ident_name]["inherits"] = "Object"
            symbol_table["classes"][cls.name_iden.ident_name]["methods"] = {
                "out_string": {
                    "return_type": "SELF_TYPE",
                    "formals": {
                        "arg": "String"
                    }
                },
                "out_int": {
                    "return_type": "SELF_TYPE",
                    "formals": {
                        "arg": "Int"
                    }
                },
                "in_string": {
                    "return_type": "String",
                    "formals": {}
                },
                "in_int": {
                    "return_type": "Int",
                    "formals": {}
                }
            }
        elif cls.name_iden.ident_name == "Int":
            symbol_table["classes"][cls.name_iden.ident_name]["inherits"] = "Object"
            symbol_table["classes"][cls.name_iden.ident_name]["methods"] = {}
        elif cls.name_iden.ident_name == "String":
            symbol_table["classes"][cls.name_iden.ident_name]["inherits"] = "Object"
            symbol_table["classes"][cls.name_iden.ident_name]["methods"] = {
                "concat": {
                    "return_type": "String",
                    "formals": {
                        "arg": "String"
                    }
                },
                "length": {
                    "return_type": "Int",
                    "formals": {}
                },                
                "substr": {
                    "return_type": "String",
                    "formals": {
                        "start": "Int",
                        "length": "Int"
                    }
                }
            }
        elif cls.name_iden.ident_name == "Bool":
            symbol_table["classes"][cls.name_iden.ident_name]["inherits"] = "Object"
            symbol_table["classes"][cls.name_iden.ident_name]["methods"] = {}
        else:
            # Setting up each class, if it is not internal, we add all of the attributes and methods they have into this list.
            # Inherited attributes and methods are added later on.
            for feature in cls.features:
                if isinstance(feature, Attribute):
                    symbol_table["classes"][cls.name_iden.ident_name]["attributes"][feature.feature_name.ident_name] = feature.feature_type.ident_name
                elif isinstance(feature, Method):
                    symbol_table["classes"][cls.name_iden.ident_name]["methods"][feature.feature_name.ident_name] = {
                        "return_type": feature.feature_type.ident_name,
                        "formals": {formal.formal_name.ident_name: formal.formal_type.ident_name for formal in feature.formals_list},
                        "body": feature.feature_body
                    }
    # After doing some basic type checking for classes, attributes, and methods, we start to look at the method and attribute feature bodies.
    for cls in ast:
        if cls.name_iden.ident_name not in ["Object", "IO", "Int", "String", "Bool"]:
            typeCheck(cls)
    # This section we are just going through and starting to write to our file depending on the conditions for PA4.
    # We sort our classes here in alphabetical order and use this to get all attributes and methods.
    sorted_classes = sorted(ast, key=lambda cls: cls.name_iden.ident_name)
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write("class_map\n")
        file.write(f"{len(sorted_classes)}\n")
        for cls in sorted_classes:
            file.write(f"{cls.name_iden.ident_name}\n")
            if cls.inherits_iden is not None:
                all_attributes = collect_parent_attributes(cls, sorted_classes)
            else:
                all_attributes = {attribute.feature_name.ident_name: (attribute, cls) for attribute in cls.attributes}
            file.write(f"{len(all_attributes)}\n")
            for attribute_name, (attribute, class_name) in all_attributes.items():
                if attribute is not None:
                    if attribute.feature_init is None:
                        file.write("no_initializer\n")
                    else:
                        file.write("initializer\n")
                    file.write(f"{attribute.feature_name.ident_name}\n")
                    file.write(f"{attribute.feature_type.ident_name}\n")
                    if attribute.feature_init is not None:
                        serialize_expression(attribute.feature_init, file)
        file.write("implementation_map\n")
        file.write(f"{len(sorted_classes)}\n")
        for cls in sorted_classes:
            file.write(f"{cls.name_iden.ident_name}\n")
            all_methods = {}
            if cls.inherits_iden is not None and cls.name_iden.ident_name != "Object":
                all_methods = collect_parent_methods(cls, sorted_classes)
            else:
                all_methods = {method.feature_name.ident_name: (method, cls) for method in cls.methods}
            file.write(f"{len(all_methods)}\n")
            for method_name, (method, inherits_class) in all_methods.items():
                if method is not None:
                    if method.internal_check:
                        if method.feature_name.ident_name in ["abort", "copy", "type_name"]:
                            serialize_internal(cls.name_iden.ident_name, method, "Object", file)
                        if method.feature_name.ident_name in ["in_int", "in_string", "out_int", "out_string"]:
                            serialize_internal(cls.name_iden.ident_name, method, "IO", file)
                        if method.feature_name.ident_name in ["concat", "length", "substr"]:
                            serialize_internal(cls.name_iden.ident_name, method, "String", file)
                    else:
                        file.write(f"{method.feature_name.ident_name}\n")
                        file.write(f"{len(method.formals_list)}\n")
                        for formal in method.formals_list:
                            file.write(f"{formal.formal_name.ident_name}\n")
                        if inherits_class.name_iden.ident_name == "Object":
                            file.write(f"{cls.name_iden.ident_name}\n")
                        else:
                            file.write(f"{inherits_class.name_iden.ident_name}\n")
                        serialize_expression(method.feature_body, file)
        file.write("parent_map\n")
        file.write(f"{len(sorted_classes) - 1}\n")
        for cls in sorted_classes:
            if cls.name_iden.ident_name == "Object":
                continue
            file.write(f"{cls.name_iden.ident_name}\n")
            if cls.inherits_iden is not None:
                file.write(f"{cls.inherits_iden.ident_name}\n")
            else:
                file.write("Object\n")
        file.write(f"{len(ast) - 5}\n")
        for cls in ast:
            if cls.name_iden.ident_name not in ["Object", "IO", "Int", "String", "Bool"]:
                file.write(f"{cls.name_iden.line_number}\n")
                file.write(f"{cls.name_iden.ident_name}\n")
                if cls.inherits_iden is None:
                    file.write("no_inherits\n")
                else:
                    if cls.inherits_object == False and cls.inherits_iden.ident_name == "Object":
                        file.write("no_inherits\n")
                    else:
                        file.write("inherits\n")
                        file.write(f"{cls.inherits_iden.line_number}\n")
                        file.write(f"{cls.inherits_iden.ident_name}\n")
                file.write(f"{len(cls.attributes) + len(cls.methods)}\n")
                for feature in cls.features:
                    if isinstance(feature, Attribute):
                        if feature.feature_init is None:
                            file.write("attribute_no_init\n")
                        else:
                            file.write("attribute_init\n")
                        file.write(f"{feature.feature_name.line_number}\n")
                        file.write(f"{feature.feature_name.ident_name}\n")
                        file.write(f"{feature.feature_name.line_number}\n")
                        file.write(f"{feature.feature_type.ident_name}\n")
                        if feature.feature_init is not None:
                            serialize_expression(feature.feature_init, file)
                    elif isinstance(feature, Method):
                        file.write("method\n")
                        file.write(f"{feature.feature_name.line_number}\n")
                        file.write(f"{feature.feature_name.ident_name}\n")
                        file.write(f"{len(feature.formals_list)}\n")
                        for formal in feature.formals_list:
                            file.write(f"{formal.formal_name.line_number}\n")
                            file.write(f"{formal.formal_name.ident_name}\n")
                            file.write(f"{formal.formal_type.line_number}\n")
                            file.write(f"{formal.formal_type.ident_name}\n")
                        file.write(f"{feature.feature_name.line_number}\n")
                        file.write(f"{feature.feature_type.ident_name}\n")
                        if feature.feature_body is not None:
                            serialize_expression(feature.feature_body, file)
        
if __name__ == '__main__':
    main()