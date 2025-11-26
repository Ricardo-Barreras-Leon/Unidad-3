import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk  # Requiere: pip install pillow
import os 
from datetime import datetime

# -------------------------
# FUNCIONES
# -------------------------

def mostrar_ticket(producto, precio, cantidad, total):
    ticket = tk.Toplevel()
    ticket.title("Ticket de Venta")
    ticket.geometry("400x450")
    ticket.resizable(False, False)
    ticket.configure(bg="#FDF6E4")

    # Fecha y hora
    fecha_hora = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")

    # Texto del ticket
    texto = (
        " *** PUNTO DE VENTA ***\n"
        "--------------------------------------\n"
        f"Fecha: {fecha_hora}\n"
        "--------------------------------------\n"
        f"Producto: {producto}\n"
        f"Precio: ${precio}\n"
        f"Cantidad: {cantidad}\n"
        "--------------------------------------\n"
        f"TOTAL: ${total}\n"
        "--------------------------------------\n"
        " ¡GRACIAS POR SU COMPRA!\n"
    )

    lbl_ticket = tk.Label(ticket, text=texto, justify="left", font=("Consolas", 11), bg="#FDF6E4", fg="#5A4634")
    lbl_ticket.pack(pady=15, padx=10)

    btn_cerrar = ttk.Button(ticket, text="Cerrar", style="Pastel.TButton", command=ticket.destroy)
    btn_cerrar.pack(pady=10)


def abrir_registro_productos():
    reg = tk.Toplevel()
    reg.title("Registro de Productos")
    reg.geometry("400x450")
    reg.resizable(False, False)
    reg.configure(bg="#FDF6E4")

    # --- Etiquetas y Campos de Texto ---
    campos = [
        ("ID del Producto:", "txt_id"),
        ("Descripción:", "txt_desc"),
        ("Precio:", "txt_precio"),
        ("Categoría:", "txt_categoria")
    ]
    entradas = {}
    for texto, nombre in campos:
        lbl = tk.Label(reg, text=texto, font=("Arial", 12), bg="#FDF6E4", fg="#5A4634")
        lbl.pack(pady=5)
        ent = tk.Entry(reg, font=("Arial", 12), relief="solid", bd=1)
        ent.pack(pady=5, ipadx=5, ipady=3)
        entradas[nombre] = ent

    txt_id = entradas["txt_id"]
    txt_desc = entradas["txt_desc"]
    txt_precio = entradas["txt_precio"]
    txt_categoria = entradas["txt_categoria"]

    # --- Función para guardar ---
    def guardar_producto():
        id_prod = txt_id.get().strip()
        descripcion = txt_desc.get().strip()
        precio = txt_precio.get().strip()
        categoria = txt_categoria.get().strip()
        if id_prod == "" or descripcion == "" or precio == "" or categoria == "":
            messagebox.showwarning("Campos Vacíos", "Por favor complete todos los campos.")
            return
        try:
            float(precio)
        except:
            messagebox.showerror("Error", "El precio debe ser un número.")
            return

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        archivo = os.path.join(BASE_DIR,"productos.txt")
        with open(archivo, "a", encoding="utf-8") as archivo:
            archivo.write(f"{id_prod}|{descripcion}|{precio}|{categoria}\n")
            messagebox.showinfo("Guardado", "Producto registrado correctamente.")
            txt_id.delete(0, tk.END)
            txt_desc.delete(0, tk.END)
            txt_precio.delete(0, tk.END)
            txt_categoria.delete(0, tk.END)

    btn_guardar = ttk.Button(reg, text="Guardar Producto", style="Pastel.TButton", command=guardar_producto)
    btn_guardar.pack(pady=20)


