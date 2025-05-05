import ply.lex as lex
import ply.yacc as yacc

# --------------------------------------------------
# PALABRAS RESERVADAS 
# --------------------------------------------------
reserved = {
    'bool': 'BOOL',
    'while': 'WHILE',
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'return': 'RETURN',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'string': 'STRING',
    'void': 'VOID',
    'main': 'MAIN',
    'true': 'TRUE',
    'false': 'FALSE',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
    'switch': 'SWITCH',
    'case': 'CASE',
    'default': 'DEFAULT',
    'do': 'DO',
    'double': 'DOUBLE',
    'long': 'LONG',
    'short': 'SHORT',
    'unsigned': 'UNSIGNED',
    'signed': 'SIGNED',
    'static': 'STATIC',
    'const': 'CONST',
    'enum': 'ENUM',
    'struct': 'STRUCT',
    'union': 'UNION',
    'typedef': 'TYPEDEF',
    'goto': 'GOTO',
    'register': 'REGISTER',
    'volatile': 'VOLATILE',
    'inline': 'INLINE',
    'auto': 'AUTO',
    'extern': 'EXTERN',
    'sizeof': 'SIZEOF',
    'namespace': 'NAMESPACE',
    'using': 'USING',
    'template': 'TEMPLATE',
    'friend': 'FRIEND',
    'operator': 'OPERATOR',
    'new': 'NEW',
    'delete': 'DELETE',
    'class': 'CLASS',
    'public': 'PUBLIC'
}

# --------------------------------------------------
# LISTA DE TOKENS
# --------------------------------------------------
tokens = (
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'ASSIGN', 'ID', 'SEMI'
) + tuple(reserved.values())

# --------------------------------------------------
# EXPRESIONES REGULARES PARA LOS TOKENS
# --------------------------------------------------
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_ASSIGN  = r'='
t_SEMI    = r';'

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    # Verifica si es palabra reservada
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# --------------------------------------------------
# GRAMÁTICA
# --------------------------------------------------
# La estructura del programa es:
#   program -> decl_list stmt_list (v1)
#
def p_program(p):
    'program : decl_list stmt_list'
    p[0] = ('program', p[1], p[2])

def p_decl_list_multiple(p):
    'decl_list : decl_list declaration'
    p[0] = p[1] + [p[2]]

def p_decl_list_empty(p):
    'decl_list : '
    p[0] = []

def p_declaration(p):
    'declaration : type_specifier ID SEMI'
    p[0] = ('declare', p[1], p[2])

def p_type_specifier(p):
    '''type_specifier : INT
                      | FLOAT
                      | BOOL
                      | CHAR
                      | STRING'''
    p[0] = p[1]

def p_stmt_list_multiple(p):
    'stmt_list : stmt_list statement'
    p[0] = p[1] + [p[2]]

def p_stmt_list_single(p):
    'stmt_list : statement'
    p[0] = [p[1]]

def p_statement_assignment(p):
    'statement : assignment'
    p[0] = p[1]

def p_statement_expr(p):
    'statement : expression SEMI'
    p[0] = p[1]

def p_statement_if(p):
    '''statement : IF LPAREN expression RPAREN statement ELSE statement
                 | IF LPAREN expression RPAREN statement'''
    if len(p) == 8:
        p[0] = ('if', p[3], p[5], p[7])
    else:
        p[0] = ('if', p[3], p[5])

def p_statement_while(p):
    'statement : WHILE LPAREN expression RPAREN statement'
    p[0] = ('while', p[3], p[5])

def p_statement_compound(p):
    'statement : LBRACE stmt_list RBRACE'
    p[0] = ('block', p[2])

def p_assignment(p):
    'assignment : ID ASSIGN expression SEMI'
    p[0] = ('assign', p[1], p[3])

# Expresiones aritméticas: suma, resta (v1)
def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = ('+', p[1], p[3])

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = ('-', p[1], p[3])

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

# Términos: multiplicación, división (v1)
def p_term_times(p):
    'term : term TIMES factor'
    p[0] = ('*', p[1], p[3])

