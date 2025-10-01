# muralla.py
from src.Tablero import Tablero
from src.Ficha import Ficha


class Muralla:
    """
    Representa una muralla que conecta dos fichas.
    """

    def __init__(self, tablero: Tablero,ficha1:Ficha,ficha2:Ficha, horizontal_player = True):
        """
        Inicializa una muralla con el tablero y las dos fichas.
        - parametro tablero: Objeto Tablero.
        - parametro ficha1: Objeto Ficha 1.
        - parametro ficha2: Objeto Ficha 2.
        """
        x, y, apuntando_derecha = self.anadir_muralla_usando_fichas(ficha1, ficha2)
        if x == None:
            print(f"La muralla {ficha1.x}{ficha1.y} con {ficha2.x}{ficha2.y} puede ponerse porque las murallas no estan alineadas diagonalmente dejando un espacio de un punto")
            return None
        # print(y)

        self.tablero = tablero
        self.simbolo = "↘ " if apuntando_derecha  else "↙ "  
        self.x = tablero.filas[y] if y < len(tablero.filas) else -1
        self.y =  tablero.columnas[x] if x < len(tablero.columnas) else -1
        self.horizontal_player= horizontal_player
        # self.anadir_muralla()

    def anadir_muralla_usando_fichas(self, ficha1:Ficha, ficha2:Ficha):
        apuntando_derecha = False
       
        ficha2_abajo_derecha = (ficha2.idx_x == ficha1.idx_x + 2) and (ficha2.idx_y == ficha1.idx_y +2)
        ficha2_abajo_izquierda = (ficha2.idx_x == ficha1.idx_x - 2) and (ficha2.idx_y == ficha1.idx_y +2)
        ficha2_arriba_derecha = (ficha2.idx_x == ficha1.idx_x +2) and (ficha2.idx_y == ficha1.idx_y -2)
        ficha2_arriba_izquierda = (ficha2.idx_x == ficha1.idx_x - 2) and (ficha2.idx_y == ficha1.idx_y -2)
        
        if(ficha2_arriba_izquierda or ficha2_abajo_izquierda):
            apuntando_derecha = False

            if(ficha2_arriba_izquierda):
                return (ficha1.idx_x -1,ficha1.idx_y -1 , apuntando_derecha)
            if(ficha2_abajo_izquierda):
                return (ficha1.idx_x -1,ficha1.idx_y +1 , apuntando_derecha)
        
        if(ficha2_arriba_derecha or ficha2_abajo_derecha):
            apuntando_derecha = True

            if(ficha2_arriba_derecha):
                return (ficha1.idx_x +1,ficha1.idx_y -1 , apuntando_derecha)
            if(ficha2_abajo_derecha):
                # print("2222")
                return (ficha1.idx_x +1,ficha1.idx_y +1 , apuntando_derecha)
        
        # print(ficha2_abajo_derecha, ficha2_abajo_izquierda, ficha2_arriba_derecha, ficha2_arriba_izquierda)
        return (None, None,None)


        


    def anadir_muralla(self) -> bool:
        """
        Añade la muralla al tablero validando la posición con el tablero.
        Define la dirección ("/" o "\\") según la posición de las fichas.
        - devuelve: True si la muralla se añadió correctamente, False si no.
        """
        resultado = self.tablero.recibir_pieza(self, False, self.horizontal_player)
        
        if resultado:
            return resultado
