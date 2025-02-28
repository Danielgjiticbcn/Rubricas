import json  # Importa la biblioteca json para manejar archivos JSON, que se usan para almacenar las rúbricas.
import tkinter as tk  # Importa la biblioteca tkinter para crear la interfaz gráfica, renombrándola como tk.
from tkinter import messagebox, ttk, simpledialog  # Importa widgets específicos de tkinter: messagebox para mensajes, ttk para elementos estilizados, y simpledialog para diálogos simples.
import datetime  # Importa la biblioteca datetime para manejar fechas y horas, usada para registrar resultados.

# Ruta del archivo JSON para almacenar las rúbricas
RUBRICAS_FILE = "rubricas.json"  # Define la ruta del archivo JSON donde se almacenarán las rúbricas, por defecto "rubricas.json".

# Cargar y guardar rúbricas (mismo código que antes)
def cargar_rubricas():
    try:  # Intenta realizar las siguientes operaciones, manejando posibles errores con except.
        with open(RUBRICAS_FILE, "r", encoding="utf-8") as file:  # Abre el archivo JSON en modo lectura con codificación UTF-8.
            return json.load(file)  # Carga y devuelve el contenido del archivo JSON como un diccionario o lista.
    except FileNotFoundError:  # Si ocurre un error de archivo no encontrado.
        return {}  # Devuelve un diccionario vacío si no se encuentra el archivo.

def guardar_rubricas(rubricas):
    with open(RUBRICAS_FILE, "w", encoding="utf-8") as file:  # Abre el archivo JSON en modo escritura con codificación UTF-8.
        json.dump(rubricas, file, indent=4, ensure_ascii=False)  # Escribe el diccionario rubricas en el archivo JSON con sangría de 4 espacios y sin problemas con caracteres no ASCII.

def calcular_promedio(puntajes, rubrica):
    total = sum(p * c["ponderacion"] for p, c in zip(puntajes, rubrica["Tasca"]))  # Calcula el promedio ponderado multiplicando cada puntaje por su ponderación y sumándolos, usando zip para iterar sobre pares de puntajes y criterios.
    return total  # Retorna el total calculado.

