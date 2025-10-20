class PacienteNaoEncontrado(Exception):
    def __init__(self, cpf):
        super().__init__(f"Paciente com cpf '{cpf}' não foi encontrado.")