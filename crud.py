import sqlite3
import os
import time
from colorama import Fore, Back, Style, init
#=====================================================================================================================================================================================

#Funcion para limpiar la pantalla
def limpiar_pantalla():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
#=====================================================================================================================================================================================

# Funcion para darle animacion al menu
def animar_menu(texto):
    for letras in texto:
        print(Fore.CYAN + Style.BRIGHT + letras, end='', flush=True)
        time.sleep(0.010)
    print()
#=====================================================================================================================================================================================

# Uso la funcion animar_menu para el esfecto
def menu_de_opciones():
    animar_menu("╔════════════════════════════╗")
    animar_menu("║      MENÚ PRINCIPAL        ║")
    animar_menu("╚════════════════════════════╝")
    animar_menu("[1] Registrar producto")
    animar_menu("[2] Ver productos")
    animar_menu("[3] Buscar producto")
    animar_menu("[4] Eliminar producto")
    animar_menu("[5] Salir")
#=====================================================================================================================================================================================

def registro_de_productos():
    continuar_registrando = True
    while continuar_registrando:
        conexion = sqlite3.connect("stock.db")
        # Crea objeto cursor que sirve para ejecutar comandos SQL
        cursor = conexion.cursor()
        try:
            conexion.execute("BEGIN TRANSACTION")
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS stock (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE,
                    categoria TEXT NOT NULL,
                    precio REAL NOT NULL
                )
            ''')

            #ingreso de datos por el usuario
            nombre = input("Nombre del producto: ").strip().lower()
            categoria =  input("Categoria del producto: ").strip()
            precio = float(input("Precio del producto: $").strip().lower())

            #Inserto los valores agregados por el usuario a mi DB stock
            cursor.execute('''
            INSERT INTO stock (nombre, categoria, precio)
            VALUES (?, ?, ? )
            ''', (nombre, categoria, precio))

            # Confirma los cambios
            conexion.commit()
            print("\n✅ Producto agregado correctamente.\n")

        except sqlite3.IntegrityError:# Valida que no se ingresen 2 productos iguales
            print(Fore.RED + "\n❌¡¡Error!! No pueden existir dos productos iguales.\n" + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "\n❌Error el precio debe ser un numero valido." + Style.RESET_ALL)
        except AttributeError:
            print(Fore.RED + "\n❌Error el atributo no existe. Intente de nuevo." + Style.RESET_ALL)
        except sqlite3.Error as e:
            # Si ocurre un error vuelve todo para atras asegurando la base de datos
            conexion.rollback()
            print(Fore.RED + f"❌Error al registrar el producto N° {e}" + Style.RESET_ALL)
        finally:
            # Cierra la conexion
            conexion.close()
            
        while True:#Bucle para que el usuario vuelva al menu principal escribiendo -salir-, sino apreta enter y sigue ingresando productos
            print(Fore.YELLOW + "\n- Ingrese 'salir' para volver al menu principal")
            print("- Presione 'Enter' para seguir cargando productos." + Style.RESET_ALL)
            volver = input("Opcion: ").lower().strip()
            if volver == "":
                break    
            if volver == "salir":
                continuar_registrando = False
                limpiar_pantalla()
                break
            else:
                print(Fore.RED + "\n❌¡¡Error!! Precione enter para cargar otro producto o escriba " + "-salir-" + " para finalizar\n" + Style.RESET_ALL)     

#=====================================================================================================================================================================================

def mostrar_productos():
    try:
        conexion = sqlite3.connect("stock.db")
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM stock ORDER BY nombre ASC")
        productos = cursor.fetchall()

        #Si no hay productos cargados entra al IF y muestra vacio con un - en cada columna
        if not productos:
            print(Fore.YELLOW + f"{'ID':<5}{'NOMBRE':<25}{'CATEGORIA':<30}{'PRECIO':<10}" + Style.RESET_ALL)
            print(f"{'-':<5}{'-':<25}{'-':<30}{'-':<10}")
        else:#Si hay productos entra al ELSE y muestra todos los productos
            print(Fore.YELLOW + f"{'ID':<5}{'NOMBRE':<25}{'CATEGORIA':<30}{'PRECIO':<10}" + Style.RESET_ALL)
            for producto in productos:
                print(f"{producto[0]:<5}{producto[1]:<25}{producto[2]:<30}${producto[3]:<10}")

        # Confirma los cambios
        conexion.commit()
    #Error si no se agregaron productos y se ingresa a la opcion de mostrar productos
    except sqlite3.OperationalError as e:
        print(Fore.RED + "\n❌Error al acceder a la Base de Datos:" + Style.RESET_ALL)
        print(Fore.RED + f"{e}" + Style.RESET_ALL)
        print(Fore.YELLOW + "Sugerencia: Primero debe agregar un producto antes de mostrar stock." + Style.RESET_ALL + "\n")
    finally:
        # Cierra la conexion
        conexion.close()

        #Con este while genero un bucle para que cuando se muestren todos los productos ingresados no vuelva a mostrar el menu principal de opciones,
    while True:#Sino que el usuario siga viendo todos los productos y el acceda al menu principal por si solo precionando la tecla Enter  
        volver = input("\nPrecione 'Enter' para volver al menu principal... ")
        if volver == "":
            limpiar_pantalla()
            break
        else: #Si se ingresa al diferente a la tecla Enter muestra error
            print(Fore.RED + "\n❌¡¡Error!! Precione la tecla Enter para salir.\n" + Style.RESET_ALL)
#=====================================================================================================================================================================================

def buscar_productos():
    conexion = sqlite3.connect("stock.db")
    cursor = conexion.cursor()
    try:
        # Verifico si hay productos en la base de datos
        cursor.execute("SELECT COUNT(*) FROM stock")
        cantidad = cursor.fetchone()[0]

        if cantidad == 0:
            print(Fore.YELLOW + "\n No hay productos registrados en stock.\n" + Style.RESET_ALL)
            input("Presione Enter para volver al menú principal...")
            limpiar_pantalla()
            return

        # Mostrar todos los productos disponibles
        cursor.execute("SELECT id, nombre, categoria, precio FROM stock ORDER BY nombre ASC")
        productos_disponibles = cursor.fetchall()

        print(Fore.YELLOW + f"{'ID':<5}{'NOMBRE':<25}{'CATEGORIA':<30}{'PRECIO':<10}" + Style.RESET_ALL)
        for producto in productos_disponibles:
            print(f"{producto[0]:<5}{producto[1]:<25}{producto[2]:<30}${producto[3]:<10}")

        # Menú de busqueda
        while True:
            print(Fore.CYAN + "\n=== BÚSQUEDA DE PRODUCTOS POR ID ===" + Style.RESET_ALL)
            print("[1] Buscar un producto")
            print("[2] Volver al menú principal")
            opcion = input("Opción: ").strip()

            if opcion == "1":
                entrada = input("\nIngrese el ID del producto que desea buscar: ").strip()

                if not entrada.isdigit():
                    limpiar_pantalla()
                    print(Fore.RED + "\n❌ Error: El ID debe ser un número válido.\n" + Style.RESET_ALL)
                    continue

                id_buscado = int(entrada)
                cursor.execute("SELECT id, nombre, categoria, precio FROM stock WHERE id = ?", (id_buscado,))
                producto = cursor.fetchone()

                if not producto:
                    print(Fore.YELLOW + f"\n No se encontró ningún artículo con el ID → {id_buscado}\n" + Style.RESET_ALL)
                else:
                    print("\n✅ Producto encontrado:")
                    print(Fore.YELLOW + f"{'ID':<5}{'NOMBRE':<25}{'CATEGORIA':<30}{'PRECIO':<10}" + Style.RESET_ALL)
                    print(f"{producto[0]:<5}{producto[1]:<25}{producto[2]:<30}${producto[3]:<10}")

                # Preguntar si desea buscar otro producto o salir
                while True:
                    print(Fore.YELLOW + "\n- Presione Enter para buscar otro producto.")
                    print("- Escriba 'salir' para volver al menú principal." + Style.RESET_ALL)
                    volver = input("Opción: ").lower().strip()

                    if volver == "":
                        break
                    elif volver == "salir":
                        limpiar_pantalla()
                        return
                    else:
                        print(Fore.RED + "\n❌ Error: Ingrese una opción válida.\n" + Style.RESET_ALL)
            # Sale al menu principal
            elif opcion == "2":
                limpiar_pantalla()
                return
            else:
                limpiar_pantalla()
                print(Fore.RED + "\n❌ Error: Opción inválida. Intente nuevamente.\n" + Style.RESET_ALL)

    except sqlite3.OperationalError as e:
        print(Fore.RED + "\n❌ Error al acceder a la Base de Datos" + Style.RESET_ALL)
        print(Fore.RED + f"{e}" + Style.RESET_ALL)
        print(Fore.YELLOW + "Sugerencia: Primero debe agregar un producto antes de hacer una búsqueda." + Style.RESET_ALL + "\n")
    except sqlite3.ProgrammingError:
        print(Fore.RED + "\n❌ Error al interactuar con la base de datos.\n" + Style.RESET_ALL)
    finally:
        conexion.close()
#=====================================================================================================================================================================================

def eliminar_productos():
    continuar_eliminando = True

    while continuar_eliminando:
        try:
            conexion = sqlite3.connect("stock.db")
            cursor = conexion.cursor()

            # Obtener todos los productos ordenados por nombre
            cursor.execute("SELECT * FROM stock ORDER BY nombre ASC")
            productos = cursor.fetchall()

            # Validar si hay productos
            if not productos:
                print(Fore.YELLOW + f"{'ID':<5}{'NOMBRE':<25}{'CATEGORIA':<30}{'PRECIO':<10}" + Style.RESET_ALL)
                print(f"{'-':<5}{'-':<25}{'-':<30}{'-':<10}")
                print(Fore.YELLOW + "\n No hay productos cargados en el sistema.\n" + Style.RESET_ALL)
                
                while True:
                    volver = input("Presione Enter para volver al menú principal... ").strip()
                    if volver == "":
                        limpiar_pantalla()
                        continuar_eliminando = False
                        break
                    else:
                        print(Fore.RED + "\n❌ Error: Presione solo Enter para volver al menú.\n" + Style.RESET_ALL)
                continue

            # Mostrar productos disponibles
            print(Fore.YELLOW + f"{'ID':<5}{'NOMBRE':<25}{'CATEGORIA':<30}{'PRECIO':<10}" + Style.RESET_ALL)
            for listado in productos:
                print(f"{listado[0]:<5}{listado[1]:<25}{listado[2]:<30}${listado[3]:<10}")

            # Mostrar menú de eliminación
            print(Fore.CYAN + "\n=== ELIMINAR PRODUCTOS ===\n" + Style.RESET_ALL)
            print("[1] Eliminar un producto")
            print("[2] Volver al menú principal")

            opcion = input("Opción: ").strip()

            if opcion == "1":
                entrada = input("\nIngrese el ID del producto que desea eliminar: ").strip()
                if not entrada.isdigit():
                    limpiar_pantalla()
                    print(Fore.RED + "\n❌ Error: El ID debe ser un número válido.\n" + Style.RESET_ALL)
                    continue

                id_a_eliminar = int(entrada)
                cursor.execute("DELETE FROM stock WHERE id = ?", (id_a_eliminar,))
                if not cursor.rowcount:
                    print(Fore.YELLOW + f"\n No se encontró ningún producto con el ID → {id_a_eliminar}\n" + Style.RESET_ALL)
                else:
                    conexion.commit()
                    print(Fore.GREEN + "✅ Producto eliminado correctamente.\n" + Style.RESET_ALL)

                # Preguntar si desea seguir eliminando o salir
                while True:
                    print(Fore.YELLOW + "- Ingrese 'salir' para volver al menú principal")
                    print("- Presione Enter para seguir eliminando productos." + Style.RESET_ALL)
                    volver = input("Opción: ").lower().strip()

                    if volver == "":
                        break
                    elif volver == "salir":
                        limpiar_pantalla()
                        continuar_eliminando = False
                        break
                    else:
                        print(Fore.RED + "\n❌ Error: Presione Enter para continuar o escriba 'salir' para salir.\n" + Style.RESET_ALL)
            # Sale al menu principal
            elif opcion == "2":
                limpiar_pantalla()
                continuar_eliminando = False
                break
            else:
                limpiar_pantalla()
                print(Fore.RED + "\n❌ Opción inválida. Intente nuevamente.\n" + Style.RESET_ALL)

        except KeyboardInterrupt:
            print(Fore.RED + "\n❌ Interrupción del programa por el usuario.\n" + Style.RESET_ALL)
            break

        except sqlite3.Error as e:
            print(Fore.RED + f"\n❌ Error al eliminar producto: {e}\n" + Style.RESET_ALL)
            while True:
                volver = input("Presione Enter para volver al menú principal... ").strip()
                if volver == "":
                    limpiar_pantalla()
                    continuar_eliminando = False
                    break
                else:
                    print(Fore.RED + "\n❌ Error: Presione solo Enter para salir.\n" + Style.RESET_ALL)

        finally:
            conexion.close()