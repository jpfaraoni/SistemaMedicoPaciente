from abstrato.dao import DAO
from entidades.medico import Medico

class MedicoDAO(DAO):
    def __init__(self):
        super().__init__('medicos.pkl')

    def add(self, medico: Medico):
        if isinstance(medico.crm, int) and (medico is not None) and isinstance(medico, Medico):
            super().add(medico.crm, medico)

    def update(self, medico: Medico):
        if((medico is not None) and isinstance(medico, Medico) and isinstance(medico.crm, int)):
            super().update(medico.crm, medico)

    def get(self, crm: int):
        if isinstance(crm, int):
            return super().get(crm)

    def remove(self, crm: int):
        if isinstance(crm, int):
            return super().remove(crm)
