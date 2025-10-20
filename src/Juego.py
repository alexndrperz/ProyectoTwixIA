# juego.py
from typing import Optional, Tuple
import string
from src.Tablero import Tablero
from src.Jugador import Jugador
from src.Ficha import Ficha
from src.Muralla import Muralla
from src.ai.state import TwixtState
from src.ai.solver import MinimaxSolver


class Juego:
    """Orquestador del flujo del juego TWIXT en consola.

    Esta clase se encarga de:
    - Crear el `Tablero` y los dos `Jugador`.
    - Gestionar el bucle principal por turnos.
    - Solicitar entradas por consola para colocar fichas o murallas.
    - Invocar a `Ficha` y `Muralla` para aplicar cambios sobre el `Tablero`.
    - Consultar `tablero.is_winner` para determinar el final de la partida.

    Notas de diseño:
    - Las validaciones de posiciones y cruces pertenecen al `Tablero` y a las
      piezas; aquí solo se maneja el flujo de interacción.
    - Tras colocar una ficha, se puede preguntar por construir una muralla si
      la función utilizada lo indica (vía un booleano retornado).
    """

    def __init__(self):
        """
        Inicializa el juego, crea tablero y jugadores.
        """
        self.tablero: Optional[Tablero] = None
        self.jugadores: list[Jugador] = []
        self.turn_index: int = 0
        self.abort_requested: bool = False
        self.restart_requested: bool = False

    def _ask_input(self, prompt: str) -> str:
        """Lee una entrada de consola no vacía.

        Args:
            prompt: Texto a mostrar al usuario.

        Returns:
            Cadena ingresada por el usuario sin espacios exteriores.

        Efectos:
            Interactúa con la consola.
        """
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("Entrada vacía. Intenta nuevamente.")

    def _ask_yes_no(self, prompt: str) -> bool:
        """Pregunta binaria (sí/no) con validación robusta.

        Args:
            prompt: Pregunta a mostrar.

        Returns:
            True si la respuesta es afirmativa, False si es negativa.

        Efectos:
            Interactúa con la consola.
        """
        while True:
            value = input(f"{prompt} [s/n]: ").strip().lower()
            if value in {"s", "si", "sí", "y", "yes"}:
                return True
            if value in {"n", "no"}:
                return False
            print("Respuesta inválida. Escribe 's' o 'n'.")

    def _ask_action(self) -> str:
        """Muestra el menú de acciones del turno y devuelve la selección.

        Returns:
            Uno de los literales: "ficha", "muralla", "pasar", "reiniciar", "salir".

        Efectos:
            Interactúa con la consola.
        """
        print("\nElige una acción:")
        print("  1) Colocar ficha")
        print("  2) Colocar muralla")
        print("  3) Pasar")
        print("  4) Reiniciar partida")
        print("  5) Salir del juego")
        while True:
            choice = input("Opción (1-5): ").strip()
            if choice == "1":
                return "ficha"
            if choice == "2":
                return "muralla"
            if choice == "3":
                return "pasar"
            if choice == "4":
                return "reiniciar"
            if choice == "5":
                return "salir"
            print("Opción inválida. Intenta nuevamente.")

    def _ask_letter(self, prompt: str) -> str:
        """Solicita una letra de fila válida según el tablero actual.

        Args:
            prompt: Texto a mostrar al usuario.

        Returns:
            Letra de fila válida.

        Raises:
            AssertionError: Si el tablero no ha sido inicializado.
        """
        assert self.tablero is not None, "El tablero no está inicializado"
        valid_letters = {letter.upper() for letter in self.tablero.filas}
        while True:
            value = input(prompt).strip().upper()
            if value in valid_letters:
                return value
            print(f"Fila inválida. Debe ser una de: {sorted(valid_letters)}")

    def _ask_int(self, prompt: str) -> int:
        """Solicita un entero de columna válido según el tablero actual.

        Args:
            prompt: Texto a mostrar al usuario.

        Returns:
            Número de columna válido.

        Raises:
            AssertionError: Si el tablero no ha sido inicializado.
        """
        assert self.tablero is not None, "El tablero no está inicializado"
        valid_columns = set(self.tablero.columnas)
        while True:
            raw = input(prompt).strip()
            if raw.isdigit():
                value = int(raw)
                if value in valid_columns:
                    return value
            print(f"Columna inválida. Debe ser una de: {sorted(valid_columns)}")

    def _list_player_pieces(self, jugador: Jugador) -> None:
        """Muestra las fichas del jugador con índice y coordenadas.

        Args:
            jugador: Jugador cuyas fichas serán listadas.

        Efectos:
            Interactúa con la consola.
        """
        if not jugador.pieces:
            print("(Sin fichas aún)")
            return
        for idx, piece in enumerate(jugador.pieces, start=1):
            print(f"  {idx}) ({piece.x}, {piece.y})")

    def _choose_two_fichas_for_wall(
        self, jugador: Jugador, prefer_include: Optional[Ficha] = None
    ) -> Tuple[Ficha, Ficha]:
        """Selecciona dos fichas del jugador para construir una muralla.

        Args:
            jugador: Dueño de las fichas.
            prefer_include: Ficha a priorizar (por ejemplo, la recién colocada).

        Returns:
            Tupla con dos fichas distintas (f1, f2).

        Raises:
            AssertionError: Si el jugador no tiene al menos dos fichas.

        Efectos:
            Interactúa con la consola.
        """
        assert len(jugador.pieces) >= 2, "Se requieren al menos dos fichas"
        pieces = list(jugador.pieces)

        def ask_index(prompt: str) -> int:
            while True:
                raw = input(prompt).strip()
                if raw.isdigit():
                    idx = int(raw)
                    if 1 <= idx <= len(pieces):
                        return idx
                print("Índice inválido. Intenta nuevamente.")

        print("\nSelecciona dos fichas para la muralla:")
        self._list_player_pieces(jugador)

        if prefer_include is not None and prefer_include in pieces:
            idx1 = pieces.index(prefer_include) + 1
            print(f"Preseleccionada la ficha recién colocada como Ficha 1: {idx1}")
        else:
            idx1 = ask_index("Número de Ficha 1: ")
        while True:
            idx2 = ask_index("Número de Ficha 2: ")
            if idx2 != idx1:
                break
            print("Debes elegir dos fichas distintas.")
        return pieces[idx1 - 1], pieces[idx2 - 1]

    def iniciar_juego(self) -> None:
        """Inicializa tablero y jugadores y ejecuta el bucle de turnos.

        Flujo general:
        - Construye el tablero.
        - Solicita nombres para Jugador A y B.
        - Alterna turnos hasta que `tablero.winner["is_winner"]` sea verdadero.

        Efectos:
            Interactúa con la consola, crea estado de juego en memoria.
        """
        print("\nBienvenido a TWIXT\n")

        filas = list(string.ascii_uppercase[:20])
        columnas = list(range(1, 21))
        self.tablero = Tablero(filas, columnas)

        nombre_a = input("Nombre del Jugador A (enter para 'Jugador A'): ").strip() or "Jugador A"
        nombre_b = input("Nombre del Jugador B (enter para 'Jugador B'): ").strip() or "Jugador B"

        modo_a = input("¿Jugador A es IA? [s/n]: ").strip().lower() in {"s", "si", "sí", "y", "yes"}
        modo_b = input("¿Jugador B es IA? [s/n]: ").strip().lower() in {"s", "si", "sí", "y", "yes"}

        jugador_a = Jugador(nombre_a, "A", is_ai=modo_a)
        jugador_b = Jugador(nombre_b, "B", is_ai=modo_b)
        self.jugadores = [jugador_a, jugador_b]
        self.turn_index = 0

        assert self.tablero is not None
        while not self.tablero.winner["is_winner"]:
            if self.abort_requested:
                print("\nSaliendo del juego...")
                return
            if self.restart_requested:
                print("\nReiniciando partida...")
                self._reset_board()
                self.restart_requested = False
            jugador_actual = self.jugadores[self.turn_index]
            print(
                f"\nTurno de {jugador_actual.nombre} (Jugador {jugador_actual.player_id.value})"
            )
            if jugador_actual.is_ai:
                self.turno_ia(jugador_actual)
            else:
                self.turno_jugador(jugador_actual)
            self.verificar_ganador()
            if self.tablero.winner["is_winner"]:
                break
            self.turn_index = 1 - self.turn_index

        if self.tablero is not None:
            self.tablero.mostrar_tablero()


    def turno_jugador(self, jugador: Jugador) -> None:
        """Ejecuta el turno de un jugador.

        Detalles:
        - Muestra el tablero.
        - Permite elegir: colocar ficha, colocar muralla o pasar.
        - Si coloca ficha y la función utilizada lo permite, ofrece construir una muralla.

        Args:
            jugador: Jugador activo del turno actual.

        Efectos:
            Interactúa con la consola y modifica `jugador.fichas`, `jugador.murallas`
            y el estado del `Tablero`.
        """
        assert self.tablero is not None, "El tablero no está inicializado"
        self.tablero.mostrar_tablero()

        while True:
            action = self._ask_action()

            if action == "ficha":
                x = self._ask_letter("Fila (letra): ")
                y = self._ask_int("Columna (número): ")
                ficha = Ficha(
                    x,
                    y,
                    self.tablero,
                    jugador.symbol,
                    jugador.is_vertical_player,
                )

                result = ficha.anadir_ficha()
                ok = bool(result)
                if not ok:
                    print("No se pudo colocar la ficha. Intenta nuevamente.")
                    continue

                jugador.add_piece(ficha)
                self.tablero.mostrar_tablero()

                if len(jugador.pieces) >= 2:
                    if self._ask_yes_no("¿Deseas añadir una muralla ahora?"):
                        f1, f2 = self._choose_two_fichas_for_wall(
                            jugador, prefer_include=ficha
                        )
                        muralla = Muralla(
                            self.tablero, f1, f2, horizontal_player=jugador.is_vertical_player
                        )
                        try:
                            if muralla.anadir_muralla():
                                jugador.add_wall(muralla)
                                self.tablero.mostrar_tablero()
                            else:
                                print("Muralla inválida. No se añadió.")
                        except AttributeError:
                            print("Muralla inválida. No se añadió.")
                return

            if action == "muralla":
                if len(jugador.pieces) < 2:
                    print("Necesitas al menos dos fichas para construir una muralla.")
                    continue
                f1, f2 = self._choose_two_fichas_for_wall(jugador)
                muralla = Muralla(
                    self.tablero, f1, f2, horizontal_player=jugador.is_vertical_player
                )
                try:
                    if muralla.anadir_muralla():
                        jugador.add_wall(muralla)
                        self.tablero.mostrar_tablero()
                        return
                    else:
                        print("Muralla inválida. Intenta nuevamente.")
                        continue
                except AttributeError:
                    print("Muralla inválida. Intenta nuevamente.")
                    continue

            if action == "reiniciar":
                self.restart_requested = True
                return

            if action == "salir":
                self.abort_requested = True
                return

            return

    def turno_ia(self, jugador: Jugador) -> None:
        """Turno de IA usando Minimax con alfa-beta."""
        assert self.tablero is not None, "El tablero no está inicializado"
        self.tablero.mostrar_tablero()
        print("IA pensando...")

        # Construir estado desde tablero
        turn_is_vertical = jugador.is_vertical_player
        state = TwixtState.from_tablero(self.tablero, turn_is_vertical)
        solver = MinimaxSolver(me_is_vertical=turn_is_vertical)
        move = solver.solve(state, max_time_s=1.0, max_depth=4)

        if move is None:
            print("IA pasa (sin jugadas).")
            return

        x, y = move
        ficha = Ficha(
            x,
            y,
            self.tablero,
            jugador.symbol,
            jugador.is_vertical_player,
        )
        result = ficha.anadir_ficha()
        ok = bool(result)
        if ok:
            jugador.add_piece(ficha)
            print(f"IA juega {x}{y}")
            self.tablero.mostrar_tablero()
            # Intento opcional de añadir una muralla útil usando la ficha recién puesta
            try:
                if len(jugador.pieces) >= 2:
                    # Prioriza muralla con la pieza más cercana en salto de caballo
                    reciente = ficha
                    mejor = None
                    mejor_dist = 1e9
                    for otra in jugador.pieces:
                        if otra is reciente:
                            continue
                        di = abs(otra.idx_y - reciente.idx_y)
                        dj = abs(otra.idx_x - reciente.idx_x)
                        if (di, dj) in {(2, 2)}:
                            d = di + dj
                            if d < mejor_dist:
                                mejor = otra
                                mejor_dist = d
                    if mejor is not None:
                        muralla = Muralla(self.tablero, reciente, mejor, horizontal_player=jugador.is_vertical_player)
                        if muralla and muralla.anadir_muralla():
                            jugador.add_wall(muralla)
                            print("IA añade una muralla")
                            self.tablero.mostrar_tablero()
            except AttributeError:
                pass
        else:
            print("IA no pudo colocar ficha; pasa.")

        # Si durante el turno humano se marcó reinicio/salida, respétalo
        if self.restart_requested or self.abort_requested:
            return

    def verificar_ganador(self) -> None:
        """Verifica condición de victoria y anuncia al ganador.

        Efectos:
            Si `tablero.is_winner` es verdadero, marca `jugador.is_winner = True`
            para el jugador que realizó la última acción y muestra un mensaje.
        """
        if self.tablero is None:
            return
        if self.tablero.winner["is_winner"]:
            winner_id = str(self.tablero.winner.get("player", "")).upper()
            ganador = next(
                (j for j in self.jugadores if j.player_id.value == winner_id),
                self.jugadores[self.turn_index],
            )
            ganador.mark_as_winner()
            print(
                f"\n¡{ganador.nombre} (Jugador {ganador.player_id.value}) ha ganado!"
            )

    # --- Utilidades de control ---
    def _reset_board(self) -> None:
        """Reinicia el estado del tablero y limpia piezas/murallas de jugadores."""
        filas = list(string.ascii_uppercase[:20])
        columnas = list(range(1, 21))
        self.tablero = Tablero(filas, columnas)
        for j in self.jugadores:
            j.clear_all_pieces()
            j.is_winner = False
        self.turn_index = 0
