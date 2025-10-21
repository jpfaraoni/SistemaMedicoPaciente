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

    @staticmethod
    def popular_salas():
        """
        Função estática para popular o arquivo salas.pkl com salas válidas.
        Cria salas em diferentes andares com capacidades variadas.
        """
        from DAO.sala_dao import SalaDAO
        
        sala_dao = SalaDAO()
        
        # Lista de salas para criar
        salas_dados = [
            # Andar 1 - Consultórios gerais
            (101, 2, 1),  # (numero, capacidade, andar)
            (102, 2, 1),
            (103, 2, 1),
            (104, 2, 1),
            
            # Andar 2 - Especialidades
            (201, 3, 2),
            (202, 3, 2),
            (203, 2, 2),
            (204, 2, 2),
            
            # Andar 3 - Cirurgias e procedimentos
            (301, 4, 3),
            (302, 4, 3),
            (303, 3, 3),
            
            # Andar 4 - Emergência
            (401, 5, 4),
            (402, 5, 4),
        ]
        
        salas_criadas = 0
        for numero, capacidade, andar in salas_dados:
            try:
                # Verifica se a sala já existe
                sala_existente = sala_dao.get(numero)
                if sala_existente is None:
                    # Cria nova sala
                    nova_sala = Sala(numero, capacidade, andar)
                    sala_dao.add(nova_sala)
                    salas_criadas += 1
                    print(f"Sala {numero} criada com sucesso (Andar {andar}, Capacidade: {capacidade})")
                else:
                    print(f"Sala {numero} já existe")
            except Exception as e:
                print(f"Erro ao criar sala {numero}: {e}")
        
        print(f"\nTotal de salas criadas: {salas_criadas}")
        return salas_criadas

    def __str__(self):
        return f"Sala {self.__numero} - Andar {self.__andar} (Capacidade: {self.__capacidade})"