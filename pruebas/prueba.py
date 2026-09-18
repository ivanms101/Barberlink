nombre= "Ivan Sanchez"
edad=32
estudiante=True
print (nombre)
print(nombre, edad, estudiante)

precio=20000
cantidad=3
total=precio*cantidad
print(total)

precio=15000
cantidad=4
precio_total=precio*cantidad
precio_descuento=precio_total-5000
precio_resto=precio_total%3
print(precio_total, precio_descuento, precio_resto)

print(type(nombre), type(edad), type(estudiante))

edad="32"
incremento=5
suma=int(edad)+incremento

numero=10
texto="5"
resultado=int(texto)+numero
resultado_2=str(numero)+texto
print(resultado, resultado_2)

servicios=["corte", "barba", "corte + barba", "tinte"]
print(servicios[3])
print(len(servicios), servicios[0], servicios[-1])
servicios.append("cejas")
print(servicios, servicios[-1])
servicios.remove("tinte")
servicios.pop(1)
print(servicios)

servicios=["corte", "barba", "corte + barba", "tinte", "cejas"]
for servicio in servicios:
    print(servicio)

precios=[15000, 10000, 25000, 30000]
for precio in precios:
    precio_descuento=precio - (precio*(10/100))
    print(int(precio_descuento))

precio=25000
condicion=precio>20000
if condicion == True:
    print("Precio alto")

precio=25000
if precio>20000:
    print("precio alto")
else:
    print("precio normal")


precios=[5000, 8000, 50000, 15000, 20000]
for precio in precios:
    if precio < 10000:
        print("precio economico")
    elif precio >= 20000:
        print("precio alto")
    else:
        print("precio normal")

edad=18
miembro=True
if edad >= 18 and miembro:
    print("descuento disponible")

edad=17
miembro=False
if edad >= 18 or miembro:
    print("puede acceder")

cliente_activo=False
if not cliente_activo:
    print("cliente inactivo")

edad=20
miembro= True
vip=False

if (edad >= 18 and miembro) or vip:
    print("descuento especial disponible")

saludo="Hola"
nombre=input("Cual es tu nombre?")
edad=int(input("Cual es tu edad?"))
print(saludo + " ,", nombre," tienes ", edad, " años")

inicio="Bienvenido"
print(inicio)
nombre = input("¿Cual es tu nombre?")
edad = int(input("¿Cual estu edad?"))
if edad >= 18:
    print("Hola, "+nombre+", eres mayor de edad")
else:
    print("Hola, "+nombre+", eres menor de edad")

servicios = ["corte", "barba", "corte + barba", "tinte"]
print("Hola")
servicio = input("Que servicio desea?")
servicio = servicio.lower().strip()
if servicio in servicios:
    print("Servicio disponible")
else:
    print("servicio no disponible")

contador = 1
while contador <= 5:
    print (contador)
    contador = contador + 1

print("Menu")
opciones = ["1. Mostrar opciones", "2. Salir"]
for opcion in opciones:
    print(opcion)

opcion = 0
while opcion != 2:
    opcion = int(input("¿Que desea hacer? "))
    if opcion == 1:
        print("1. Mostrar servicios")
    elif opcion == 2:
        print("Hasta luego")
    else:
        print("Opcion no valida")

nombre = "Ivan"
def saludar(nombre):
    print("Hola ",nombre," Bienvenido a Barberlink")

saludar(nombre)

precio = 15000
cantidad = 3

def calcular_total(precio, cantidad):
    total = precio * cantidad
    return total

total = calcular_total(precio, cantidad)
print(total)

precio = 30000
es_miembro = False

def calcular_descuento(precio, es_miembro):
    if es_miembro:
        precio_desc = precio * (10/100)
        precio = precio - precio_desc
    return precio

precio = calcular_descuento(precio, es_miembro)
print(precio)

servicio = {
    "nombre":"corte",
    "precio":15000,
    "duracion":30
}

servicio["precio"] = 18000
servicio["duracion"] = 35
servicio["disponible"] = True
print(servicio["disponible"])

servicios = [
    {
        "nombre":"corte",
        "precio": 18000
    },
    {
        "nombre":"barba",
        "precio": 12000
    }
]
print(servicios[1]["precio"])

servicios = [
    {
        "nombre":"corte",
        "precio": 18000
    },
    {
        "nombre":"barba",
        "precio": 12000
    }
]
for servicio in servicios:
    print(servicio["nombre"]," - ", servicio["precio"])

