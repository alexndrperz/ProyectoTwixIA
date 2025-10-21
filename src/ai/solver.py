from __future__ import annotations

import time
from typing import List, Tuple

from .state import TwixtState
from .heuristics import evaluate


class MinimaxSolver:
    """Minimax con poda alfa-beta e iterative deepening por tiempo o profundidad."""

    def __init__(self, me_is_vertical: bool):
        self.me_is_vertical = me_is_vertical

    def solve(self, root_state: TwixtState, max_time_s: float = 1.0, max_depth: int = 4) -> Tuple[str, int] | None:
        deadline = time.time() + max_time_s
        best_move: Tuple[str, int] | None = None
        for depth in range(1, max_depth + 1):
            move, _ = self._search_depth(root_state, depth, float("-inf"), float("inf"), deadline)
            if move is not None:
                best_move = move
            if time.time() >= deadline:
                break
        return best_move

    def _search_depth(
        self,
        state: TwixtState,
        depth: int,
        alpha: float,
        beta: float,
        deadline: float,
    ) -> tuple[Tuple[str, int] | None, float]:
        if time.time() >= deadline or depth == 0 or state.is_terminal():
            return None, evaluate(state, self.me_is_vertical)

        is_max = (state.turn_is_vertical == self.me_is_vertical)
        best_move: Tuple[str, int] | None = None
        best_val = float("-inf") if is_max else float("inf")

        for move in self._ordered_moves(state):
            child = state.apply(move)
            _, val = self._search_depth(child, depth - 1, alpha, beta, deadline)
            if is_max:
                if val > best_val:
                    best_val = val
                    best_move = move
                if best_val > alpha:
                    alpha = best_val
            else:
                if val < best_val:
                    best_val = val
                    best_move = move
                if best_val < beta:
                    beta = best_val
            if beta <= alpha:
                break
        return best_move, best_val

    def _ordered_moves(self, state: TwixtState) -> List[Tuple[str, int]]:
        moves = state.legal_moves()
        if not moves:
            return moves

        own = set(state.get_piece_positions(state.turn_is_vertical))
        def hint(move: Tuple[str, int]) -> float:
            x, y = move
            i = state.filas.index(x)
            j = state.columnas.index(y)
            prog = i if state.turn_is_vertical else j
            near = 0.0
            for pi, pj in own:
                d = abs(pi - i) + abs(pj - j)
                if d == 0:
                    continue
                near = max(near, 1.0 / d)
            return prog + near

        return sorted(moves, key=hint, reverse=True)