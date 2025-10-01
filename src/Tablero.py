import string

class Tablero:
    """
    Representa el tablero del juego.
    - Es una matriz (lista de listas) con letras para filas y números para columnas.
    """

    def __init__(self, filas=None, columnas=None):
        """
        Inicializa el tablero con las dimensiones dadas.
        """
        # Valores por defecto: tablero estándar Twixt 24x24
        if filas is None:
            filas = list(string.ascii_uppercase[:12])  # ['A','B',...,'X']
        if columnas is None:
            columnas = list(range(1, 13))  # 1 a 24

        self.filas = filas
        self.columnas = columnas 
        self.matriz = self._get_rows_columns_table(columnas, filas)
        self.winner = {"is_winner":False, "player": ""}

    def mostrar_tablero(self) -> None:
        """
        Muestra el estado actual del tablero con filas y columnas.
        """
        header = "   " + "".join([f"{c}  " for c in self.columnas])
        print(header)
        for i, fila in enumerate(self.filas):
            row = self._mostrar_fila(fila, i)

            # row = f"{fila:2} " + " ".join([cell for cell in self.matriz[i]])
            print(row)

    def validar_posicion(self, x: str, y: int, es_muralla= False, vertical_player = True, simbolo_jugador = "") -> bool:
        """
        Valida si la posición (x, y) es válida para colocar ficha o muralla.
        """

        # print(x, y, es_muralla)
        if x not in self.filas:
            # print(x, "no")
            return False
        
        if y not in self.columnas:
            # print("noy")
            return False

        
        fila_idx = self.filas.index(x)
        col_idx = self.columnas.index(y)

        casilla_ocupada = self.matriz[fila_idx][col_idx].strip() not in (None, ".", "|", "-")
        
        mensaje_muralla = ""
        mensaje_player = ""
        if(es_muralla):
            mensaje_muralla = " No se puede añadir una muralla:"

        mensaje_player = "jugador horizontal" if vertical_player else "jugador vertical"

        if casilla_ocupada:
            print(f"{x}{y}:{mensaje_muralla} La casilla ya esta ocupada")
            return False
        
        limite_correcto = self.validar_si_limite_correcto(col_idx, fila_idx, vertical_player)
        if not limite_correcto:
            print(f"{x}{y}:{mensaje_muralla} Usted no es un {mensaje_player}, no puede añadir una ficha en ese limite a menos de que este proximo a ganar")
            return False
        
        if  fila_idx == len(self.filas)-1:
            ficha_en_otro_extremo_no_valida = not self.validar_ficha_en_extremo_ganador(vertical_player, es_muralla, col_idx, fila_idx,simbolo_jugador, x, y)
            if ficha_en_otro_extremo_no_valida:
                return False
        # return self.matriz[fila_idx][col_idx] is None
        return True
    

    def validar_ficha_en_extremo_ganador(self, vertical_player, es_muralla, idx_x, idx_y, simbolo_jugador, x,y):
        if vertical_player:
            idx_ficha_a_izquierda =idx_x - 2 
            idx_ficha_a_derecha =idx_x + 2 
            coleccion_a_evaluar = self.matriz[len(self.filas)-3] 
            result_derecha = False
            result_izquierda = False
            if idx_ficha_a_derecha < len(coleccion_a_evaluar):
                result_derecha =  coleccion_a_evaluar[idx_ficha_a_derecha] == simbolo_jugador
            if idx_ficha_a_izquierda >= 0:
                print(coleccion_a_evaluar[idx_ficha_a_izquierda], idx_x)
                result_izquierda=  coleccion_a_evaluar[idx_ficha_a_izquierda] == simbolo_jugador

            if not result_derecha and not result_izquierda:
                print(f"{x}{y}: La ficha que intento poner en la fila L no se puede añadir ya que no hay ninguna ficha ni a derecha ni a izquierda en la fila J")
                return False 
            else:
                return True
        
        else:
            print(self.columnas)

     
    """ Validacion de que no puede poner una ficha
      en los limites de otro jugador a menos de que 
      hayan fichas en la fila o columna N-1, """
    def validar_si_limite_correcto(self, idx_x, idx_y, horizontal_player:bool) -> bool:
        if horizontal_player: 
            if idx_y > 0 and (idx_x == 0 or idx_x == len(self.columnas) - 1):
                return False
        else:
            # print(idx_y, idxz_x)
            if idx_x > 0 and (idx_y == 0 or idx_y == len(self.filas) - 1):
                return False
        return True

        

    def recibir_pieza(self, pieza, es_ficha, horizontal_player:bool, simbolo_jugador="") -> None:
        """
        Recibe una pieza (ficha o muralla) para añadirla al tablero.
        """
        # print(pieza)
        if self.validar_posicion(pieza.x, pieza.y,not es_ficha,horizontal_player, simbolo_jugador ):

            fila_idx = self.filas.index(pieza.x)
            col_idx = self.columnas.index(pieza.y)
            self.matriz[fila_idx][col_idx] = pieza.simbolo
            if col_idx == len(self.columnas)-1: 
                self.winner["is_winner"] = True
                self.winner["player"] = "B"

            if fila_idx == len(self.filas)-1: 
                self.winner["is_winner"] = True
                self.winner["player"] = "A"
            return {"x_index":col_idx, "y_index":fila_idx}
    
    
    def _mostrar_fila(self, fila, index):
        filaStr = f"{fila:2} " + " ".join([cell for cell in self.matriz[index]])
        return filaStr
    

    def _get_rows_columns_table(self, columnas, filas):
        matriz = [[". " for _ in columnas] for _ in filas]
        for i in range(len(matriz)): 
            fila = matriz[i]
        
            if i != 0 and i != len(matriz) -1:
                fila[1] = "| "
                fila[len(fila)-2] = "| "
            
            if i == 1 or i == len(matriz) - 2:
                for iFila in range(len(fila)):
                    if iFila > 0 and iFila < len(fila) -1:
                        fila[iFila]= "- " 
        
        return matriz