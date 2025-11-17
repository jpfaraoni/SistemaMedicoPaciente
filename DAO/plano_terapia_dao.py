# Arquivo: DAO/plano_terapia_dao.py

from abstrato.dao import DAO
from entidades.plano_terapia import PlanoDeTerapia

class PlanoDeTerapiaDAO(DAO):
    def __init__(self):
        super().__init__('planos.pkl')

    def add(self, plano: PlanoDeTerapia):
        if (plano is not None) and isinstance(plano, PlanoDeTerapia) and isinstance(plano.id_plano, int):
            # A chave de persistência será o ID do plano
            super().add(plano.id_plano, plano)

    def update(self, plano: PlanoDeTerapia):
        if (plano is not None) and isinstance(plano, PlanoDeTerapia) and isinstance(plano.id_plano, int):
            super().update(plano.id_plano, plano)
    
    def get(self, key_id_plano: int):
        if isinstance(key_id_plano, int):
            return super().get(key_id_plano)

    def remove(self, key_id_plano: int):
        if isinstance(key_id_plano, int):
            return super().remove(key_id_plano)