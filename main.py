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


tablero.mostrar_tablero()

###  4 Validar malos movimientos

#

