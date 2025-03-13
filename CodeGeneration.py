# Hunter Mast / hunter.c.mast@vanderbilt.edu
# Resources used were Dr. Leach's videos.
import sys

# Here are all of our classes to create objects based on each of these methods, attrributes, or expressions.

class Attribute(object):
    def __init__(self, _id, _type, _init = None):
        self.id = _id
        self.type = _type
        self.init = _init

class Method(object):
    def __init__(self, method_name, formals, method_label):
        self.method_name = method_name
        self.formals = formals
        self.method_label = method_label

# This one is used for how the methods will be implemented in code generation.
class MethodImplementation(Method):
    def __init__(self, class_name, method_name, formals, method_label, exp):
        Method.__init__(self, method_name, formals, method_label)
        self.exp = exp
        self.class_name = class_name

class Variable(object):
    def __init__(self, line_number, name):
        self.line_number = line_number
        self.name = name

class Plus(object):
    def __init__(self, line_number, e1, e2):
        self.line_number = line_number
        self.e1 = e1
        self.e2 = e2

class Minus(object):
    def __init__(self, line_number, e1, e2):
        self.line_number = line_number
        self.e1 = e1
        self.e2 = e2

class Times(object):
    def __init__(self, line_number, e1, e2):
        self.line_number = line_number
        self.e1 = e1
        self.e2 = e2

class Divide(object):
    def __init__(self, line_number, e1, e2):
        self.line_number = line_number
        self.e1 = e1
        self.e2 = e2

class Lt(object):
    def __init__(self, line_number, e1, e2):
        self.line_number = line_number
        self.e1 = e1
        self.e2 = e2

class Le(object):
    def __init__(self, line_number, e1, e2):
        self.line_number = line_number
        self.e1 = e1
        self.e2 = e2

class Eq(object):
    def __init__(self, line_number, e1, e2):
        self.line_number = line_number
        self.e1 = e1
        self.e2 = e2

# This is for internal methods.
class Internal(object):
    def __init__(self, method):
        self.method = method

class Dispatch(object):
    def __init__(self, line_number, class_name, ro, method, formals, dispatch_type, method_type = None):
        self.line_number = line_number
        self.class_name = class_name
        self.ro = ro
        self.method = method
        self.formals = formals
        self.dispatch_type = dispatch_type
        self.method_type = method_type

class Assign(object):
    def __init__(self, line_number, assignee, rhs):
        self.line_number = line_number
        self.assignee = assignee
        self.rhs = rhs

class If(object):
    def __init__(self, line_number, predicate, then_body, else_body):
        self.line_number = line_number
        self.predicate = predicate
        self.then_body = then_body
        self.else_body = else_body

class While(object):
    def __init__(self, line_number, predicate, body):
        self.line_number = line_number
        self.predicate = predicate
        self.body = body

class Block(object):
    def __init__(self, line_number, exps):
        self.line_number = line_number
        self.exps = exps

class New(object):
    def __init__(self, line_number, new_type):
        self.line_number = line_number
        self.new_type = new_type

class IsVoid(object):
    def __init__(self, line_number, void_type):
        self.line_number = line_number
        self.void_type = void_type

class Not(object):
    def __init__(self, line_number, exp):
        self.line_number = line_number
        self.exp = exp

class Negate(object):
    def __init__(self, line_number, exp):
        self.line_number = line_number
        self.exp = exp

class Let(object):
    def __init__(self, line_number, body, binds):
        self.line_number = line_number
        self.body = body
        self.binds = binds

class Case(object):
    def __init__(self, line_number, case, exp):
        self.line_number = line_number
        self.case = case
        self.exp = exp

class Int(object):
    def __init__(self, line_number, value):
        self.line_number = line_number
        self.value = value

class String(object):
    def __init__(self, line_number, value):
        self.line_number = line_number
        self.value = value

class Bool(object):
    def __init__(self, line_number, value):
        self.line_number = line_number
        self.value = value

# This sets up register allocation, frame pointer allocation, and stack pointer allocation.

class Register(object):
    def __init__(self, offset = None):
        self.offset = offset

class FP(Register):
    def __init__(self, offset = None):
        self.offset = offset

    def __str__(self):
        if self.offset is None:
            return "fp"
        else:
            return "fp[%d]" % self.offset

class SP(Register):
    def __init__(self, offset = None):
        self.offset = offset

    def __str__(self):
        if self.offset is None:
            return "sp"
        else:
            return "sp[%d]" % self.offset

class R(Register):
    def __init__(self, which, offset = None):
        self.which = which
        self.offset = offset
        self.use_check = False

    def off(self, offset):
        return R(self.which, offset)

    def __str__(self):
        if self.offset is None:
            return "r%d" % self.which
        else:
            return "r%d[%d]" % (self.which, self.offset)

    def mark_used(self):
        self.use_check = True

    def mark_free(self):
        self.use_check = False

    def is_in_use(self):
        return self.use_check

# Here, all of the instructions in COOL assembly are formed here so they can be called and will return the correct string utilizing registers and more.

class Instruction:
    def __str__(self):
        return "instruction" 

class AddInstruction(Instruction):
    def __init__(self, recv, op1, op2):
        self.recv = recv
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        return "\t\t\t\tadd %s <- %s %s\n" % (self.recv, self.op1, self.op2)

class SubtractInstruction(Instruction):
    def __init__(self, recv, op1, op2):
        self.recv = recv
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        return "\t\t\t\tsub %s <- %s %s\n" % (self.recv, self.op1, self.op2)

class TimesInstruction(Instruction):
    def __init__(self, recv, op1, op2):
        self.recv = recv
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        return "\t\t\t\tmul %s <- %s %s\n" % (self.recv, self.op1, self.op2)

class DivideInstruction(Instruction):
    def __init__(self, recv, op1, op2):
        self.recv = recv
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        return "\t\t\t\tdiv %s <- %s %s\n" % (self.recv, self.op1, self.op2)

class StoreInstruction(Instruction):
    def __init__(self, address, offset, value):
        self.address = address
        self.offset = offset
        self.value = value

    def __str__(self):
        if self.offset is None:
            return "\t\t\t\tst %s <- %s\n" % (self.address, self.value)
        else:
            return "\t\t\t\tst %s[%d] <- %s\n" % (self.address, self.offset, self.value)

class LoadDoublewordInstruction(Instruction):
    def __init__(self, recv, address, offset = None):
        self.recv = recv
        self.address = address
        self.offset = offset

    def __str__(self):
        if self.offset is not None:
            return "\t\t\t\tld %s <- %s[%d]\n" % (self.recv, self.address, self.offset)
        else:
            return "\t\t\t\tld %s <- %s\n" % (self.recv, self.address) 

class LoadAddressInstruction(Instruction):
    def __init__(self, recv, label, title = None):
        self.recv = recv
        self.label = label
        self.title = title

    def __str__(self):
        if self.title is not None:
            return "\t\t\t\tla %s <- %s%s\n" % (self.recv, self.label, self.title)
        else:
            return "\t\t\t\tla %s <- %s\n" % (self.recv, self.label)

class LoadImmediateInstruction(Instruction):
    def __init__(self, recv, value):
        self.recv = recv
        self.value = value

    def __str__(self):
        return "\t\t\t\tli %s <- %d\n" % (self.recv, int(self.value))

class CallInstruction(Instruction):
    def __init__(self, recv):
        self.recv = recv

    def __str__(self):
        return "\t\t\t\tcall %s\n" % self.recv

class SystemCallInstruction(Instruction):
    def __init__(self, recv):
        self.recv = recv

    def __str__(self):
        return f"\t\t\t\tsyscall {self.recv}\n"

class JumpInstruction(Instruction):
    def __init__(self, label):
        self.label = label

    def __str__(self):
        return "\t\t\t\tjmp %s\n" % self.label

class MoveInstruction(Instruction):
    def __init__(self, recv, source):
        self.recv = recv
        self.source = source

    def __str__(self):
        return "\t\t\t\tmov %s <- %s\n" % (self.recv, self.source)

class AllocateInstruction(Instruction):
    def __init__(self, recv, size):
        self.recv = recv
        self.size = size

    def __str__(self):
        return "\t\t\t\talloc %s %s\n" % (self.recv, self.size)

class BranchOnZeroInstruction(Instruction):
    def __init__(self, conditional, label):
        self.conditional = conditional
        self.label = label

    def __str__(self):
        return "\t\t\t\tbz %s %s\n" % (self.conditional, self.label)

class BranchNotOnZeroInstruction(Instruction):
    def __init__(self, conditional, label):
        self.conditional = conditional
        self.label = label

    def __str__(self):
        return "\t\t\t\tbnz %s %s\n" % (self.conditional, self.label)

class BranchEqualInstruction(Instruction):
    def __init__(self, conditional1, conditional2, label):
        self.conditional1 = conditional1
        self.conditional2 = conditional2
        self.label = label

    def __str__(self):
        return "\t\t\t\tbeq %s %s %s\n" % (self.conditional1, self.conditional2, self.label)

class BranchLessThanInstruction(Instruction):
    def __init__(self, conditional1, conditional2, label):
        self.conditional1 = conditional1
        self.conditional2 = conditional2
        self.label = label

    def __str__(self):
        return "\t\t\t\tblt %s %s %s\n" % (self.conditional1, self.conditional2, self.label)

class BranchLessThanEqualToInstruction(Instruction):
    def __init__(self, conditional1, conditional2, label):
        self.conditional1 = conditional1
        self.conditional2 = conditional2
        self.label = label

    def __str__(self):
        return "\t\t\t\tble %s %s %s\n" % (self.conditional1, self.conditional2, self.label)

class PushInstruction(Instruction):
    def __init__(self, recv):
        self.recv = recv

    def __str__(self):
        return "\t\t\t\tpush %s\n" % self.recv

class PopInstruction(Instruction):
    def __init__(self, recv):
        self.recv = recv

    def __str__(self):
        return "\t\t\t\tpop %s\n" % self.recv

# Here, we go through and create our initial .asm file from a .type file.
annotated_ast_lines = []
if len(sys.argv) < 2:
    print("Specify .cl-type input file.\n")
    sys.exit(1)
input_filename = sys.argv[1]
if input_filename.endswith('.cl-type'):
    output_filename = input_filename[:-len('.cl-type')] + '.cl-asm'
else:
    output_filename = input_filename + '.cl-asm'
with open(input_filename) as f:
    annotated_ast_lines = [x[:-1] if x.endswith('\n') else x for x in f.readlines()]

