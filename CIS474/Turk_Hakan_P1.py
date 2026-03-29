# Author: Hakan Turk, Course: CIS 474, Project: Lexical Analyser

from sly import Lexer

class lexicalAnalyzer(Lexer):
    # token names 
    tokens = {
        ID, DOUBLE_CONST, INT_CONST, STRING_CONST,

        # keywords
        NOTHING, INT, DOUBLE, BOOL, STRING, CLASS, INTERFACE, NULL, THIS,
        EXTENDS, IMPLEMENTS, FOR, WHILE, IF, ELSE, RETURN, BREAK, NEW,
        ARRAYINSTANCE, OUTPUT, INPUTINT, INPUTLINE,

        # boolean constants
        TRUE, FALSE,

        # operators & punctuation 
        PLUS, MINUS, TIMES, DIVIDE, MOD,
        LT, LTE, GT, GTE,
        ASSIGN, EQ, NE, NOT,
        AND, OR,
        SEMI, COMMA, DOT,
        LBRACK, RBRACK, LPAREN, RPAREN, LBRACE, RBRACE
    }

    # single-line comment
    ignore_single_comment = r'//.*'

    # single-line block comment // does not work for multi-line, but requirements do not say it has to...
    ignore_block_comment = r'/\*(.|\n)*?\*/'

    # double constrant
    @_(r'\d+\.\d*([eE][+-]?\d+)?')
    def DOUBLE_CONST(self, t):
        if 'e' in t.value:
            print(f"[LEXICAL ERROR] lowercase 'e' not allowed in double constant: {t.value}")
            return None
        return t

    # integer constant
    INT_CONST = r'\d+'

    STRING_CONST = r'"[^"\n]*"'

    # comparison 
    LTE     = r'<='
    GTE     = r'>='
    EQ      = r'=='
    NE      = r'!='
    LT      = r'<'
    GT      = r'>'
    ASSIGN  = r'='
    NOT     = r'!'
    
    # logical operators
    AND = r'&&'
    OR  = r'\|\|'

    # arithmetics operators
    PLUS   = r'\+'
    MINUS  = r'-'
    TIMES  = r'\*'
    DIVIDE = r'/'
    MOD    = r'%'

    # punctuation
    SEMI   = r';'
    COMMA  = r','
    DOT    = r'\.'
    LBRACK = r'\['
    RBRACK = r'\]'
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACE = r'\{'
    RBRACE = r'\}'

    # identifiers
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # keyword mapping
    ID['nothing'] = NOTHING
    ID['int'] = INT
    ID['double'] = DOUBLE
    ID['bool'] = BOOL
    ID['string'] = STRING
    ID['class'] = CLASS
    ID['interface'] = INTERFACE
    ID['null'] = NULL
    ID['this'] = THIS
    ID['extends'] = EXTENDS
    ID['implements'] = IMPLEMENTS
    ID['for'] = FOR
    ID['while'] = WHILE
    ID['if'] = IF
    ID['else'] = ELSE
    ID['return'] = RETURN
    ID['break'] = BREAK
    ID['new'] = NEW
    ID['ArrayInstance'] = ARRAYINSTANCE
    ID['Output'] = OUTPUT
    ID['InputInt'] = INPUTINT
    ID['InputLine'] = INPUTLINE

    # boolean constants
    ID['True'] = TRUE
    ID['False'] = FALSE

    # ignored characters (spaces and tabs)
    ignore = ' \t\r'
    # track line numbers
    ignore_newline = r'\n+'

    def ignore_newline(self, t):
        self.lineno += len(t.value)

    # graceful error handling
    def error(self, t):
        column = self.index
        print(f"[LEXICAL ERROR] line {self.lineno}, column {column}: "
            f"illegal character '{t.value[0]}'")
        self.index += 1


def main():
    lexer = lexicalAnalyzer()
    print("Lexical Analyzer (type 'exit' to quit)")

    while True:
        text = input(">>> ")
        if text.lower() == "exit":
            break

        for token in lexer.tokenize(text):
            # enforce max 50 characters for identifiers here
            if token.type == 'ID' and len(token.value) > 50:
                print(f"[LEXICAL ERROR] identifier exceeds 50 characters: {token.value}")
                token.value = token.value[:50]  # optional truncation
            print(token)


if __name__ == "__main__":
    main()
