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
        self.is_winner = False

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

    def validar_posicion(self, x: str, y: int) -> bool:
        """
        Valida si la posición (x, y) es válida para colocar ficha o muralla.
        """


        if x not in self.filas:
            print(self.filas)
            return False
        
        if y not in self.columnas:
            print(self.columnas)
            return False

        
        fila_idx = self.filas.index(x)
        col_idx = self.columnas.index(y)

        casilla_ocupada = self.matriz[fila_idx][col_idx] not in [".", "|", "-"]
        
        if casilla_ocupada:
            return False
        
        # return self.matriz[fila_idx][col_idx] is None
        return True

    def recibir_pieza(self, pieza, es_ficha) -> None:
        """
        Recibe una pieza (ficha o muralla) para añadirla al tablero.
        """
        if self.validar_posicion(pieza.x, pieza.y):
            fila_idx = self.filas.index(pieza.x)
            col_idx = self.columnas.index(pieza.y)
            self.matriz[fila_idx][col_idx] = pieza.simbolo
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