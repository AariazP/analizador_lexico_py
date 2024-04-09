# Metodo que valida las palabras reservadas del leguaje
def es_palabra_reservada(palabra):
    palabras_reservadas = ['para', 'mientras', 'si', 'clase', 'sino', 'interface']
    return palabra in palabras_reservadas

# Metedo para obtener las palabras completas y llenar la tabla
def obtener_palabra_completa(palabra):
    palabras_completas = {'para': 'para', 'si': 'si','sino':'sino' ,'mientras': 'mientras', 'clase': 'clase',
                          'interface': 'interface', 'publico': 'publico', 'privado': 'privado', 'protegido': 'protegido'}
    return palabras_completas.get(palabra, palabra)

# Metodo que valida si la cadena es un identificar y que cumpla con las reglas
def es_identificador(palabra):
    if palabra[0].isalpha() and palabra[1:].isalnum():
        return True
    return False

# Metodo que valida si un numero es natural
def es_numero_natural(palabra):
    return palabra.isdigit()

# Metodo que valida si un numero es real
def es_numero_real(palabra):
    try:
        float(palabra)
        return True
    except ValueError:
        return False
    
# Metodo que valida si una cadena es una cadena de texto
def es_cadena_texto(palabra):
    if palabra.startswith('//"') and palabra.endswith('"//'):
        return True
    return False

# Metodo donde tenemos los demas simbolos para hacer las validaciones,
def analizador_lexico(codigo):
    patrones = [
        ('-', 'Operador de Resta'),
        ('+', 'Operador de Suma'),
        ('>', 'Operador Mayor Que (>)'),
        ('<', 'Operador Menor Que (<)'),
        ('=', 'Operador de asignacion'),
        ('!=', 'Operador de diferente'),
        ('+=', 'Operador de concatenacion '),
        ('==', 'Operador de igualdad'),
        ('&', 'Operador Y'),
        ('||', 'Operador O'),
        ('!', 'Operador para diferente '),
        ('(', 'Parentesis (Apertura)'),
        (')', 'Parentesis (Cierre)'),
        ('{', 'Llave (Apertura)'),
        ('}', 'Llave (Cierre)'),
        ('#[0-9A-F]+', 'Numero hexadecimal'),
        ('#', 'Comentario'),
        (';', 'Punto y coma'),
    ]

    tabla_resultados = set()

    # Ciclos para recorrer las lineas del documento
    for linea_numero, linea in enumerate(codigo.split('\n'), start=1):
        linea = linea.strip()
        #verifico si inicio con # para saber si es un comentario
        if '#' in linea:
            #remuevo los espacios en blanco al inicio de la linea y al final
            elemento = (linea.strip(), 'Comentario')
            tabla_resultados.add(elemento)
            continue
        
        #verifico si es una funcion
        # una funcion se identifica por tener un parentesis de apertura y cierre
        if '(' in linea and ')' in linea:

            

            #verifico si la funcion tiene un parametro y extraigo el parametro
            #para ello busco el parentesis de apertura y cierre
            inicio = linea.index('(')
            fin = linea.index(')')
            parametro = linea[inicio+1:fin]

            #extraigo el nombre de la funcion y le agrego los parentesis
            nombre_funcion = linea[:inicio+1] + ')'
            tabla_resultados.add((nombre_funcion.strip(), 'Funcion'))

            if ',' in parametro:
                #si el parametro tiene una coma entonces es un parametro
                #de tipo lista
                elemento = (linea.strip(), 'Funcion con parametro de tipo lista')
                print( "tipo del parametro" + str(analizador_lexico(parametro)))
                continue
            else:
                #si no tiene coma entonces es un parametro de tipo simple
                elemento = (linea.strip(), 'Funcion con parametro simple')
                analizador_lexico(parametro)
                print( "tipo del parametro" + str(analizador_lexico(parametro)))
                continue

            

        for palabra in linea.split():
            tipo = 'No Reconocido'

            if palabra.startswith('//"') and palabra.endswith('"//'):
                tipo = 'Cadena de texto'
                continue
                

            # Recorremos los patrones y lo que obtenes por cada fragmento de linea
            for patron, tipo_definido in patrones:
                # Validamos si la palabra esta en el patro y cambiamos el tipo
                if palabra == patron:
                    tipo = tipo_definido
                    break

            # Validaciones para cambiar el tipo dependiendo la palabra 
            if es_palabra_reservada(palabra):
                tipo = 'Palabra reservada: ' + obtener_palabra_completa(palabra)

            elif es_cadena_texto(palabra):
                tipo = 'Cadena de texto'

            elif es_identificador(palabra):
                tipo = 'Identificador'

            elif es_numero_natural(palabra):
                tipo = 'Numero Natural'

            elif es_numero_real(palabra):
                tipo = 'Numero Real'

            elemento = (palabra, tipo)
            tabla_resultados.add(elemento)

    return tabla_resultados

# Lectura del archivo .txt para obtener el codigo
codigo_fuente = 'codigo2.txt'
with open(codigo_fuente, 'r') as archivo:
    codigo_fuente = archivo.read()

resultados = analizador_lexico(codigo_fuente)

# Mostrar resultados en una tabla
print("-" * 87)
print("|{:<40}  | {:<40} |".format("Valor", "Tipo"))
print("-" * 87)
for resultado in resultados:
    print("| {:<40} | {:<40} |".format(resultado[0], resultado[1]))
print("-" * 87)

