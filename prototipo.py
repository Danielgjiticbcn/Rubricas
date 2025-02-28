import json
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import datetime

# Ruta del archivo JSON para almacenar las rúbricas
RUBRICAS_FILE = "rubricas.json"

# Cargar y guardar rúbricas (mismo código que antes)
def cargar_rubricas():
    try:
        with open(RUBRICAS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Error", "No se pudo cargar el archivo JSON. Por favor, añada el archivo 'rubricas.json'.")
        guardar_rubricas(rubricas_default)
        return rubricas_default

def guardar_rubricas(rubricas):
    with open(RUBRICAS_FILE, "w", encoding="utf-8") as file:
        json.dump(rubricas, file, indent=4, ensure_ascii=False)

def calcular_promedio(puntajes, rubrica):
    total = sum(p * c["ponderacion"] for p, c in zip(puntajes, rubrica["Tasca"]))
    return total

# Clase para la interfaz gráfica
class RubricaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Evaluación de Rúbricas")
        self.root.geometry("800x600")  # Configurar tamaño inicial de la ventana
        self.root.resizable(True, True)  # Permitir redimensionar la ventana
        
        self.rubricas = cargar_rubricas()
        self.puntuaciones = {}
        
        # Elementos de la interfaz
        self.label_rubrica = tk.Label(root, text="Selecciona una rúbrica:")
        self.label_rubrica.pack(pady=10)
        
        self.combo_rubrica = ttk.Combobox(root, values=list(self.rubricas.keys()))
        self.combo_rubrica.pack(pady=5)
        self.combo_rubrica.bind("<<ComboboxSelected>>", self.mostrar_criterios)
        
        self.frame_criterios = tk.Frame(root)
        self.criterios_vars = {}
        
        self.boton_evaluar = tk.Button(root, text="Evaluar Rúbrica", command=self.evaluar_rubrica)
        self.boton_evaluar.pack(pady=10)
        
        self.label_resultado = tk.Label(root, text="")
        self.label_resultado.pack(pady=10)
        
        self.boton_guardar = tk.Button(root, text="Guardar Resultados", command=self.guardar_resultados)
        self.boton_guardar.pack(pady=5)
        
        self.boton_promedio = tk.Button(root, text="Calcular Promedio General", command=self.calcular_promedio_general)
        self.boton_promedio.pack(pady=5)
        
        self.boton_cargar = tk.Button(root, text="Cargar Archivo JSON", command=self.cargar_archivo_json)
        self.boton_cargar.pack(pady=5)
    
    def cargar_archivo_json(self):
        file_path = tk.filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            global RUBRICAS_FILE
            RUBRICAS_FILE = file_path
            self.rubricas = cargar_rubricas()
            self.combo_rubrica['values'] = list(self.rubricas.keys())
            messagebox.showinfo("Éxito", "Archivo JSON cargado correctamente.")
    
    def mostrar_criterios(self, event=None):
        self.frame_criterios.pack_forget()
        self.frame_criterios = tk.Frame(self.root)
        self.frame_criterios.pack(pady=10, padx=10)  # Añadir padding horizontal
        
        rubrica_seleccionada = self.combo_rubrica.get()
        if rubrica_seleccionada:
            rubrica = self.rubricas[rubrica_seleccionada]
            self.criterios_vars = {}
            num_criterios = len(rubrica["Tasca"])
            columns = min(3, num_criterios)  # Máximo 3 columnas
            
            for i, criterio in enumerate(rubrica["Tasca"], 1):
                row = (i - 1) // columns  # Calcular fila
                col = (i - 1) % columns   # Calcular columna
                
                # Crear frame para cada criterio para mejor organización
                criterio_frame = tk.Frame(self.frame_criterios)
                criterio_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                
                label = tk.Label(criterio_frame, text=f"{i}. {criterio['nombre']}", wraplength=250, justify="left")
                label.pack()
                
                var = tk.StringVar()
                opciones = list(rubrica["Puntuació"].keys())
                combo = ttk.Combobox(criterio_frame, values=opciones, textvariable=var, width=10)
                combo.pack(pady=2)
                self.criterios_vars[criterio["nombre"]] = var
            
            # Configurar el grid para que las columnas se expandan uniformemente
            for col in range(columns):
                self.frame_criterios.grid_columnconfigure(col, weight=1)
            self.frame_criterios.grid_rowconfigure((num_criterios - 1) // columns, weight=1)
    
    def evaluar_rubrica(self):
        rubrica_seleccionada = self.combo_rubrica.get()
        if not rubrica_seleccionada:
            messagebox.showwarning("Advertencia", "Selecciona una rúbrica primero.")
            return
        
        rubrica = self.rubricas[rubrica_seleccionada]
        puntajes = []
        
        for criterio in rubrica["Tasca"]:
            calificacion = self.criterios_vars[criterio["nombre"]].get()
            if not calificacion:
                messagebox.showwarning("Advertencia", f"Selecciona una calificación para '{criterio['nombre']}'.")
                return
            puntajes.append(rubrica["Puntuació"][calificacion])
        
        promedio = calcular_promedio(puntajes, rubrica)
        self.puntuaciones[rubrica_seleccionada] = puntajes
        self.label_resultado.config(text=f"Puntajes: {puntajes}\nPromedio ponderado: {promedio:.2f} / 10")
    
    def guardar_resultados(self):
        if not self.puntuaciones:
            messagebox.showwarning("Advertencia", "No hay puntuaciones para guardar.")
            return
        
        with open("resultados_rubrica.txt", "a", encoding="utf-8") as archivo:
            archivo.write(f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            for rubrica, puntajes in self.puntuaciones.items():
                promedio = calcular_promedio(puntajes, self.rubricas[rubrica])
                archivo.write(f"Rúbrica: {rubrica}\nPuntajes: {puntajes}\nPromedio: {promedio:.2f}\n\n")
        messagebox.showinfo("Éxito", "Resultados guardados en 'resultados_rubrica.txt'")
    
    def calcular_promedio_general(self):
        if not self.puntuaciones:
            messagebox.showwarning("Advertencia", "No hay puntuaciones para calcular el promedio.")
            return
        
        promedios = []
        for rubrica, puntajes in self.puntuaciones.items():
            promedio = calcular_promedio(puntajes, self.rubricas[rubrica])
            promedios.append(promedio)
        
        promedio_general = sum(promedios) / len(promedios)
        messagebox.showinfo("Promedio General", f"Promedio general de todas las rúbricas: {promedio_general:.2f} / 10")

if __name__ == "__main__":
    root = tk.Tk()
    app = RubricaApp(root)
    root.mainloop()