# Hunter Mast / hunter.c.mast@vanderbilt.edu
import sys
import re

# Here are all of our tokens in RegEx for our TAC expressions.
TAC_TOKENS = {
    'Label': r'^label\s+(\S+)$',
    'Return': r'^return\s+(\S+)$',
    'Jump': r'^jmp\s+(\S+)$',
    'Branch': r'^bt\s+(\S+)\s*(\S+)$',
    'Int': r'^\s*(\S+)\s+<-\s+int\s+(\d+)\s*$',
    'String': r'^(\S+)\s+<-\s+string\s*$',
    'Bool': r'^(\S+)\s+<-\s+bool\s+(true|false)$',
    'Assign': r'^(\S+)\s+<-\s+(\S+)$',
    'BinaryOperators': r'^(\S+)\s+<-\s+(<=|[+\-*\/<=])\s+(\S+)\s+(\S+)$',
    'UnaryOperators': r'^(\S+)\s+<-\s+(not|~|isvoid)\s+(\S+)$',
    'New': r'^(\S+)\s+<-\s+new\s+(\S+)$',
    'Default': r'^(\S+)\s+<-\s+default\s+(\S+)$',
    'Call': r'^(\S+)\s+<-\s+call\s+(\S+)(.*)$',
}

# We go through and parse all of the file given for TAC code and separate it.
def parse_instructions(three_address_code):
    instructions = []
    lines = three_address_code.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # We ignore comments (Can easily be removed if comments are wanted).
        if line.startswith('comment'):
            i += 1
            continue
        # If we run into a string, we make sure that the next line (The actual string) is kept.
        match = re.match(r'^(\S+)\s+<-\s+string\s*$', line)
        if match:
            string_location = match.group(1)
            i += 1
            string_content = lines[i].strip()
            instructions.append(('String', string_location, string_content))
        else:
            for pattern, regex in TAC_TOKENS.items():
                match = re.match(regex, line)
                if match:
                    match_group = match.groups()
                    instructions.append((pattern, *match_group))
                    break
        i += 1
    return instructions

# Here is where we perform liveness analysis and determine which variables and expressions are live and which are dead.
def liveness_analysis(instructions):
    # Here, we get all of the successors to each instruction and set it to an index.
    successors = [[] for _ in instructions]
    label_check = {instruction[1]: index for index, instruction in enumerate(instructions) if instruction[0] == 'Label'}
    for index, instruction in enumerate(instructions):
        pattern = instruction[0]
        if pattern == 'Branch':
            successors[index] = [label_check[instruction[2]]]
        elif pattern == 'Jump':
            successors[index] = [label_check[instruction[1]]]
        elif index + 1 < len(instructions):
            successors[index] = [index + 1]
    # We get all defined and used variables for liveness analysis.
    application = []
    for instruction in instructions:
        pattern = instruction[0]
        if pattern == 'Assign':
            defined = instruction[1]
            used = [instruction[2]]
        elif pattern in ['Int', 'Bool', 'String']:
            defined = instruction[1]
            used = []
        elif pattern == 'BinaryOperators':
            defined = instruction[1]
            used = [instruction[3], instruction[4]]
        elif pattern == 'UnaryOperators':
            defined = instruction[1]
            used = [instruction[3]]
        elif pattern == 'Call':
            defined = instruction[1]
            used = [instruction[3].strip() if len(instruction) > 3 else []]
        elif pattern == 'Branch':
            defined = None
            used = [instruction[1]]
        elif pattern == 'Jump':
            defined = None
            used = []
        elif pattern == 'Return':
            defined = None
            used = [instruction[1]]
        else:
            defined = None
            used = []
        application.append((defined, used))
    # We go through each instruction and perform liveness analysis (live_in = live_out - defined + used).
    live_in = [set() for _ in instructions]
    live_out = [set() for _ in instructions]
    while True:
        changes = False
        for index in reversed(range(len(instructions))):
            live_in_check = live_in[index].copy()
            live_out_check = live_out[index].copy()
            live_out[index] = set().union(*(live_in[succeed] for succeed in successors[index]))
            defined, used = application[index]
            live_in[index] = (live_out[index] - ({defined} if defined else set())) | set(used)
            if live_in[index] != live_in_check or live_out[index] != live_out_check:
                changes = True
        if not changes:
            break
    return live_out

