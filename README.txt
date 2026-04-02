SISTEMA DE GESTIÓN DE STOCK DE PRODUCTOS
=========================================

📌 DESCRIPCIÓN

Este programa permite gestionar el stock de productos de un local o empresa mediante una interfaz por consola.
Está desarrollado en Python y utiliza una base de datos en SQLite para almacenar los datos ingresados.

Las funcionalidades disponibles permiten:
✔ Registrar productos (nombre, categoría y precio)
✔ Visualizar todos los productos registrados
✔ Buscar productos por su ID (Numero Unico)
✔ Eliminar productos del sistema
✔ Fecha y hora de carga de cada producto

------------------------------------------------------------------------------------------------------------------------

🔧 INSTALACIÓN Y EJECUCIÓN

1. Asegúrese de tener Python 3 instalado en su computadora.
2. El archivo `crud.py` debe estar en la misma carpeta que `main.py`.
3. Se debe instalar el paquete `colorama` en powershell o cmd (Ejecutar como administrador):

  pip install colorama

4. La base de datos `stock.db` se genera automáticamente al registrar el primer producto.

------------------------------------------------------------------------------------------------------------------------

📚 FUNCIONALIDADES IMPLEMENTADAS

● Menú principal con interfaz animada y colorida (utilizando Colorama).
● Cada opcion tiene su validacion para que el usuario elija salir,
  muy util en la opcion 3 y 4 mas que nada por que si el usuario entra a buscar o eliminar productos por error puede volver atras.
● Registro de productos con validaciones de entrada.
● Visualización ordenada alfabéticamente por nombre.
● Búsqueda de productos por ID.
● Eliminación de productos
● Persistencia de datos en la base SQLite `stock.db`.
● Manejo de errores y entradas inválidas para una mejor experiencia de uso.
● Se implemento dejar registrada la fecha y la hora en la cual se realiza cada carga de un producto, teniendo un mejor registro y seguridad del stock.