index = 0
implemented_classes = []
# This is how we deserialize expressions.
def deserialize_expression(lines):
    global index
    global implemented_classes
    # We start with getting the line number and what value is next we need to check.
    expression = None
    line_number = lines[index]
    index += 1
    value_check = lines[index]
    index += 1
    exp_type = None
    identifier_name = None
    expression_name = None
    # If the value is a type, we look in here.
    if value_check in ["Int", "String", "Bool", "SELF_TYPE"] or value_check in implemented_classes:
        exp_type = value_check
        value_check = lines[index]
        index += 1
        # If the value under the type is an identifier, this is a variable and we send that back.
        if value_check == "identifier":
            index += 1
            identifier_name = lines[index]
            index += 1
            expression = Variable(line_number, identifier_name)
        # If the value under the type is not any expression, we do not move further for the name and we send back another variable.
        elif value_check not in ["assign", "dynamic_dispatch", "static_dispatch", "self_dispatch", "if", "while", "block", "new", "isvoid", "plus", "minus", "times", "divide", "lt", "le", "eq", "not", "negate", "let", "case", "integer", "string", "true", "false"]:
            identifier_name = lines[index]
            index += 1
            expression = Variable(line_number, identifier_name)
        # If the value is true or false, we go below and create a Bool.
        elif value_check == "true" or value_check == "false":
            expression_name = "bool"
        else:
            # If it is not a variable at all, it is an expression and we continue below.
            expression_name = value_check
    # If the value is an expression, we continue below and perform whatever operations for that expression.
    elif value_check in ["assign", "dynamic_dispatch", "static_dispatch", "self_dispatch", "if", "while", "block", "new", "isvoid", "plus", "minus", "times", "divide", "lt", "le", "eq", "not", "negate", "let", "case", "integer", "string", "true", "false"]:
        expression_name = value_check
    # If the value is not a type explicitly or an expression, we treat it like a type and continue just in case.
    else:
        exp_type = value_check
        expression_name = lines[index]
        if expression_name == "self_dispatch":
            index -= 1
        index += 1
    # We get the assignee name and the right hand side through recursion.
    if expression_name == "assign":
        index += 1
        assignee_name = lines[index]
        index += 1
        right_hand_side = deserialize_expression(lines)
        expression = Assign(line_number, assignee_name, right_hand_side)
    # For dynamic dispatch and static dispatch, we need to make sure we check to object type for it possibly being new, an identifier, a string, or self dispatch.
    elif expression_name == "dynamic_dispatch":
        index += 1
        class_name = lines[index]
        obj_type = None
        if lines[index + 1] == "new":
            obj_type = New(line_number, lines[index])
            index += 3
            method_type = lines[index]
            index += 2
        elif lines[index + 1] == "identifier":
            index += 3
            obj_type = Variable(line_number, lines[index])
            index += 2
        elif lines[index + 1] == "string":
            index += 2
            obj_type = String(line_number, lines[index])
            index += 2
        elif lines[index + 1] == "self_dispatch":
            index += 3
            method = lines[index]
            index += 1
            num_arguments = int(lines[index])
            index += 1
            arguments = []
            for _ in range(num_arguments):
                arguments.append(deserialize_expression(lines))
            obj_type = Dispatch(line_number, "self", Variable(line_number, "self_dispatch"), method, arguments, "self")
            index += 1
        method_name = lines[index]
        index += 1
        num_arguments = int(lines[index])
        index += 1
        arguments = []
        for _ in range(num_arguments):
            arguments.append(deserialize_expression(lines))
        expression = Dispatch(line_number, class_name, obj_type, method_name, arguments, "dynamic")
    elif expression_name == "static_dispatch":
        index += 1
        class_name = lines[index]
        obj_type = None
        if lines[index + 1] == "new":
            obj_type = New(line_number, lines[index])
            index += 3
            conform_type = lines[index]
            index += 2
        elif lines[index + 1] == "identifier":
            index += 3
            obj_type = Variable(line_number, lines[index])
            index += 2
        elif lines[index + 1] == "string":
            index += 2
            obj_type = String(line_number, lines[index])
            index += 2
        elif lines[index + 1] == "self_dispatch":
            index += 3
            method = lines[index]
            index += 1
            num_arguments = int(lines[index])
            index += 1
            arguments = []
            for _ in range(num_arguments):
                arguments.append(deserialize_expression(lines))
            obj_type = Dispatch(line_number, "self", Variable(line_number, "self_dispatch"), method, arguments, "self")
            index += 1
        method_type = lines[index]
        index += 2
        method_name = lines[index]
        index += 1
        num_arguments = int(lines[index])
        index += 1
        arguments = []
        for _ in range(num_arguments):
            arguments.append(deserialize_expression(lines))
        # The static type also needs to return the type of method we are dispatching to.
        expression = Dispatch(line_number, class_name, obj_type, method_name, arguments, "static", method_type)
    # Self dispatch is like dynamic and static dispatch, except the object type is always self.
    elif expression_name == "self_dispatch":
        index += 1
        method = lines[index]
        index += 1
        num_arguments = int(lines[index])
        index += 1
        arguments = []
        for _ in range(num_arguments):
            arguments.append(deserialize_expression(lines))
        expression = Dispatch(line_number, "self", Variable(line_number, "self_dispatch"), method, arguments, "self")
    # For if, while, isvoid, plus, minus, times, divide, lt, le, eq, not, and negate, we recursively get the information we need.
    elif expression_name == "if":
        expression = If(line_number, deserialize_expression(lines), deserialize_expression(lines), deserialize_expression(lines))
    elif expression_name == "while":
        expression = While(line_number, deserialize_expression(lines), deserialize_expression(lines))
    # This gets how many expressions are in the block and go through each one to return to the Block class object.
    elif expression_name == "block":
        expression_count = int(lines[index])
        index += 1
        expressions = []
        for _ in range(expression_count):
            expressions.append(deserialize_expression(lines))
        expression = Block(line_number, expressions)
    # New just gets the method name directly.
    elif expression_name == "new":
        index += 1
        method = lines[index]
        index += 1
        expression = New(line_number, method)
    elif expression_name == "isvoid":
        expression = IsVoid(line_number, deserialize_expression(lines))
    elif expression_name == "plus":
        expression = Plus(line_number, deserialize_expression(lines), deserialize_expression(lines))
    elif expression_name == "minus":
        expression = Minus(line_number, deserialize_expression(lines), deserialize_expression(lines))
    elif expression_name == "times":
        expression = Times(line_number, deserialize_expression(lines), deserialize_expression(lines))
    elif expression_name == "divide":
        expression = Divide(line_number, deserialize_expression(lines), deserialize_expression(lines))
    elif expression_name == "lt":
        expression = Lt(line_number, deserialize_expression(lines), deserialize_expression(lines))
    elif expression_name == "le":
        expression = Le(line_number, deserialize_expression(lines), deserialize_expression(lines))
    elif expression_name == "eq":
        expression = Eq(line_number, deserialize_expression(lines), deserialize_expression(lines))
    elif expression_name == "not":
        expression = Not(line_number, deserialize_expression(lines))
    elif expression_name == "negate":
        expression = Negate(line_number, deserialize_expression(lines))
    # For let, we get the number of binds and then make sure if we have an initializer or not.
    elif expression_name == "let":
        num_binds = int(lines[index])
        index += 1
        binds = []
        for _ in range(num_binds):
            bind_type = lines[index]
            index += 2
            identifier_name = lines[index]
            exp_type = None
            initializer_expr = None
            if bind_type == "let_binding_init":
                index += 2
                exp_type = lines[index]
                index += 1
                initializer_expr = deserialize_expression(lines)
            else:
                index += 2
                exp_type = lines[index]
                index += 1
            binds.append((identifier_name, exp_type, initializer_expr))
        expression = Let(line_number, deserialize_expression(lines), binds)
    # This is the same as let, but gets the case expression and will always get the case body.
    elif expression_name == "case":
        case_expression = deserialize_expression(lines)
        num_binds = int(lines[index])
        index += 1
        binds = []
        for _ in range(num_binds):
            index += 1
            case_exp = lines[index]
            index += 2
            case_type = lines[index]
            index += 1
            binds.append([case_exp, case_type, deserialize_expression(lines)])
        expression = Case(line_number, case_expression, binds)
    # This is for integer and string values.
    elif expression_name == "integer":
        value = lines[index]
        index += 1
        expression = Int(line_number, value)
    elif expression_name == "string":
        value = lines[index]
        index += 1
        expression = String(line_number, value)
    # For Bool, we need to go backwards one due to how it works with the checks above.
    elif expression_name == "bool":
        value = lines[index - 1]
        expression = Bool(line_number, value)
    return expression

# This deserializes the class map to get all of the attributes.
def deserialize_class_map(lines):
    global index
    global implemented_classes
    class_map = {}
    index += 1
    num_classes = int(lines[index])
    index += 1
    for _ in range(num_classes):
        class_name = lines[index]
        implemented_classes.append(class_name)
        index += 1
        attributes = []
        # This creates an unboxed attribute for Int, String, and Bool
        if class_name == "Int":
            attributes.append(Attribute("contents", "unboxed_int", 0))
        if class_name == "String":
            attributes.append(Attribute("contents", "unboxed_string", "the.empty.string"))
        if class_name == "Bool":
            attributes.append(Attribute("contents", "unboxed_bool", False))
        num_attributes = int(lines[index])
        index += 1
        for _ in range(num_attributes):
            attr_init = lines[index]
            index += 1
            if attr_init == "initializer":
                attr_name = lines[index]
                index += 1
                attr_type = lines[index]
                index += 1
                initializer_expression = deserialize_expression(lines)
                attributes.append(Attribute(attr_name, attr_type, initializer_expression))
            elif attr_init == "no_initializer":
                attr_name = lines[index]
                index += 1
                attr_type = lines[index]
                index += 1
                attributes.append(Attribute(attr_name, attr_type, None))
        class_map[class_name] = attributes
    return class_map

# This goes through the implementation map and will get all of the methods.
def deserialize_implementation_map(lines):
    global index
    implementation_map = {}
    index += 1
    num_classes = int(lines[index])
    index += 1
    for _ in range(num_classes):
        class_name = lines[index]
        index += 1
        methods = []
        num_methods = int(lines[index])
        index += 1
        for _ in range(num_methods):
            method_name = lines[index]
            index += 1
            num_formals = int(lines[index])
            index += 1
            formals = []
            for _ in range(num_formals):
                formal_name = lines[index]
                index += 1
                formals.append(formal_name)
            inheritance_class = lines[index]
            index += 1
            method_label = None
            # Here, we get if the method is internal.
            if lines[index + 2] == "internal" and method_name in ["abort", "copy", "type_name", "in_int", "in_string", "out_int", "out_string", "concat", "length", "substr"]:
                index += 1
                method_type = lines[index]
                index += 2
                method_label = lines[index]
                index += 1
                methods.append(Method(Internal(method_name), formals, method_label))
            # If it is internal, but created like with copy self dispatch, we go through that method body.
            elif lines[index + 2] != "internal" and method_name in ["abort", "copy", "type_name", "in_int", "in_string", "out_int", "out_string", "concat", "length", "substr"]:
                method_body = deserialize_expression(lines)
                method_label = inheritance_class + "." + method_name
                methods.append(Method(Internal(method_name), formals, method_label))
            else:
                # We get the method label from the inheritance class and method name, then go through it's body if the method is not inernal.
                method_label = inheritance_class + "." + method_name
                if method_name not in ["abort", "copy", "type_name", "in_int", "in_string", "out_int", "out_string", "concat", "length", "substr"]:
                    method_body = deserialize_expression(lines)
                methods.append(Method(method_name, formals, method_label))
        implementation_map[class_name] = methods
    return implementation_map

# We get all of of the parents and children from the parent map.
def deserialize_parent_map(lines):
    global index
    parent_map = {}
    index += 1
    parent_relationship_count = int(lines[index])
    index += 1
    for _ in range(parent_relationship_count):
        child_class = lines[index]
        index += 1
        parent_class = lines[index]
        index += 1
        parent_map[child_class] = parent_class
    return parent_map

# This uses the parent map to create a heirarchy.
def compute_hierarchy(parent_map):
    hierarchy = {cls: [] for cls in parent_map}
    hierarchy["Object"] = []
    for child, parent in parent_map.items():
        if parent not in hierarchy:
            hierarchy[parent] = []
        hierarchy[parent].append(child)
    return hierarchy

# This uses to heirarchy for depth first search to get each class's depth for case code generation.
def compute_depths(hierarchy):
    depths = {}
    def depth_first_search(class_name, depth):
        depths[class_name] = depth
        for child in hierarchy.get(class_name, []):
            depth_first_search(child, depth + 1)
    depth_first_search("Object", 0)
    return depths

