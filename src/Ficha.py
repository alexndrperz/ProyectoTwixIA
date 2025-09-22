# ficha.py
from src.Tablero import Tablero

class Ficha:
    """
    Representa una ficha en el tablero.
    """

    def __init__(self, x: str, y: int, tablero: Tablero):
        """
        Inicializa una ficha con sus coordenadas y tablero.
        - parametro x: Letra de la fila.
        - parametro y: Número de la columna.
        - parametro tablero: Objeto Tablero donde se colocará la ficha.
        """
        self.x = x
        self.y = y
        self.tablero = tablero

    def anadir_ficha(self) -> object:
        """
        Añade la ficha al tablero usando el método recibir_pieza del tablero.
        Valida primero si la posición es correcta.
        - devuelve: El objeto retornado por el tablero si es válida, None si no se añade.
        """
        pass