def abrir_registro_ventas():
    ven = tk.Toplevel()
    ven.title("Registro de Ventas")
    ven.geometry("420x430")
    ven.resizable(False, False)
    ven.configure(bg="#FDF6E4")

    # Cargar productos
    productos = {}
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        archivof = os.path.join(BASE_DIR,"productos.txt")
        with open(archivof, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                partes = linea.strip().split("|")
                if len(partes) == 4:
                    idp, desc, precio, cat = partes
                    productos[desc] = float(precio)
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo productos.txt")
        ven.destroy()
        return

    lista_productos = list(productos.keys())

    # Controles visuales
    lbl_prod = tk.Label(ven, text="Producto:", font=("Arial", 12), bg="#FDF6E4", fg="#5A4634")
    lbl_prod.pack(pady=5)
    cb_producto = ttk.Combobox(ven, values=lista_productos, font=("Arial", 12), state="readonly")
    cb_producto.pack(pady=5)

    lbl_precio = tk.Label(ven, text="Precio:", font=("Arial", 12), bg="#FDF6E4", fg="#5A4634")
    lbl_precio.pack(pady=5)
    txt_precio = tk.Entry(ven, font=("Arial", 12), state="readonly", relief="solid", bd=1)
    txt_precio.pack(pady=5, ipadx=5, ipady=3)

    lbl_cantidad = tk.Label(ven, text="Cantidad:", font=("Arial", 12), bg="#FDF6E4", fg="#5A4634")
    lbl_cantidad.pack(pady=5)
    cantidad_var = tk.StringVar(ven)
    ven.cantidad_var = cantidad_var
    txt_cantidad = tk.Entry(ven, font=("Arial", 12), textvariable=cantidad_var, relief="solid", bd=1)
    txt_cantidad.pack(pady=5, ipadx=5, ipady=3)
    cantidad_var.trace_add("write", lambda *args: calcular_total())

    lbl_total = tk.Label(ven, text="Total:", font=("Arial", 12), bg="#FDF6E4", fg="#5A4634")
    lbl_total.pack(pady=5)
    txt_total = tk.Entry(ven, font=("Arial", 12), state="readonly", relief="solid", bd=1)
    txt_total.pack(pady=5, ipadx=5, ipady=3)

    # Funciones
    def actualizar_precio(event):
        prod = cb_producto.get()
        if prod in productos:
            txt_precio.config(state="normal")
            txt_precio.delete(0, tk.END)
            txt_precio.insert(0, productos[prod])
            txt_precio.config(state="readonly")
            calcular_total()

    def calcular_total(*args):
        try:
            cant = int(txt_cantidad.get())
            precio = float(txt_precio.get())
            total = cant * precio
            txt_total.config(state="normal")
            txt_total.delete(0, tk.END)
            txt_total.insert(0, total)
            txt_total.config(state="readonly")
        except:
            txt_total.config(state="normal")
            txt_total.delete(0, tk.END)
            txt_total.config(state="readonly")

    def registrar_venta():
        prod = cb_producto.get()
        precio = txt_precio.get()
        cant = txt_cantidad.get()
        total = txt_total.get()
        if prod == "" or precio == "" or cant == "" or total == "":
            messagebox.showwarning("Campos Vacíos", "Todos los campos deben estar completos.")
            return

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        archivov = os.path.join(BASE_DIR,"ventas.txt")
        with open(archivov, "a", encoding="utf-8") as archivo:
            archivo.write(f"{prod}|{precio}|{cant}|{total}\n")
            mostrar_ticket(prod, precio, cant, total)

        cb_producto.set("")
        txt_precio.config(state="normal"); txt_precio.delete(0, tk.END); txt_precio.config(state="readonly")
        txt_cantidad.delete(0, tk.END)
        txt_total.config(state="normal"); txt_total.delete(0, tk.END); txt_total.config(state="readonly")

    cb_producto.bind("<<ComboboxSelected>>", actualizar_precio)
    btn_guardar = ttk.Button(ven, text="Registrar Venta", style="Pastel.TButton", command=registrar_venta)
    btn_guardar.pack(pady=25)


def abrir_reportes():
    ventana = tk.Toplevel()
    ventana.title("Reporte de Ventas")
    ventana.geometry("750x450")
    ventana.configure(bg="#FDF6E4")

    titulo = tk.Label(ventana, text="Reporte de Ventas Realizadas", font=("Arial", 16, "bold"), bg="#FDF6E4", fg="#5A4634")
    titulo.pack(pady=10)

    frame_tabla = tk.Frame(ventana, bg="#FDF6E4")
    frame_tabla.pack(pady=10)

    columnas = ("producto", "precio", "cantidad", "total")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)

    for col, ancho in zip(columnas, [250, 100, 100, 120]):
        tabla.heading(col, text=col.capitalize())
        tabla.column(col, width=ancho, anchor="center")
    tabla.pack()

    total_ventas = 0.0
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        archivo = os.path.join(BASE_DIR,"ventas.txt")
        with open(archivo, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                if linea.strip():
                    datos = linea.strip().split("|")
                    if len(datos) == 4:
                        tabla.insert("", tk.END, values=datos)
                        total_ventas += float(datos[3])
    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo ventas.txt no existe.")
        ventana.destroy()
        return

    lbl_total = tk.Label(ventana, text=f"Total de Ventas: ${total_ventas:.2f}", font=("Arial", 14, "bold"), bg="#FDF6E4", fg="#5A4634")
    lbl_total.pack(pady=10)


def abrir_acerca_de():
    acerca = tk.Toplevel()
    acerca.title("Acerca de")
    acerca.geometry("600x420")
    acerca.resizable(False, False)
    acerca.configure(bg="#FDF6E4")

    lbl_titulo = tk.Label(acerca, text="Punto de Venta de Ropa", font=("Arial", 18, "bold"), bg="#FDF6E4", fg="#5A4634")
    lbl_titulo.pack(pady=10)

    separator = ttk.Separator(acerca, orient='horizontal')
    separator.pack(fill='x', padx=20, pady=5)

    texto = (
        "Versión: 1.0\n"
        "Iniciado el: 23 de noviembre de 2025\n"
        "Finalizada el: 27 de noviembre de 2025\n\n"
        "Desarrollada por: Barreras León Ricardo (estudiante)\n"
        "Guiado por un tutor y con apoyo de ChatGPT\n\n"
        "Objetivo: Crear un sistema de punto de venta sencillo para una tienda de ropa.\n"
        "Tecnologías utilizadas: Python, Tkinter y PIL (Pillow)\n\n"
        "Proyecto escolar / aprendizaje guiado.\n"
        "¡Gracias por usar la aplicación!"
    )
    lbl_info = tk.Label(acerca, text=texto, font=("Arial", 12), bg="#FDF6E4", fg="#5A4634", justify="center")
    lbl_info.pack(pady=20, padx=15)

    btn_cerrar = ttk.Button(acerca, text="Cerrar", style="Pastel.TButton", command=acerca.destroy)
    btn_cerrar.pack(pady=15)


# -------------------------
# VENTANA PRINCIPAL
# -------------------------
ventana = tk.Tk()
ventana.title("Punto de Venta - Ropa")
ventana.geometry("500x600")
ventana.resizable(False, False)
ventana.configure(bg="#FDF6E4")  # Fondo cálido pastel

# LOGO
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    imagen = Image.open(os.path.join(BASE_DIR, "ventas2025.png"))
    imagen = imagen.resize((250, 250))
    img_logo = ImageTk.PhotoImage(imagen)

    lbl_logo = tk.Label(ventana, image=img_logo, bg="#FDF6E4")
    lbl_logo.pack(pady=20)
except:
    lbl_sin_logo = tk.Label(ventana, text="(Aquí va el logo del sistema)", font=("Arial", 14), bg="#FDF6E4", fg="#5A4634")
    lbl_sin_logo.pack(pady=40)

# ESTILOS PASTEL
estilo = ttk.Style()
estilo.theme_use("clam")
estilo.configure(
    "Pastel.TButton",
    font=("Arial", 12),
    padding=10,
    background="#F7D8BA",   # Pastel peach
    foreground="#5A4634",    # Café suave
    relief="flat"
)
estilo.map(
    "Pastel.TButton",
    background=[("active", "#F4C9A2")],
    foreground=[("active", "#3E3025")]
)

# BOTONES PRINCIPALES
btn_reg_prod = ttk.Button(ventana, text="Registro de Productos", style="Pastel.TButton", command=abrir_registro_productos)
btn_reg_prod.pack(pady=10)

btn_reg_ventas = ttk.Button(ventana, text="Registro de Ventas", style="Pastel.TButton", command=abrir_registro_ventas)
btn_reg_ventas.pack(pady=10)

btn_reportes = ttk.Button(ventana, text="Reportes", style="Pastel.TButton", command=abrir_reportes)
btn_reportes.pack(pady=10)

btn_acerca = ttk.Button(ventana, text="Acerca de", style="Pastel.TButton", command=abrir_acerca_de)
btn_acerca.pack(pady=10)

# INICIO APP
ventana.mainloop()
