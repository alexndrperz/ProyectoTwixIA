# muralla.py
from src.Tablero import Tablero
from src.Ficha import Ficha


class Muralla:
    """
    Representa una muralla que conecta dos fichas.
    """

    def __init__(self, tablero: Tablero, ficha1: Ficha, ficha2: Ficha):
        """
        Inicializa una muralla con el tablero y las dos fichas.
        - parametro tablero: Objeto Tablero.
        - parametro ficha1: Objeto Ficha 1.
        - parametro ficha2: Objeto Ficha 2.
        """
        self.tablero = tablero
        self.ficha1 = ficha1
        self.ficha2 = ficha2

    def anadir_muralla(self) -> bool:
        """
        Añade la muralla al tablero validando la posición con el tablero.
        Define la dirección ("/" o "\\") según la posición de las fichas.
        - devuelve: True si la muralla se añadió correctamente, False si no.
        """
        pass
