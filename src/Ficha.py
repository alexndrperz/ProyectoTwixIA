# ficha.py
from src.Tablero import Tablero

class Ficha:
    """
    Representa una ficha en el tablero.
    """

    def __init__(self, x: str, y: int, tablero: Tablero, simbolo_jugador: str,vertical_player = True):
        """
        Inicializa una ficha con sus coordenadas y tablero.
        - parametro x: Letra de la fila.
        - parametro y: Número de la columna.
        - parametro tablero: Objeto Tablero donde se colocará la ficha.
        """
        # print(tablero.columnas, tablero.filas)
        self.x = x
        self.idx_x =  tablero.columnas.index(y)
        self.idx_y =  tablero.filas.index(x)
        self.vertical_player =  vertical_player
        self.simbolo = f"{simbolo_jugador} "
        self.y = y
        self.tablero = tablero
        # return self.anadir_ficha()
        

    def anadir_ficha(self) -> object:
        """
        Añade la ficha al tablero usando el método recibir_pieza del tablero.
        Valida primero si la posición es correcta.
        - devuelve: El objeto retornado por el tablero si es válida, None si no se añade.
        """
        

        resultado = self.tablero.recibir_pieza(self, True, self.vertical_player, self.simbolo)
        if resultado:
            return resultado
        return None

