#!/usr/bin/env python3
"""
Script para popular o arquivo pacientes.pkl com pacientes válidos.
Execute este script para criar os pacientes iniciais do sistema.
"""
# Imports necessários para este script
from entidades.paciente import Paciente
from DAO.paciente_dao import PacienteDAO

def popular_pacientes():
    """
    Função para popular o arquivo pacientes.pkl com pacientes válidos.
    Cria pacientes com dados fictícios.
    """
    print("=== Populando arquivo pacientes.pkl ===")
    print("Criando pacientes para o sistema médico...\n")
    
    paciente_dao = PacienteDAO()
    
    # Lista de pacientes para criar (com todos os atributos de Pessoa e Paciente)
    # (nome, email, cpf, contato, data_nasc, genero, convenio, deficiente, tipo_sanguineo)
    pacientes_dados = [
        ("João da Silva", "joao.silva@email.com", 11122233344, "48988887777", "10/05/1985", "Masculino", "Unimed", False, "O+"),
        ("Maria Oliveira", "maria.oliveira@email.com", 22233344455, "48977776666", "22/09/1990", "Feminino", "Bradesco Saúde", False, "A-"),
        ("Carlos Pereira", "carlos.pereira@email.com", 33344455566, "48966665555", "15/02/2000", "Masculino", "SUS", True, "B+"),
        ("Ana Souza", "ana.souza@email.com", 44455566677, "48955554444", "30/11/1995", "Feminino", "Unimed", False, "AB+"),
    ]
    
    pacientes_criados = 0
    try:
        for (nome, email, cpf, contato, data_nasc, genero, convenio, deficiente, tipo_s) in pacientes_dados:
            # Verifica se o paciente já existe
            paciente_existente = paciente_dao.get(cpf)
            if paciente_existente is None:
                # Cria novo paciente
                novo_paciente = Paciente(nome, email, cpf, contato, data_nasc, genero, convenio, deficiente, tipo_s)
                paciente_dao.add(novo_paciente)
                pacientes_criados += 1
                print(f"Paciente {nome} (CPF: {cpf}) criado com sucesso.")
            else:
                print(f"Paciente CPF {cpf} já existe")
        
        if pacientes_criados > 0:
            print(f"\n✅ Sucesso! {pacientes_criados} pacientes foram criados e salvos em pacientes.pkl")
        else:
            print("\nℹ️  Todos os pacientes de exemplo já existem no arquivo pacientes.pkl")
            
    except Exception as e:
        print(f"\n❌ Erro ao popular pacientes: {e}")
        print("Verifique se todos os arquivos necessários estão presentes.")
    
    return pacientes_criados

if __name__ == "__main__":
    popular_pacientes()