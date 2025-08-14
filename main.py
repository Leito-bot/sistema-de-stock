# GAMA DE COLORES PARA EL PROGRAMA
# --> Informacion = COLOR AMARILLO
# --> Errores = COLOR ROJO
# --> Confirmacion = COLOR VERDE

import crud
from colorama import Fore, Back, Style, init
while True:
    try:
        # Llamo a la funcion
        crud.menu_de_opciones()
        opcion_menu = int(input(Fore.YELLOW + "Opcion: " + Style.RESET_ALL))
        if opcion_menu in [1, 2, 3, 4, 5]: #Si opcion_menu es del 1 al 5 limpie la pantalla
            crud.limpiar_pantalla()
        match opcion_menu:
            case 1:
                # Llamo a la funcion
                crud.registro_de_productos()
            case 2:
                # Llamo a la funcion
                crud.mostrar_productos()
            case 3:
                # Llamo a la funcion
                crud.buscar_productos()
            case 4:
                # Llamo a la funcion
                crud.eliminar_productos()                 
            case 5:
                # Termina mi programa
                print("\n===========================================")
                crud.animar_menu("Saliendo del programa, hasta la proxima...")
                print("===========================================\n")
                break
            case _:
                # Muestro error al ingresar una opcion fuera del menu
                print(Fore.RED + "\n❌¡¡Error!! Seleccione una opcion del menu.\n" + Style.RESET_ALL)
    except KeyboardInterrupt: #Evita que el usuario corte el flujo del programa y arroja un mensaje indicando el error
        crud.limpiar_pantalla()
        print(Fore.RED + "\n\n¡¡Error al interrumpir flujo de ejecucion!!" + Style.RESET_ALL)
        print(Fore.YELLOW + "Precione la opcion 5 del menu para finalizar el programa.\n" + Style.RESET_ALL)
    except ValueError:# Evita el corte del flujo del programa si el usuario ingresa caracteres no numericos
        crud.limpiar_pantalla()
        print(Fore.RED + "\n❌¡¡Error!! Valor incorrecto.\n" + Style.RESET_ALL)