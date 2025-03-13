# Hunter Mast / hunter.c.mast@vanderbilt.edu
# This is where I recieved most information on the PLY lexer: https://ply.readthedocs.io/en/latest/

import sys
import ply.lex as lex

# Here is a list of all the possible tokens.
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

# Here, we ignore all of the comments.
def t_COMMENT(t):
    r"--.*"
    pass

# Here, we are handling all multi-line comments.
def t_COMMENT_MULTIPLE_LINES(t):
    # We first find an instance of '(*'.
    r"\(\*"
    depth = 1
    while depth > 0:
        # We then go character by character until we either find '*)' and end the search, or find '(*' and continue to now look for two closing comment ends.
        if t.lexer.lexpos < len(t.lexer.lexdata):
            character = t.lexer.lexdata[t.lexer.lexpos]
            t.lexer.lexpos += 1
            if character == '*':
                if t.lexer.lexdata[t.lexer.lexpos] == ')':
                    t.lexer.lexpos += 1
                    depth -= 1
            elif character == '(':
                if t.lexer.lexdata[t.lexer.lexpos] == "*":
                    t.lexer.lexpos += 1
                    depth += 1
            # We make sure to count new lines.
            elif character == '\n':
                t.lexer.lineno += 1
        # Here, we check for errors and that the comments do end and we don't reach the end of file not ending.
        elif t.lexer.lexpos == len(t.lexer.lexdata):
            print(f"ERROR: {t.lexer.lineno}: Lexer: EOF in (* comment *)!")
            t.lexer.error_occurred = True
            break
        else:
            break
    pass

# These are all of the definitions and regular expressions for each token to determine what part of the code coordinates with what token.
# Most of these I have case insensitive, except for true and false are not.
def t_AT(t):
    r"@"
    return t

def t_CASE(t):
    r"\b[cC][aA][sS][eE]\b"
    return t

def t_CLASS(t):
    r"\b[cC][lL][aA][sS][sS]\b"
    return t

def t_COLON(t):
    r":"
    return t

def t_COMMA(t):
    r","
    return t

def t_DIVIDE(t):
    r"/"
    return t

def t_DOT(t):
    r"\."
    return t

def t_ELSE(t):
    r"\b[eE][lL][sS][eE]\b"
    return t

# RARROW and EQUALS were being confused.
def t_RARROW(t):
    r"=>"
    return t

def t_EQUALS(t):
    r"="
    return t

def t_ESAC(t):
    r"\b[eE][sS][aA][cC]\b"
    return t

def t_FALSE(t):
    r"\bf[aA][lL][sS][eE]\b"
    return t

def t_FI(t):
    r"\b[fF][iI]\b"
    return t

def t_IF(t):
    r"\b[iI][fF]\b"
    return t

# INHERITS and IN had to be switched as the lexer kept recognizing the beginning of inherits as just in.
def t_INHERITS(t):
    r"\b[iI][nN][hH][eE][rR][iI][tT][sS]\b"
    return t

# Something else I did was add \b to in, which in regular expression make sure that there is a boundary around in and that it is alone.
# This solved a lot of issues I had for variable names like "class_type" just being seen as class, so I added it to every token that is just a word.
def t_IN(t):
    r"\b[iI][nN]\b"
    return t

def t_ISVOID(t):
    r"\b[iI][sS][vV][oO][iI][dD]\b"
    return t

def t_LARROW(t):
    r"<-"
    return t

def t_LBRACE(t):
    r"{"
    return t

# Same as INHERITS AND IN happen here for LET and LE
def t_LET(t):
    r"\b[lL][eE][tT]\b"
    return t

def t_LE(t):
    r"<="
    return t

def t_LOOP(t):
    r"\b[lL][oO][oO][pP]\b"
    return t

def t_LPAREN(t):
    r"\("
    return t

def t_LT(t):
    r"<"
    return t

def t_MINUS(t):
    r"-"
    return t

def t_NEW(t):
    r"\b[nN][eE][wW]\b"
    return t

def t_NOT(t):
    r"\b[nN][oO][tT]\b"
    return t

def t_OF(t):
    r"\b[oO][fF]\b"
    return t

def t_PLUS(t):
    r"\+"
    return t

def t_POOL(t):
    r"\b[pP][oO][oO][lL]\b"
    return t

def t_RBRACE(t):
    r"}"
    return t

def t_RPAREN(t):
    r"\)"
    return t

def t_SEMI(t):
    r";"
    return t

def t_THEN(t):
    r"\b[tT][hH][eE][nN]\b"
    return t

def t_TILDE(t):
    r"~"
    return t

def t_TIMES(t):
    r"\*"
    return t

def t_TRUE(t):
    r"\bt[rR][uU][eE]\b"
    return t

def t_WHILE(t):
    r"\b[wW][hH][iI][lL][eE]\b"
    return t

# This here tells the lexer to ignore all whitespaces and tabs.
t_ignore = " \t\v"