# This goes through and deserailizes the annotated abstract syntax tree.
def deserialize_ast(lines):
    global index
    annotated_ast = []
    # Object is added first so it is printed first.
    annotated_ast.append(MethodImplementation("Object", "abort", [], "Object.abort", Internal("Object.abort")))
    annotated_ast.append(MethodImplementation("Object", "copy", [], "Object.copy", Internal("Object.copy")))
    annotated_ast.append(MethodImplementation("Object", "type_name", [], "Object.type_name", Internal("Object.type_name")))
    num_classes = int(lines[index])
    index += 1
    methods_unsorted = []
    for _ in range(num_classes):
        index += 1
        class_name = lines[index]
        index += 1
        if class_name == "Main":
            # Before class, we add IO to make sure they are only added once.
            methods_unsorted.append(MethodImplementation("IO", "in_int", [], "IO.in_int", Internal("IO.in_int")))
            methods_unsorted.append(MethodImplementation("IO", "in_string", [], "IO.in_string", Internal("IO.in_string")))
            methods_unsorted.append(MethodImplementation("IO", "out_int", ["x"], "IO.out_int", Internal("IO.out_int")))
            methods_unsorted.append(MethodImplementation("IO", "out_string", ["s"], "IO.out_string", Internal("IO.out_string")))
        inherits_check = lines[index]
        inheritance_class = None
        if inherits_check == "no_inherits":
            inheritance_class = class_name
            index += 1
        elif inherits_check == "inherits":
            index += 2
            inheritance_class = lines[index]
            index += 1
        num_attributes_and_methods = int(lines[index])
        index += 1
        attributes = []
        for _ in range(num_attributes_and_methods):
            attribute_or_method_check = lines[index]
            index += 2
            # Attributes are not needed here, so we don't do anything with them.
            if attribute_or_method_check == "attribute_no_init":
                attribute_name = lines[index]
                index += 2
                attribute_type = lines[index]
                index += 1
            elif attribute_or_method_check == "attribute_init":
                attribute_name = lines[index]
                index += 2
                attribute_type = lines[index]
                index += 1
                initializer_expression = deserialize_expression(lines)
            # This works like how we get the method in the implementation map, except the method bodies are included.
            elif attribute_or_method_check == "method":
                method_name = lines[index]
                index += 1
                num_formals = int(lines[index])
                index += 1
                formals = []
                for _ in range(num_formals):
                    index += 1
                    formal_name = lines[index]
                    index += 2
                    formal_type = lines[index]
                    index += 1
                    formals.append(formal_name)
                index += 2
                method_body = deserialize_expression(lines)
                method_label = None
                if method_name in ["abort", "copy", "type_name", "in_int", "in_string", "out_int", "out_string", "concat", "length", "substr"]:
                    method_label = inheritance_class + "." + method_name
                    methods_unsorted.append(MethodImplementation(class_name, Internal(method_label), formals, method_label, method_body))
                else:
                    method_label = class_name + "." + method_name
                    methods_unsorted.append(MethodImplementation(class_name, method_name, formals, method_label, method_body))
    # We sort the methods by class name and added to the ast list.
    methods_unsorted.sort(key = lambda method: method.class_name)
    for method_implemented in methods_unsorted:
        annotated_ast.append(method_implemented)
    # String is always at the end.
    annotated_ast.append(MethodImplementation("String", "concat", ["s"], "String.concat", Internal("String.concat")))
    annotated_ast.append(MethodImplementation("String", "length", [], "String.length", Internal("String.length")))
    annotated_ast.append(MethodImplementation("String", "substr", ["i", "l"], "String.substr", Internal("String.substr")))
    return annotated_ast

# This goes through and deserializes everything.
class_map = deserialize_class_map(annotated_ast_lines)
implementation_map = deserialize_implementation_map(annotated_ast_lines)
parent_map = deserialize_parent_map(annotated_ast_lines)
class_hierarchy = compute_hierarchy(parent_map)
class_depths = compute_depths(class_hierarchy)
ast = deserialize_ast(annotated_ast_lines)

# Here, we populate the string constants with class names and handle them.
classes = []
for class_name, attributes in class_map.items():
    classes.append(str(class_name))
string_constants = []
string_constants.append(("the.empty.string", ""))
for i, cls in enumerate(classes):
    string_constants.append((f"string{i + 1}", cls))

# This deals with class tags and how they are labeled.
class_tags = {}
current_tag = 10
for cls in classes:
    if cls == "Bool":
        class_tags[cls] = 0
    if cls == "Int":
        class_tags[cls] = 1
    if cls == "String":
        class_tags[cls] = 3
    if cls not in class_tags:
        class_tags[cls] = current_tag
        current_tag += 1

# These are the main registers we use (r0 - self, r1 - accumulator, r2 - temporary, r3 - field).
self_reg = R(0)
acc_reg = R(1)
tmp_reg = R(2)
field_reg = R(3)

# Here are all of our offsets and how we track them.
vtable_offset = 0
int_constant_offset = 1
argument_offset = 2
self_offset = 3
attribute_offset = 0
nested_offset = 0
local_offset = []
last_local_offset = 1
case_offset = 0

# These are some other global variables we keep track of (Class name, loops, and all of the instructions out).
current_class = None
loop_counter = 1
out_instructions = []