# We use 'live_out' to remove all of the dead code from our TAC code that is not used or defined.
def dead_code_elimination(instructions, live_out):
    optimized_code = []
    side_effect_check = set()
    for index, instruction in enumerate(instructions):
        if instruction[0] == 'Call':
            defined = instruction[1]
            side_effect_check.add(defined)
            if len(instruction) > 3:
                side_effect_check.update(instruction[3])
    for index, instruction in enumerate(instructions):
        pattern = instruction[0]
        defined = None
        if pattern == 'Assign':
            defined = instruction[1]
        elif pattern in ['Int', 'Bool', 'String']:
            defined = instruction[1]
        elif pattern == 'BinaryOperators':
            defined = instruction[1]
        elif pattern == 'UnaryOperators':
            defined = instruction[1]
        if defined in live_out[index] or defined in side_effect_check or pattern in ['Label', 'Branch', 'Jump', 'Call', 'Return']:
            optimized_code.append(instruction)
    return optimized_code

# After analysis and removing dead code, we rebuild our entire TAC file using which instructions are still live.
def format_instructions(instructions):
    formatted_instruction = []
    for instruction in instructions:
        pattern = instruction[0]
        if pattern == 'Label':
            formatted_instruction.append(f'label {instruction[1]}')
        elif pattern == 'Return':
            formatted_instruction.append(f'return {instruction[1]}')
        elif pattern == 'Jump':
            formatted_instruction.append(f'jmp {instruction[1]}')
        elif pattern == 'Branch':
            formatted_instruction.append(f'bt {instruction[1]} {instruction[2]}')
        elif pattern in ['Int', 'Bool']:
            formatted_instruction.append(f'{instruction[1]} <- {pattern.lower()} {instruction[2]}')
        elif pattern == 'String':
            formatted_instruction.append(f'{instruction[1]} <- string')
            formatted_instruction.append(instruction[2])
        elif pattern == 'Assign':
            formatted_instruction.append(f'{instruction[1]} <- {instruction[2]}')
        elif pattern == 'BinaryOperators':
            formatted_instruction.append(f'{instruction[1]} <- {instruction[2]} {instruction[3]} {instruction[4]}')
        elif pattern == 'UnaryOperators':
            formatted_instruction.append(f'{instruction[1]} <- {instruction[2]} {instruction[3]}')
        elif pattern == 'New':
            formatted_instruction.append(f'{instruction[1]} <- new {instruction[2]}')
        elif pattern == 'Default':
            formatted_instruction.append(f'{instruction[1]} <- default {instruction[2]}')
        elif pattern == 'Call':
            if len(instruction[3]) > 3 :
                formatted_instruction.append(f'{instruction[1]} <- call {instruction[2]} {instruction[3].strip()}')
            else:
                formatted_instruction.append(f'{instruction[1]} <- call {instruction[2]}')
    return '\n'.join(formatted_instruction)

# This is where we call all of our functions, receive input, and output to a file.
def main(input_file):
    with open(input_file, 'r') as file:
        three_address_code = file.read()
    instructions = parse_instructions(three_address_code)
    # We go through until we have done all we can with eliminating dead code.
    previous_instructions = []
    while instructions != previous_instructions:
        previous_instructions = instructions.copy()
        live_out = liveness_analysis(instructions)
        instructions = dead_code_elimination(instructions, live_out)
    optimized_code = format_instructions(instructions)
    sys.stdout.write(optimized_code)

if __name__ == '__main__':
    main(sys.argv[1])