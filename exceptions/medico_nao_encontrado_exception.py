class MedicoNaoEncontrado(Exception):
    def __init__(self, crm):
        super().__init__(f"Médico com CRM '{crm}' não foi encontrado.")