def cgen(exp, symbol_table):
    global string_constants
    global loop_counter
    global nested_offset
    global local_offset
    global last_local_offset
    global case_offset
    global current_class
    # For variables, we need to load to the r1 or r2, depending on the situation.
    if isinstance(exp, Variable):
        # If the symbol table has an offset, we print it directly with it.
        if hasattr(symbol_table[exp.name], "offset") and symbol_table[exp.name].offset != None:
            if acc_reg.is_in_use():
                out_instructions.append(LoadDoublewordInstruction(tmp_reg, symbol_table[exp.name]))
            else:
                out_instructions.append(LoadDoublewordInstruction(acc_reg, symbol_table[exp.name]))
        else:
            # If it has no offset, just make it a move instruction.
            out_instructions.append(MoveInstruction(acc_reg, symbol_table[exp.name]))
        return symbol_table[exp.name]
    # If it is an integer, we create a new integer and load it's value immediately.
    elif isinstance(exp, Int):
        cgen(New(exp.line_number, "Int"), symbol_table)
        out_instructions.append("\t\t\t\t;; INT\n")
        out_instructions.append(LoadImmediateInstruction(tmp_reg, exp.value))
        out_instructions.append(StoreInstruction(acc_reg, self_offset, tmp_reg))
        return acc_reg.off(2)
    # For strings, we make a new one if we do not already have a matching one, otherwise we create a new string constant.
    elif isinstance(exp, String):
        out_instructions.append("\t\t\t\t;; STRING\n")
        string_flag = False
        name_flag = None
        for name, value in string_constants:
            if exp.value == value:
                string_flag = True
                name_flag = name
        if string_flag and exp.value != "":
            out_instructions.append(f"\t\t\t\t;; STRING: {exp.value}\n")
            cgen(New(exp.line_number, "String"), symbol_table)
            out_instructions.append(LoadAddressInstruction(tmp_reg, name_flag))
            out_instructions.append(StoreInstruction(acc_reg, self_offset, tmp_reg))
        else:
            out_instructions.append(f"\t\t\t\t;; STRING: {exp.value}\n")
            string_constants.append((f"string{len(string_constants)}", exp.value))
            string_name = string_constants[len(string_constants) - 1][0]
            cgen(New(exp.line_number, "String"), symbol_table)
            out_instructions.append(LoadAddressInstruction(tmp_reg, string_name))
            out_instructions.append(StoreInstruction(acc_reg, self_offset, tmp_reg))
        return acc_reg.off(2)
    # If it is a bool, we create a new Bool and if it is true, load 1 immediately.
    elif isinstance(exp, Bool):
        out_instructions.append("\t\t\t\t;; BOOL\n")
        cgen(New(exp.line_number, "Bool"), symbol_table)
        if exp.value == "true":
            out_instructions.append(LoadImmediateInstruction(tmp_reg, 1))
            out_instructions.append(StoreInstruction(acc_reg, self_offset, tmp_reg))
        return acc_reg.off(2)
    # If itis new we reset the frame pointer, the self register, and the new type and go back to the old frame pointer.
    elif isinstance(exp, New):
        out_instructions.append("\t\t\t\t;; NEW\n")
        new_value = None
        if exp.new_type == "SELF_TYPE":
            new_value = current_class
        else:
            new_value = exp.new_type
        out_instructions.append(PushInstruction("fp"))
        out_instructions.append(PushInstruction(self_reg))
        out_instructions.append(LoadAddressInstruction(tmp_reg, new_value, "..new"))
        out_instructions.append(CallInstruction(tmp_reg))
        out_instructions.append(PopInstruction(self_reg))
        out_instructions.append(PopInstruction("fp"))
        return acc_reg
    # For dispatch, we handle dynamic, static, and self.
    elif isinstance(exp, Dispatch):
        out_instructions.append(f"\t\t\t\t;; DISPATCH ({exp.method})\n")
        out_instructions.append(PushInstruction(self_reg))
        out_instructions.append(PushInstruction("fp"))
        # We add self_dispatch to our new symbol table here for r0[2]
        symbol_table["self_dispatch"] = self_reg.off(2)
        # We go through each formal in our dispatch here recursively.
        for i, formal in enumerate(exp.formals):
            f_loc = cgen(formal, symbol_table)
            out_instructions.append(PushInstruction(acc_reg))
        # If our object type is dispatch we recursively call it.
        if isinstance(exp.ro, Dispatch):
            cgen(exp.ro, symbol_table)
        string_dispatch = None
        # Our class name should be our ro_type
        ro_type = exp.class_name
        # If our class name is SELF_TYPE, then we go through and set it to the correctly class.
        if ro_type == "SELF_TYPE":
            if exp.method in ["out_string", "out_int", "in_string", "in_int"]:
                ro_type = "IO"
            elif exp.method in ["abort", "copy", "type_name"]:
                ro_type = "Object"
            if exp.method in ["concat", "substr", "length"]:
                ro_type = "String"
        # Here, we go through each method and get the currnt offset for our method.
        method_offset = -1
        for i, method in enumerate(implementation_map[ro_type]):
            method_title = method.method_name
            if isinstance(method.method_name, Internal):
                method_title = method.method_name.method
            if exp.method == "abort":
                method_offset = 2
                break
            elif exp.method == "copy":
                method_offset = 3
                break
            elif exp.method == "type_name":
                method_offset = 4
                break
            elif exp.method == "concat" or exp.method == "in_int":
                method_offset = 5
                break
            elif exp.method == "length" or exp.method == "in_string":
                method_offset = 6
                break
            elif exp.method == "substr" or exp.method == "out_int":
                method_offset = 7
                break
            elif exp.method == "out_string":
                method_offset = 8
                break
            elif method_title == exp.method:
                method_offset = i + 2
                break
        # If we are going through dynamic and static dispatch, we need to create a branch for the dispatch on void exception.
        if str(exp.dispatch_type) == "dynamic" or str(exp.dispatch_type) == "static":
            out_instructions.append(f"\t\t\t\t;; RO ({exp.ro})\n")
            ro_loc = None
            if not isinstance(exp.ro, Dispatch):
                ro_loc = cgen(exp.ro, symbol_table)
            else:
                ro_loc = self_reg.off(2)
            loop = loop_counter
            loop_counter += 1
            out_instructions.append(BranchNotOnZeroInstruction(acc_reg, f"l{loop}"))
            dispatch_constant = None
            for name, value in string_constants:
                if value == f"ERROR: {int(exp.line_number)}: Exception: dispatch on void\\n":
                    dispatch_constant = name
            if dispatch_constant is None:
                string_constants.append((f"string{len(string_constants)}", f"ERROR: {int(exp.line_number)}: Exception: dispatch on void\\n"))
                dispatch_constant = string_constants[len(string_constants) - 1][0]
            out_instructions.append(LoadAddressInstruction(acc_reg, dispatch_constant))
            out_instructions.append(SystemCallInstruction("IO.out_string"))
            out_instructions.append(SystemCallInstruction("exit"))
            out_instructions.append(f"l{loop}:\n")
            out_instructions.append(PushInstruction(acc_reg))
            # Depending what our ro_type is, we need to set it to one of the below.
            call_type = ro_loc
            out_instructions.append(f"\t\t\t\t;; RO ({ro_type})\n")
            if ro_type == "SELF_TYPE" and exp.method in ["abort", "copy", "type_name", "out_string", "out_int", "in_string", "in_int", "concat", "substr", "length"]:
                call_type = self_reg.off(2)
            if ro_type == "SELF_TYPE":
                call_type = acc_reg.off(2)
            elif ro_type in class_map and ro_type != "self":
                call_type = acc_reg.off(2)
            elif ro_type == "self":
                call_type = self_reg.off(2)
            # If static, we need to load from the VTable.
            if exp.dispatch_type == "static":
                out_instructions.append(LoadAddressInstruction(tmp_reg, str(exp.method_type) + "..vtable"))
            else:
                out_instructions.append(LoadDoublewordInstruction(tmp_reg, call_type))
            out_instructions.append(LoadDoublewordInstruction(tmp_reg, tmp_reg, method_offset))
        # Self dispatch does not need an extra branch.
        else:
            out_instructions.append(PushInstruction(self_reg))
            ro_loc = None
            acc_reg.mark_used()
            if not isinstance(exp.ro, Dispatch):
                ro_loc = cgen(exp.ro, symbol_table)
            else:
                ro_loc = self_reg.off(2)
            acc_reg.mark_free()
            out_instructions.append(LoadDoublewordInstruction(tmp_reg, tmp_reg, method_offset))
        out_instructions.append(CallInstruction(tmp_reg))
        out_instructions.append(PopInstruction("fp"))
        out_instructions.append(PopInstruction(self_reg))
        return acc_reg
    # Here, we print all of the internal methods (These do not change and are only printed when we print the IO, Object, and String classes).
    elif isinstance(exp, Internal):
        out_instructions.append("\t\t\t\t;; INTERNAL\n")
        if exp.method == "IO.out_int":
            acc_reg.mark_used()
            v_loc = cgen(Variable(0, "x"), symbol_table)
            acc_reg.mark_free()
            out_instructions.append(LoadDoublewordInstruction(acc_reg, tmp_reg, self_offset))
            out_instructions.append(SystemCallInstruction("IO.out_int"))
            out_instructions.append(MoveInstruction(acc_reg, self_reg))
            return acc_reg
        elif exp.method == "IO.out_string":
            acc_reg.mark_used()
            v_loc = cgen(Variable(0, "s"), symbol_table)
            acc_reg.mark_free()
            out_instructions.append(LoadDoublewordInstruction(acc_reg, tmp_reg, self_offset))
            out_instructions.append(SystemCallInstruction("IO.out_string"))
            out_instructions.append(MoveInstruction(acc_reg, self_reg))
            return acc_reg
        elif exp.method == "IO.in_int":
            out_instructions.append(PushInstruction("fp"))
            out_instructions.append(PushInstruction(self_reg))
            out_instructions.append(LoadAddressInstruction(tmp_reg, "Int", "..new"))
            out_instructions.append(CallInstruction(tmp_reg))
            out_instructions.append(PopInstruction(self_reg))
            out_instructions.append(PopInstruction("fp"))
            out_instructions.append(MoveInstruction(tmp_reg, acc_reg))
            out_instructions.append(SystemCallInstruction("IO.in_int"))
            out_instructions.append(StoreInstruction(tmp_reg, self_offset, acc_reg))
            out_instructions.append(MoveInstruction(acc_reg, tmp_reg))
            return acc_reg
        elif exp.method == "IO.in_string":
            out_instructions.append(PushInstruction("fp"))
            out_instructions.append(PushInstruction(self_reg))
            out_instructions.append(LoadAddressInstruction(tmp_reg, "String", "..new"))
            out_instructions.append(CallInstruction(tmp_reg))
            out_instructions.append(PopInstruction(self_reg))
            out_instructions.append(PopInstruction("fp"))
            out_instructions.append(MoveInstruction(tmp_reg, acc_reg))
            out_instructions.append(SystemCallInstruction("IO.in_string"))
            out_instructions.append(StoreInstruction(tmp_reg, self_offset, acc_reg))
            out_instructions.append(MoveInstruction(acc_reg, tmp_reg))
            return acc_reg
        elif exp.method == "Object.abort":
            string_constants.append((f"string{len(string_constants)}", "abort\\n"))
            abort_constant = string_constants[len(string_constants) - 1][0]
            out_instructions.append(LoadAddressInstruction(acc_reg, abort_constant))
            out_instructions.append(SystemCallInstruction("IO.out_string"))
            out_instructions.append(SystemCallInstruction("exit"))
            return acc_reg
        elif exp.method == "Object.copy":
            out_instructions.append(LoadDoublewordInstruction(tmp_reg, self_reg, int_constant_offset))
            out_instructions.append(AllocateInstruction(acc_reg, tmp_reg))
            out_instructions.append(PushInstruction(acc_reg))
            loop1 = loop_counter
            loop_counter += 1
            loop2 = loop_counter
            loop_counter += 1
            out_instructions.append(f"l{loop1}:\n")
            out_instructions.append(BranchOnZeroInstruction(tmp_reg, f"l{loop2}"))
            out_instructions.append(LoadDoublewordInstruction(field_reg, self_reg, vtable_offset))
            out_instructions.append(StoreInstruction(acc_reg, vtable_offset, field_reg))
            out_instructions.append(LoadImmediateInstruction(field_reg, int_constant_offset))
            out_instructions.append(AddInstruction(self_reg, self_reg, field_reg))
            out_instructions.append(AddInstruction(acc_reg, acc_reg, field_reg))
            out_instructions.append(LoadImmediateInstruction(field_reg, int_constant_offset))
            out_instructions.append(SubtractInstruction(tmp_reg, tmp_reg, field_reg))
            out_instructions.append(JumpInstruction(f"l{loop1}"))
            out_instructions.append(f"l{loop2}:\n")
            out_instructions.append(PopInstruction(acc_reg))
            return acc_reg
        elif exp.method == "Object.type_name":
            out_instructions.append(PushInstruction("fp"))
            out_instructions.append(PushInstruction(self_reg))
            out_instructions.append(LoadAddressInstruction(tmp_reg, "String", "..new"))
            out_instructions.append(CallInstruction(tmp_reg))
            out_instructions.append(PopInstruction(self_reg))
            out_instructions.append(PopInstruction("fp"))
            out_instructions.append(LoadDoublewordInstruction(tmp_reg, self_reg, 2))
            out_instructions.append(LoadDoublewordInstruction(tmp_reg, tmp_reg, vtable_offset))
            out_instructions.append(StoreInstruction(acc_reg, self_offset, tmp_reg))
            return acc_reg
        elif exp.method == "String.concat":
            out_instructions.append(PushInstruction("fp"))
            out_instructions.append(PushInstruction(self_reg))
            out_instructions.append(LoadAddressInstruction(tmp_reg, "String", "..new"))
            out_instructions.append(CallInstruction(tmp_reg))
            out_instructions.append(PopInstruction(self_reg))
            out_instructions.append(PopInstruction("fp"))
            out_instructions.append(MoveInstruction(field_reg, acc_reg))
            acc_reg.mark_used()
            v_loc = cgen(Variable(0, "s"), symbol_table)
            acc_reg.mark_free()
            out_instructions.append(LoadDoublewordInstruction(tmp_reg, tmp_reg, self_offset))
            out_instructions.append(LoadDoublewordInstruction(acc_reg, self_reg, self_offset))
            out_instructions.append(SystemCallInstruction("String.concat"))
            out_instructions.append(StoreInstruction(field_reg, self_offset, acc_reg))
            out_instructions.append(MoveInstruction(acc_reg, field_reg))
            return acc_reg
        elif exp.method == "String.length":
            out_instructions.append(PushInstruction("fp"))
            out_instructions.append(PushInstruction(self_reg))
            out_instructions.append(LoadAddressInstruction(tmp_reg, "Int", "..new"))
            out_instructions.append(CallInstruction(tmp_reg))
            out_instructions.append(PopInstruction(self_reg))
            out_instructions.append(PopInstruction("fp"))
            out_instructions.append(MoveInstruction(tmp_reg, acc_reg))
            out_instructions.append(LoadDoublewordInstruction(acc_reg, self_reg, self_offset))
            out_instructions.append(SystemCallInstruction("String.length"))
            out_instructions.append(StoreInstruction(tmp_reg, self_offset, acc_reg))
            out_instructions.append(MoveInstruction(acc_reg, tmp_reg))
            return acc_reg
        elif exp.method == "String.substr":
            string_constants.append((f"string{len(string_constants)}", "ERROR: 0: Exception: String.substr out of range\\n"))
            substr_constant = string_constants[len(string_constants) - 1][0]
            out_instructions.append(PushInstruction("fp"))
            out_instructions.append(PushInstruction(self_reg))
            out_instructions.append(LoadAddressInstruction(tmp_reg, "String", "..new"))
            out_instructions.append(CallInstruction(tmp_reg))
            out_instructions.append(PopInstruction(self_reg))
            out_instructions.append(PopInstruction("fp"))
            out_instructions.append(MoveInstruction(field_reg, acc_reg))
            acc_reg.mark_used()
            v_loc_1 = cgen(Variable(0, "i"), symbol_table)
            acc_reg.mark_free()
            out_instructions.append(LoadDoublewordInstruction(tmp_reg, tmp_reg, self_offset))
            v_loc_2 = cgen(Variable(0, "l"), symbol_table)
            out_instructions.append(LoadDoublewordInstruction(acc_reg, acc_reg, self_offset))
            out_instructions.append(LoadDoublewordInstruction(self_reg, self_reg, self_offset))
            out_instructions.append(SystemCallInstruction("String.substr"))
            loop = loop_counter
            loop_counter += 1
            out_instructions.append(BranchNotOnZeroInstruction(acc_reg, f"l{loop}"))
            out_instructions.append(LoadAddressInstruction(acc_reg, substr_constant))
            out_instructions.append(SystemCallInstruction("IO.out_string"))
            out_instructions.append(SystemCallInstruction("exit"))
            out_instructions.append(f"l{loop}:\n")
            out_instructions.append(StoreInstruction(field_reg, self_offset, acc_reg))
            out_instructions.append(MoveInstruction(acc_reg, field_reg))
            return acc_reg
    # All of the arethmetic equations are set up the same.
    # We go through e1 and store it, then go through e2.
    # It performs the operation, then creates a new integer to store it in.
    elif isinstance(exp, Plus):
        last_local_offset -= 1
        out_instructions.append("\t\t\t\t;; Plus\n")
        out_instructions.append("\t\t\t\t;; E1\n")
        # This is how local offsets are being controlled and when we get deeper into a function, how we handle it.
        # If it is the same as the expression we are going through we add 1.
        if isinstance(exp.e1, Plus):
            last_local_offset += 1
        e1_loc = cgen(exp.e1, symbol_table)
        # If it is different, we add 1 after.
        if isinstance(exp.e1, (Minus, Times, Divide, Negate)):
            last_local_offset += 1
        out_instructions.append(LoadDoublewordInstruction(acc_reg, acc_reg, self_offset))
        out_instructions.append(StoreInstruction("fp", last_local_offset, acc_reg))
        out_instructions.append("\t\t\t\t;; E2\n")
        if isinstance(exp.e2, Plus):
            last_local_offset += 1
        e2_loc = cgen(exp.e2, symbol_table)
        if isinstance(exp.e2, (Minus, Times, Divide, Negate)):
            last_local_offset += 1
        out_instructions.append(LoadDoublewordInstruction(acc_reg, acc_reg, self_offset))
        out_instructions.append(LoadDoublewordInstruction(tmp_reg, "fp", last_local_offset))
        out_instructions.append(AddInstruction(acc_reg, tmp_reg, acc_reg))
        out_instructions.append(StoreInstruction("fp", last_local_offset, acc_reg))
        cgen(New(exp.line_number, "Int"), symbol_table)
        out_instructions.append(LoadDoublewordInstruction(tmp_reg, "fp", last_local_offset))
        out_instructions.append(StoreInstruction(acc_reg, self_offset, tmp_reg))
        return acc_reg
    elif isinstance(exp, Minus):
        last_local_offset -= 1
        out_instructions.append("\t\t\t\t;; Minus\n")
        out_instructions.append("\t\t\t\t;; E1\n")
        if isinstance(exp.e1, Minus):
            last_local_offset += 1
        e1_loc = cgen(exp.e1, symbol_table)
        if isinstance(exp.e1, (Plus, Times, Divide, Negate)):
            last_local_offset += 1
        out_instructions.append(LoadDoublewordInstruction(acc_reg, acc_reg, self_offset))
        out_instructions.append(StoreInstruction("fp", last_local_offset, acc_reg))
        out_instructions.append("\t\t\t\t;; E2\n")
        if isinstance(exp.e2, Minus):
            last_local_offset += 1
        e2_loc = cgen(exp.e2, symbol_table)
        if isinstance(exp.e2, (Plus, Times, Divide, Negate)):
            last_local_offset += 1
        out_instructions.append(LoadDoublewordInstruction(acc_reg, acc_reg, self_offset))
        out_instructions.append(LoadDoublewordInstruction(tmp_reg, "fp", last_local_offset))
        out_instructions.append(SubtractInstruction(acc_reg, tmp_reg, acc_reg))
        out_instructions.append(StoreInstruction("fp", last_local_offset, acc_reg))
        cgen(New(exp.line_number, "Int"), symbol_table)
        out_instructions.append(LoadDoublewordInstruction(tmp_reg, "fp", last_local_offset))
        out_instructions.append(StoreInstruction(acc_reg, self_offset, tmp_reg))
        return acc_reg
    elif isinstance(exp, Times):
        last_local_offset -= 1
        out_instructions.append("\t\t\t\t;; Times\n")
        out_instructions.append("\t\t\t\t;; E1\n")
        if isinstance(exp.e1, Times):
            last_local_offset += 1
        e1_loc = cgen(exp.e1, symbol_table)
        if isinstance(exp.e1, (Plus, Minus, Divide, Negate)):
            last_local_offset += 1
        out_instructions.append(LoadDoublewordInstruction(acc_reg, acc_reg, self_offset))
        out_instructions.append(StoreInstruction("fp", last_local_offset, acc_reg))
        out_instructions.append("\t\t\t\t;; E2\n")
        if isinstance(exp.e2, Times):
            last_local_offset += 1
        e2_loc = cgen(exp.e2, symbol_table)
        if isinstance(exp.e2, (Plus, Minus, Divide, Negate)):
            last_local_offset += 1
        out_instructions.append(LoadDoublewordInstruction(acc_reg, acc_reg, self_offset))
        out_instructions.append(LoadDoublewordInstruction(tmp_reg, "fp", last_local_offset))
        out_instructions.append(TimesInstruction(acc_reg, tmp_reg, acc_reg))
        out_instructions.append(StoreInstruction("fp", last_local_offset, acc_reg))
        cgen(New(exp.line_number, "Int"), symbol_table)
        out_instructions.append(LoadDoublewordInstruction(tmp_reg, "fp", last_local_offset))
        out_instructions.append(StoreInstruction(acc_reg, self_offset, tmp_reg))
        return acc_reg
    # Divide is mostly the same, but we have to create a branch for it.
    elif isinstance(exp, Divide):
        last_local_offset -= 1
        out_instructions.append("\t\t\t\t;; Divide\n")
        out_instructions.append("\t\t\t\t;; E1\n")
        if isinstance(exp.e1, Divide):
            last_local_offset += 1
        e1_loc = cgen(exp.e1, symbol_table)
        if isinstance(exp.e1, (Plus, Minus, Times, Negate)):
            last_local_offset += 1
        out_instructions.append(LoadDoublewordInstruction(acc_reg, acc_reg, self_offset))
        out_instructions.append(StoreInstruction("fp", last_local_offset, acc_reg))
        out_instructions.append("\t\t\t\t;; E2\n")
        if isinstance(exp.e2, Divide):
            last_local_offset += 1
        e2_loc = cgen(exp.e2, symbol_table)
        if isinstance(exp.e2, (Plus, Minus, Times, Negate)):
            last_local_offset += 1
        out_instructions.append(LoadDoublewordInstruction(tmp_reg, acc_reg, self_offset))
        loop = loop_counter
        loop_counter += 1
        # This branch creates an error exception for division by 0.
        out_instructions.append(BranchNotOnZeroInstruction(tmp_reg, f"l{loop}"))
        string_constant_name = None
        for name, value in string_constants:
            if value == f"ERROR: {exp.line_number}: Exception: division by zero\\n":
                string_constant_name = name
        if string_constant_name is None:
            string_constants.append((f"string{len(string_constants)}", f"ERROR: {exp.line_number}: Exception: division by zero\\n"))
            string_constant_name = string_constants[len(string_constants) - 1][0]
        out_instructions.append(LoadAddressInstruction(acc_reg, string_constant_name))
        out_instructions.append(SystemCallInstruction("IO.out_string"))
        out_instructions.append(SystemCallInstruction("exit"))
        out_instructions.append(f"l{loop}:\n")
        out_instructions.append(LoadDoublewordInstruction(acc_reg, acc_reg, self_offset))
        out_instructions.append(LoadDoublewordInstruction(tmp_reg, "fp", last_local_offset))
        out_instructions.append(DivideInstruction(acc_reg, tmp_reg, acc_reg))
        out_instructions.append(StoreInstruction("fp", last_local_offset, acc_reg))
        cgen(New(exp.line_number, "Int"), symbol_table)
        out_instructions.append(LoadDoublewordInstruction(tmp_reg, "fp", last_local_offset))
        out_instructions.append(StoreInstruction(acc_reg, self_offset, tmp_reg))
        return acc_reg
    if isinstance(exp, Assign):
        out_instructions.append("\t\t\t\t;; ASSIGN\n")
        if not isinstance(exp.rhs, (Plus, Minus, Times, Divide, Negate)):
            last_local_offset -= 1
        rhs = cgen(exp.rhs, symbol_table)
        if not isinstance(exp.rhs, (Plus, Minus, Times, Divide, Negate)):
            last_local_offset += 1
        # Here, we check if the assignee is already in our symbol table and at what offset to store it into.
        if exp.assignee in symbol_table:
            if hasattr(symbol_table[exp.assignee], "offset"):
                variable_offset = symbol_table[exp.assignee].offset
                out_instructions.append(StoreInstruction(symbol_table[exp.assignee], None, acc_reg))
        # If we have not stored to it before, we find where it needs stored to.
        else:
            class_info = class_layout.get(exp.class_name)
            if class_info and "fields" in class_info:
                if exp.assignee in class_info["fields"]:
                    field_offset = class_info["fields"][exp.assignee]
                    out_instructions.append(StoreInstruction(self_reg, field_offset, acc_reg))
        return acc_reg
    elif isinstance(exp, If):
        out_instructions.append("\t\t\t\t;; If statement\n")
        cond_reg = cgen(exp.predicate, symbol_table)
        # For the if expression, we need to create different branches for each else body, then body, and the end of the if statement.
        else_loop = loop_counter
        else_label = f"l{else_loop}"
        loop_counter += 1
        then_loop = loop_counter
        then_label = f"l{then_loop}"
        loop_counter += 1
        end_loop = loop_counter
        end_loop = f"l{end_loop}"
        loop_counter += 1
        out_instructions.append(LoadDoublewordInstruction(acc_reg, acc_reg , self_offset))
        out_instructions.append(BranchNotOnZeroInstruction(acc_reg, else_label))
        out_instructions.append(f"{then_label}:\n")
        if exp.else_body:
            cgen(exp.else_body, symbol_table)
        # If finished with the else body, we jump to the end.
        out_instructions.append(JumpInstruction(end_loop))
        out_instructions.append(f"{else_label}:\n")
        if exp.then_body:
            cgen(exp.then_body, symbol_table)
        out_instructions.append(f"{end_loop}:\n")
        return acc_reg
    elif isinstance(exp, While):
        out_instructions.append("\t\t\t\t;; WHILE loop\n")
        loop = loop_counter
        loop_label = f"l{loop}"
        loop_counter += 1
        pool = loop_counter
        pool_label = f"l{pool}"
        loop_counter += 1
        out_instructions.append(f"{loop_label}:\n")
        cond_reg = cgen(exp.predicate, symbol_table)
        out_instructions.append(LoadDoublewordInstruction(acc_reg, acc_reg, self_offset))
        out_instructions.append(BranchOnZeroInstruction(acc_reg, pool_label))
        cgen(exp.body, symbol_table)
        # Our loop brings us back to the label above if we are not leaving the loop yet.
        out_instructions.append(JumpInstruction(loop_label))
        out_instructions.append(f"{pool_label}:\n")
        return acc_reg
    # For Block, we just go through each expression set inside of it.
    elif isinstance(exp, Block):
        for i, expression in enumerate(exp.exps):
            cgen(expression, symbol_table)
        return acc_reg
    # Void is similar to if and while, except we need to create a new true or false Bool, depending on the outcome.
    elif isinstance(exp, IsVoid):
        out_instructions.append("\t\t\t\t;; ISVOID\n")
        cond_reg = cgen(exp.void_type, symbol_table)
        else_loop = loop_counter
        else_label = f"l{else_loop}"
        loop_counter += 1
        then_loop = loop_counter
        then_label = f"l{then_loop}"
        loop_counter += 1
        end_loop = loop_counter
        end_loop = f"l{end_loop}"
        loop_counter += 1
        out_instructions.append(BranchOnZeroInstruction(acc_reg, else_label))
        out_instructions.append(f"{then_label}:\n")
        # False bool and jump to end.
        cgen(New(exp.line_number, "Bool"), symbol_table)
        out_instructions.append(JumpInstruction(end_loop))
        out_instructions.append(f"{else_label}:\n")
        # True bool.
        cgen(New(exp.line_number, "Bool"), symbol_table)
        out_instructions.append(LoadImmediateInstruction(tmp_reg, 1))
        out_instructions.append(StoreInstruction(acc_reg, self_offset, tmp_reg))
        out_instructions.append(f"{end_loop}:\n")
        return acc_reg
    # Not reverses what the current Boolean value is and replaces it with the opposite.
    elif isinstance(exp, Not):
        out_instructions.append("\t\t\t\t;; NOT\n")
        cond_reg = cgen(exp.exp, symbol_table)
        else_loop = loop_counter
        else_label = f"l{else_loop}"
        loop_counter += 1
        then_loop = loop_counter
        then_label = f"l{then_loop}"
        loop_counter += 1
        end_loop = loop_counter
        end_loop = f"l{end_loop}"
        loop_counter += 1
        out_instructions.append(LoadDoublewordInstruction(acc_reg, acc_reg, self_offset))
        out_instructions.append(BranchNotOnZeroInstruction(acc_reg, else_label))
        out_instructions.append(f"{then_label}:\n")
        cgen(New(exp.line_number, "Bool"), symbol_table)
        out_instructions.append(LoadImmediateInstruction(tmp_reg, 1))
        out_instructions.append(StoreInstruction(acc_reg, self_offset, tmp_reg))
        out_instructions.append(JumpInstruction(end_loop))
        out_instructions.append(f"{else_label}:\n")
        cgen(New(exp.line_number, "Bool"), symbol_table)
        out_instructions.append(f"{end_loop}:\n")
        return acc_reg
    # Negate works similar to not, except we need to create new ints.
    elif isinstance(exp, Negate):
        out_instructions.append("\t\t\t\t;; NEGATE\n")
        # Here, we create an integer equal to 0.
        cgen(New(exp.line_number, "Int"), symbol_table)
        out_instructions.append(LoadImmediateInstruction(tmp_reg, 0))
        out_instructions.append(StoreInstruction(acc_reg, self_offset, tmp_reg))
        out_instructions.append(LoadDoublewordInstruction(acc_reg, acc_reg, self_offset))
        out_instructions.append(StoreInstruction("fp", last_local_offset, acc_reg))
        out_instructions.append("\t\t\t\t;; NEGATE EXP\n")
        cgen(exp.exp, symbol_table)
        out_instructions.append(LoadDoublewordInstruction(acc_reg, acc_reg, self_offset))
        out_instructions.append(LoadDoublewordInstruction(tmp_reg, "fp", last_local_offset))
        out_instructions.append(SubtractInstruction(acc_reg, tmp_reg, acc_reg))
        # After we load our value to be negated, we subtract it from 0 to get the negative of that number and save it.
        out_instructions.append(StoreInstruction("fp", last_local_offset, acc_reg))
        cgen(New(exp.line_number, "Int"), symbol_table)
        out_instructions.append(LoadDoublewordInstruction(tmp_reg, "fp", last_local_offset))
        out_instructions.append(StoreInstruction(acc_reg, self_offset, tmp_reg))
        return acc_reg
    elif isinstance(exp, Let):
        out_instructions.append("\t\t\t\t;; LET\n")
        # Here, we create a copy of the symbol table to pass around.
        local_symbol_table = symbol_table.copy()
        offset_counter = 0
        for var, exp_type, init in exp.binds:
            # This is where we handle the local offset in a let expression and start implementing it.
            offset = -len(local_offset) - 1
            offset_counter += 1
            local_offset.append(0)
            # We add each variable to our symbol table and add it to the frame pointer at the current offset.
            local_symbol_table[var] = FP(offset + 1)
            # If we have no initialization and it is of our primitive types, we create a new type from that.
            if exp_type in ["Int", "String", "Bool"] and init is None:
                out_instructions.append("\t\t\t\t;; LET HERE\n")
                cgen(New(exp.line_number, str(exp_type)), local_symbol_table)
                if exp_type == "String":
                    out_instructions.append(LoadAddressInstruction(field_reg, "the.empty.string"))
                    out_instructions.append(StoreInstruction(acc_reg, self_offset, field_reg))
            # If none, it just loads 0 to r1.
            elif init is None:
                out_instructions.append(LoadImmediateInstruction(acc_reg, 0))
            # Here, we run through the initialization.
            if init is not None:
                cgen(init, local_symbol_table)
            out_instructions.append(StoreInstruction("fp", offset + 1, acc_reg))
        # This will reset the last_local_offset to what it currently is and then goes through the body.
        last_local_offset = -len(local_offset) + 1
        cgen(exp.body, local_symbol_table)
        for _ in range(offset_counter):
            local_offset.pop()
        return acc_reg
    # The case expression is similar to let.
    elif isinstance(exp, Case):
        out_instructions.append("\t\t\t\t;; CASE Start\n")
        local_symbol_table = symbol_table.copy()
        offset_counter = 0
        offset = -len(local_offset) - 1
        local_offset.append(0)
        offset_counter += 1
        # We add what case returns to our symbol table (This should I believe always be a variable, so the else should not matter).
        if isinstance(exp.case, Variable):
            local_symbol_table[exp.case.name] = cgen(exp.case, local_symbol_table)
        else:
            local_symbol_table[str(exp.case)] = cgen(exp.case, local_symbol_table)
        void_case = loop_counter
        loop_counter += 1
        # We branch on zero to check if case is void.
        out_instructions.append(BranchOnZeroInstruction(acc_reg, f"l{void_case}"))
        out_instructions.append(StoreInstruction("fp", offset + 1, acc_reg))
        out_instructions.append(LoadDoublewordInstruction(acc_reg, acc_reg, 0))
        out_instructions.append("\t\t\t\t;; CASE Expression\n")
        # Here, we use depth first search to go through each of the branches and create a label for them while mapping where they should go.
        branch_labels = {}
        for branch_name, branch_type, branch_body in exp.exp:
            if branch_type in class_tags:
                branch_label = loop_counter
                loop_counter += 1
                branch_labels[branch_type] = branch_label
        case_error = loop_counter
        loop_counter += 1
        for class_tag, tag_value in class_tags.items():
            if class_tag in branch_labels:
                out_instructions.append(LoadImmediateInstruction(tmp_reg, tag_value))
                out_instructions.append(BranchEqualInstruction(acc_reg, tmp_reg, f"l{branch_labels[class_tag]}"))
            else:
                # If they do not ahve any specific case to go to, they are sent to object.
                if "Object" in branch_labels:
                    class_tag = "Object"
                    out_instructions.append(LoadImmediateInstruction(tmp_reg, tag_value))
                    out_instructions.append(BranchEqualInstruction(acc_reg, tmp_reg, f"l{branch_labels[class_tag]}"))
                else:
                    out_instructions.append(LoadImmediateInstruction(tmp_reg, tag_value))
                    out_instructions.append(BranchEqualInstruction(acc_reg, tmp_reg, f"l{case_error}"))
        # If case is missing branches or cannot find a matching one, we throw an error.
        out_instructions.append(f"l{case_error}:\n")
        string_constant_name = None
        for name, value in string_constants:
            if value == f"ERROR: {exp.line_number}: Exception: case without matching branch.\\n":
                string_constant_name = name
        if string_constant_name is None:
            string_constants.append((f"string{len(string_constants)}", f"ERROR: {exp.line_number}: Exception: case without matching branch.\\n"))
            string_constant_name = string_constants[len(string_constants) - 1][0]
        out_instructions.append(LoadAddressInstruction(acc_reg, string_constant_name))
        out_instructions.append(SystemCallInstruction("IO.out_string"))
        out_instructions.append(SystemCallInstruction("exit"))
        # If the case expression is void, we throw an error.
        out_instructions.append(f"l{void_case}:\n")
        string_constant_name = None
        for name, value in string_constants:
            if value == f"ERROR: {exp.line_number}: Exception: case on void.\\n":
                string_constant_name = name
        if string_constant_name is None:
            string_constants.append((f"string{len(string_constants)}", f"ERROR: {exp.line_number}: Exception: case on void.\\n"))
            string_constant_name = string_constants[len(string_constants) - 1][0]
        out_instructions.append(LoadAddressInstruction(acc_reg, string_constant_name))
        out_instructions.append(SystemCallInstruction("IO.out_string"))
        out_instructions.append(SystemCallInstruction("exit"))
        end_label = loop_counter
        loop_counter += 1
        # Finally, we go through each branch and print it's body.
        last_local_offset = -len(local_offset) + 1
        for branch_name, branch_type, branch_body in exp.exp:
            out_instructions.append(f"l{branch_labels[branch_type]}:\n")
            local_symbol_table[branch_name] = FP(offset + 1)
            cgen(branch_body, local_symbol_table)
            out_instructions.append(JumpInstruction(f"l{end_label}"))
        out_instructions.append(f"l{end_label}:\n")
        for _ in range(offset_counter):
            local_offset.pop()
        return acc_reg
    # For these, it works pretty much the same as the other arithmetic operations, except it calls the appropriate handler instead of r2.
    elif isinstance(exp, Eq):
        out_instructions.append("\t\t\t\t;; Equal To\n")
        out_instructions.append(PushInstruction(self_reg))
        out_instructions.append(PushInstruction("fp"))
        e1_loc = cgen(exp.e1, symbol_table)
        out_instructions.append(PushInstruction(acc_reg))
        e2_loc = cgen(exp.e2, symbol_table)
        out_instructions.append(PushInstruction(acc_reg))
        out_instructions.append(PushInstruction(self_reg))
        out_instructions.append(CallInstruction("eq_handler"))
        out_instructions.append(PopInstruction("fp"))
        out_instructions.append(PopInstruction(self_reg))
        return acc_reg
    elif isinstance(exp, Le):
        out_instructions.append("\t\t\t\t;; Less Then or Equal To\n")
        out_instructions.append(PushInstruction(self_reg))
        out_instructions.append(PushInstruction("fp"))
        e1_loc = cgen(exp.e1, symbol_table)
        out_instructions.append(PushInstruction(acc_reg))
        e2_loc = cgen(exp.e2, symbol_table)
        out_instructions.append(PushInstruction(acc_reg))
        out_instructions.append(PushInstruction(self_reg))
        out_instructions.append(CallInstruction("le_handler"))
        out_instructions.append(PopInstruction("fp"))
        out_instructions.append(PopInstruction(self_reg))
        return acc_reg
    elif isinstance(exp, Lt):
        out_instructions.append("\t\t\t\t;; Less Than\n")
        out_instructions.append(PushInstruction(self_reg))
        out_instructions.append(PushInstruction("fp"))
        e1_loc = cgen(exp.e1, symbol_table)
        out_instructions.append(PushInstruction(acc_reg))
        e2_loc = cgen(exp.e2, symbol_table)
        out_instructions.append(PushInstruction(acc_reg))
        out_instructions.append(PushInstruction(self_reg))
        out_instructions.append(CallInstruction("lt_handler"))
        out_instructions.append(PopInstruction("fp"))
        out_instructions.append(PopInstruction(self_reg))
        return acc_reg

