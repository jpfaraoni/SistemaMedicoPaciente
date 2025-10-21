from entidades.paciente import Paciente
from entidades.medico import Medico

class Consulta:
    def __init__(self, numero: int, paciente: Paciente, medico: Medico, data: str, horario: str, sala: str):
        if isinstance(numero, int):
            self.__numero = numero
        if isinstance(paciente, Paciente):
            self.__paciente = paciente
        if isinstance(medico, Medico):
            self.__medico = medico
        if isinstance(data, str):
            self.__data = data
        if isinstance(horario, str):
            self.__horario = horario
        if isinstance(sala, str):
            self.__sala = sala

    @property
    def numero(self):
        return self.__numero

    @numero.setter
    def numero(self, numero:int):
        if isinstance(numero, int):
            self.__numero = numero

    @property
    def paciente(self):
        return self.__paciente

    @paciente.setter
    def paciente(self, paciente: Paciente):
        if isinstance(paciente, Paciente):
            self.__paciente = paciente

    @property
    def medico(self):
        return self.__medico

    @medico.setter
    def medico(self, medico: Medico):
        if isinstance(medico, Medico):
            self.__medico = medico

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data: str):
        if isinstance(data, str):
            self.__data = data

    @property
    def horario(self):
        return self.__horario

    @horario.setter
    def horario(self, horario: str):
        if isinstance(horario, str):
            self.__horario = horario

    @property
    def sala(self):
        return self.__sala

    @sala.setter
    def sala(self, sala: str):
        if isinstance(sala, str):
            self.__sala = sala