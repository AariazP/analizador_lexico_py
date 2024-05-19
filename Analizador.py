import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

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

def es_palabra_reservada(palabra):
    palabras_reservadas = ['para', 'mientras', 'si', 'clase', 'sino', 'interface']
    return palabra in palabras_reservadas

def obtener_palabra_completa(palabra):
    palabras_completas = {'para': 'para', 'si': 'si','sino':'sino' ,'mientras': 'mientras', 'clase': 'clase',
                          'interface': 'interface', 'publico': 'publico', 'privado': 'privado', 'protegido': 'protegido'}
    return palabras_completas.get(palabra, palabra)

def es_identificador(palabra):
    if palabra[0].isalpha() and palabra[1:].isalnum():
        return True
    return False

def es_numero_natural(palabra):
    return palabra.isdigit()

def es_numero_real(palabra):
    try:
        float(palabra)
        return True
    except ValueError:
        return False
    
def es_cadena_texto(palabra):
    if palabra.startswith('//"') and palabra.endswith('"//'):
        return True
    return False

def verificarLinea(linea):
    result = []
    
    if '#' in linea:
        elemento = (linea.strip(), 'Comentario')
        result.append(elemento)
        return result

    palabras = linea.split() 
    for palabra in palabras:        
        if '(' in linea and ')' in linea:
            inicio = linea.index('(')
            fin = linea.index(')')
            parametro = linea[inicio+1:fin]
            nombre_funcion = linea[:inicio+1] + ')'
            result.append((nombre_funcion.strip(), 'Funcion'))

            if ',' in parametro:
                elemento = (linea.strip(), 'Funcion con parametro de tipo lista')
                parametros = parametro.split(',')
                for param in parametros:
                    result.append(("tipo del parametro", str(verificarLinea(param))))
            else:
                elemento = (linea.strip(), 'Funcion con parametro simple')
                analizador_lexico(parametro)
                result.append(("tipo del parametro", str(verificarLinea(parametro))))

        for palabra in linea.split():
            tipo = 'No Reconocido'

            if palabra.startswith('//"') and palabra.endswith('"//'):
                tipo = 'Cadena de texto'
                continue

            for patron, tipo_definido in patrones:
                if palabra == patron:
                    tipo = tipo_definido
                    break

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
            result.append(elemento)

    return result

def analizador_lexico(codigo):
    tabla_resultados = set()

    for linea_numero, linea in enumerate(codigo.split('\n'), start=1):
        linea = linea.strip()
        result = verificarLinea(linea)      

        for res in result:
            tabla_resultados.add(res)  

    return tabla_resultados

def leerCodigo(path):
    with open(path, 'r') as archivo:
        codigo = archivo.read()

    resultados = analizador_lexico(codigo)
    return resultados

def mostrar_resultados(resultados):
    for resultado in resultados:
        tree.insert('', tk.END, values=(resultado[0], resultado[1]))

def seleccionar_archivo():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            resultados = leerCodigo(file_path)
            for row in tree.get_children():
                tree.delete(row)
            mostrar_resultados(resultados)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo analizar el archivo: {e}")

root = tk.Tk()
root.title("Analizador Léxico")
root.geometry("800x600")

frame = tk.Frame(root)
frame.pack(pady=20)

btn_seleccionar_archivo = tk.Button(frame, text="Seleccionar archivo .txt", command=seleccionar_archivo)
btn_seleccionar_archivo.pack()

columns = ('Valor', 'Tipo')
tree = ttk.Treeview(root, columns=columns, show='headings')
tree.heading('Valor', text='Valor')
tree.heading('Tipo', text='Tipo')
tree.pack(expand=True, fill='both')

root.mainloop()