# This will go through and calculate how temporary stack room is calculated based on certain conditions.
# Lots of this logic is based on how NumTemps are calculated.
def calculate_reserve_space(exp):
    if isinstance(exp, Variable):
        return 0
    elif isinstance(exp, (Int, String, Bool)):
        return 0
    elif isinstance(exp, (Plus, Minus, Times, Divide, Eq, Lt, Le)):
        left_space = calculate_reserve_space(exp.e1)
        right_space = calculate_reserve_space(exp.e2)
        return max(left_space, 1 + right_space)
    elif isinstance(exp, Dispatch):
        receiver_space = calculate_reserve_space(exp.ro)
        arg_spaces = sum(calculate_reserve_space(arg) for arg in exp.formals)
        return max(receiver_space, arg_spaces) + 1
    elif isinstance(exp, Assign):
        return calculate_reserve_space(exp.rhs) + 1
    elif isinstance(exp, If):
        predicate_space = calculate_reserve_space(exp.predicate)
        if exp.then_body is not None:
            then_space = calculate_reserve_space(exp.then_body)
        if exp.else_body is not None:
            else_space = calculate_reserve_space(exp.else_body)
        return max(predicate_space, then_space, else_space)
    elif isinstance(exp, While):
        predicate_space = calculate_reserve_space(exp.predicate)
        body_space = calculate_reserve_space(exp.body)
        return max(predicate_space, body_space) + 1
    elif isinstance(exp, Block):
        return max(calculate_reserve_space(sub_exp) for sub_exp in exp.exps)
    elif isinstance(exp, New):
        return 1
    elif isinstance(exp, IsVoid):
        return calculate_reserve_space(exp.void_type)
    elif isinstance(exp, (Not, Negate)):
        return calculate_reserve_space(exp.exp) + 1
    elif isinstance(exp, Let):
        bindings_space = 0
        for bind_name, bind_type, init in exp.binds:
            if init is not None:
                bindings_space = max(bindings_space, calculate_reserve_space(init))
        body_space = calculate_reserve_space(exp.body)
        return max(bindings_space, body_space) + len(exp.binds)
    elif isinstance(exp, Case):
        case_space = calculate_reserve_space(exp.case)
        branch_spaces = [calculate_reserve_space(branch_expr) for _, _, branch_expr in exp.exp]
        return max([case_space] + branch_spaces) + 1
    elif isinstance(exp, Internal):
        return 1
    else:
        return 0

