#!/usr/bin/env python3
"""
Script para inicializar o sistema médico.
Cria salas, pacientes, médicos e usuários iniciais.
"""

# Importa as FUNÇÕES de população dos outros scripts
from popular_salas import popular_salas
from popular_pacientes import popular_pacientes
from popular_medicos import popular_medicos
from popular_usuarios import popular_usuarios
from popular_planos import popular_planos # <-- 1. IMPORTAR A NOVA FUNÇÃO

def inicializar_sistema():
    """Inicializa o sistema chamando os populadores em ordem."""
    print("="*60)
    print("INICIALIZAÇÃO DO SISTEMA MÉDICO")
    print("="*60)
    
    # 1. Criar as salas (dependência para médicos)
    print("\n--- 1. Criando Salas ---")
    try:
        popular_salas()
    except Exception as e:
        print(f"❌ Erro fatal ao criar salas: {e}")
        return False
    
    # 2. Criar os pacientes (dependência para usuários)
    print("\n--- 2. Criando Pacientes ---")
    try:
        popular_pacientes()
    except Exception as e:
        print(f"❌ Erro fatal ao criar pacientes: {e}")
        return False
    
    # 3. Criar os médicos (depende das salas, dependência para usuários)
    print("\n--- 3. Criando Médicos ---")
    try:
        popular_medicos()
    except Exception as e:
        print(f"❌ Erro fatal ao criar médicos: {e}")
        return False
    
    # 4. Criar os usuários (depende dos pacientes e médicos existirem)
    print("\n--- 4. Criando Usuários (Login) ---") # <-- 2. ADICIONAR ESTE PASSO
    try:
        popular_usuarios()
    except Exception as e:
        print(f"❌ Erro fatal ao criar usuários: {e}")
        return False

    print("\n--- 4. Criando Planos de Terapia ---") # 2. ADICIONAR ESTE PASSO
    try:
        popular_planos()
    except Exception as e:
        print(f"❌ Erro fatal ao criar planos: {e}")
        return False
    
    
    print("\n" + "="*60)
    print("✅ SISTEMA INICIALIZADO COM SUCESSO!")
    print("="*60)
    print("Agora você pode executar o sistema principal com: python main.py")
    
    return True

if __name__ == "__main__":
    inicializar_sistema()