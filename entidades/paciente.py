from entidades.pessoa import Pessoa

class Paciente(Pessoa):
    
    def __init__(self, nome: str, email: str, cpf: int, contato: str, data_nascimento: str, genero: str, 
                 convenio: str, deficiente: bool, tipo_sanguineo: str):
        
        super().__init__(nome, email, cpf, contato, data_nascimento, genero)
<<<<<<< Updated upstream
<<<<<<< Updated upstream
  
=======

>>>>>>> Stashed changes
=======

>>>>>>> Stashed changes
        if isinstance(convenio, str):
            self.__convenio = convenio
        if isinstance(deficiente, bool):
            self.__deficiente = deficiente
        if isinstance(tipo_sanguineo, str):
            self.__tipo_sanguineo = tipo_sanguineo

    @property
    def convenio(self):
        return self.__convenio

    @convenio.setter
    def convenio(self, convenio: str):
        if isinstance(convenio, str):
            self.__convenio = convenio

    @property
    def deficiente(self):
        return self.__deficiente

    @deficiente.setter
    def deficiente(self, deficiente: bool):
        if isinstance(deficiente, bool):
            self.__deficiente = deficiente

    @property
    def tipo_sanguineo(self):
        return self.__tipo_sanguineo

    @tipo_sanguineo.setter
    def tipo_sanguineo(self, tipo_sanguineo: str):
        if isinstance(tipo_sanguineo, str):
<<<<<<< Updated upstream
<<<<<<< Updated upstream
            self.__tipo_sanguineo = tipo_sanguineo
=======
            self.__tipo_sanguineo = tipo_sanguineo
>>>>>>> Stashed changes
=======
            self.__tipo_sanguineo = tipo_sanguineo
>>>>>>> Stashed changes