def main():
    global output_filename
    global classes
    global class_tags
    global string_constants
    global out_instructions
    global attribute_offset
    global local_offset
    global last_local_offset
    global current_class
    # VTables are created here from each class, creating the method constants by the method label from the implementation map.
    vtable_instructions = []
    for i, cls in enumerate(classes):
        vtable_instructions.append("\t\t\t\t;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\n")
        vtable_instructions.append("%s..vtable:\n" % cls)
        vtable_instructions.append(f"\t\t\t\tconstant {string_constants[i + 1][0]}\n")
        vtable_instructions.append("\t\t\t\tconstant %s..new\n" % cls)
        if cls in implementation_map:
            for method in implementation_map[cls]:
                vtable_instructions.append("\t\t\t\tconstant %s\n" % method.method_label)
    # Here, we create objects for each class that are used throughout for each method class instance.
    constructor_instructions = []
    for cls in classes:
        out_instructions = []
        constructor_instructions.append("\t\t\t\t;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\n")
        constructor_instructions.append("%s..new:\n" % cls)
        constructor_instructions.append(MoveInstruction("fp", "sp"))
        # The temporary stack room space is always 1, so we do not change this.
        tmp_space = 1
        constructor_instructions.append(f"\t\t\t\t;; temporary stack room: {tmp_space}\n")
        constructor_instructions.append(LoadImmediateInstruction(tmp_reg, tmp_space))
        constructor_instructions.append(SubtractInstruction("sp", "sp", tmp_reg))
        constructor_instructions.append(PushInstruction("ra"))
        constructor_instructions.append(LoadImmediateInstruction(self_reg, len(class_map[cls]) + 3))
        constructor_instructions.append(AllocateInstruction(self_reg, self_reg))
        # We store the class tag, object size, and VTable pointer here.
        constructor_instructions.append(f"\t\t\t\t;; store class tag, object size, and vtable pointer\n")
        constructor_instructions.append(LoadImmediateInstruction(tmp_reg, class_tags[cls]))
        constructor_instructions.append(StoreInstruction(self_reg, vtable_offset, tmp_reg))
        constructor_instructions.append(LoadImmediateInstruction(tmp_reg, len(class_map[cls]) + 3))
        constructor_instructions.append(StoreInstruction(self_reg, int_constant_offset, tmp_reg))
        constructor_instructions.append(LoadAddressInstruction(tmp_reg, cls, "..vtable"))
        constructor_instructions.append(StoreInstruction(self_reg, argument_offset, tmp_reg))
        # We initialize our attributes.
        constructor_instructions.append(f"\t\t\t\t;; initialize attributes\n")
        for i, attribute in enumerate(class_map[cls]):
            attribute_offset = i + 3
            constructor_instructions.append(f"\t\t\t\t;; self[{attribute_offset}] holds field\n")
            # We load each attribute that is an unboxed type.
            if attribute.type == "unboxed_int":
                constructor_instructions.append(LoadImmediateInstruction(acc_reg, attribute.init))
                constructor_instructions.append(StoreInstruction(self_reg, attribute_offset, acc_reg))
            elif attribute.type == "unboxed_string":
                constructor_instructions.append(LoadAddressInstruction(acc_reg, attribute.init))
                constructor_instructions.append(StoreInstruction(self_reg, attribute_offset, acc_reg))
            elif attribute.type == "unboxed_bool":
                constructor_instructions.append(LoadImmediateInstruction(acc_reg, 0 if attribute.init == False else 1))
                constructor_instructions.append(StoreInstruction(self_reg, attribute_offset, acc_reg))
            else:
                # If it is not an unboxed type, we check if it is Int, String, or Bool and load from that class.
                if attribute.type in ["Int", "String", "Bool"]:
                    constructor_instructions.append(PushInstruction("fp"))
                    constructor_instructions.append(PushInstruction(self_reg))
                    constructor_instructions.append(LoadAddressInstruction(tmp_reg, attribute.type, "..new"))
                    constructor_instructions.append(CallInstruction(tmp_reg))
                    constructor_instructions.append(PopInstruction(self_reg))
                    constructor_instructions.append(PopInstruction("fp"))
                else:
                    # If it is not one of those 3 classes, we just load 0 into r1.
                    constructor_instructions.append(LoadImmediateInstruction(acc_reg, 0))
                constructor_instructions.append(StoreInstruction(self_reg, attribute_offset, acc_reg))
                # If we have an attribute initializer, we use code generation to add it's initializated body.
                cgen(attribute.init, {})
                if attribute.init is not None:
                    out_instructions.append(StoreInstruction(self_reg, attribute_offset, acc_reg))
        for instruction in out_instructions:
            constructor_instructions.append(instruction)
        # This section is how we end each constructor by resetting everything and returning.
        constructor_instructions.append(MoveInstruction(acc_reg, self_reg))
        constructor_instructions.append(PopInstruction("ra"))
        constructor_instructions.append(LoadImmediateInstruction(tmp_reg, int_constant_offset))
        constructor_instructions.append(AddInstruction("sp", "sp", tmp_reg))
        constructor_instructions.append("\t\t\t\treturn\n")
    # Here, we go through each method to create the method implementations that will be called in COOL assembly.
    method_instructions = []
    for method in ast:
        # We reset most of our global variables here that are used in code generation.
        current_class = method.class_name
        out_instructions = []
        local_offset = []
        last_local_offset = 1
        method_instructions.append("\t\t\t\t;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\n")
        method_instructions.append(f"{method.method_label}:\n")
        method_instructions.append(MoveInstruction("fp", "sp"))
        method_instructions.append(PopInstruction(self_reg))
        # This is where we populate the symbol table from the class map.
        symbol_table = {}
        from_class = class_map[method.class_name]
        # Attributes are r0 with it's offset changing for each one it is.
        for i, attribute in enumerate(from_class):
            symbol_table[attribute.id] = self_reg.off(i + 3)
        # Formals are placed in the frame pointer with an offset of i + 2.
        for i, formal in enumerate(method.formals):
            symbol_table[formal] = FP(i + 2)
        # We add self and SELF_TYPE into the symbol table and implementation map manually for when these are used.
        symbol_table["self"] = self_reg
        implementation_map["self"] = implementation_map[method.class_name]
        symbol_table["SELF_TYPE"] = acc_reg.off(2)
        implementation_map["SELF_TYPE"] = implementation_map[method.class_name]
        # Extra space added to ensure room, but we calculate the reserve space here.
        tmp_space = calculate_reserve_space(method.exp) + 3
        method_instructions.append(f"\t\t\t\t;; Reserved temporary space: {tmp_space}\n")
        method_instructions.append(LoadImmediateInstruction(tmp_reg, tmp_space))
        method_instructions.append(SubtractInstruction("sp", "sp", tmp_reg))
        method_instructions.append(PushInstruction("ra"))
        method_instructions.append("\t\t\t\t;; Method body begins.\n")
        # This will go through and generate the method body.
        cgen(method.exp, symbol_table)
        for instruction in out_instructions:
            method_instructions.append(instruction)
        method_instructions.append("\t\t\t\t;; Method body ends.\n")
        # We end the method here and reset everything.
        method_instructions.append(f"{method.method_label}.end:\n")
        method_instructions.append(PopInstruction("ra"))
        # The length of the formals are added to the temporary space as that needs reset also.
        method_instructions.append(LoadImmediateInstruction(tmp_reg, tmp_space + len(method.formals)))
        method_instructions.append(AddInstruction("sp", "sp", tmp_reg))
        method_instructions.append("\t\t\t\treturn\n")
    string_instructions = []
    for label, content in string_constants:
        string_instructions.append(f"{label}:\t\t\t\tconstant \"{content}\"\n")
    # We finally write the VTables, constructors, methods, and string constants all here at the end to our file.
    with open(output_filename, 'w', encoding='utf-8') as file:
        for vtable in vtable_instructions:
            file.write(str(vtable))
        for constructor in constructor_instructions:
            file.write(str(constructor))
        for method in method_instructions:
            file.write(str(method))
        for string in string_instructions:
            file.write(str(string))
        # Here, the eq_handler, lt_handler, and le_handlers do not change, so they are just implemented here and written at the end.
        file.write("eq_handler:\n")
        file.write(str(MoveInstruction("fp", "sp")))
        file.write(str(PopInstruction(self_reg)))
        file.write(str(PushInstruction("ra")))
        file.write(str(LoadDoublewordInstruction(acc_reg, "fp", self_offset)))
        file.write(str(LoadDoublewordInstruction(tmp_reg, "fp", argument_offset)))
        file.write(str(BranchEqualInstruction(acc_reg, tmp_reg, "eq_true")))
        file.write(str(LoadImmediateInstruction(field_reg, vtable_offset)))
        file.write(str(BranchEqualInstruction(acc_reg, field_reg, "eq_false")))
        file.write(str(BranchEqualInstruction(tmp_reg, field_reg, "eq_false")))
        file.write(str(LoadDoublewordInstruction(acc_reg, acc_reg, vtable_offset)))
        file.write(str(LoadDoublewordInstruction(tmp_reg, tmp_reg, vtable_offset)))
        file.write(str(AddInstruction(acc_reg, acc_reg, tmp_reg)))
        file.write(str(LoadImmediateInstruction(tmp_reg, vtable_offset)))
        file.write(str(BranchEqualInstruction(acc_reg, tmp_reg, "eq_bool")))
        file.write(str(LoadImmediateInstruction(tmp_reg, argument_offset)))
        file.write(str(BranchEqualInstruction(acc_reg, tmp_reg, "eq_int")))
        file.write(str(LoadImmediateInstruction(tmp_reg, 6)))
        file.write(str(BranchEqualInstruction(acc_reg, tmp_reg, "eq_string")))
        file.write(str(LoadDoublewordInstruction(acc_reg, "fp", self_offset)))
        file.write(str(LoadDoublewordInstruction(tmp_reg, "fp", argument_offset)))
        file.write(str(BranchEqualInstruction(acc_reg, tmp_reg, "eq_true")))
        file.write("eq_false:\n")
        file.write(str(PushInstruction("fp")))
        file.write(str(PushInstruction(self_reg)))
        file.write(str(LoadAddressInstruction(tmp_reg, "Bool", "..new")))
        file.write(str(CallInstruction(tmp_reg)))
        file.write(str(PopInstruction(self_reg)))
        file.write(str(PopInstruction("fp")))
        file.write(str(JumpInstruction("eq_end")))
        file.write("eq_true:\n")
        file.write(str(PushInstruction("fp")))
        file.write(str(PushInstruction(self_reg)))
        file.write(str(LoadAddressInstruction(tmp_reg, "Bool", "..new")))
        file.write(str(CallInstruction(tmp_reg)))
        file.write(str(PopInstruction(self_reg)))
        file.write(str(PopInstruction("fp")))
        file.write(str(LoadImmediateInstruction(tmp_reg, 1)))
        file.write(str(StoreInstruction(acc_reg, self_offset, tmp_reg)))
        file.write(str(JumpInstruction("eq_end")))
        file.write("eq_bool:\n")
        file.write("eq_int:\n")
        file.write(str(LoadDoublewordInstruction(acc_reg, "fp", self_offset)))
        file.write(str(LoadDoublewordInstruction(tmp_reg, "fp", argument_offset)))
        file.write(str(LoadDoublewordInstruction(acc_reg, acc_reg, self_offset)))
        file.write(str(LoadDoublewordInstruction(tmp_reg, tmp_reg, self_offset)))
        file.write(str(BranchEqualInstruction(acc_reg, tmp_reg, "eq_true")))
        file.write(str(JumpInstruction("eq_false")))
        file.write("eq_string:\n")
        file.write(str(LoadDoublewordInstruction(acc_reg, "fp", self_offset)))
        file.write(str(LoadDoublewordInstruction(tmp_reg, "fp", argument_offset)))
        file.write(str(LoadDoublewordInstruction(acc_reg, acc_reg, self_offset)))
        file.write(str(LoadDoublewordInstruction(tmp_reg, tmp_reg, self_offset)))
        file.write(str(LoadDoublewordInstruction(acc_reg, acc_reg, vtable_offset)))
        file.write(str(LoadDoublewordInstruction(tmp_reg, tmp_reg, vtable_offset)))
        file.write(str(BranchEqualInstruction(acc_reg, tmp_reg, "eq_true")))
        file.write(str(JumpInstruction("eq_false")))
        file.write("eq_end:\n")
        file.write(str(PopInstruction("ra")))
        file.write(str(LoadImmediateInstruction(tmp_reg, argument_offset)))
        file.write(str(AddInstruction("sp", "sp", tmp_reg)))
        file.write("\t\t\t\treturn\n")
        file.write("le_handler:\n")
        file.write(str(MoveInstruction("fp", "sp")))
        file.write(str(PopInstruction(self_reg)))
        file.write(str(PushInstruction("ra")))
        file.write(str(LoadDoublewordInstruction(acc_reg, "fp", self_offset)))
        file.write(str(LoadDoublewordInstruction(tmp_reg, "fp", argument_offset)))
        file.write(str(BranchEqualInstruction(acc_reg, tmp_reg, "le_true")))
        file.write(str(LoadImmediateInstruction(field_reg, vtable_offset)))
        file.write(str(BranchEqualInstruction(acc_reg, field_reg, "le_false")))
        file.write(str(BranchEqualInstruction(tmp_reg, field_reg, "le_false")))
        file.write(str(LoadDoublewordInstruction(acc_reg, acc_reg, vtable_offset)))
        file.write(str(LoadDoublewordInstruction(tmp_reg, tmp_reg, vtable_offset)))
        file.write(str(AddInstruction(acc_reg, acc_reg, tmp_reg)))
        file.write(str(LoadImmediateInstruction(tmp_reg, vtable_offset)))
        file.write(str(BranchEqualInstruction(acc_reg, tmp_reg, "le_bool")))
        file.write(str(LoadImmediateInstruction(tmp_reg, argument_offset)))
        file.write(str(BranchEqualInstruction(acc_reg, tmp_reg, "le_int")))
        file.write(str(LoadImmediateInstruction(tmp_reg, 6)))
        file.write(str(BranchEqualInstruction(acc_reg, tmp_reg, "le_string")))
        file.write(str(LoadDoublewordInstruction(acc_reg, "fp", self_offset)))
        file.write(str(LoadDoublewordInstruction(tmp_reg, "fp", argument_offset)))
        file.write(str(BranchEqualInstruction(acc_reg, tmp_reg, "le_true")))
        file.write("le_false:\n")
        file.write(str(PushInstruction("fp")))
        file.write(str(PushInstruction(self_reg)))
        file.write(str(LoadAddressInstruction(tmp_reg, "Bool", "..new")))
        file.write(str(CallInstruction(tmp_reg)))
        file.write(str(PopInstruction(self_reg)))
        file.write(str(PopInstruction("fp")))
        file.write(str(JumpInstruction("le_end")))
        file.write("le_true:\n")
        file.write(str(PushInstruction("fp")))
        file.write(str(PushInstruction(self_reg)))
        file.write(str(LoadAddressInstruction(tmp_reg, "Bool", "..new")))
        file.write(str(CallInstruction(tmp_reg)))
        file.write(str(PopInstruction(self_reg)))
        file.write(str(PopInstruction("fp")))
        file.write(str(LoadImmediateInstruction(tmp_reg, 1)))
        file.write(str(StoreInstruction(acc_reg, self_offset, tmp_reg)))
        file.write(str(JumpInstruction("le_end")))
        file.write("le_bool:\n")
        file.write("le_int:\n")
        file.write(str(LoadDoublewordInstruction(acc_reg, "fp", self_offset)))
        file.write(str(LoadDoublewordInstruction(tmp_reg, "fp", argument_offset)))
        file.write(str(LoadDoublewordInstruction(acc_reg, acc_reg, self_offset)))
        file.write(str(LoadDoublewordInstruction(tmp_reg, tmp_reg, self_offset)))
        file.write(str(BranchLessThanEqualToInstruction(acc_reg, tmp_reg, "le_true")))
        file.write(str(JumpInstruction("le_false")))
        file.write("le_string:\n")
        file.write(str(LoadDoublewordInstruction(acc_reg, "fp", self_offset)))
        file.write(str(LoadDoublewordInstruction(tmp_reg, "fp", argument_offset)))
        file.write(str(LoadDoublewordInstruction(acc_reg, acc_reg, self_offset)))
        file.write(str(LoadDoublewordInstruction(tmp_reg, tmp_reg, self_offset)))
        file.write(str(LoadDoublewordInstruction(acc_reg, acc_reg, vtable_offset)))
        file.write(str(LoadDoublewordInstruction(tmp_reg, tmp_reg, vtable_offset)))
        file.write(str(BranchLessThanEqualToInstruction(acc_reg, tmp_reg, "le_true")))
        file.write(str(JumpInstruction("le_false")))
        file.write("le_end:\n")
        file.write(str(PopInstruction("ra")))
        file.write(str(LoadImmediateInstruction(tmp_reg, argument_offset)))
        file.write(str(AddInstruction("sp", "sp", tmp_reg)))
        file.write("\t\t\t\treturn\n")
        file.write("lt_handler:\n")
        file.write(str(MoveInstruction("fp", "sp")))
        file.write(str(PopInstruction(self_reg)))
        file.write(str(PushInstruction("ra")))
        file.write(str(LoadDoublewordInstruction(acc_reg, "fp", self_offset)))
        file.write(str(LoadDoublewordInstruction(tmp_reg, "fp", argument_offset)))
        file.write(str(LoadImmediateInstruction(field_reg, vtable_offset)))
        file.write(str(BranchEqualInstruction(acc_reg, field_reg, "lt_false")))
        file.write(str(BranchEqualInstruction(tmp_reg, field_reg, "lt_false")))
        file.write(str(LoadDoublewordInstruction(acc_reg, acc_reg, vtable_offset)))
        file.write(str(LoadDoublewordInstruction(tmp_reg, tmp_reg, vtable_offset)))
        file.write(str(AddInstruction(acc_reg, acc_reg, tmp_reg)))
        file.write(str(LoadImmediateInstruction(tmp_reg, vtable_offset)))
        file.write(str(BranchEqualInstruction(acc_reg, tmp_reg, "lt_bool")))
        file.write(str(LoadImmediateInstruction(tmp_reg, argument_offset)))
        file.write(str(BranchEqualInstruction(acc_reg, tmp_reg, "lt_int")))
        file.write(str(LoadImmediateInstruction(tmp_reg, 6)))
        file.write(str(BranchEqualInstruction(acc_reg, tmp_reg, "lt_string")))
        file.write("lt_false:\n")
        file.write(str(PushInstruction("fp")))
        file.write(str(PushInstruction(self_reg)))
        file.write(str(LoadAddressInstruction(tmp_reg, "Bool", "..new")))
        file.write(str(CallInstruction(tmp_reg)))
        file.write(str(PopInstruction(self_reg)))
        file.write(str(PopInstruction("fp")))
        file.write(str(JumpInstruction("lt_end")))
        file.write("lt_true:\n")
        file.write(str(PushInstruction("fp")))
        file.write(str(PushInstruction(self_reg)))
        file.write(str(LoadAddressInstruction(tmp_reg, "Bool", "..new")))
        file.write(str(CallInstruction(tmp_reg)))
        file.write(str(PopInstruction(self_reg)))
        file.write(str(PopInstruction("fp")))
        file.write(str(LoadImmediateInstruction(tmp_reg, 1)))
        file.write(str(StoreInstruction(acc_reg, self_offset, tmp_reg)))
        file.write(str(JumpInstruction("lt_end")))
        file.write("lt_bool:\n")
        file.write("lt_int:\n")
        file.write(str(LoadDoublewordInstruction(acc_reg, "fp", self_offset)))
        file.write(str(LoadDoublewordInstruction(tmp_reg, "fp", argument_offset)))
        file.write(str(LoadDoublewordInstruction(acc_reg, acc_reg, self_offset)))
        file.write(str(LoadDoublewordInstruction(tmp_reg, tmp_reg, self_offset)))
        file.write(str(BranchLessThanInstruction(acc_reg, tmp_reg, "lt_true")))
        file.write(str(JumpInstruction("lt_false")))
        file.write("lt_string:\n")
        file.write(str(LoadDoublewordInstruction(acc_reg, "fp", self_offset)))
        file.write(str(LoadDoublewordInstruction(tmp_reg, "fp", argument_offset)))
        file.write(str(LoadDoublewordInstruction(acc_reg, acc_reg, self_offset)))
        file.write(str(LoadDoublewordInstruction(tmp_reg, tmp_reg, self_offset)))
        file.write(str(LoadDoublewordInstruction(acc_reg, acc_reg, vtable_offset)))
        file.write(str(LoadDoublewordInstruction(tmp_reg, tmp_reg, vtable_offset)))
        file.write(str(BranchLessThanInstruction(acc_reg, tmp_reg, "lt_true")))
        file.write(str(JumpInstruction("lt_false")))
        file.write("lt_end:\n")
        file.write(str(PopInstruction("ra")))
        file.write(str(LoadImmediateInstruction(tmp_reg, argument_offset)))
        file.write(str(AddInstruction("sp", "sp", tmp_reg)))
        file.write("\t\t\t\treturn\n")
        # Here is how the program starts in the Main class's method, main.
        file.write("start:\n")
        file.write(str(LoadAddressInstruction(tmp_reg, "Main", "..new")))
        file.write(str(PushInstruction("fp")))
        file.write(str(CallInstruction(tmp_reg)))
        file.write(str(PushInstruction("fp")))
        file.write(str(PushInstruction(acc_reg)))
        file.write(str(LoadAddressInstruction(tmp_reg, "Main", ".main")))
        file.write(str(CallInstruction(tmp_reg)))
        file.write(str(SystemCallInstruction("exit")))

if __name__ == '__main__':
    main()