# Clase para la interfaz gráfica
class RubricaApp:
    def __init__(self, root):
        self.root = root  # Asigna la ventana principal (root) como atributo de la instancia.
        self.root.title("Evaluación de Rúbricas")  # Establece el título de la ventana.
        self.root.geometry("800x600")  # Define el tamaño inicial de la ventana (800 píxeles de ancho, 600 de alto).
        self.root.resizable(True, True)  # Permite que la ventana sea redimensionable en ambas dimensiones (ancho y alto).

        self.rubricas = cargar_rubricas()  # Carga las rúbricas desde el archivo JSON al iniciar la aplicación.
        self.puntuaciones = {}  # Inicializa un diccionario vacío para almacenar las puntuaciones de las rúbricas evaluadas.

        # Elementos de la interfaz
        self.label_rubrica = tk.Label(root, text="Selecciona una rúbrica:")  # Crea una etiqueta para indicar que se debe seleccionar una rúbrica.
        self.label_rubrica.pack(pady=10)  # Coloca la etiqueta en la ventana usando pack, con un padding vertical de 10 píxeles.

        self.combo_rubrica = ttk.Combobox(root, values=list(self.rubricas.keys()))  # Crea un desplegable (Combobox) con los nombres de las rúbricas disponibles.
        self.combo_rubrica.pack(pady=5)  # Coloca el Combobox en la ventana con un padding vertical de 5 píxeles.
        self.combo_rubrica.bind("<<ComboboxSelected>>", self.mostrar_criterios)  # Vincula el evento de selección en el Combobox al método mostrar_criterios.

        self.frame_criterios = tk.Frame(root)  # Crea un frame para contener los criterios de la rúbrica seleccionada.
        self.criterios_vars = {}  # Inicializa un diccionario para almacenar las variables de las calificaciones de los criterios.

        self.boton_evaluar = tk.Button(root, text="Evaluar Rúbrica", command=self.evaluar_rubrica)  # Crea un botón para evaluar la rúbrica, vinculado al método evaluar_rubrica.
        self.boton_evaluar.pack(pady=10)  # Coloca el botón en la ventana con un padding vertical de 10 píxeles.

        self.label_resultado = tk.Label(root, text="")  # Crea una etiqueta para mostrar los resultados de la evaluación (inicialmente vacía).
        self.label_resultado.pack(pady=10)  # Coloca la etiqueta en la ventana con un padding vertical de 10 píxeles.

        self.boton_guardar = tk.Button(root, text="Guardar Resultados", command=self.guardar_resultados)  # Crea un botón para guardar resultados, vinculado al método guardar_resultados.
        self.boton_guardar.pack(pady=5)  # Coloca el botón en la ventana con un padding vertical de 5 píxeles.

        self.boton_promedio = tk.Button(root, text="Calcular Promedio General", command=self.calcular_promedio_general)  # Crea un botón para calcular el promedio general, vinculado al método calcular_promedio_general.
        self.boton_promedio.pack(pady=5)  # Coloca el botón en la ventana con un padding vertical de 5 píxeles.

        self.boton_cargar = tk.Button(root, text="Cargar Archivo JSON", command=self.cargar_archivo_json)  # Crea un botón para cargar un archivo JSON, vinculado al método cargar_archivo_json.
        self.boton_cargar.pack(pady=5)  # Coloca el botón en la ventana con un padding vertical de 5 píxeles.

    def cargar_archivo_json(self):
        file_path = tk.filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])  # Abre un diálogo para seleccionar un archivo JSON.
        if file_path:  # Si se seleccionó un archivo.
            global RUBRICAS_FILE  # Declara RUBRICAS_FILE como global para modificarlo.
            RUBRICAS_FILE = file_path  # Actualiza la ruta del archivo JSON con la seleccionada.
            self.rubricas = cargar_rubricas()  # Recarga las rúbricas desde el nuevo archivo.
            self.combo_rubrica['values'] = list(self.rubricas.keys())  # Actualiza las opciones del Combobox con las rúbricas cargadas.
            messagebox.showinfo("Éxito", "Archivo JSON cargado correctamente.")  # Muestra un mensaje de éxito.

    def mostrar_criterios(self, event=None):
        self.frame_criterios.pack_forget()  # Elimina el frame de criterios actual de la ventana para evitar superposiciones.
        self.frame_criterios = tk.Frame(self.root)  # Crea un nuevo frame para los criterios.
        self.frame_criterios.pack(pady=10, padx=10)  # Coloca el frame en la ventana con padding vertical y horizontal.

        rubrica_seleccionada = self.combo_rubrica.get()  # Obtiene el nombre de la rúbrica seleccionada en el Combobox.
        if rubrica_seleccionada:  # Si se seleccionó una rúbrica.
            rubrica = self.rubricas[rubrica_seleccionada]  # Accede a la rúbrica correspondiente en el diccionario.
            self.criterios_vars = {}  # Reinicia el diccionario de variables de calificación.
            num_criterios = len(rubrica["Tasca"])  # Cuenta el número de criterios en la rúbrica.
            columns = min(3, num_criterios)  # Define el número de columnas, máximo 3.

            for i, criterio in enumerate(rubrica["Tasca"], 1):  # Itera sobre los criterios, numerándolos desde 1.
                row = (i - 1) // columns  # Calcula la fila basada en la posición y el número de columnas.
                col = (i - 1) % columns   # Calcula la columna basada en la posición y el número de columnas.

                # Crear frame para cada criterio para mejor organización
                criterio_frame = tk.Frame(self.frame_criterios)  # Crea un frame para cada criterio.
                criterio_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")  # Coloca el frame en el grid con espaciado y expansión.

                label = tk.Label(criterio_frame, text=f"{i}. {criterio['nombre']}", wraplength=250, justify="left")  # Crea una etiqueta con el número y nombre del criterio, con ajuste de texto y alineación izquierda.
                label.pack()  # Coloca la etiqueta dentro del frame del criterio.

                var = tk.StringVar()  # Crea una variable StringVar para almacenar la calificación seleccionada.
                opciones = list(rubrica["Puntuació"].keys())  # Obtiene las opciones de calificación (claves del diccionario Puntuació).
                combo = ttk.Combobox(criterio_frame, values=opciones, textvariable=var, width=10)  # Crea un Combobox para seleccionar la calificación, con un ancho de 10.
                combo.pack(pady=2)  # Coloca el Combobox dentro del frame con un padding vertical de 2 píxeles.
                self.criterios_vars[criterio["nombre"]] = var  # Almacena la variable en el diccionario para acceder después.

            # Configurar el grid para que las columnas se expandan uniformemente
            for col in range(columns):  # Itera sobre las columnas.
                self.frame_criterios.grid_columnconfigure(col, weight=1)  # Configura cada columna para que se expanda uniformemente al redimensionar la ventana.
            self.frame_criterios.grid_rowconfigure((num_criterios - 1) // columns, weight=1)  # Configura la última fila para que se expanda si es necesario.

    def evaluar_rubrica(self):
        rubrica_seleccionada = self.combo_rubrica.get()  # Obtiene el nombre de la rúbrica seleccionada.
        if not rubrica_seleccionada:  # Si no se seleccionó ninguna rúbrica.
            messagebox.showwarning("Advertencia", "Selecciona una rúbrica primero.")  # Muestra un mensaje de advertencia.
            return  # Sale del método.

        rubrica = self.rubricas[rubrica_seleccionada]  # Accede a la rúbrica seleccionada.
        puntajes = []  # Inicializa una lista para almacenar los puntajes.

        for criterio in rubrica["Tasca"]:  # Itera sobre los criterios de la rúbrica.
            calificacion = self.criterios_vars[criterio["nombre"]].get()  # Obtiene la calificación seleccionada para el criterio.
            if not calificacion:  # Si no se seleccionó una calificación.
                messagebox.showwarning("Advertencia", f"Selecciona una calificación para '{criterio['nombre']}'.")  # Muestra un mensaje de advertencia.
                return  # Sale del método.
            puntajes.append(rubrica["Puntuació"][calificacion])  # Añade el puntaje correspondiente a la calificación seleccionada.

        promedio = calcular_promedio(puntajes, rubrica)  # Calcula el promedio ponderado usando la función calcular_promedio.
        self.puntuaciones[rubrica_seleccionada] = puntajes  # Almacena los puntajes en el diccionario de puntuaciones.
        self.label_resultado.config(text=f"Puntajes: {puntajes}\nPromedio ponderado: {promedio:.2f} / 10")  # Actualiza el texto de la etiqueta de resultados con los puntajes y el promedio.

    def guardar_resultados(self):
        if not self.puntuaciones:  # Si no hay puntuaciones almacenadas.
            messagebox.showwarning("Advertencia", "No hay puntuaciones para guardar.")  # Muestra un mensaje de advertencia.
            return  # Sale del método.

        with open("resultados_rubrica.txt", "a", encoding="utf-8") as archivo:  # Abre el archivo de resultados en modo append con codificación UTF-8.
            archivo.write(f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")  # Escribe la fecha y hora actual en el archivo.
            for rubrica, puntajes in self.puntuaciones.items():  # Itera sobre las puntuaciones almacenadas.
                promedio = calcular_promedio(puntajes, self.rubricas[rubrica])  # Calcula el promedio para cada rúbrica.
                archivo.write(f"Rúbrica: {rubrica}\nPuntajes: {puntajes}\nPromedio: {promedio:.2f}\n\n")  # Escribe la rúbrica, los puntajes y el promedio en el archivo.
        messagebox.showinfo("Éxito", "Resultados guardados en 'resultados_rubrica.txt'")  # Muestra un mensaje de éxito.

    def calcular_promedio_general(self):
        if not self.puntuaciones:  # Si no hay puntuaciones almacenadas.
            messagebox.showwarning("Advertencia", "No hay puntuaciones para calcular el promedio.")  # Muestra un mensaje de advertencia.
            return  # Sale del método.

        promedios = []  # Inicializa una lista para almacenar los promedios de cada rúbrica.
        for rubrica, puntajes in self.puntuaciones.items():  # Itera sobre las puntuaciones almacenadas.
            promedio = calcular_promedio(puntajes, self.rubricas[rubrica])  # Calcula el promedio para cada rúbrica.
            promedios.append(promedio)  # Añade el promedio a la lista.

        promedio_general = sum(promedios) / len(promedios)  # Calcula el promedio general dividiendo la suma de los promedios por su cantidad.
        messagebox.showinfo("Promedio General", f"Promedio general de todas las rúbricas: {promedio_general:.2f} / 10")  # Muestra un mensaje con el promedio general.

if __name__ == "__main__":
    root = tk.Tk()  # Crea la ventana principal de tkinter.
    app = RubricaApp(root)  # Instancia la clase RubricaApp con la ventana principal.
    root.mainloop()  # Inicia el bucle principal de la interfaz gráfica, manteniendo la ventana abierta hasta que se cierre.