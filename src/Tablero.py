
class Tablero:
    """
    Representa el tablero del juego.
    - Es una matriz (lista de listas) con letras para filas y números para columnas.
    """

    def __init__(self, filas, columnas):
        """
        Inicializa el tablero con las dimensiones dadas.
        - parametro filas: Lista de letras que representan las filas.
        - parametro columnas: Lista de números que representan las columnas.
        """
        self.filas = filas
        self.columnas = columnas
        self.matriz = []  # Aquí irá la representación interna del tablero
        self.is_winner = False  # Propiedad para indicar si hay ganador en el tablero

    def mostrar_tablero(self) -> None:
        """
        Muestra el estado actual del tablero con filas y columnas.
        """
        pass

    def recibir_pieza(self, pieza) -> None:
        """
        Recibe una pieza (ficha o muralla) para añadirla al tablero.
        - parametro pieza: Objeto Ficha o Muralla.
        """
        pass

    def validar_posicion(self, x: str, y: int) -> bool:
        """
        Valida si la posición (x, y) es válida para colocar ficha o muralla.
        Además, devuelve si hay una ficha cerca (cuando se añade ficha).
        - parametro x: Letra de la fila.
        - parametro y: Número de la columna.
        - devuelve: True si la posición es válida, False si no.
        """
        pass
