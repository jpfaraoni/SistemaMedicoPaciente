#!/usr/bin/env python3
"""
Script para popular o arquivo salas.pkl com salas válidas.
Execute este script para criar as salas iniciais do sistema.
"""
# Imports necessários para este script
from entidades.sala import Sala
from DAO.sala_dao import SalaDAO

def popular_salas():
    """
    Função para popular o arquivo salas.pkl com salas válidas.
    Cria salas em diferentes andares com capacidades variadas.
    """
    print("=== Populando arquivo salas.pkl ===")
    print("Criando salas para o sistema médico...\n")
    
    sala_dao = SalaDAO()
    
    # Lista de salas para criar
    salas_dados = [
        # Andar 1 - Consultórios gerais
        (101, 2, 1),  # (numero, capacidade, andar)
        (102, 2, 1),
        (103, 2, 1),
        (104, 2, 1),
        
        # Andar 2 - Especialidades
        (201, 3, 2),
        (202, 3, 2),
        (203, 2, 2),
        (204, 2, 2),
        
        # Andar 3 - Cirurgias e procedimentos
        (301, 4, 3),
        (302, 4, 3),
        (303, 3, 3),
        
        # Andar 4 - Emergência
        (401, 5, 4),
        (402, 5, 4),
    ]
    
    salas_criadas = 0
    try:
        for numero, capacidade, andar in salas_dados:
            # Verifica se a sala já existe
            sala_existente = sala_dao.get(numero)
            if sala_existente is None:
                # Cria nova sala
                nova_sala = Sala(numero, capacidade, andar)
                sala_dao.add(nova_sala)
                salas_criadas += 1
                print(f"Sala {numero} criada com sucesso (Andar {andar}, Capacidade: {capacidade})")
            else:
                print(f"Sala {numero} já existe")
        
        if salas_criadas > 0:
            print(f"\n✅ Sucesso! {salas_criadas} salas foram criadas e salvas em salas.pkl")
        else:
            print("\nℹ️  Todas as salas já existem no arquivo salas.pkl")
            
    except Exception as e:
        print(f"\n❌ Erro ao popular salas: {e}")
        print("Verifique se todos os arquivos necessários estão presentes.")
    
    return salas_criadas

if __name__ == "__main__":
    popular_salas()