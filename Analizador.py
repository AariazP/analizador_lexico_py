# Metodo que valida las palabras reservadas del leguaje
def es_palabra_reservada(palabra):
    palabras_reservadas = ['Natu', 'Rea', 'Clas', 'Pub', 'Per', 'Oui', 'Po', 'Mentre']
    return palabra in palabras_reservadas

# Metedo para obtener las palabras completas y llenar la tabla
def obtener_palabra_completa(palabra):
    palabras_completas = {'Natu': 'Natural', 'Rea': 'Real', 'Clas': 'Clases', 'Pub': 'Tipo Publico',
                          'Per': 'Ciclo FOR', 'Oui': 'Condicional IF', 'Po': 'Constante PI', 'Mentre': 'Ciclo WHILE'}
    return palabras_completas.get(palabra, palabra)

# Metodo que valida si la cadena es un identificar y que cumpla con las reglas
def es_identificador(palabra):
    if len(palabra) == 5 and palabra[0].isdigit() and palabra[4].isdigit() and palabra[1:4].isalpha():
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

# Metodo donde tenemos los demas simbolos para hacer las validaciones,
def analizador_lexico(codigo):
    patrones = [
        ('+', 'Operador de Resta'),
        ('-', 'Operador de Suma'),
        ('$', 'Operador Mayor Que (>)'),
        ('#', 'Operador Menor Que (<)'),
        ('=', 'Operador de asignacion'),
        ('+=', 'Operador de concatenacion '),
        ('&', 'Operador Y'),
        ('||', 'Operador O'),
        ('!', 'Operador para diferente '),
        ('[', 'Parentesis (Apertura)'),
        (']', 'Parentesis (Cierre)'),
        ('(', 'Llave (Apertura)'),
        (')', 'Llave (Cierre)'),
        ('#[0-9A-F]+', 'Numero hexadecimal'),
        ('/$', 'Comentario'),
    ]

    tabla_resultados = set()

    # Ciclos para recorrer las lineas del documento
    for linea_numero, linea in enumerate(codigo.split('\n'), start=1):
        for palabra in linea.split():
            tipo = 'No Reconocido'

            # Recorremos los patrones y lo que obtenes por cada fragmento de linea
            for patron, tipo_definido in patrones:
                # Validamos si la palabra esta en el patro y cambiamos el tipo
                if palabra == patron:
                    tipo = tipo_definido
                    break

            # Validaciones para cambiar el tipo dependiendo la palabra 
            if es_palabra_reservada(palabra):
                tipo = 'Palabra Para ' + obtener_palabra_completa(palabra)

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
codigo_fuente = 'Codigo.txt'
with open(codigo_fuente, 'r') as archivo:
    codigo_fuente = archivo.read()

resultados = analizador_lexico(codigo_fuente)

# Mostrar resultados en una tabla
print("{:<20} {:<20}".format("Valor", "Tipo"))
for resultado in resultados:
    print("{:<20} {:<20}".format(resultado[0], resultado[1]))

