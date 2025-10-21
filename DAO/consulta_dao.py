from abstrato.dao import DAO
from entidades.consulta import Consulta
from limite.tela_consulta import TelaConsulta
from limite.tela_sistema import TelaSistema

class ConsultaDAO(DAO):
    def __init__(self):
        super().__init__('consultas.pkl')
        self.__telaconsulta = TelaConsulta(TelaSistema)

    def add(self, consulta: Consulta):
        if isinstance(consulta.numero, int) and (consulta is not None) and isinstance(consulta, Consulta):
            super().add(consulta.numero, consulta)
        else:
            self.__telapacientes.mostra_mensagem("Erro", "Erro ao adicionar paciente.")
            return None
    
    def update(self, consulta:Consulta):
        if isinstance(consulta.numero, int) and (consulta is not None) and isinstance(consulta, Consulta):
            super().update(consulta.numero, consulta)
        else:
            self.__telaconsulta.mostra_mensagem("Erro", "Erro ao atualizar consulta.")
            return None      
    
    def get(self, cpf: int):
        if isinstance(cpf, int) and (cpf is not None):
            return super().get(cpf)
        else:
            self.__telapacientes.mostra_mensagem("Erro", "Erro ao buscar consulta.")
            return None

    def remove(self, key: int):
        if isinstance(key, int) and (key is not None):
            super().remove(key)
        else:
            self.__telaconsulta.mostra_mensagem("Erro", "Erro ao remover consulta.")
            return None