# This evaluates string tokens between quotations and will cutoff the quotations for reporting.
# We also reset t.lexer.type_check.
def t_STRING(t):
    # This regular expression finds anything betweel two quotation marks both between lines.
    # This one is the hardest has it must keep anything within those two quotation marks.
    # *? is used to make sure we get the whole string and ignore if we have two strings next to each other to not get everything between that.
    r'"([^\\\n\x00]|(\\.))*?"'
    # This should make sure each string ends with a quotation, but our original regular expression already checks for that, so this is just a second check.
    if t.value[-1] != '"':
        print(f"ERROR: {t.lineno}: Lexer: EOF in string!")
        t.lexer.error_occurred = True
        t.lexer.input("")
    t.value = t.value[1:-1]
    # Here, we make sure that null cannot be inside of a string by checking for x00.
    if '\x00' in t.value:
        print(f"ERROR: {t.lineno}: Lexer: Null found in string!")
        t.lexer.error_occurred = True
        t.lexer.input("")
    # This we make sure that the string is not too long and looks at max string character length.
    if len(t.value) > 1024:
        print(f"ERROR: {t.lineno}: Lexer: String too long!")
        t.lexer.error_occurred = True
        t.lexer.input("")
    return t

# This evaluates integers as tokens and will convert the text value to the actual integer.
# We also reset t.lexer.type_check.
def t_INTEGER(t):
    # This just checks if 1 or more digits exist by themself.
    r"\d+"
    t.value = int(t.value)
    # Here, we make sure that each integer is within range of the 32 bit-limit.
    if t.value > 2147483647:
        print(f"ERROR: {t.lineno}: Lexer: Integer out of range of bit-limit!")
        t.lexer.error_occurred = True
        t.lexer.input("")
    return t

# This checks if the token is a type or not. Types are capitalized, identifiers are not.
def t_TYPE(t):
    # The first part here matches the first character which must be any sort of letter.
    # The second part matches the rest of the string which can be any letter, number, or underscore.
    r"[A-Z][a-zA-Z_0-9]*"
    # We have to make sure that that if we have objectid, it is not valid in COOL.
    if t.value == "objectid":
        print(f"ERROR: {t.lineno}: Lexer: Object ID is invalid!")
        t.lexer.error_occurred = True
        t.lexer.input("")
    # This makes sure underscore does not exist by itself.
    if t.value == "_":
        print(f"ERROR: {t.lineno}: Lexer: Underscore cannot be alone!")
        t.lexer.error_occurred = True
        t.lexer.input("")
    return t

# This figures out if a token is an identifier or if not.
def t_IDENTIFIER(t):
    # The first part here matches the first character which must be any sort of letter.
    # The second part matches the rest of the string which can be any letter, number, or underscore.
    r"[a-z][a-zA-Z_0-9]*"
    # We have to make sure that that if we have objectid, it is not valid in COOL.
    if t.value == "objectid":
        print(f"ERROR: {t.lineno}: Lexer: Object ID is invalid!")
        t.lexer.error_occurred = True
        t.lexer.input("")
    # This makes sure underscore does not exist by itself.
    if t.value == "_":
        print(f"ERROR: {t.lineno}: Lexer: Underscore cannot be alone!")
        t.lexer.error_occurred = True
        t.lexer.input("")
    return t

# This checks if hexidecimal and octal numbers exist and if so, seperate them into different sections.
def t_HEX_OCTAL(t):
    r'0[xXoO][a-zA-Z0-9_]+'
    if t.value.startswith('0x') or t.value.startswith('0X'):
        t.type = "INTEGER"
        t.value = 0
        t.lexer.lexpos -= len(t.value) - 1
        return t
    elif t.value.startswith('0o') or t.value.startswith('0O'):
        t.type = "INTEGER"
        t.value = 0
        t.lexer.lexpos -= len(t.value) - 1
        return t
    else:
        print(f"ERROR: {t.lineno}: Lexer: invalid character: {t.value[0]}")
        t.lexer.error_occurred = True
        t.lexer.input("")

# This handles switching between new lines and ignoring empty lines.
# We also update the line number by however many we skip.
# We also reset t.lexer.type_check.
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)

# We sent error reports if a character does not coordinate with any part of our lexer.
# t.lexer.error_occurred is sent to evaluate that an error has occured and to stop the program.
# We also reset t.lexer.type_check.
def t_error(t):
    print(f"ERROR: {t.lineno}: Lexer: invalid character: {t.value[0]}")
    t.lexer.error_occurred = True
    t.lexer.input("")

# This will initialize our lexer using PLY.
lexer = lex.lex()
# We get the name of the file from command line using this.
filename = sys.argv[1]
# lexer.type_check is used to evaluate whether or not a token is a type or an identifier.
lexer.type_check = False
# lexer.error_occurred is used to evaluate whether or not an error has been reported.
lexer.error_occurred = False

# Here, we open the file and read it.
# If we cannot read it and get any data, then we sent and error and end the program.
try:
    with open(filename, "r") as file:
        data = file.read()
except FileNotFoundError:
    print(f"ERROR: The file, {filename}, was not found!")
    lexer.error_occurred = True

# Here we just read the data using our lexer from PLY.
lexer.input(data)
# This will create a filename from the original file, but a version that is lexed.
lexed_filename = f"{filename}-lex"
# This keeps a list of all the tokens after being lexed to then write onto our lex document.
token_list = []

# This here goes through and sorts our tokens.
# If the token has a type, we also append that type to our token list and print that.
while True:
    if lexer.error_occurred:
        break
    tok = lexer.token()
    if tok:
        token_list.append((tok.lineno, tok.type.lower(), tok.value if tok.type in ["IDENTIFIER", "TYPE", "INTEGER", "STRING"] else None))
    else:
        break

# This writes onto the document if no error is found.
if not lexer.error_occurred:
    with open(lexed_filename, "w") as lexed_file:
        for line_number, token_type, token_value in token_list:
            lexed_file.write(f"{line_number}\n")
            lexed_file.write(f"{token_type}\n")
            if token_value != None:
                lexed_file.write(f"{token_value}\n")