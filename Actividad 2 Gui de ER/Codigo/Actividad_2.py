import tkinter as tk
from tkinter import messagebox
import re

# Función que se invoca al presionar el botón "Validar"
def validate_entries():
    # Se recuperan los valores ingresados en cada campo
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()
    curp = curp_entry.get().strip()
    rfc = rfc_entry.get().strip()
    ip = ip_entry.get().strip()
    birthday = birthday_entry.get().strip()

    errors = []  # Lista para acumular mensajes de error

    # Definición de las expresiones regulares para cada caso

    # Teléfono de 10 dígitos: exactamente 10 números
    regex_phone = re.compile(r'^\d{10}$')

    # Correo electrónico: patrón básico para email (puedes extenderlo si es necesario)
    regex_email = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')

    # CURP: El formato generalmente consiste en 4 letras, 6 dígitos (fecha en formato YYMMDD),
    # una letra que indica sexo (H o M), 5 letras (incluyendo el estado) y 2 dígitos o caracteres alfanuméricos.
    # Nota: Este regex es un ejemplo simplificado.
    regex_curp = re.compile(r'^[A-Z]{4}\d{6}[HM][A-Z]{5}[0-9A-Z]\d$')

    # RFC: Para personas físicas generalmente se utiliza 4 letras, 6 dígitos (fecha) y 3 dígitos o letras.
    regex_rfc = re.compile(r'^([A-ZÑ&]{3,4})(\d{6})([A-Z\d]{3})$')

    # Dirección IP v4: Cada octeto debe estar en el rango 0-255
    regex_ip = re.compile(
        r'^(?:(?:25[0-5]|2[0-4]\d|[01]?\d?\d)\.){3}'
        r'(?:25[0-5]|2[0-4]\d|[01]?\d?\d)$'
    )

    # Fecha de cumpleaños en formato DD/MM/AA:
    # Días entre 01 y 31, meses entre 01 y 12 y 2 dígitos para el año.
    regex_birthday = re.compile(r'^(0[1-9]|[12]\d|3[01])/(0[1-9]|1[0-2])/\d{2}$')

    # Validación de cada campo; si no coincide con el patrón se añade un mensaje de error.
    if not regex_phone.match(phone):
        errors.append("Teléfono de 10 dígitos inválido.")
    if not regex_email.match(email):
        errors.append("Correo electrónico inválido.")
    if not regex_curp.match(curp):
        errors.append("CURP inválido.")
    if not regex_rfc.match(rfc):
        errors.append("RFC inválido.")
    if not regex_ip.match(ip):
        errors.append("Dirección IP v4 inválida.")
    if not regex_birthday.match(birthday):
        errors.append("Fecha de cumpleaños inválida (DD/MM/AA).")

    # Se muestra una ventana emergente indicando si hubo errores o si la validación fue exitosa
    if errors:
        messagebox.showerror("Errores de validación", "\n".join(errors))
    else:
        messagebox.showinfo("Validación exitosa", "Todos los campos son válidos.")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Validador de Cadenas con Expresiones Regulares")

# Configuración de la cuadrícula (grid) para organizar los widgets

# Campo para Teléfono de 10 dígitos
tk.Label(root, text="Teléfono de 10 dígitos:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
phone_entry = tk.Entry(root, width=30)
phone_entry.grid(row=0, column=1, padx=5, pady=5)

# Campo para Correo Electrónico
tk.Label(root, text="Correo Electrónico:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
email_entry = tk.Entry(root, width=30)
email_entry.grid(row=1, column=1, padx=5, pady=5)

# Campo para CURP
tk.Label(root, text="CURP:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
curp_entry = tk.Entry(root, width=30)
curp_entry.grid(row=2, column=1, padx=5, pady=5)

# Campo para RFC
tk.Label(root, text="RFC:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
rfc_entry = tk.Entry(root, width=30)
rfc_entry.grid(row=3, column=1, padx=5, pady=5)

# Campo para Dirección IP v4
tk.Label(root, text="Dirección IP v4:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
ip_entry = tk.Entry(root, width=30)
ip_entry.grid(row=4, column=1, padx=5, pady=5)

# Campo para Fecha de cumpleaños (DD/MM/AA)
tk.Label(root, text="Fecha de cumpleaños (DD/MM/AA):").grid(row=5, column=0, padx=5, pady=5, sticky="e")
birthday_entry = tk.Entry(root, width=30)
birthday_entry.grid(row=5, column=1, padx=5, pady=5)

# Botón para activar la validación de los campos
validate_button = tk.Button(root, text="Validar", command=validate_entries)
validate_button.grid(row=6, column=0, columnspan=2, padx=5, pady=10)

# Inicia el bucle principal de la aplicación
root.mainloop()
