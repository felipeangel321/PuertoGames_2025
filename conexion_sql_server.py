import pyodbc
##definimos una funcion, llamada Conectar que se conecta con la base de datos
## para que al crear otras funciones solo llamemos a esta funcionsita
def conectar():
    conn = pyodbc.connect(   'DRIVER={ODBC Driver 17 for SQL Server};'#Especificamos el driver
        'SERVER=localhost;'
        'DATABASE=PuertoGames2025;'
        'Trusted_Connection=yes;')
    return conn

##hacemos la funcion para INSERTAR datos alas tablas.
def crear_videojuego(titulo, precio,stock,id_plataforma):

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Videojuegos (titulo, precio, stock, id_plataforma)
        VALUES (?, ?, ?, ?)
    """, (titulo, precio, stock, id_plataforma))
    conn.commit()##al ser una funcion INSERT debe llevar commit para confirmar los cambios en la bd

    conn.close()##usamos conn.close para ahorrar recursitos

##esta es la funcion que muestra los juegos con un SELECT
def listarVideojuego():
    conn= conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT v.id_videojuego, v.titulo, v.precio, v.stock, p.nombre
        FROM Videojuegos v
        JOIN Plataformas p ON v.id_plataforma = p.id_plataforma;
                   """)
    resultados = cursor.fetchall()
    conn.close()
    return resultados

##Ahora haremos la funcion para Actualizar videoJuegos

def actualizarVideojuego (nuevo_titulo,nuevo_stock,nuevo_precio,nueva_idPlataforma,id_videojuego):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(("""
         UPDATE VideoJuegoS
         SET titulo =?,stock=?,precio=?,id_plataforma=?
        WHERE id_videojuego = ?
                   """),(nuevo_titulo,nuevo_stock,nuevo_precio,nueva_idPlataforma,id_videojuego))
   
    conn.commit()
    conn.close()
    print ("Se ha actualizado el nuevo juego ")
    
##funcionsita para buscar video juego pero por nombre
def buscarVideojuego(nombre_busqueda = None):
    conn = conectar()
    cursor = conn.cursor()
    if nombre_busqueda:
        consulta ="""
                    SELECT v.titulo,v.precio,v.stock,p.Nombre AS Plataforma
        FROM VideoJuegos v
        JOIN Plataformas P ON v.id_Plataforma = p.id_Plataforma
        WHERE v.titulo LIKE ?;                  
                   """
        cursor.execute(consulta,('%' + nombre_busqueda + '%',))
    else:
        consulta=("""SELECT v.titulo,v.precio,v.stock,p.Nombre AS Plataforma
        FROM VideoJuegos v
        JOIN Plataformas P ON v.id_Plataforma = p.id_Plataforma


         """)
        cursor.execute(consulta)
    resultados = cursor.fetchall()
    conn.close()
    return resultados
##ahora funcionsita para eliminar juego 

def eliminarVideojuego(titulo):
    conn=conectar()
    cursor= conn.cursor()
    cursor.execute("""

        DELETE FROM VideoJuegos
        WHERE titulo = ?
                 """,(titulo,))##en esta linea decimos que titulo es una tupla por eso lleva una coma
    conn.commit()
    conn.close()
    print("has eliminado un video juego ")

