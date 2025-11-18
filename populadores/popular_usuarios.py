#!/usr/bin/env python3
"""
Script para popular o arquivo usuarios.pkl com usuários iniciais
(Secretaria, Pacientes e Médicos) para o sistema de login.
"""

import hashlib
from entidades.usuario import Usuario
from DAO.usuario_dao import UsuarioDAO

# IMPORTANTE: Esta constante DEVE ser idêntica à definida em
# controle/controlador_sistema.py
APP_SECRET_PEPPER = "meu_projeto_didatico_super_secreto"

def __hash_senha(senha: str) -> str:
    """
    Cria um hash SHA256 da senha com um pepper.
    (CÓPIA EXATA do método em ControladorSistema)
    """
    senha_com_pepper = senha.encode('utf-8') + APP_SECRET_PEPPER.encode('utf-8')
    hash_obj = hashlib.sha256(senha_com_pepper)
    return hash_obj.hexdigest()

def popular_usuarios():
    """
    Função principal para criar e salvar os usuários iniciais.
    """
    print("=== Populando arquivo usuarios.pkl ===")
    print("Criando usuários de login (Secretaria, Pacientes, Médicos)...")
    
    dao = UsuarioDAO()
    
    # (login, senha_pura, tipo_usuario, id_entidade)
    # Use os CPFs e CRMs dos seus outros scripts de população
    usuarios_a_criar = [
        # Secretaria (login coringa, id_entidade pode ser 0 ou None)
        ("secretaria", "admin123", "secretaria", 0),
        
        # Pacientes (login=cpf_str, id_entidade=cpf_int)
        ("11122233344", "paciente1", "paciente", 11122233344),
        ("22233344455", "paciente2", "paciente", 22233344455),
        ("33344455566", "paciente3", "paciente", 33344455566),
        
        # Medicos (login=crm_str, id_entidade=crm_int)
        ("12345", "medico1", "medico", 12345),
        ("12346", "medico2", "medico", 12346),
    ]
    
    usuarios_criados = 0
    try:
        for login, senha_pura, tipo, id_entidade in usuarios_a_criar:
            if dao.get(login) is None: # Verifica se já não existe
                # Criptografa a senha pura
                senha_hash = __hash_senha(senha_pura)
                
                # Cria a entidade Usuario
                novo_usuario = Usuario(login, senha_hash, tipo, id_entidade)
                
                # Salva no usuarios.pkl
                dao.add(novo_usuario)
                usuarios_criados += 1
                print(f"Usuário '{login}' ({tipo}) criado com sucesso.")
            else:
                print(f"Usuário '{login}' já existe.")
        
        if usuarios_criados > 0:
            print(f"\n✅ Sucesso! {usuarios_criados} usuários foram criados e salvos em usuarios.pkl")
        else:
            print("\nℹ️  Todos os usuários de exemplo já existem no arquivo usuarios.pkl")

    except Exception as e:
        print(f"\n❌ Erro ao popular usuários: {e}")
    
    return usuarios_criados

# Permite que o script seja executado sozinho
if __name__ == "__main__":
    popular_usuarios()