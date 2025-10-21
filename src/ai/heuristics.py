from __future__ import annotations

from .state import TwixtState


def evaluate(state: TwixtState, me_is_vertical: bool) -> float:
    """Evalua heuristicas del juego para el minimax solver

    _count_pieces: Cuenta el numero de piezas que hay en el tablero para cada jugada posible
    _progress_vertical: Dice que tan cerca estas del limite ganador verticalmente(osea de poner una pieza donde tienes que ponerla para ganar)
    _progress_horizontal: Dice que tan cerca del limite ganador estas horizontalmente
    _center_control: Dice que tantas piezas tienes que controlan el centro
    _connectivity_score: Dice que tantas murallas tienes en el tablero   
    """
    if state.is_terminal():
        if state.winner_vertical is True:
            return 1e9 if me_is_vertical else -1e9
        if state.winner_vertical is False:
            return -1e9 if me_is_vertical else 1e9

    a_count, b_count = _count_pieces(state)
    prog_a = _progress_vertical(state)
    prog_b = _progress_horizontal(state)
    center_a = _center_control(state, True)
    center_b = _center_control(state, False)
    conn_a = _connectivity_score(state, True)
    conn_b = _connectivity_score(state, False)

    mob_a, mob_b = _mobility(state)

    if me_is_vertical:
        score = (
            2.0 * (prog_a - prog_b)
            + 0.5 * (a_count - b_count)
            + 0.3 * (conn_a - conn_b)
            + 0.2 * (center_a - center_b)
            + 0.15 * (_normalize_mobility(mob_a) - _normalize_mobility(mob_b))
        )
    else:
        score = (
            2.0 * (prog_b - prog_a)
            + 0.5 * (b_count - a_count)
            + 0.3 * (conn_b - conn_a)
            + 0.2 * (center_b - center_a)
            + 0.15 * (_normalize_mobility(mob_b) - _normalize_mobility(mob_a))
        )
    return float(score)


def _count_pieces(state: TwixtState) -> tuple[int, int]:
    a = 0
    b = 0
    for row in state.matrix:
        for cell in row:
            if cell == "A ":
                a += 1
            elif cell == "B ":
                b += 1
    return a, b


def _progress_vertical(state: TwixtState) -> float:
    max_row = -1
    for i, row in enumerate(state.matrix):
        if any(cell == "A " for cell in row):
            max_row = i
    if max_row < 0:
        return 0.0
    return max_row / (len(state.filas) - 1)


def _progress_horizontal(state: TwixtState) -> float:
    max_col = -1
    for row in state.matrix:
        for j, cell in enumerate(row):
            if cell == "B ":
                if j > max_col:
                    max_col = j
    if max_col < 0:
        return 0.0
    return max_col / (len(state.columnas) - 1)


def _center_control(state: TwixtState, vertical: bool) -> float:
    """Control en el centro"""
    target = "A " if vertical else "B "
    h = len(state.filas)
    w = len(state.columnas)
    cy = (h - 1) / 2.0
    cx = (w - 1) / 2.0
    total = 0.0
    cnt = 0
    for i, row in enumerate(state.matrix):
        for j, cell in enumerate(row):
            if cell == target:
                dy = abs(i - cy)
                dx = abs(j - cx)
                dist = dx + dy
                total += (1.0 / (1.0 + dist))
                cnt += 1
    return (total / max(1, cnt))


def _connectivity_score(state: TwixtState, vertical: bool) -> float:
    """Que tantas murallas tiene el player"""
    positions = state.get_piece_positions(vertical)
    pos_set = set(positions)
    offsets = [(-2, -2), (2, -2), (-2, 2), (2, 2)]
    links = 0
    for i, j in positions:
        for di, dj in offsets:
            ni, nj = i + di, j + dj
            if (ni, nj) in pos_set:
                links += 1
    return links / 2.0


def _mobility(state: TwixtState) -> tuple[int, int]:
    """Devuelve (movimientos posibles de A, B): número de jugadas legales para cada bando."""
    as_state = TwixtState(
        filas=state.filas,
        columnas=state.columnas,
        matrix=state.matrix,
        turn_is_vertical=True,
        winner_vertical=state.winner_vertical,
    )
    bs_state = TwixtState(
        filas=state.filas,
        columnas=state.columnas,
        matrix=state.matrix,
        turn_is_vertical=False,
        winner_vertical=state.winner_vertical,
    )
    return len(as_state.legal_moves()), len(bs_state.legal_moves())


def _normalize_mobility(m: int) -> float:
    """Normaliza movilidad a ~[0,1] para pesos estables (div. por tamaño típico)."""
    return min(1.0, m / 100.0)