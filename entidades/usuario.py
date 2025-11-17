class Usuario:
    def __init__(self, login: str, senha_hash: str, tipo_usuario: str, id_entidade: int):
        self.__login = login
        self.__senha_hash = senha_hash
        self.__tipo_usuario = tipo_usuario
        self.__id_entidade = id_entidade

    @property
    def login(self):
        return self.__login
    
    @property
    def senha_hash(self):
        return self.__senha_hash
    
    @property
    def tipo_usuario(self):
        return self.__tipo_usuario
    
    @property
    def id_entidade(self):
        return self.__id_entidade