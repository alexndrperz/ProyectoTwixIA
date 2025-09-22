# juego.py
from src.Tablero import Tablero
from src.Jugador import Jugador
from src.Ficha import Ficha
from src.Muralla import Muralla


class Juego:
    """
    Controla el flujo del juego.
    """

    def __init__(self):
        """
        Inicializa el juego, crea tablero y jugadores.
        """
        self.tablero: Tablero = None
        self.jugadores: list[Jugador] = []

    def iniciar_juego(self) -> None:
        """
        Da inicio al bucle del juego, crea jugadores y tablero,
        y gestiona los turnos.
        """
        pass

    def turno_jugador(self, jugador: Jugador) -> None:
        """
        Ejecuta el turno de un jugador.
        Muestra el tablero, pregunta al usuario dónde colocar su ficha o muralla,
        y usa los métodos de Ficha y Muralla para crearlos.
        También valida si puede colocar muralla después de poner ficha.
        """
        pass

    def verificar_ganador(self) -> None:
        """
        Detecta un ganador con la propiedad is_winner del tablero.
        """
        pass
