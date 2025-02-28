# Actividad 1.- Validacion simple de una instruccion
# Profe: LUIS FELIPE MUNOZ MENDOZA
# Materia: Seminario de solucion de problemas de Traductores de lenguajes 2
# Mi nombre: Juan Pablo Hernandez Orozco
# Matricula: 219294285

import re

def validar_print_instruccion(instruccion):
    """
    Valida si una instruccion sigue la sintaxis de print("cadena") en Python.
    Se verifica que:
    - La instruccion comience con 'print'
    - Contenga parentesis correctamente balanceados
    - Contenga una cadena encerrada en comillas simples o dobles
    """
    
    # Eliminar espacios al inicio y al final
    instruccion = instruccion.strip()
    
    # Verificar que la instruccion comienza con "print"
    if not instruccion.startswith("print"):
        return False, "La instruccion no comienza con 'print'"
    
    # Verificar que contiene parentesis correctamente colocados
    if not (instruccion.endswith(")") and "(" in instruccion):
        return False, "Falta el parentesis de apertura o cierre"
    
    # Extraer el contenido dentro de los parentesis
    patron_parentesis = r'^print\s*\((.*)\)$'
    match = re.match(patron_parentesis, instruccion)
    if not match:
        return False, "La estructura de parentesis no es valida"
    
    contenido = match.group(1).strip()
    
    # Verificar que el contenido es una cadena valida: debe comenzar y terminar con comillas iguales
    if len(contenido) < 2:
        return False, "No hay contenido suficiente entre parentesis"
    
    # Verificar comillas: pueden ser simples o dobles
    if (contenido[0] == '"' and contenido[-1] == '"') or (contenido[0] == "'" and contenido[-1] == "'"):
        return True, "La instruccion es valida"
    else:
        return False, "La cadena no esta delimitada correctamente por comillas"

# Ejemplos de pruebas
if __name__ == "__main__":
    pruebas = [
        'print("Hola mundo")',
        "print('Hola mundo')",
        'print( "Hola mundo" )',
        ' print("Hola mundo") ',
        'printf("Hola mundo")',             # Incorrecto: empieza con 'printf'
        'print("Hola mundo)',                # Incorrecto: comillas desbalanceadas
        'print(Hola mundo)',                 # Incorrecto: sin comillas
        'print("Hola "mundo")'               # Incorrecto: comillas internas mal ubicadas
    ]
    
    for idx, instruccion in enumerate(pruebas, 1):
        es_valido, mensaje = validar_print_instruccion(instruccion)
        print(f"Prueba {idx}: {instruccion}\nResultado: {mensaje}\n")