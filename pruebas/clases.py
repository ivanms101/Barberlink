from abc import ABC, abstractmethod

class Servicio:
    def __init__(self, nombre, precio):
        if precio <= 0:
            raise ValueError("El precio debe ser un valor mayor que 0")
        self.nombre = nombre
        self.__precio = precio
    @property
    def precio (self):
        return self.__precio
    @precio.setter
    def precio(self, nuevo_precio):
        if nuevo_precio <= 0 :
            raise ValueError("El precio debe ser un valor mayor que 0")
        self.__precio = nuevo_precio
    def mostrar_info(self):
        print(self.nombre)
        print(self.__precio)
    def cambiar_precio(self, nuevo_precio):
        self.__precio = nuevo_precio

class Servicio_preminum(Servicio):
    def __init__(self, nombre, precio, beneficio):
        super().__init__(nombre, precio)
        self.beneficio = beneficio
    def mostrar_info(self):
        print("Servicio premium: ")
        super().mostrar_info()
        print("Beneficio: ",self.beneficio)

class Animal(ABC):
    @abstractmethod
    def hacer_sonido(self):
        pass

class Perro(Animal):
    def hacer_sonido(self):
        print("Guau")

perro = Perro()
perro.hacer_sonido()

corte = Servicio("corte", 18000)
corte_prem = Servicio_preminum("corte preminum", 30000, "masaje")
barba_prem = Servicio_preminum("barba premium", 20000, "toalla caliente")

servicios = [corte, corte_prem]
for servicio in servicios:
    servicio.mostrar_info()