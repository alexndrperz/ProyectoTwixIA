# jugador.py
from src.Ficha import Ficha
from src.Muralla import Muralla


class Jugador:
    """
    Representa un jugador del juego.
    """

    def __init__(self, nombre: str, jugador_id: str):
        """
        Inicializa un jugador.
        - parametro nombre: Nombre del jugador.
        - parametro jugador_id: ID del jugador (A o B).
        """
        self.nombre = nombre
        self.jugador_id = jugador_id
        self.fichas: list[Ficha] = []
        self.murallas: list[Muralla] = []
        self.is_winner: bool = False
