# 📟 TWIXT en Consola

## 📲 Descripción
Este proyecto implementa el juego TWIXT 100% en consola, utilizando caracteres ASCII para representar el tablero, las fichas (postes) y las murallas (conexiones). El objetivo es conectar los lados opuestos del tablero, respetando las reglas del juego.

El juego se ejecuta en Python y renderiza el tablero en texto, permitiendo colocar fichas, construir murallas válidas y detectar automáticamente la condición de victoria. Incluye además un modo de juego contra una IA basada en Minimax con poda alfa‑beta.

✨ Características:
- ✅ Gestión de Fichas y Murallas – Colocación de postes y construcción de murallas siguiendo las reglas de TWIXT.
- ✅ Render ASCII en Consola – Tablero con filas y columnas; murallas dibujadas con caracteres diagonales.
- ✅ Validaciones de Reglas – Prevención de posiciones inválidas y cruces ilegales; turnos alternos.
- ✅ Detección de Ganador – Verificación automática de la conexión ganadora.
- ✅ Modo IA – Opción de jugar contra la computadora (Minimax con poda alfa‑beta e iterative deepening).

Es el primer examen parcial de la materia de Inteligencia Artificial impartida por el profesor **Carlos Bienvenido Ogando Montas**.

## 🧠 IA: Minimax con poda alfa‑beta
La IA usa un estado inmutable del tablero y una heurística rápida para evaluar posiciones, buscando con Minimax y poda alfa‑beta. Se emplea iterative deepening (aumentando la profundidad hasta agotar un tiempo objetivo).

- Estado (`src/ai/state.py`):
  - `TwixtState` captura una vista inmutable del tablero, el turno y el posible ganador.
  - Genera jugadas legales enfocadas: aperturas en el borde permitido y saltos tipo “caballo” (±2, ±2), que son los que permiten puentes/murallas legales en TWIXT.

- Heurística (`src/ai/heuristics.py`): combina componentes simples y eficientes:
  - Progreso hacia el objetivo propio vs rival.
  - Diferencia de número de piezas colocadas.
  - Control de centro (distancia Manhattan inversa al centro).
  - Conectividad por saltos (enlaces potenciales a salto de “caballo”).
  - Movilidad (cantidad de jugadas legales disponibles por bando), normalizada.

- Búsqueda (`src/ai/solver.py`):
  - Minimax con poda alfa‑beta y ordenamiento de jugadas.
  - Iterative deepening por tiempo o profundidad: por defecto, 1 segundo y profundidad máxima 4.

### Profundidad y nodos expandidos
- Profundidad: número de medias‑jugadas (plies) que la IA mira hacia adelante desde el estado actual. Cuando la profundidad llega a 0 (o el estado es terminal/vence el tiempo), se evalúa la posición con la heurística.
- Nodos expandidos: estados a los que se les generan sucesores durante la búsqueda (cada vez que se listan jugadas y se aplican para explorar los hijos).

## 👤 Autores
- Equipo (5 participantes):
- **Christian Gil** – **2012-1036**
- **Omar Martinez** – **2021-0806**
- **Jeison Rosario** – **2023-1046**
- **Lesley Peguero** – **2023-1591**
- **Alan Perez** - **2023-1069**
## 📸 Capturas de Pantalla
A continuación, se muestran capturas del juego ejecutándose en consola:

1. ![Captura 1](/imgs/img1.png)
2. ![Captura 2](/imgs/img2.png)

## 🚀 Instrucciones de Uso
1. 🛠️ Clona este repositorio.
```bash
   git clone https://github.com/alexndrperz/ProyectoTwixIA.git
   ```
2. Ejecuta `python main.py` en tu terminal (Python 3.12+ recomendado).

### Jugar contra la IA
Al iniciar una partida, el sistema pregunta si cada jugador será IA:
- Responde “s” para activar IA en Jugador A (vertical) y/o Jugador B (horizontal).
- En el turno de IA, el agente elige una jugada automáticamente y, si es posible, añade una muralla útil.

### Parámetros de la IA
Los parámetros por defecto están en `src/ai/solver.py`:
- Tiempo por movimiento: `max_time_s = 1.0`
- Profundidad máxima: `max_depth = 4`
Puedes ajustarlos en la llamada a `solve` dentro de `src/Juego.py` si deseas que la IA piense más tiempo o explore más profundo.

## ⚙️ Requisitos
- Python 3.12+
- No requiere dependencias externas para ejecutar el juego en consola.

## 🗂️ Estructura del Proyecto (resumen)
- `main.py`: punto de entrada.
- `src/Tablero.py`: tablero y validaciones de posiciones/murallas.
- `src/Juego.py`: orquestación del flujo del juego y turnos (humano/IA).
- `src/Jugador.py`: modelo de jugador, fichas y murallas propias.
- `src/Ficha.py`, `src/Muralla.py`: piezas del juego y lógica de colocación.
- `src/ai/state.py`: estado inmutable para búsqueda (jugadas legales y transición).
- `src/ai/heuristics.py`: función de evaluación heurística.
- `src/ai/solver.py`: Minimax con alfa‑beta e iterative deepening.

## 🚀 Tecnologías Utilizadas
![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 🙏 Créditos
Esta tarea fue desarrollada como parte de la materia de Inteligencia Artificial impartida por el profesor **Carlos Bienvenido Ogando Montas**.

## 📄 Licencia
Este proyecto se distribuye bajo una licencia propietaria (uso restringido). Para utilizarlo o explotarlo comercialmente, debe obtenerse autorización previa y por escrito del titular.


