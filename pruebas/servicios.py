import json

def cargar_servicios():
    with open("servicios.json", "r") as archivo:
        servicios = json.load(archivo)
    return servicios

def guardar_servicios(servicios):
    with open("servicios.json", "w") as archivo:
        json.dump(servicios, archivo)

def buscar_servicio(nombre):
    servicios = cargar_servicios()
    for servicio in servicios:
        if nombre == servicio["nombre"]:
            return servicio
    return None

def listar_servicios():
    servicios = cargar_servicios()
    for servicio in servicios:
        print(servicio["nombre"]," - ", "$ " + str(servicio["precio"]))

def agregar_servicio():
    servicios = cargar_servicios()
    servicio = input("Ingrese el nuevo servicio: ")
    servicio = servicio.strip().lower()
    if servicio == "" : 
        print("El nombre del servicio no puede estar vacio")
        return
    busqueda = buscar_servicio(servicio)
    if busqueda is not None :
        print("El servicio ya existe")
        return
    try:
        precio = int(input("Ingrese el precio del servicio: "))
    except ValueError:
        print("Debe ingresar un valor numerico")
        return
    if precio <= 0:
        print("Valor no valido")
        return
    servicio_nuevo = {
        "nombre" : servicio,
        "precio" : precio
    }
    servicios.append(servicio_nuevo)
    guardar_servicios(servicios)

def modificar_servicio():
    servicios = cargar_servicios()
    servicio_a_cambiar = input("ingrese servicio a cambiar: ")
    servicio_a_cambiar = servicio_a_cambiar.strip().lower()
    if servicio_a_cambiar == "" :
        print("Debe ingresar un servicio")
        return
    busqueda = buscar_servicio(servicio_a_cambiar)
    if busqueda is None:
        print("No existe el servicio")
        return
    try:
        nuevo_precio = int(input("ingrese el nuevo valor: "))
    except ValueError:
        print("Debe ingresar un valor numerico")
        return
    if nuevo_precio <= 0:
        print("Valor no valido")
        return
    busqueda["precio"] = nuevo_precio
    guardar_servicios(servicios)

def eliminar_servicio():
    servicios = cargar_servicios()
    servicio_eliminado = input("Ingrese el servicio a eliminar: ")
    servicio_eliminado = servicio_eliminado.strip().lower()
    if servicio_eliminado == "" :
        print("Debe ingresar un servicio")
        return
    busqueda = buscar_servicio(servicio_eliminado)
    if busqueda is None:
        print("No existe el servicio")
        return
    servicios.remove(busqueda)
    print("Servicio eliminado...")
    guardar_servicios(servicios)