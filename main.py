from src.Tablero import Tablero
from src.Ficha import Ficha
from src.Muralla import Muralla


tablero = Tablero()

## 1 Objeto tablero.

# for row in tablero.matriz:
#     print(row)

## 2 funcion de mostrar tabler como va
# tablero.mostrar_tablero()

## 3 Añadir fichas 
ficha = Ficha("A", 3, tablero, "A")
muralla = Muralla(tablero, "B",4, True)
muralla2 = Muralla(tablero, "D",4, False)
ficha2 = Ficha("C", 5, tablero, "A")
ficha3 = Ficha("E", 3, tablero, "A")


resultFicha = ficha.anadir_ficha()
print(resultFicha)
ficha2.anadir_ficha()
ficha3.anadir_ficha()

muralla.anadir_muralla()
muralla2.anadir_muralla()


print()
###  4 Validar malos movimientos

# Ficha o muralla donde ya gat uno
ficha4 = Ficha("A", 3, tablero, "B")
muralla4 = Muralla(tablero, "D",4, False)
muralla4.anadir_muralla()

ficha4.anadir_ficha()

# Validacion de que no puede poner una ficha en los limites de otro jugador a menos de que hayan fichas en
#la fila o columna N-1: el resultado de esta prueba debe ser "no valido", ya que por defecto
# el programa asume que es un player horizontal

#Deberia no añadirse y dar mensaje de error
ficha5 = Ficha("G", 1, tablero, "B")

muralla5 = Muralla(tablero, "F",2, False)

if ficha5.anadir_ficha() != None:
    muralla5.anadir_muralla()

#Deberia  añadirse 
ficha6 = Ficha("G", 1, tablero, "B", False)

muralla6 = Muralla(tablero, "H",2, True, False)

if ficha6.anadir_ficha() != None:
    muralla6.anadir_muralla()


#Deberia  no añadirse 
ficha6 = Ficha("L", 5, tablero, "B", False)

muralla6 = Muralla(tablero, "K",6, False, False)

if ficha6.anadir_ficha() != None:
    muralla6.anadir_muralla()


# 


# Validacion de que no se pueda poner una muralla debajo de otra muralla.


print()
tablero.mostrar_tablero()

