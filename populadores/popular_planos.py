#!/usr/bin/env python3
"""
Script para popular o arquivo planos.pkl com planos de terapia iniciais.
"""
from entidades.plano_terapia import PlanoDeTerapia
from DAO.plano_terapia_dao import PlanoDeTerapiaDAO
from DAO.paciente_dao import PacienteDAO
from DAO.medico_dao import MedicoDAO
from random import randint
from datetime import datetime

def popular_planos():
    print("=== Populando arquivo planos.pkl ===")
    
    plano_dao = PlanoDeTerapiaDAO()
    paciente_dao = PacienteDAO()
    medico_dao = MedicoDAO()
    
    planos_criados = 0
    try:
        # Pega o primeiro paciente e médico (com base nos seus scripts anteriores)
        paciente = paciente_dao.get(11122233344) # Paciente "João da Silva"
        medico = medico_dao.get(12345)           # Medico "Dr. João Silva"

        if paciente and medico:
            id_plano_1 = 1001
            if plano_dao.get(id_plano_1) is None:
                texto_1 = "Paciente deve continuar com a medicação atual (Aspirina 100mg/dia).\nRecomenda-se caminhada leve 3x por semana, 30 minutos.\nEvitar alimentos gordurosos e reduzir o consumo de sal.\nRetornar em 3 meses para exames de acompanhamento."
                plano_1 = PlanoDeTerapia(id_plano_1, paciente, medico, "15/11/2025", texto_1)
                plano_dao.add(plano_1)
                planos_criados += 1
                print(f"Plano {id_plano_1} criado para {paciente.nome}.")

            id_plano_2 = 1002
            paciente_2 = paciente_dao.get(44455566677) # Paciente "Ana Souza"
            medico_2 = medico_dao.get(12348)          # Medico "Dra. Ana Oliveira"
            
            if paciente_2 and medico_2 and plano_dao.get(id_plano_2) is None:
                texto_2 = "Uso contínuo de protetor solar fator 50+.\nHidratação da pele com creme à base de ureia 2x ao dia.\nEvitar exposição solar direta entre 10h e 16h.\nRetorno em 6 meses para reavaliação de manchas."
                plano_2 = PlanoDeTerapia(id_plano_2, paciente_2, medico_2, "10/11/2025", texto_2)
                plano_dao.add(plano_2)
                planos_criados += 1
                print(f"Plano {id_plano_2} criado para {paciente_2.nome}.")

        else:
            print("Não foi possível criar planos. Pacientes ou Médicos de exemplo não encontrados.")

        if planos_criados > 0:
            print(f"\n✅ Sucesso! {planos_criados} planos foram criados e salvos em planos.pkl")
        else:
            print("\nℹ️  Todos os planos de exemplo já existem no arquivo planos.pkl")
            
    except Exception as e:
        print(f"\n❌ Erro ao popular planos: {e}")
    
    return planos_criados

if __name__ == "__main__":
    popular_planos()