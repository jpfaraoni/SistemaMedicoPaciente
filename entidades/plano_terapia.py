from entidades.paciente import Paciente
from entidades.medico import Medico
from datetime import datetime

class PlanoDeTerapia:
    def __init__(self, 
                 id_plano: int, 
                 paciente: Paciente, 
                 medico: Medico, 
                 data_criacao: str, 
                 texto_plano: str):
        
        if isinstance(id_plano, int):
            self.__id_plano = id_plano
        if isinstance(paciente, Paciente):
            self.__paciente = paciente
        if isinstance(medico, Medico):
            self.__medico = medico
        if isinstance(data_criacao, str):
            self.__data_criacao = data_criacao
        if isinstance(texto_plano, str):
            self.__texto_plano = texto_plano

    @property
    def id_plano(self):
        return self.__id_plano

    @property
    def paciente(self):
        return self.__paciente

    @property
    def medico(self):
        return self.__medico

    @property
    def data_criacao(self):
        return self.__data_criacao

    @property
    def texto_plano(self):
        return self.__texto_plano

    @texto_plano.setter
    def texto_plano(self, texto_plano: str):
        if isinstance(texto_plano, str):
            self.__texto_plano = texto_plano