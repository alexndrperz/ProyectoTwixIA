from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple


EMPTY_MARKS = {None, ".", "|", "-"}


@dataclass(frozen=True)
class TwixtState:
    """Estado inmutable para búsqueda Minimax en Twixt.

    Atributos:
        filas: Etiquetas de filas (letras).
        columnas: Etiquetas de columnas (números).
        matrix: Matriz de strings (por ejemplo ". ", "A ", "B ", "| ", "- ").
        turn_is_vertical: True si juega A (vertical), False si juega B (horizontal).
        winner_vertical: True si A ganó; False si B ganó; None si no terminal.
    """

    filas: List[str]
    columnas: List[int]
    matrix: List[List[str]]
    turn_is_vertical: bool
    winner_vertical: bool | None = None

    @staticmethod
    def from_tablero(tablero, turn_is_vertical: bool) -> "TwixtState":
        """Crea un estado desde un `Tablero` actual sin efectos secundarios."""
        matrix_copy = [row[:] for row in tablero.matriz]
        player = tablero.winner.get("player")
        winner_vertical = True if player == "A" else False if player == "B" else None
        return TwixtState(
            filas=list(tablero.filas),
            columnas=list(tablero.columnas),
            matrix=matrix_copy,
            turn_is_vertical=turn_is_vertical,
            winner_vertical=winner_vertical,
        )

    def is_terminal(self) -> bool:
        """Indica si el estado es terminal (algún jugador ganó)."""
        return self.winner_vertical is not None

    def legal_moves(self) -> List[Tuple[str, int]]:
        """Genera jugadas legales enfocadas: aperturas y saltos tipo caballo."""
        focused = self._focused_moves()
        if focused:
            return focused
        # Fallback amplio si no hay candidatos
        moves: List[Tuple[str, int]] = []
        for x in self.filas:
            for y in self.columnas:
                if self._is_legal_cell(x, y, self.turn_is_vertical):
                    moves.append((x, y))
        return moves

    def apply(self, move: Tuple[str, int]) -> "TwixtState":
        """Aplica la jugada devolviendo un nuevo estado actualizado."""
        x, y = move
        i = self.filas.index(x)
        j = self.columnas.index(y)

        next_matrix = [row[:] for row in self.matrix]
        symbol = "A " if self.turn_is_vertical else "B "
        next_matrix[i][j] = symbol

        winner_vertical: bool | None = None
        if j == len(self.columnas) - 1:
            winner_vertical = False
        if i == len(self.filas) - 1:
            winner_vertical = True

        return TwixtState(
            filas=self.filas,
            columnas=self.columnas,
            matrix=next_matrix,
            turn_is_vertical=not self.turn_is_vertical,
            winner_vertical=winner_vertical,
        )

    # --- Utilidades internas ---
    def _is_inside(self, x: str, y: int) -> bool:
        return x in self.filas and y in self.columnas

    def _is_empty(self, i: int, j: int) -> bool:
        return self.matrix[i][j].strip() in EMPTY_MARKS

    def _is_legal_cell(self, x: str, y: int, vertical_player: bool) -> bool:
        if not self._is_inside(x, y):
            return False
        i = self.filas.index(x)
        j = self.columnas.index(y)
        if not self._is_empty(i, j):
            return False
        # Bordes según reglas actuales del Tablero
        if vertical_player:
            if i > 0 and (j == 0 or j == len(self.columnas) - 1):
                return False
        else:
            if j > 0 and (i == 0 or i == len(self.filas) - 1):
                return False
        # Extremos ganadores: requiere “apoyo” a distancia 2
        if i == len(self.filas) - 1 and vertical_player:
            row_before = self.matrix[len(self.filas) - 3]
            left_idx = j - 2
            right_idx = j + 2
            left_ok = left_idx >= 0 and row_before[left_idx] == "A "
            right_ok = right_idx < len(row_before) and row_before[right_idx] == "A "
            if not (left_ok or right_ok):
                return False
        if j == len(self.columnas) - 1 and (not vertical_player):
            col_before: List[str] = [row[len(row) - 3] for row in self.matrix]
            up_idx = i - 2
            down_idx = i + 2
            up_ok = up_idx > 0 and col_before[up_idx] == "B "
            down_ok = down_idx < len(col_before) and col_before[down_idx] == "B "
            if not (up_ok or down_ok):
                return False
        return True

    def get_piece_positions(self, for_vertical: bool) -> List[Tuple[int, int]]:
        """Devuelve coordenadas (i, j) de piezas del jugador indicado."""
        want = "A " if for_vertical else "B "
        pos: List[Tuple[int, int]] = []
        for i, row in enumerate(self.matrix):
            for j, cell in enumerate(row):
                if cell == want:
                    pos.append((i, j))
        return pos

    def _focused_moves(self) -> List[Tuple[str, int]]:
        """Devuelve jugadas candidatas: aperturas o saltos de caballo desde piezas propias."""
        candidates: list[Tuple[str, int]] = []
        own_positions = self.get_piece_positions(self.turn_is_vertical)
        # Aperturas: primera fila o primera columna según bando si aún no hay piezas
        if not own_positions:
            if self.turn_is_vertical:
                x = self.filas[0]
                for y in self.columnas:
                    if self._is_legal_cell(x, y, True):
                        candidates.append((x, y))
            else:
                y = self.columnas[0]
                for x in self.filas:
                    if self._is_legal_cell(x, y, False):
                        candidates.append((x, y))
            return candidates

        # Saltos tipo caballo (±2, ±2) que son los que permiten puentes legales
        offsets = [(-2, -2), (2, -2), (-2, 2), (2, 2)]
        for i, j in own_positions:
            for di, dj in offsets:
                ni, nj = i + di, j + dj
                if 0 <= ni < len(self.filas) and 0 <= nj < len(self.columnas):
                    x = self.filas[ni]
                    y = self.columnas[nj]
                    if self._is_legal_cell(x, y, self.turn_is_vertical):
                        candidates.append((x, y))

        # Quitar duplicados preservando orden
        seen: set[Tuple[str, int]] = set()
        unique: list[Tuple[str, int]] = []
        for m in candidates:
            if m not in seen:
                seen.add(m)
                unique.append(m)
        return unique