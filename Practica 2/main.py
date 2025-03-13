import ply.lex as lex
import ply.yacc as yacc

# Lista de tokens
tokens = (
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'ASSIGN', 'ID', 'SEMI'
)

# Reglas de los tokens (expresiones regulares)
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_ASSIGN  = r'='
t_SEMI    = r';'

# Regla para identificadores: deben comenzar con letra, seguidos de letras, dígitos o '_'
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    return t

# Regla para números: uno o más dígitos
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignorar espacios en blanco y tabulaciones
t_ignore = ' \t'

# Regla para manejar errores léxicos
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Construir el analizador léxico
lexer = lex.lex()

# ---------------------------------------------------
# Definición de la gramática:
#
# program     -> assignment | assignment program
# assignment  -> ID ASSIGN expression SEMI
# expression  -> expression PLUS term
#             | expression MINUS term
#             | term
# term        -> term TIMES factor
#             | term DIVIDE factor
#             | factor
# factor      -> NUMBER | ID | LPAREN expression RPAREN
# ---------------------------------------------------

# Regla: Un programa puede consistir en una única asignación.
def p_program_single(p):
    'program : assignment'
    p[0] = [p[1]]

# Regla: Un programa es una asignación seguida de otro programa.
def p_program_multiple(p):
    'program : assignment program'
    p[0] = [p[1]] + p[2]

# Regla para asignación: ID = expression ;
def p_assignment(p):
    'assignment : ID ASSIGN expression SEMI'
    # Se crea un nodo de asignación representado como ('assign', identificador, expresión)
    p[0] = ('assign', p[1], p[3])

# Regla para expresiones (operadores + y -)
def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = ('+', p[1], p[3])

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = ('-', p[1], p[3])

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

# Regla para términos (operadores * y /)
def p_term_times(p):
    'term : term TIMES factor'
    p[0] = ('*', p[1], p[3])

def p_term_divide(p):
    'term : term DIVIDE factor'
    p[0] = ('/', p[1], p[3])

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

# Regla para factores
def p_factor_number(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_id(p):
    'factor : ID'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

# Regla para errores de sintaxis
def p_error(p):
    if p:
        print("Error de sintaxis en token:", p.type, "valor:", p.value)
    else:
        print("Error de sintaxis: Entrada incompleta")

# Construir el analizador sintáctico
parser = yacc.yacc()

# Función para analizar una cadena y mostrar el árbol sintáctico
def analyze_code(code):
    result = parser.parse(code)
    print("Árbol sintáctico:", result)

# Ejemplo de uso interactivo
if __name__ == '__main__':
    while True:
        code = input("Ingrese una cadena a validar: ")
        analyze_code(code)
        continuar = input("¿Desea validar otra cadena? (1.- Si / 2.- No): ")
        if continuar == '2':
            break
