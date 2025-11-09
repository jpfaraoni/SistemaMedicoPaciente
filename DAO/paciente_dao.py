from abstrato.dao import DAO
from entidades.paciente import Paciente
from limite.tela_pacientes import TelaPacientes
from limite.tela_sistema import TelaSistema

class PacienteDAO(DAO):
    def __init__(self):
        super().__init__('pacientes.pkl')
        self.__telapacientes = TelaPacientes(TelaSistema)

    def add(self, paciente: Paciente):
        if isinstance(paciente.cpf, int) and (paciente is not None) and isinstance(paciente, Paciente):
            super().add(paciente.cpf, paciente)
        else:
            self.__telapacientes.mostra_mensagem("Erro", "Erro ao adicionar paciente.")
            return None
    
    def update(self, paciente: Paciente):
        if isinstance(paciente.cpf, int) and (paciente is not None) and isinstance(paciente, Paciente):
            super().update(paciente.cpf, paciente)
        else:
            self.__telapacientes.mostra_mensagem("Erro", "Erro ao atualizar paciente.")
            return None      
    
    def get(self, cpf: int):
        if isinstance(cpf, int) and (cpf is not None):
            return super().get(cpf)
        return None

    def remove(self, cpf: int):
        if isinstance(cpf, int) and (cpf is not None):
            super().remove(cpf)
        else:
            self.__telapacientes.mostra_mensagem("Erro", "Erro ao remover paciente.")
            return None


