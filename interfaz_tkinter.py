import tkinter as tk
from tkinter import messagebox, ttk
from conexion_sql_server import conectar, crear_videojuego, listarVideojuego, actualizarVideojuego, buscarVideojuego, eliminarVideojuego
import matplotlib.pyplot as plt


def obtener_id_plataforma(nombre_plataforma):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_plataforma FROM Plataformas WHERE Nombre = ?", (nombre_plataforma,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None

def actualizar_lista(datos=None):
    texto.delete(1.0, tk.END)
    try:
        juegos = datos if datos else listarVideojuego()
        texto.insert(tk.END, f"{'ID':<5} {'Título':<30} {'Precio':<10} {'Stock':<10} {'Plataforma'}\n")
        texto.insert(tk.END, "-" * 80 + "\n")
        for juego in juegos:
            id_vj, titulo, precio, stock, plataforma = juego
            texto.insert(tk.END, f"{id_vj:<5} {titulo:<30} ${precio:<10.2f} {stock:<10} {plataforma}\n")
    except Exception as e:
        messagebox.showerror("Error", f"Error al mostrar la lista: {str(e)}")
        texto.insert(tk.END, "Error al cargar los datos. Por favor, intente nuevamente.")

def crear_desde_interfaz():
    titulo = entry_titulo.get()
    precio = entry_precio.get()
    stock = entry_stock.get()
    plataforma = combo_plataforma.get()
    
    if not all([titulo, precio, stock, plataforma]):
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
        return
    
    try:
        precio = float(precio)
        stock = int(stock)
    except ValueError:
        messagebox.showwarning("Advertencia", "Precio y stock deben ser números válidos.")
        return
    
    id_plataforma = obtener_id_plataforma(plataforma)
    if id_plataforma is None:
        messagebox.showwarning("Advertencia", "Plataforma no válida.")
        return
    
    try:
        crear_videojuego(titulo, precio, stock, id_plataforma)
        messagebox.showinfo("Éxito", f"Se agregó el videojuego '{titulo}'")
        
        # Limpiar campos
        entry_titulo.delete(0, tk.END)
        entry_precio.delete(0, tk.END)
        entry_stock.delete(0, tk.END)
        combo_plataforma.set('')
        
        actualizar_lista()
    except Exception as e:
        messagebox.showerror("Error", f"Error al crear el videojuego: {str(e)}")

def actualizar_desde_interfaz():
    id_vj = entry_id_actualizar.get()
    titulo = entry_titulo_actualizar.get()
    precio = entry_precio_actualizar.get()
    stock = entry_stock_actualizar.get()
    plataforma = combo_plataforma_actualizar.get()
    
    if not all([id_vj, titulo, precio, stock, plataforma]):
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
        return
    
    try:
        id_vj = int(id_vj)
        precio = float(precio)
        stock = int(stock)
    except ValueError:
        messagebox.showwarning("Advertencia", "ID, precio y stock deben ser números válidos.")
        return
    
    id_plataforma = obtener_id_plataforma(plataforma)
    if id_plataforma is None:
        messagebox.showwarning("Advertencia", "Plataforma no válida.")
        return
    
    try:
        actualizarVideojuego(titulo, stock, precio, id_plataforma, id_vj)
        messagebox.showinfo("Éxito", f"Se actualizó el videojuego '{titulo}'")
        
        # Limpiar campos
        entry_id_actualizar.delete(0, tk.END)
        entry_titulo_actualizar.delete(0, tk.END)
        entry_precio_actualizar.delete(0, tk.END)
        entry_stock_actualizar.delete(0, tk.END)
        combo_plataforma_actualizar.set('')
        
        actualizar_lista()
    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar el videojuego: {str(e)}")

def eliminar_desde_interfaz():
    titulo = entry_eliminar.get()
    if titulo.strip() == "":
        messagebox.showwarning("Advertencia", "Ingresa el nombre del videojuego a eliminar.")
        return
    
    try:
        eliminarVideojuego(titulo)
        messagebox.showinfo("Éxito", f"Se eliminó (si existía) el videojuego '{titulo}'")
        entry_eliminar.delete(0, tk.END)
        actualizar_lista()
    except Exception as e:
        messagebox.showerror("Error", f"Error al eliminar el videojuego: {str(e)}")

def buscar_desde_interfaz():
    busqueda = entry_busqueda.get().strip()
    try:
        if not busqueda:
            actualizar_lista()
            return
            
        resultados = buscarVideojuego(busqueda)
        if resultados:
            actualizar_lista(resultados)
        else:
            messagebox.showinfo("Sin resultados", f"No se encontraron videojuegos con '{busqueda}'.")
            actualizar_lista()
    except Exception as e:
        messagebox.showerror("Error", f"Error al buscar videojuegos: {str(e)}")
        actualizar_lista()

# --- Ventana principal ---
ventana = tk.Tk()
ventana.title("PuertoGames2025 - Gestión de Videojuegos")
ventana.geometry("850x800")

label_titulo = tk.Label(ventana, text="🎮 Catálogo de Videojuegos", font=("Arial", 16, "bold"))
label_titulo.pack(pady=10)

# Área de texto con scroll
frame_texto = tk.Frame(ventana)
scrollbar = tk.Scrollbar(frame_texto)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

texto = tk.Text(frame_texto, height=15, width=110, font=("Courier", 10), yscrollcommand=scrollbar.set)
scrollbar.config(command=texto.yview)
texto.pack()
frame_texto.pack()

# Obtener lista de plataformas
conn = conectar()
cursor = conn.cursor()
cursor.execute("SELECT Nombre FROM Plataformas ORDER BY Nombre")
plataformas = [row[0] for row in cursor.fetchall()]
conn.close()

