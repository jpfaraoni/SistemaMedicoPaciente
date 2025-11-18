from abc import ABC, abstractmethod
from datetime import datetime


class Pessoa(ABC):
    @abstractmethod
    def __init__(self, nome: str, email: str, cpf: int, contato: str, data_nascimento: str, genero: str):
        if isinstance(nome, str):
            self.__nome = nome
        if isinstance(email, str):
            self.__email = email
        if isinstance(cpf, int):
            self.__cpf = cpf
        if isinstance(contato, str):
            self.__contato = contato
        if isinstance(data_nascimento, str):
            self.__data_nascimento = data_nascimento
        if isinstance(genero, str):
            self.__genero = genero

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        if isinstance(nome, str):
            self.__nome = nome

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email: str):
        if isinstance(email, str):
            self.__email = email

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf: int):
        if isinstance(cpf, int):
            self.__cpf = cpf

    @property
    def contato(self):
        return self.__contato

    @contato.setter
    def contato(self, contato: str):
        if isinstance(contato, str):
            self.__contato = contato

    @property
    def data_nascimento(self):
        return self.__data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, data_nascimento: str):
        if isinstance(data_nascimento, str):
            self.__data_nascimento = data_nascimento

    @property
    def genero(self):
        return self.__genero

    @genero.setter
    def genero(self, genero: str):
        if isinstance(genero, str):
            self.__genero = genero

    @property
    def idade(self) -> int:
        """
        Calcula a idade dinamicamente a partir da data de nascimento.
        Retorna 0 se a data de nascimento for inválida.
        """
        try:
            nascimento = datetime.strptime(self.data_nascimento, "%d/%m/%Y").date()
            hoje = datetime.today().date()
            

            idade_calculada = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
            return idade_calculada
        except (ValueError, TypeError):
            return 0