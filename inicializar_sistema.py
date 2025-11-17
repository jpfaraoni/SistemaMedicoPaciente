#!/usr/bin/env python3
"""
Script para inicializar o sistema médico.
Cria salas e médicos iniciais necessários para o funcionamento do sistema.
"""
"""
from entidades.sala import Sala
from entidades.medico import Medico

def inicializar_sistema():
    #Inicializa o sistema criando salas e médicos iniciais
    print("="*60)
    print("INICIALIZAÇÃO DO SISTEMA MÉDICO")
    print("="*60)
    
    # Primeiro, criar as salas
    print("\n1. Criando salas...")
    try:
        salas_criadas = Sala.popular_salas()
        if salas_criadas > 0:
            print(f"✅ {salas_criadas} salas criadas com sucesso!")
        else:
            print("ℹ️  Salas já existem no sistema.")
    except Exception as e:
        print(f"❌ Erro ao criar salas: {e}")
        return False
    
    # Depois, criar os médicos
    print("\n2. Criando médicos...")
    try:
        medicos_criados = Medico.popular_medicos()
        if medicos_criados > 0:
            print(f"✅ {medicos_criados} médicos criados com sucesso!")
        else:
            print("ℹ️  Médicos já existem no sistema.")
    except Exception as e:
        print(f"❌ Erro ao criar médicos: {e}")
        return False
    
    print("\n" + "="*60)
    print("✅ SISTEMA INICIALIZADO COM SUCESSO!")
    print("="*60)
    print("Agora você pode executar o sistema principal com: python main.py")
    
    return True

if __name__ == "__main__":
    inicializar_sistema()
"""
