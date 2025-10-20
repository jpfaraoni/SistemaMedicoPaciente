from limite.tela_sistema import TelaSistema
from controle.controlador_pacientes import ControladorPacientes

class ControladorSistema:

    def __init__(self):
        self.__controlador_pacientes = ControladorPacientes(self)
        self.__tela_sistema = TelaSistema()

    def inicializa_sistema(self):
        self.abre_tela()

    def cadastra_paciente(self):
        self.__controlador_pacientes.abre_tela()

    def encerra_sistema(self):
        exit(0)

    def abre_tela(self):
        lista_opcoes = {1: self.cadastra_paciente,
                        0: self.encerra_sistema}

        while True:
            opcao_escolhida = self.__tela_sistema.tela_opcoes()
            funcao_escolhida = lista_opcoes[opcao_escolhida]
            funcao_escolhida()