from controle.controlador_sistema import ControladorSistema


def main():
    """Ponto de entrada que delega toda a orquestração para a fachada ControladorSistema."""
    ControladorSistema().inicializa_sistema()


if __name__ == "__main__":
    main()