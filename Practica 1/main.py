def lexer(cadena):
    """
    Función que recibe una cadena y devuelve una lista de tokens.
    Cada token es una tupla (tipo, lexema)
    """
    tokens = []
    i = 0
    n = len(cadena)

    while i < n:
        # Saltar espacios y saltos de línea
        if cadena[i].isspace():
            i += 1
            continue

        # Primero se revisan los tokens compuestos de 2 caracteres:
        dos_chars = cadena[i:i+2]
        if dos_chars in ['<<', '>>']:
            tokens.append(('opMultiplicacion', dos_chars))
            i += 2
            continue
        if dos_chars in ['&&', '||']:
            tokens.append(('opLogico', dos_chars))
            i += 2
            continue
        if dos_chars in ['>=', '<=', '==', '!=']:
            tokens.append(('opRelacional', dos_chars))
            i += 2
            continue

        # Ahora los tokens de 1 carácter:
        ch = cadena[i]
        if ch in [';', ',', '(', ')', '{', '}', '=', '+', '-', '*', '/', '<', '>', '$']:
            tokens.append(('simbolo', ch))
            i += 1
            continue

        # Constante especial: la palabra "pi"
        if cadena[i:i+2] == 'pi' and (i+2 == n or not cadena[i+2].isalnum()):
            tokens.append(('constante', 'pi'))
            i += 2
            continue

        # Constantes numéricas: enteros o decimales
        if cadena[i].isdigit():
            num = ""
            dot_count = 0
            while i < n and (cadena[i].isdigit() or cadena[i] == '.'):
                if cadena[i] == '.':
                    dot_count += 1
                    if dot_count > 1:
                        break
                num += cadena[i]
                i += 1
            tokens.append(('constante', num))
            continue

        # Palabras (identificadores, palabras reservadas y tipos de dato)
        if cadena[i].isalpha():
            palabra = ""
            while i < n and (cadena[i].isalnum() or cadena[i] == '_'):
                palabra += cadena[i]
                i += 1
            if palabra in ['if', 'while', 'return', 'else', 'for']:
                tokens.append((palabra, palabra))
            elif palabra in ['int', 'float', 'char', 'void', 'string']:
                tokens.append(('tipo_dato', palabra))
            else:
                tokens.append(('identificador', palabra))
            continue

        # Si no se reconoce el carácter, se marca como error
        tokens.append(('error', ch))
        i += 1

    return tokens


def main():
    try:
        with open("entrada.txt", "r") as archivo:
            entrada = archivo.read()
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'entrada.txt'.")
        return

    tokens = lexer(entrada)

    # Mostrar los tokens encontrados
    print("\nTokens encontrados:")
    for ttipo, lexema in tokens:
        print(f"Tipo: {ttipo}, Lexema: {lexema}")

    # Conteo de tokens por categoría
    conteo = {}
    for ttipo, _ in tokens:
        conteo[ttipo] = conteo.get(ttipo, 0) + 1

    print("\nConteo de tokens por categoría:")
    for categoria, cantidad in conteo.items():
        print(f"{categoria}: {cantidad}")

    # Si se encontró algún error, se notifica
    if 'error' in conteo:
        print("\nSe encontraron errores en el análisis léxico.")


if __name__ == "__main__":
    main()
