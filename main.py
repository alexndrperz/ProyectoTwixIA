"""Punto de entrada del juego TWIXT en consola.

Este módulo inicializa el ciclo principal del juego utilizando la clase `Juego`.
"""
from src.Juego import Juego


def main() -> None:
    """Ejecuta el juego TWIXT en la consola con manejo básico de errores."""
    try:
        juego = Juego()
        juego.iniciar_juego()
    except KeyboardInterrupt:
        print("\nJuego interrumpido por el usuario.")
    except Exception:
        # Mantener mensaje amigable; no exponer stack trace al usuario final
        print("\nOcurrió un error inesperado. Intenta nuevamente.")


if __name__ == "__main__":
    main()