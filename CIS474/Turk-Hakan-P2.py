import sys
from Turk_Hakan_P1 import lexicalAnalyzer #import from last project 
from sly import Parser

"""
this parser reads a dlang source program (test-parser.ddlang) and analyzes its syntax according 
to the dlang grammar. it is integrated with a lexical analyzer (from project 1) to tokenize the input, 
then applythe parsing rules. this parser recognizes constructs such as variable declarations, 
function declarations, statement blocks, and various statements. it handles expressions with proper 
operator precedence. as parsing progresses, the parser prints messages indicating each recognized construct. 
in case of syntax errors, it prints clear messages identifying the current construct and the  token, which helps
the user locate and correct errors. the parser also outputs the parsing process and 
any shift/reduce conflicts directly to the terminal for verification and analysis.
"""

class DLangParser(Parser):
    tokens = lexicalAnalyzer.tokens  # import tokens from lexer so parser knows terminal symbols

    # operator precedence table
    # helps resolve shift/reduce conflicts for expressions
    precedence = (
        ('right', 'ASSIGN'),  # assignment binds right to left
        ('left', 'OR'), # logical or
        ('left', 'AND'), # logical and
        ('left', 'EQ', 'NE'), # equality operators
        ('left', 'LT', 'LTE', 'GT', 'GTE'), # relational operators
        ('left', 'PLUS', 'MINUS'), # addition/subtraction
        ('left', 'TIMES', 'DIVIDE', 'MOD'), # multiplication/division/mod
        ('right', 'NOT', 'UMINUS'), # unary operators 
    )

    def __init__(self):
        self.current_construct = '' # tracks the current construct for error reporting



    # Program Rules 

    @_('decls')
    def program(self, p): # program is one or more declarations
        return p.decls

    @_('decl decls')
    def decls(self, p): # prepend first declaration to remaining list
        return [p.decl] + p.decls

    @_('decl')
    def decls(self, p): # base case: single declaration
        return [p.decl]

    @_('variable_decl', 'function_decl')
    def decl(self, p): # a declaration is either a variable or function declaration
        return p[0]



    # Variable Declaration Rules

    @_('variable SEMI')
    def variable_decl(self, p): # variable declaration followed by semicolon
        self.current_construct = 'VariableDecl'
        print("Found VariableDecl") # report progress
        return p.variable

    @_('type ID')
    def variable(self, p): # a variable consists of a type and identifier
        return (p.type, p.ID)

    @_('INT', 'DOUBLE', 'BOOL', 'STRING') # valid types for dlang variables
    def type(self, p):
        return p[0]



    # Function Declaration Rules

    @_('type ID LPAREN formals RPAREN stmt_block',
       'NOTHING ID LPAREN formals RPAREN stmt_block')
    def function_decl(self, p): # function declaration: type, identifier, formals, and body block
        self.current_construct = 'FunctionDecl'
        print("Found FunctionDecl") # report progress
        return (p[0], p.ID, p.formals, p.stmt_block)

    @_('variables', '')
    def formals(self, p): # function formal parameters may be empty
        if len(p) == 0:
            return []
        return p.variables

    @_('variable COMMA variables') # multiple variables in formals separated by commas
    def variables(self, p):
        return [p.variable] + p.variables

    @_('variable') # single variable as base case
    def variables(self, p):
        return [p.variable]



    # Statement Block Rules

    @_('LBRACE variable_decl_star stmt_star RBRACE')
    def stmt_block(self, p): # a block: zero or more variable declarations + zero or more statements
        self.current_construct = 'StmtBlock'
        print("Found StmtBlock")
        return ('Block', p.variable_decl_star, p.stmt_star)

    @_('variable_decl variable_decl_star', '')
    def variable_decl_star(self, p): # zero or more variable declarations
        if len(p) == 0:
            return []
        return [p.variable_decl] + p.variable_decl_star

    @_('stmt stmt_star', '')
    def stmt_star(self, p): # zero or more statements in a block
        if len(p) == 0:
            return []
        return [p.stmt] + p.stmt_star



    # Statement Rules 

    @_('expr SEMI')
    def stmt(self, p): # expression statement followed by semicolon
        if isinstance(p.expr, tuple):
            if p.expr[0] == 'Assign':
                print("Found Assignment")
            elif p.expr[0] == 'Call':
                print("Found FunctionCall")
            else:
                print("Found ExprStmt")
        else:
            print("Found ExprStmt")
        return p.expr

    @_('SEMI')
    def stmt(self, p): # empty statement: just a semicolon
        print("Found EmptyStmt")
        return None

    @_('if_stmt',
       'while_stmt',
       'for_stmt',
       'break_stmt',
       'return_stmt',
       'output_stmt',
       'stmt_block')
    def stmt(self, p):
        return p[0]

    # if statement
    @_('IF LPAREN expr RPAREN stmt ELSE stmt')
    def if_stmt(self, p):
        print("Found IfStmt")
        return ('If', p.expr, p.stmt0, p.stmt1)

    # while statement
    @_('WHILE LPAREN expr RPAREN stmt')
    def while_stmt(self, p):
        print("Found WhileStmt")
        return ('While', p.expr, p.stmt)

    # for statement
    @_('FOR LPAREN expr SEMI expr SEMI expr RPAREN stmt')
    def for_stmt(self, p):
        print("Found ForStmt")
        return ('For', p.expr0, p.expr1, p.expr2, p.stmt)

    # break statement
    @_('BREAK SEMI')
    def break_stmt(self, p):
        print("Found BreakStmt")
        return 'break'

    # return statement
    @_('RETURN expr SEMI')
    def return_stmt(self, p):
        print("Found ReturnStmt")
        return ('Return', p.expr)

    # output statement  
    @_('OUTPUT LPAREN expr_list RPAREN SEMI')
    def output_stmt(self, p):
        print("Found OutputStmt")
        return ('Output', p.expr_list)

    @_('expr COMMA expr_list') # comma-separated expressions
    def expr_list(self, p):
        return [p.expr] + p.expr_list

    @_('expr') # single expression
    def expr_list(self, p):
        return [p.expr]



    # Expression Rules

    @_('ID ASSIGN expr') 
    def expr(self, p): # assignment expression: variable = value
        return ('Assign', p.ID, p.expr)

    @_('expr PLUS expr',
       'expr MINUS expr',
       'expr TIMES expr',
       'expr DIVIDE expr',
       'expr MOD expr',
       'expr LT expr',
       'expr LTE expr',
       'expr GT expr',
       'expr GTE expr',
       'expr EQ expr',
       'expr NE expr',
       'expr AND expr',
       'expr OR expr')
    def expr(self, p): # binary operations
        return ('BinOp', p[1], p.expr0, p.expr1)

    @_('MINUS expr %prec UMINUS',
       'NOT expr')
    def expr(self, p): # unary operations
        return ('UnaryOp', p[0], p.expr)

    @_('LPAREN expr RPAREN')
    def expr(self, p): # parenthesized expression
        return p.expr

    @_('ID LPAREN actuals RPAREN')
    def expr(self, p): # function call: identifier + arguments
        print("Found FunctionCall")
        return ('Call', p.ID, p.actuals)

    @_('INPUTINT LPAREN RPAREN',
       'INPUTLINE LPAREN RPAREN')
    def expr(self, p): # input expressions: read int or line
        return (p[0],)

    @_('ID', 'constant')
    def expr(self, p): # simple identifiers or constants
        return p[0]

    @_('INT_CONST', 'DOUBLE_CONST', 'STRING_CONST', 'TRUE', 'FALSE', 'NULL')
    def constant(self, p): # literal constants for expressions
        return ('Const', p[0])
    


    # Function Call Actuals

    @_('expr COMMA actuals')
    def actuals(self, p): # multiple function arguments separated by commas
        return [p.expr] + p.actuals

    @_('expr')
    def actuals(self, p): # single argument 
        return [p.expr]

    @_('')
    def actuals(self, p): # no arguments case (empty list)
        return []



    # Error Handling

    def error(self, token):
        # print syntax error messages with current construct context
        construct = self.current_construct or "UnknownConstruct"
        if token: # token exists: show token type and value
            print(f"Found syntax error at {construct} (token: {token.type} '{token.value}')")
        else: # end of input
            print("Found syntax error at end of input")



# Main Program

def main():
    if len(sys.argv) != 2: # ensure exactly one command-line argument
        print("python3 Turk-Hakan-P2.py <source_file>")
        return

    source_file = sys.argv[1] 
    try: # open and read source file
        with open(source_file, 'r') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"File not found: {source_file}")
        return

    # create lexer and parser instances
    lexer = lexicalAnalyzer()
    parser = DLangParser()

    # parse input tokens
    parser.parse(lexer.tokenize(data))
    print("Parsing completed successfully!")

    # enable sly parser debug output to show conflicts and parsing steps
    parser.debugfile = None  # print debug info to terminal
    parser.debug = True      # turn on parser debug

if __name__ == '__main__':
    main()