servicios = [
    {
        "nombre":"corte",
        "precio": 18000
    },
    {
        "nombre":"barba",
        "precio": 12000
    }
]

def buscar_servicio(nombre):
    for servicio in servicios:
        if nombre == servicio["nombre"]:
            return servicio
    return None

resultado = buscar_servicio("tinte")
if resultado is None:
    print("Servicio no encontrado")
else:
    print(resultado["nombre"], resultado["precio"])

servicios = [
    {
        "nombre":"corte",
        "precio": 18000
    },
    {
        "nombre":"barba",
        "precio": 12000
    }
]

def agregar_servicio(nombre,precio):
    servicio = {
        "nombre": nombre,
        "precio": precio
    }
    return servicio

nombre = input("Nombre del servicio: ")
precio = int(input("precio del servicio: "))
nuevo_servicio = agregar_servicio(nombre, precio)
servicios.append(nuevo_servicio)
print(servicios)

archivo = open("prueba.txt", "w")
archivo.write("Hola, Barberlink")
archivo.close()

with open("prueba.txt", "w") as archivo:
    archivo.write("Hola, Barberlink")

with open("prueba.txt", "r") as archivo:
    contenido = archivo.read()
print(contenido)

with open("prueba.txt", "a") as archivo:
    archivo.write("\ncorte - 18000")

servicios = [
    {
        "nombre":"corte",
        "precio": 18000
    },
    {
        "nombre":"barba",
        "precio": 12000
    }
]

with open("servicios.txt","w") as archivo:
    for servicio in servicios:
        archivo.write(servicio["nombre"]+" - "+str(servicio["precio"])+"\n")

    with open("servicios.txt", "r") as archivo:
        contenido = archivo.read()
    print(contenido)

servicios = [
    {
        "nombre":"corte",
        "precio": 18000
    },
    {
        "nombre":"barba",
        "precio": 12000
    }
]

import json
with open("servicios.json","w") as archivo:
    json.dump(servicios, archivo)

with open("servicios.json","r") as archivo:
    servicios_leidos = json.load(archivo)

import json
with open("servicios.json", "r") as archivo:
    servicios = json.load(archivo)

nombre = input("Ingrese el nombre del nuevo servicio")
precio = int(input("ingrese el precio del nuevo servicio"))

nuevo_servicio = {
    "nombre": nombre,
    "precio": precio
}

servicios.append(nuevo_servicio)

with open("servicios.json","w") as archivo:
    json.dump(servicios, archivo)

servicios = [
    {
        "nombre":"corte",
        "precio": 18000
    },
    {
        "nombre":"barba",
        "precio": 12000
    }
]

import json
with open("servicios.json", "r") as archivo:
    servicios = json.load(archivo)

servicio_a_cambiar = input("ingrese servicio a cambiar: ")
nuevo_precio = int(input("ingrese el nuevo valor: "))

servicio_a_cambiar = servicio_a_cambiar.strip().lower()
encontrado = False

for servicio in servicios:
    if servicio_a_cambiar == servicio["nombre"]:
        servicio["precio"] = nuevo_precio
        encontrado = True

if not encontrado:
    print("Servicio no definido")

with open("servicios.json", "w") as archivo:
    json.dump(servicios, archivo)

import json
with open("servicios.json", "r") as archivo:
    servicios = json.load(archivo)

encontrado = False
servicio_eliminado = input("Ingrese el servicio a eliminar")
servicio_eliminado = servicio_eliminado.strip().lower()

for indice, servicio in enumerate(servicios):
    if servicio_eliminado == servicio["nombre"]:
        servicios.pop(indice)
        encontrado = True
        break

if not encontrado:
    print("Servicio no encontrado")

with open("servicios.json", "w") as archivo:
    json.dump(servicios, archivo)

#CRUD basico Barberlink
import json

#Funciones
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
        listar_servicios()
    elif opcion == 2:
        print("Has seleccionado: Agregar")
        agregar_servicio()
    elif opcion == 3:
        print("Has seleccionado: Modificar")
        modificar_servicio()
    elif opcion == 4:
        print("Has seleccionado: Eliminar")
        eliminar_servicio()
    elif opcion == 5:
        print("Saliendo del programa...")
    else:
        print("Opcion no valida")