def p_term_divide(p):
    'term : term DIVIDE factor'
    p[0] = ('/', p[1], p[3])

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_number(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_id(p):
    'factor : ID'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    if p:
        print("Error de sintaxis en token:", p.type, "valor:", p.value)
    else:
        print("Error de sintaxis: Entrada incompleta")

parser = yacc.yacc()

# --------------------------------------------------
# ANÁLISIS SEMÁNTICO
# --------------------------------------------------
symbol_table_stack = [{}]

def current_scope():
    return symbol_table_stack[-1]

def lookup(var):
    for scope in reversed(symbol_table_stack):
        if var in scope:
            return scope[var]
    return None

def declare_variable(var, vartype):
    scope = current_scope()
    if var in scope:
        raise Exception(f"Error semántico: Variable '{var}' ya declarada en el ámbito actual.")
    scope[var] = {'type': vartype, 'value': None}

def assign_variable(var, value):
    for scope in reversed(symbol_table_stack):
        if var in scope:
            decl_type = scope[var]['type']
            if decl_type == 'int' and not isinstance(value, int):
                raise Exception(f"Incompatible asignación: '{var}' es de tipo int, pero se asigna {value}.")
            if decl_type == 'float' and not isinstance(value, (int, float)):
                raise Exception(f"Incompatible asignación: '{var}' es de tipo float, pero se asigna {value}.")
            # Puede ampliarse la verificación para bool, char, etc.
            scope[var]['value'] = value
            return
    raise Exception(f"Error semántico: Variable '{var}' no declarada.")

def evaluate_expression(node):
    """
    Evalúa el nodo del árbol sintáctico de la expresión.
    Se soportan números, identificadores y operaciones aritméticas.
    """
    if isinstance(node, (int, float)):
        return node
    if isinstance(node, str):
        var = lookup(node)
        if var is None or var['value'] is None:
            raise Exception(f"Error semántico: Variable '{node}' usada antes de asignarse.")
        return var['value']
    if isinstance(node, tuple):
        op = node[0]
        if op == 'declare':
            declare_variable(node[2], str(node[1]).lower())
            return None
        elif op == 'assign':
            value = evaluate_expression(node[2])
            assign_variable(node[1], value)
            return value
        elif op in ['+', '-', '*', '/']:
            left = evaluate_expression(node[1])
            right = evaluate_expression(node[2])
            if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                raise Exception("Error semántico: Operación aritmética con operandos no numéricos.")
            if op == '+': return left + right
            if op == '-': return left - right
            if op == '*': return left * right
            if op == '/':
                if right == 0:
                    raise Exception("Error semántico: División por cero.")
                return left / right
        elif op == 'if':
            cond = evaluate_expression(node[1])
            if not isinstance(cond, bool):
                raise Exception("Error semántico: La condición del if debe evaluar a un valor booleano.")
            if cond:
                return evaluate_expression(node[2])
            elif len(node) == 4:
                return evaluate_expression(node[3])
            return None
        elif op == 'while':
            result = None
            if not isinstance(evaluate_expression(node[1]), bool):
                raise Exception("Error semántico: La condición del while debe evaluar a un valor booleano.")
            while evaluate_expression(node[1]):
                result = evaluate_expression(node[2])
            return result
        elif op == 'block':
            symbol_table_stack.append({})
            result = None
            for stmt in node[1]:
                result = evaluate_expression(stmt)
            symbol_table_stack.pop()
            return result
    raise Exception("Error semántico: Nodo desconocido.")

def semantic_analysis(ast):
    global symbol_table_stack
    symbol_table_stack = [{}]
    if ast[0] != 'program':
        raise Exception("Error interno: El nodo raíz debe ser 'program'.")
    decl_list = ast[1]
    stmt_list = ast[2]
    for decl in decl_list:
        if decl[0] == 'declare':
            declare_variable(decl[2], str(decl[1]).lower())
    results = []
    for stmt in stmt_list:
        results.append(evaluate_expression(stmt))
    return results

def analyze_code(code):
    ast = parser.parse(code)
    if ast is None:
        print("No se pudo construir el árbol sintáctico debido a errores.")
        return
    print("Árbol sintáctico:", ast)
    try:
        result = semantic_analysis(ast)
        print("Validación semántica exitosa.")
        print("Resultados:", result)
        print("Tabla de símbolos (ámbito global):", symbol_table_stack[0])
    except Exception as e:
        print(e)

# --------------------------------------------------
# EJECUCIÓN INTERACTIVA
# --------------------------------------------------
if __name__ == '__main__':
    while True:
        code = input("Ingrese una cadena a validar: ")
        analyze_code(code)
        continuar = input("¿Desea validar otra cadena? (1.- Si / 2.- No): ")
        if continuar.strip() == '2':
            break
