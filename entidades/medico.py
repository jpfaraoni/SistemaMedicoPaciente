from entidades.sala import Sala

class Medico:
    def __init__(self, crm: int, nome: str, especialidade: str, expediente_inicial: str, expediente_final: str, sala: Sala):
        if isinstance(crm, int):
            self.__crm = crm
        if isinstance(nome, str):
            self.__nome = nome
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
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        if isinstance(nome, str):
            self.__nome = nome

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

    @staticmethod
    def popular_medicos():
        """
        Função estática para popular o arquivo medicos.pkl com médicos válidos.
        Cria médicos com diferentes especialidades e salas.
        """
        from DAO.medico_dao import MedicoDAO
        from DAO.sala_dao import SalaDAO
        
        medico_dao = MedicoDAO()
        sala_dao = SalaDAO()
        
        # Lista de médicos para criar
        medicos_dados = [
            # (crm, nome, especialidade, expediente_inicial, expediente_final, numero_sala)
            (12345, "Dr. João Silva", "Cardiologia", "08:00", "17:00", 101),
            (12346, "Dra. Maria Santos", "Pediatria", "07:00", "16:00", 102),
            (12347, "Dr. Pedro Costa", "Ortopedia", "09:00", "18:00", 103),
            (12348, "Dra. Ana Oliveira", "Dermatologia", "08:30", "17:30", 201),
            (12349, "Dr. Carlos Lima", "Neurologia", "07:30", "16:30", 202),
            (12350, "Dra. Fernanda Rocha", "Ginecologia", "08:00", "17:00", 203),
            (12351, "Dr. Roberto Alves", "Urologia", "09:00", "18:00", 204),
            (12352, "Dra. Juliana Ferreira", "Psiquiatria", "08:30", "17:30", 301),
            (12353, "Dr. Marcos Pereira", "Cirurgia Geral", "07:00", "16:00", 302),
            (12354, "Dra. Patricia Souza", "Oftalmologia", "08:00", "17:00", 303),
        ]
        
        medicos_criados = 0
        for crm, nome, especialidade, expediente_inicial, expediente_final, numero_sala in medicos_dados:
            try:
                # Verifica se o médico já existe
                medico_existente = medico_dao.get(crm)
                if medico_existente is None:
                    # Busca a sala pelo número
                    sala = sala_dao.get(numero_sala)
                    if sala is not None:
                        # Cria novo médico
                        novo_medico = Medico(crm, nome, especialidade, expediente_inicial, expediente_final, sala)
                        medico_dao.add(novo_medico)
                        medicos_criados += 1
                        print(f"Médico {nome} (CRM: {crm}) criado com sucesso - {especialidade} - Sala {numero_sala}")
                    else:
                        print(f"Sala {numero_sala} não encontrada para o médico {nome}")
                else:
                    print(f"Médico CRM {crm} já existe")
            except Exception as e:
                print(f"Erro ao criar médico {nome}: {e}")
        
        print(f"\nTotal de médicos criados: {medicos_criados}")
        return medicos_criados

    def __str__(self):
        return f"Dr(a). {self.__nome} - CRM: {self.__crm} - {self.__especialidade} - Sala {self.__sala.numero}"
