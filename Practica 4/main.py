import ply.lex as lex
import ply.yacc as yacc
import tkinter as tk
from tkinter import filedialog

# ---------------------------
# Lista de tokens
# ---------------------------
tokens = (
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'ASSIGN', 'ID', 'SEMI'
)

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_ASSIGN  = r'='
t_SEMI    = r';'

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"[Error léxico] Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

lexer = lex.lex()

# ---------------------------
# Gramática y AST
# ---------------------------
def p_program_single(p):
    'program : assignment'
    p[0] = [p[1]]

def p_program_multiple(p):
    'program : assignment program'
    p[0] = [p[1]] + p[2]

def p_assignment(p):
    'assignment : ID ASSIGN expression SEMI'
    p[0] = ('assign', p[1], p[3])

def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = ('+', p[1], p[3])

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = ('-', p[1], p[3])

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

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
        print("[Error sintáctico] Token inesperado:", p.type, "valor:", p.value)
    else:
        print("[Error sintáctico] Entrada incompleta")

parser = yacc.yacc()

# ---------------------------
# Código intermedio y ASM
# ---------------------------
temp_counter = 0
def new_temp():
    global temp_counter
    t = f"t{temp_counter}"
    temp_counter += 1
    return t

def generate_code(ast):
    code = []
    for stmt in ast:
        gen_stmt(stmt, code)
    return code

def gen_stmt(stmt, code):
    if stmt[0] == 'assign':
        target = stmt[1]
        src = gen_expr(stmt[2], code)
        code.append(("MOV", src, target))

def gen_expr(expr, code):
    if isinstance(expr, int):
        return str(expr)
    if isinstance(expr, str):
        return expr
    op = expr[0]
    a = gen_expr(expr[1], code)
    b = gen_expr(expr[2], code)
    result = new_temp()
    instr = {'+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV'}[op]
    code.append((instr, a, b, result))
    return result

def write_asm(code, filename="output.asm"):
    with open(filename, 'w') as f:
        for instr in code:
            if instr[0] == 'MOV':
                f.write(f"    MOV {instr[2]}, {instr[1]}\n")
            else:
                f.write(f"    {instr[0]} {instr[3]}, {instr[1]}, {instr[2]}\n")
    print(f"✅ Archivo ensamblador generado: {filename}")

# ---------------------------
# Selección de archivo
# ---------------------------
def select_and_process_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Selecciona el archivo .txt", filetypes=[("Archivos de texto", "*.txt")])
    if not file_path:
        print("No se seleccionó ningún archivo.")
        return
    with open(file_path, 'r') as f:
        code = f.read()
    result = parser.parse(code)
    if result:
        print("Árbol sintáctico:", result)
        asm_code = generate_code(result)
        write_asm(asm_code)
    else:
        print("No se pudo generar el árbol sintáctico.")

# ---------------------------
# Main
# ---------------------------
if __name__ == '__main__':
    select_and_process_file()
