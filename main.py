from src.Tablero import Tablero
from src.Ficha import Ficha
from src.Muralla import Muralla
print()

tablero = Tablero()

# 1 Objeto tablero.
# print("1")
# for row in tablero.matriz:
#     print(row)
# print()

## 2 funcion de mostrar tabler como va
# tablero.mostrar_tablero()

## 3 Añadir fichas 
print("prueba 3")
ficha = Ficha("A", 3, tablero, "A")
ficha2 = Ficha("C", 5, tablero, "A")
ficha3 = Ficha("E", 3, tablero, "A")

muralla = Muralla(tablero, ficha,ficha2, True)
muralla2 = Muralla(tablero, ficha2,ficha3, False)


resultFicha = ficha.anadir_ficha()
# print(resultFicha)
ficha2.anadir_ficha()
ficha3.anadir_ficha()


muralla.anadir_muralla()
muralla2.anadir_muralla()

tablero.mostrar_tablero()


print()
# ###  4 Validar malos movimientos

# Ficha o muralla donde ya hay uno (no deberia añadirse)
print("Prueba 4 ")
ficha4 = Ficha("A", 3, tablero, "B")
ficha4b = Ficha("C", 5, tablero, "B")
muralla4 = Muralla(tablero, ficha4,ficha4b, False)

ficha4.anadir_ficha()
ficha4b.anadir_ficha()
muralla4.anadir_muralla()

tablero.mostrar_tablero()

print()

# Validacion de que no puede poner una ficha en los limites de otro jugador a menos de que hayan fichas en
#la fila o columna N-1: el resultado de esta prueba debe ser "no valido", ya que por defecto
# el programa asume que es un player horizontal

#Deberia no añadirse y dar mensaje de error
print("Prueba 5, jugador vertical poniendo ficha en limite horizontal")
ficha5 = Ficha("G", 1, tablero, "A")
ficha5.anadir_ficha()
print()

# Deberia no añadirse y dar mensaje de error
print("Prueba 5, jugador horizontal poniendo ficha en limite vertical")
ficha5hor = Ficha("L", 7, tablero, "B", False)
ficha5hor.anadir_ficha()
print()


# Validacion de que no ponga una muralla muy lejos una de otra o invalida
print("Prueba 6, Muralla mal puesta")
ficha6 = Ficha("L", 7, tablero, "A")
ficha7 = Ficha("J", 7,tablero,"A")
muralla= Muralla(tablero, ficha6, ficha7)

ficha6.anadir_ficha()
ficha7.anadir_ficha()

tablero.mostrar_tablero()
