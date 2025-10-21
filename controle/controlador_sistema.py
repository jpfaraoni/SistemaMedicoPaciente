from limite.tela_sistema import TelaSistema
from controle.controlador_pacientes import ControladorPacientes
from controle.controlador_consulta import ControladorConsultas
from controle.controlador_medicos import ControladorMedicos

class ControladorSistema:

    def __init__(self):
        self.__controlador_pacientes = ControladorPacientes(self)
        self.__controlador_consulta = ControladorConsultas(self)
        self.__controlador_medicos = ControladorMedicos(self)
        self.__tela_sistema = TelaSistema()

    @property
    def controlador_pacientes(self):
        return self.__controlador_pacientes

    @property
    def controlador_consulta(self):
        return self.__controlador_consulta

    @property
    def controlador_medicos(self):
        return self.__controlador_medicos

    def inicializa_sistema(self):
        self.abre_tela()

    def cadastra_paciente(self):
        self.__controlador_pacientes.abre_tela()

    def cadastra_consultas(self):
        self.__controlador_consulta.abre_tela()

    def cadastra_medicos(self):
        self.__controlador_medicos.menu_medicos()

    def encerra_sistema(self):
        exit(0)

    def abre_tela(self):
        lista_opcoes = {1: self.cadastra_paciente,
                        2: self.cadastra_medicos,
                        3: self.cadastra_consultas,
                        0: self.encerra_sistema}

        while True:
            opcao_escolhida = self.__tela_sistema.tela_opcoes()
            funcao_escolhida = lista_opcoes[opcao_escolhida]
            funcao_escolhida()