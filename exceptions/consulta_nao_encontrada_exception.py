class ConsultaNaoEncontrada(Exception):
    def __init__(self, numero):
        super().__init__(f"Consulta número '{numero}' não foi encontrada.")