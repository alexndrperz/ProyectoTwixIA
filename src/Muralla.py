# muralla.py
from src.Tablero import Tablero
from src.Ficha import Ficha


class Muralla:
    """
    Representa una muralla que conecta dos fichas.
    """

    def __init__(self, tablero: Tablero, x: str, y: int, apuntando_derecha: bool, horizontal_player = True):
        """
        Inicializa una muralla con el tablero y las dos fichas.
        - parametro tablero: Objeto Tablero.
        - parametro ficha1: Objeto Ficha 1.
        - parametro ficha2: Objeto Ficha 2.
        """
        self.tablero = tablero
        self.simbolo = "↘ " if apuntando_derecha  else "↙ "  
        self.x = x
        self.y = y
        self.horizontal_player= horizontal_player

    def anadir_muralla(self) -> bool:
        """
        Añade la muralla al tablero validando la posición con el tablero.
        Define la dirección ("/" o "\\") según la posición de las fichas.
        - devuelve: True si la muralla se añadió correctamente, False si no.
        """
        resultado = self.tablero.recibir_pieza(self, False, self.horizontal_player)
        if resultado:
            return resultado
