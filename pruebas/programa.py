#CRUD basico Barberlink
import pruebas.servicios as servicios

#Menu Barberlink
opcion = 0
while opcion != 5:
    print("====Menu===="+"\n","1. Listar servicios"+"\n","2. Agregar servicio"+"\n","3. Modificar servicio"+"\n", "4. Eliminar servicio"+"\n", "5. Salir")
    try:
        opcion = int(input("Bienvenido seleccione una opcion del menu: "))
    except ValueError:
        print("Opcion no valida, debe ingresar un numero...")
        continue
    if opcion == 1:
        print("Has seleccionado: Listar")
        servicios.listar_servicios()
    elif opcion == 2:
        print("Has seleccionado: Agregar")
        servicios.agregar_servicio()
    elif opcion == 3:
        print("Has seleccionado: Modificar")
        servicios.modificar_servicio()
    elif opcion == 4:
        print("Has seleccionado: Eliminar")
        servicios.eliminar_servicio()
    elif opcion == 5:
        print("Saliendo del programa...")
    else:
        print("Opcion no valida")