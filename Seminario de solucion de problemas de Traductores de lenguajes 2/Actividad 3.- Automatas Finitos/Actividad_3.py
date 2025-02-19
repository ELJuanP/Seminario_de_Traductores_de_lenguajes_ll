import tkinter as tk

class AFDValidadorEscalas:
    def __init__(self):
        # Diccionario ampliado: escalas mayores y variantes de escalas menores.
        self.escalas = {
            "mayor": {
                "C": {"notas": {"C", "D", "E", "F", "G", "A", "B"},
                      "acordes": {"C", "Dm", "Em", "F", "G", "Am", "Bdim", "G7"}},
                "A": {"notas": {"A", "B", "C#", "D", "E", "F#", "G#"},
                      "acordes": {"A", "Bm", "C#m", "D", "E", "F#m", "G#dim", "E7"}},
                "G": {"notas": {"G", "A", "B", "C", "D", "E", "F#"},
                      "acordes": {"G", "Am", "Bm", "C", "D", "Em", "F#dim", "D7"}},
                "F": {"notas": {"F", "G", "A", "Bb", "C", "D", "E"},
                      "acordes": {"F", "Gm", "Am", "Bb", "C", "Dm", "Edim", "C7"}}
            },
            "menor natural": {
                "A": {"notas": {"A", "B", "C", "D", "E", "F", "G"},
                      "acordes": {"Am", "Bdim", "C", "Dm", "Em", "F", "G"}},
                "C": {"notas": {"C", "D", "Eb", "F", "G", "Ab", "Bb"},
                      "acordes": {"Cm", "Ddim", "Eb", "Fm", "Gm", "Ab", "Bb"}}
            },
            "menor armónica": {
                "A": {"notas": {"A", "B", "C", "D", "E", "F", "G#"},
                      "acordes": {"Am", "Bdim", "Caug", "Dm", "E", "F", "G#dim"}},
                "C": {"notas": {"C", "D", "Eb", "F", "G", "Ab", "B"},
                      "acordes": {"Cm", "Ddim", "Ebaug", "Fm", "G", "Ab", "Bdim"}}
            },
            "menor melódica": {
                "A": {"notas": {"A", "B", "C", "D", "E", "F#", "G#"},
                      "acordes": {"Am", "Bm", "Caug", "Dm", "E", "F#m", "G#dim"}},
                "C": {"notas": {"C", "D", "Eb", "F", "G", "A", "B"},
                      "acordes": {"Cm", "D", "Ebdim", "Fm", "G", "Am", "Bdim"}}
            }
        }

    def validar_secuencia(self, tonalidad, tipo_escala, secuencia):
        """
        Verifica si una secuencia de notas y acordes pertenece a la escala seleccionada.
        Retorna un mensaje indicando si es válida o cuál elemento no pertenece a la escala.
        """
        if tipo_escala not in self.escalas or tonalidad not in self.escalas[tipo_escala]:
            return "⚠️ Tonalidad o tipo de escala no válidos."
        
        escala = self.escalas[tipo_escala][tonalidad]
        for elemento in secuencia:
            if elemento not in escala["notas"] and elemento not in escala["acordes"]:
                return f"❌ Secuencia inválida en {tonalidad} {tipo_escala}. '{elemento}' no pertenece a la escala."
        
        return f"✅ Secuencia válida en {tonalidad} {tipo_escala}."

# Función llamada al presionar el botón "Validar" en la interfaz
def validar():
    tonalidad = tonalidad_entry.get().strip()
    tipo_escala = tipo_escala_var.get().strip().lower()
    secuencia_text = secuencia_entry.get().strip()
    # Separa la secuencia por espacios (cada elemento debe ingresarse separado)
    secuencia = secuencia_text.split()
    
    resultado = afd.validar_secuencia(tonalidad, tipo_escala, secuencia)
    resultado_label.config(text=resultado)

# Instancia del AFD
afd = AFDValidadorEscalas()

# Configuración de la ventana principal de Tkinter
root = tk.Tk()
root.title("Actividad 3.- Autómatas finitos")

# Campo para ingresar la tonalidad
tk.Label(root, text="Tonalidad (ej. C, A, D#):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
tonalidad_entry = tk.Entry(root)
tonalidad_entry.grid(row=0, column=1, padx=5, pady=5)

# Menú desplegable para seleccionar el tipo de escala (incluye variantes para menor)
tk.Label(root, text="Tipo de escala:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
tipo_escala_var = tk.StringVar(root)
tipo_escala_var.set("mayor")  # valor por defecto
tipo_escala_menu = tk.OptionMenu(root, tipo_escala_var, "mayor", "menor natural", "menor armónica", "menor melódica")
tipo_escala_menu.grid(row=1, column=1, padx=5, pady=5)

# Campo para ingresar la secuencia de notas/acordes
tk.Label(root, text="Secuencia (notas/acordes separados por espacio):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
secuencia_entry = tk.Entry(root, width=40)
secuencia_entry.grid(row=2, column=1, padx=5, pady=5)

# Botón para validar la secuencia
validar_button = tk.Button(root, text="Validar", command=validar)
validar_button.grid(row=3, column=0, columnspan=2, pady=10)

# Etiqueta para mostrar el resultado
resultado_label = tk.Label(root, text="", fg="blue")
resultado_label.grid(row=4, column=0, columnspan=2, pady=5)

root.mainloop()