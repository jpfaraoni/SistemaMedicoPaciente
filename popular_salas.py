#!/usr/bin/env python3
"""
Script para popular o arquivo salas.pkl com salas válidas.
Execute este script para criar as salas iniciais do sistema.
"""

from entidades.sala import Sala

if __name__ == "__main__":
    print("=== Populando arquivo salas.pkl ===")
    print("Criando salas para o sistema médico...\n")
    
    try:
        salas_criadas = Sala.popular_salas()
        
        if salas_criadas > 0:
            print(f"\n✅ Sucesso! {salas_criadas} salas foram criadas e salvas em salas.pkl")
        else:
            print("\nℹ️  Todas as salas já existem no arquivo salas.pkl")
            
    except Exception as e:
        print(f"\n❌ Erro ao popular salas: {e}")
        print("Verifique se todos os arquivos necessários estão presentes.")
