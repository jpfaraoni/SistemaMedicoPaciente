#!/usr/bin/env python3
"""
Script para popular o arquivo medicos.pkl com médicos válidos.
Execute este script para criar os médicos iniciais do sistema.
"""

from entidades.medico import Medico

if __name__ == "__main__":
    print("=== Populando arquivo medicos.pkl ===")
    print("Criando médicos iniciais...\n")
    
    try:
        medicos_criados = Medico.popular_medicos()
        
        if medicos_criados > 0:
            print(f"\n✅ Sucesso! {medicos_criados} médicos foram criados e salvos em medicos.pkl")
        else:
            print("\nℹ️  Todos os médicos já existem no arquivo medicos.pkl")
            
    except Exception as e:
        print(f"\n❌ Erro ao popular médicos: {e}")
        print("Verifique se as salas foram criadas primeiro executando: python popular_salas.py")
