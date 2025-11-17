class Sala:
    def __init__(self, numero:int, capacidade:int, andar:int):
        if isinstance(numero, int):
            self.__numero = numero
        if isinstance(capacidade, int):
            self.__capacidade = capacidade
        if isinstance(andar, int):
            self.__andar = andar

    @property
    def numero(self):
        return self.__numero

    @numero.setter
    def numero(self, numero: int):
        if isinstance(numero, int):
            self.__numero = numero

    @property
    def capacidade(self):
        return self.__capacidade

    @capacidade.setter
    def capacidade(self, capacidade: int):
        if isinstance(capacidade, int):
            self.__capacidade = capacidade

    @property
    def andar(self):
        return self.__andar

    @andar.setter
    def andar(self, andar: int):
        if isinstance(andar, int):
            self.__andar = andar