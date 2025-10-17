from enum import Enum
from typing import Any

from src.Ficha import Ficha
from src.Muralla import Muralla
from src.Tablero import Tablero


class PlayerID(Enum):
    """Identifica el tipo de jugador en el juego TWIXT."""

    A = "A"  # Jugador vertical
    B = "B"  # Jugador horizontal


class Jugador:
    """
    Representa un jugador del juego TWIXT.

    Cada jugador tiene un objetivo específico:
    - Jugador A (vertical): Conectar la fila superior con la fila inferior
    - Jugador B (horizontal): Conectar la columna izquierda con la columna derecha

    Attributes:
        nombre: Nombre del jugador.
        player_id: Identificador del jugador (A o B).
        pieces: Lista de fichas colocadas por el jugador.
        walls: Lista de murallas construidas por el jugador.
        is_winner: Indica si el jugador ha ganado.
        is_vertical_player: True si es jugador vertical (A), False si es horizontal (B).
        symbol: Símbolo usado para representar al jugador en el tablero.
    """

    MIN_PIECES_FOR_WALL = 2  # Mínimo de fichas necesarias para construir muralla

    def __init__(self, nombre: str, jugador_id: str):
        """
        Inicializa un jugador del juego TWIXT.

        Args:
            nombre: Nombre del jugador.
            jugador_id: ID del jugador ('A' o 'B').

        Raises:
            ValueError: Si jugador_id no es 'A' o 'B'.
        """
        player_id_upper = jugador_id.upper()
        if player_id_upper not in ["A", "B"]:
            raise ValueError(f"jugador_id debe ser 'A' o 'B', recibido: {jugador_id}")

        self.nombre = nombre
        self.player_id = PlayerID(player_id_upper)
        self.pieces: list[Ficha] = []
        self.walls: list[Muralla] = []
        self.is_winner: bool = False
        self.is_first_play:bool = len(self.pieces) == 0 
        self.is_vertical_player: bool = self.player_id == PlayerID.A
        self.symbol: str = f"{self.player_id.value} "

    def add_piece(self, ficha: Ficha) -> bool:
        """
        Añade una ficha a la colección del jugador.

        Args:
            ficha: Ficha a añadir.

        Returns:
            True si la ficha se añadió correctamente, False si ya existe.
        """
        if ficha not in self.pieces:
            self.pieces.append(ficha)
            return True
        return False

    def add_wall(self, muralla: Muralla) -> bool:
        """
        Añade una muralla a la colección del jugador.

        Args:
            muralla: Muralla a añadir.

        Returns:
            True si la muralla se añadió correctamente, False si ya existe.
        """
        if muralla not in self.walls:
            self.walls.append(muralla)
            return True
        return False

    def can_place_piece_on_border(self, x: str, y: int, tablero: Tablero) -> bool:
        """
        Valida si el jugador puede colocar una ficha en los bordes del tablero.

        Según las reglas de TWIXT:
        - Jugador vertical (A) no puede colocar en bordes horizontales (izquierda/derecha)
        - Jugador horizontal (B) no puede colocar en bordes verticales (arriba/abajo)

        Args:
            x: Coordenada x (fila).
            y: Coordenada y (columna).
            tablero: Tablero del juego.

        Returns:
            True si puede colocar la ficha en esa posición.
        """
        if x not in tablero.filas or y not in tablero.columnas:
            return False

        fila_idx = tablero.filas.index(x)
        col_idx = tablero.columnas.index(y)

        # Jugador vertical (A) no puede colocar en los límites horizontales
        if self.is_vertical_player:
            if col_idx == 0 or col_idx == len(tablero.columnas) - 1:
                return False
        # Jugador horizontal (B) no puede colocar en los límites verticales
        else:
            if fila_idx == 0 or fila_idx == len(tablero.filas) - 1:
                return False

        return True

    def has_enough_pieces_for_wall(self) -> bool:
        """
        Verifica si el jugador tiene fichas suficientes para construir una muralla.

        Returns:
            True si tiene al menos MIN_PIECES_FOR_WALL fichas.
        """
        return len(self.pieces) >= self.MIN_PIECES_FOR_WALL

    def get_pieces_by_position(self, x: str, y: int) -> list[Ficha]:
        """
        Obtiene todas las fichas del jugador en una posición específica.

        Args:
            x: Coordenada x (fila).
            y: Coordenada y (columna).

        Returns:
            Lista de fichas en esa posición.
        """
        return [piece for piece in self.pieces if piece.x == x and piece.y == y]

    def get_pieces_by_row(self, fila: str) -> list[Ficha]:
        """
        Obtiene todas las fichas del jugador en una fila específica.

        Args:
            fila: Fila a buscar.

        Returns:
            Lista de fichas en esa fila.
        """
        return [piece for piece in self.pieces if piece.x == fila]

    def get_pieces_by_column(self, columna: int) -> list[Ficha]:
        """
        Obtiene todas las fichas del jugador en una columna específica.

        Args:
            columna: Columna a buscar.

        Returns:
            Lista de fichas en esa columna.
        """
        return [piece for piece in self.pieces if piece.y == columna]

    def count_pieces(self) -> int:
        """
        Cuenta el número total de fichas del jugador.

        Returns:
            Número de fichas.
        """
        return len(self.pieces)

    def count_walls(self) -> int:
        """
        Cuenta el número total de murallas del jugador.

        Returns:
            Número de murallas.
        """
        return len(self.walls)

    def clear_all_pieces(self) -> None:
        """
        Limpia todas las fichas y murallas del jugador.

        Útil para reiniciar una partida o resetear el estado del jugador.
        """
        self.pieces.clear()
        self.walls.clear()

    def mark_as_winner(self) -> None:
        """Marca al jugador como ganador de la partida."""
        self.is_winner = True

    def check_is_winner(self) -> bool:
        """
        Verifica si el jugador ha ganado la partida.

        Returns:
            True si el jugador es ganador, False en caso contrario.
        """
        return self.is_winner

    def get_player_info(self) -> dict[str, Any]:
        """
        Obtiene información completa del jugador.

        Returns:
            Diccionario con toda la información del jugador:
            - nombre: Nombre del jugador
            - player_id: ID del jugador (A o B)
            - is_vertical: Si es jugador vertical
            - symbol: Símbolo del jugador
            - pieces: Número de fichas
            - walls: Número de murallas
            - is_winner: Si es ganador
        """
        return {
            "nombre": self.nombre,
            "player_id": self.player_id.value,
            "is_vertical": self.is_vertical_player,
            "symbol": self.symbol,
            "pieces": len(self.pieces),
            "walls": len(self.walls),
            "is_winner": self.is_winner,
        }

    def __str__(self) -> str:
        """
        Representación legible del jugador para mostrar en consola.

        Returns:
            String con información básica del jugador.
        """
        return (
            f"{self.nombre} (Jugador {self.player_id.value}) - "
            f"Fichas: {len(self.pieces)}, Murallas: {len(self.walls)}"
        )

    def __repr__(self) -> str:
        """
        Representación técnica del jugador para debugging.

        Returns:
            String técnico del jugador.
        """
        return f"Jugador(nombre='{self.nombre}', player_id='{self.player_id.value}')"