# --- Crear videojuego ---
frame_crear = tk.LabelFrame(ventana, text="Crear Videojuego", padx=10, pady=5)
frame_crear.pack(pady=5, padx=10, fill="x")

tk.Label(frame_crear, text="Título:").grid(row=0, column=0, padx=5, pady=2)
entry_titulo = tk.Entry(frame_crear, width=30)
entry_titulo.grid(row=0, column=1, padx=5, pady=2)

tk.Label(frame_crear, text="Precio:").grid(row=0, column=2, padx=5, pady=2)
entry_precio = tk.Entry(frame_crear, width=10)
entry_precio.grid(row=0, column=3, padx=5, pady=2)

tk.Label(frame_crear, text="Stock:").grid(row=1, column=0, padx=5, pady=2)
entry_stock = tk.Entry(frame_crear, width=10)
entry_stock.grid(row=1, column=1, padx=5, pady=2)

tk.Label(frame_crear, text="Plataforma:").grid(row=1, column=2, padx=5, pady=2)
combo_plataforma = ttk.Combobox(frame_crear, values=plataformas, width=27)
combo_plataforma.grid(row=1, column=3, padx=5, pady=2)

boton_crear = tk.Button(frame_crear, text="Crear", command=crear_desde_interfaz)
boton_crear.grid(row=2, column=0, columnspan=4, pady=5)

# --- Actualizar videojuego ---
frame_actualizar = tk.LabelFrame(ventana, text="Actualizar Videojuego", padx=10, pady=5)
frame_actualizar.pack(pady=5, padx=10, fill="x")

tk.Label(frame_actualizar, text="ID:").grid(row=0, column=0, padx=5, pady=2)
entry_id_actualizar = tk.Entry(frame_actualizar, width=10)
entry_id_actualizar.grid(row=0, column=1, padx=5, pady=2)

tk.Label(frame_actualizar, text="Título:").grid(row=0, column=2, padx=5, pady=2)
entry_titulo_actualizar = tk.Entry(frame_actualizar, width=30)
entry_titulo_actualizar.grid(row=0, column=3, padx=5, pady=2)

tk.Label(frame_actualizar, text="Precio:").grid(row=1, column=0, padx=5, pady=2)
entry_precio_actualizar = tk.Entry(frame_actualizar, width=10)
entry_precio_actualizar.grid(row=1, column=1, padx=5, pady=2)

tk.Label(frame_actualizar, text="Stock:").grid(row=1, column=2, padx=5, pady=2)
entry_stock_actualizar = tk.Entry(frame_actualizar, width=10)
entry_stock_actualizar.grid(row=1, column=3, padx=5, pady=2)

tk.Label(frame_actualizar, text="Plataforma:").grid(row=2, column=0, padx=5, pady=2)
combo_plataforma_actualizar = ttk.Combobox(frame_actualizar, values=plataformas, width=27)
combo_plataforma_actualizar.grid(row=2, column=1, columnspan=3, padx=5, pady=2)

boton_actualizar = tk.Button(frame_actualizar, text="Actualizar", command=actualizar_desde_interfaz)
boton_actualizar.grid(row=3, column=0, columnspan=4, pady=5)

# --- Buscar videojuego ---
frame_busqueda = tk.Frame(ventana)
label_busqueda = tk.Label(frame_busqueda, text="Buscar videojuego por título:")
label_busqueda.pack(side=tk.LEFT, padx=5)
entry_busqueda = tk.Entry(frame_busqueda, width=30)
entry_busqueda.pack(side=tk.LEFT, padx=5)
boton_buscar = tk.Button(frame_busqueda, text="Buscar", command=buscar_desde_interfaz)
boton_buscar.pack(side=tk.LEFT, padx=5)
frame_busqueda.pack(pady=5)

# --- Eliminar videojuego ---
frame_eliminar = tk.Frame(ventana)
label_eliminar = tk.Label(frame_eliminar, text="Eliminar videojuego por título:")
label_eliminar.pack(side=tk.LEFT, padx=5)
entry_eliminar = tk.Entry(frame_eliminar, width=30)
entry_eliminar.pack(side=tk.LEFT, padx=5)
boton_eliminar = tk.Button(frame_eliminar, text="Eliminar", command=eliminar_desde_interfaz)
boton_eliminar.pack(side=tk.LEFT, padx=5)
frame_eliminar.pack(pady=5)

# --- Botón actualizar lista completa ---
boton_actualizar = tk.Button(ventana, text="🔁 Ver todos", command=actualizar_lista)
boton_actualizar.pack(pady=5)

# Cargar lista al iniciar
actualizar_lista()

def mostrar_grafico():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.Nombre, COUNT(*) as cantidad
            FROM Videojuegos v
            JOIN Plataformas p ON v.id_plataforma = p.id_plataforma
            GROUP BY p.Nombre
        """)
        datos = cursor.fetchall()
        conn.close()

        plataformas = [row[0] for row in datos]
        cantidades = [row[1] for row in datos]

        # Mostrar gráfico de barras
        plt.figure(figsize=(8, 5))
        plt.bar(plataformas, cantidades)
        plt.title("🎮 Videojuegos por Plataforma")
        plt.xlabel("Plataforma")
        plt.ylabel("Cantidad de Juegos")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo mostrar el gráfico: {str(e)}")
boton_estadisticas = tk.Button(ventana, text="📊 Ver estadísticas", command=mostrar_grafico)
boton_estadisticas.pack(pady=10)        



ventana.mainloop()