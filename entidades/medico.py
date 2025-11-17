from entidades.pessoa import Pessoa
from entidades.sala import Sala

class Medico(Pessoa):
    
    def __init__(self, 
                 nome: str, email: str, cpf: int, contato: str, data_nascimento: str, genero: str, 
                 crm: int, especialidade: str, expediente_inicial: str, expediente_final: str, sala: Sala):
        
        super().__init__(nome, email, cpf, contato, data_nascimento, genero)

        if isinstance(crm, int):
            self.__crm = crm
        if isinstance(especialidade, str):
            self.__especialidade = especialidade
        if isinstance(expediente_inicial, str):
            self.__expediente_inicial = expediente_inicial
        if isinstance(expediente_final, str):
            self.__expediente_final = expediente_final
        if isinstance(sala, Sala):
            self.__sala = sala

    @property
    def crm(self):
        return self.__crm

    @crm.setter
    def crm(self, crm: int):
        if isinstance(crm, int):
            self.__crm = crm

    @property
    def especialidade(self):
        return self.__especialidade

    @especialidade.setter
    def especialidade(self, especialidade: str):
        if isinstance(especialidade, str):
            self.__especialidade = especialidade

    @property
    def expediente_inicial(self):
        return self.__expediente_inicial

    @expediente_inicial.setter
    def expediente_inicial(self, expediente_inicial: str):
        if isinstance(expediente_inicial, str):
            self.__expediente_inicial = expediente_inicial

    @property
    def expediente_final(self):
        return self.__expediente_final

    @expediente_final.setter
    def expediente_final(self, expediente_final: str):
        if isinstance(expediente_final, str):
            self.__expediente_final = expediente_final

    @property
    def sala(self):
        return self.__sala

    @sala.setter
    def sala(self, sala: Sala):
        if isinstance(sala, Sala):
            self.__sala = sala