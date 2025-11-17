#!/usr/bin/env python3
"""
Script para popular o arquivo medicos.pkl com médicos válidos.
Execute este script para criar os médicos iniciais do sistema.
"""
# Imports necessários para este script
from entidades.medico import Medico
from DAO.medico_dao import MedicoDAO
from DAO.sala_dao import SalaDAO

def popular_medicos():
    """
    Função para popular o arquivo medicos.pkl com médicos válidos.
    Cria médicos com diferentes especialidades e salas.
    """
    print("=== Populando arquivo medicos.pkl ===")
    print("Criando médicos iniciais...\n")
    
    medico_dao = MedicoDAO()
    sala_dao = SalaDAO()
    
    # Lista de médicos para criar (agora com todos os campos de Pessoa)
    # (crm, nome, especialidade, exp_inicial, exp_final, num_sala, email, cpf, contato, data_nasc, genero)
    medicos_dados = [
        (12345, "Dr. João Silva", "Cardiologia", "08:00", "17:00", 101, "joao.silva@med.com", 11122233344, "4899991111", "10/01/1980", "Masculino"),
        (12346, "Dra. Maria Santos", "Pediatria", "07:00", "16:00", 102, "maria.santos@med.com", 22233344455, "4899992222", "15/05/1985", "Feminino"),
        (12347, "Dr. Pedro Costa", "Ortopedia", "09:00", "18:00", 103, "pedro.costa@med.com", 33344455566, "4899993333", "20/03/1978", "Masculino"),
        (12348, "Dra. Ana Oliveira", "Dermatologia", "08:30", "17:30", 201, "ana.oliveira@med.com", 44455566677, "4899994444", "25/11/1990", "Feminino"),
        (12349, "Dr. Carlos Lima", "Neurologia", "07:30", "16:30", 202, "carlos.lima@med.com", 55566677788, "4899995555", "30/07/1982", "Masculino"),
        (12350, "Dra. Fernanda Rocha", "Ginecologia", "08:00", "17:00", 203, "fernanda.rocha@med.com", 66677788899, "4899996666", "05/09/1988", "Feminino"),
        (12351, "Dr. Roberto Alves", "Urologia", "09:00", "18:00", 204, "roberto.alves@med.com", 77788899900, "4899997777", "12/04/1975", "Masculino"),
        (12352, "Dra. Juliana Ferreira", "Psiquiatria", "08:30", "17:30", 301, "juliana.ferreira@med.com", 88899900011, "4899998888", "18/02/1983", "Feminino"),
        (12353, "Dr. Marcos Pereira", "Cirurgia Geral", "07:00", "16:00", 302, "marcos.pereira@med.com", 99900011122, "4899999999", "22/10/1970", "Masculino"),
        (12354, "Dra. Patricia Souza", "Oftalmologia", "08:00", "17:00", 303, "patricia.souza@med.com", 12312312311, "4899990000", "08/06/1987", "Feminino"),
    ]
    
    medicos_criados = 0
    try:
        for (crm, nome, especialidade, exp_inicial, exp_final, num_sala, email, cpf, contato, data_nasc, genero) in medicos_dados:
            medico_existente = medico_dao.get(crm)
            if medico_existente is None:
                sala = sala_dao.get(num_sala)
                if sala is not None:
                    # Cria novo médico com todos os parâmetros de Pessoa e Medico
                    novo_medico = Medico(nome, email, cpf, contato, data_nasc, genero, 
                                         crm, especialidade, exp_inicial, exp_final, sala)
                    medico_dao.add(novo_medico)
                    medicos_criados += 1
                    print(f"Médico {nome} (CRM: {crm}) criado com sucesso.")
                else:
                    print(f"Sala {num_sala} não encontrada para o médico {nome}")
            else:
                print(f"Médico CRM {crm} já existe")

        if medicos_criados > 0:
            print(f"\n✅ Sucesso! {medicos_criados} médicos foram criados e salvos em medicos.pkl")
        else:
            print("\nℹ️  Todos os médicos já existem no arquivo medicos.pkl")
            
    except Exception as e:
        print(f"\n❌ Erro ao popular médicos: {e}")
        print("Verifique se as salas foram criadas primeiro.")
    
    return medicos_criados

if __name__ == "__main__":
    popular_medicos()