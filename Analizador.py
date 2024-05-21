import tkinter as tk
from tkinter import filedialog, messagebox
import graphviz
import os

# Patrón de los símbolos que se van a validar
patrones = [
    ('-', 'Operador de Resta'),
    ('+', 'Operador de Suma'),
    ('>', 'Operador Mayor Que (>)'),
    ('<', 'Operador Menor Que (<)'),
    ('=', 'Operador de asignación'),
    ('!=', 'Operador de diferente'),
    ('+=', 'Operador de concatenación '),
    ('==', 'Operador de igualdad'),
    ('&', 'Operador Y'),
    ('||', 'Operador O'),
    ('!', 'Operador para diferente '),
    ('(', 'Paréntesis (Apertura)'),
    (')', 'Paréntesis (Cierre)'),
    ('{', 'Llave (Apertura)'),
    ('}', 'Llave (Cierre)'),
    ('#', 'Comentario'),
    (';', 'Punto y coma'),
    ('SUMA', 'Operador de Suma'),
    ('MENOS', 'Operador de Resta'),
    ('POR', 'Operador de Multiplicación'),
    ('DIVIDIR', 'Operador de División'),
    ('IGUAL', 'Operador de Igualdad'),
    ('DIFERENTE', 'Operador de Diferencia'),
    ('AND', 'Operador Lógico Y'),
    ('OR', 'Operador Lógico O'),
    ('PARA', 'Palabra Reservada Para Bucle'),
    ('SI', 'Palabra Reservada Para Decisión'),
    ('SINO', 'Palabra Reservada Para Alternativa'),
    ('MIENTRAS', 'Palabra Reservada Para Bucle Mientras'),
    ('CLASE', 'Palabra Reservada Para Clase'),
    ('int', 'Palabra Reservada Para Enteros'),
    ('float', 'Palabra Reservada Para Reales'),
    ('String', 'Palabra Reservada Para Cadenas de Caracteres'),
    ('char', 'Palabra Reservada Para Caracteres'),
    ('boolean', 'Palabra Reservada Para Booleanos')
]

# Método que valida las palabras reservadas del lenguaje
def es_palabra_reservada(palabra):
    palabras_reservadas = ['PARA', 'SI', 'SINO', 'MIENTRAS', 'CLASE', 'int', 'float', 'String', 'char', 'boolean']
    return palabra.upper() in palabras_reservadas

# Método que valida si una cadena es un identificador y que cumpla con las reglas
def es_identificador(palabra):
    if len(palabra) >= 5 and palabra[0].isalpha():
        for char in palabra[1:]:
            if not char.isalnum():
                return False
        return True
    return False

# Método que valida si un número es natural
def es_numero_natural(palabra):
    return palabra.isdigit()

# Método que valida si un número es real
def es_numero_real(palabra):
    try:
        float(palabra)
        return True
    except ValueError:
        return False

# Método que valida si una cadena es una cadena de texto
def es_cadena_texto(palabra):
    return palabra.startswith('"') and palabra.endswith('"')

# Método que verifica cada línea del código
def verificar_linea(linea):
    result = []

    if linea.startswith('#'):
        result.append((linea, 'Comentario'))
        return result

    palabras = linea.split()

    for palabra in palabras:
        tipo = 'No Reconocido'

        for patron, tipo_definido in patrones:
            if palabra == patron:
                tipo = tipo_definido
                break

        if tipo == 'No Reconocido':
            if es_palabra_reservada(palabra):
                tipo = f'Palabra Reservada: {palabra.upper()}'
            elif es_identificador(palabra):
                tipo = 'Identificador'
            elif es_numero_natural(palabra):
                tipo = 'Número Natural'
            elif es_numero_real(palabra):
                tipo = 'Número Real'
            elif es_cadena_texto(palabra):
                tipo = 'Cadena de Texto'

        if tipo == 'No Reconocido':
            tipo = f'Token no reconocido: {palabra}'

        result.append((palabra, tipo))

    return result

# Método que realiza el análisis léxico
def analizador_lexico(codigo):
    tabla_resultados = set()

    for linea in codigo.split('\n'):
        linea = linea.strip()
        result = verificar_linea(linea)

        for res in result:
            tabla_resultados.add(res)

    return tabla_resultados

# Método que lee el contenido del archivo
def leer_codigo(path, text_widget):
    with open(path, 'r') as archivo:
        codigo = archivo.read()

    resultados = analizador_lexico(codigo)
    mostrar_resultados(resultados, text_widget)
    generar_automatas(resultados)

# Método que muestra los resultados en un widget de texto
def mostrar_resultados(resultados, text_widget):
    text_widget.delete(1.0, tk.END)  # Limpiar el contenido del widget de texto
    result_str = "-" * 87 + "\n"
    result_str += "|{:<40}  | {:<40} |\n".format("Valor", "Tipo")
    result_str += "-" * 87 + "\n"
    for resultado in resultados:
        result_str += "| {:<40} | {:<40} |\n".format(resultado[0], resultado[1])
    result_str += "-" * 87 + "\n"
    text_widget.insert(tk.END, result_str)  # Insertar el contenido en el widget de texto

# Método para seleccionar el archivo a analizar
def seleccionar_archivo(text_widget):
    path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if path:
        leer_codigo(path, text_widget)

# Método para crear el gráfico del autómata
def crear_automata(token):
    dot = graphviz.Digraph(comment=f'Autómata para {token}')

    # Crear nodos y transiciones para cada letra del token
    previous_state = 'q0'
    dot.node(previous_state, shape='circle')

    for i, letra in enumerate(token):
        current_state = f'q{i + 1}'
        dot.node(current_state, shape='circle')
        dot.edge(previous_state, current_state, label=letra)
        previous_state = current_state

    # Estado final
    dot.node(previous_state, shape='doublecircle')

    output_dir = "automatas"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = os.path.join(output_dir, f'automata_{token}.gv')
    dot.render(filename, format='png', cleanup=True)
    return filename + '.png'

# Método para generar autómatas para todos los tokens reconocidos
def generar_automatas(resultados):
    for token, tipo in resultados:
        if tipo != 'Token no reconocido: ' + token and tipo != 'Comentario':
            crear_automata(token)
    messagebox.showinfo("Completado", "Se han generado los autómatas para los tokens reconocidos.")

# Configuración de la interfaz gráfica
def configurar_interfaz():
    root = tk.Tk()
    root.title("Analizador Léxico")
    root.geometry("800x600")

    label = tk.Label(root, text="Seleccione el archivo .txt para analizar:")
    label.pack(pady=10)

    boton_seleccionar = tk.Button(root, text="Seleccionar Archivo", command=lambda: seleccionar_archivo(text_widget))
    boton_seleccionar.pack(pady=20)

    text_widget = tk.Text(root, wrap=tk.NONE)
    text_widget.pack(expand=True, fill=tk.BOTH)

    root.mainloop()

if __name__ == '__main__':
    configurar_interfaz()
