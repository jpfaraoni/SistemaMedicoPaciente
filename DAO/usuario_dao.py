from abstrato.dao import DAO
from entidades.usuario import Usuario

class UsuarioDAO(DAO):
    def __init__(self):
        super().__init__('usuarios.pkl')

    def add(self, usuario: Usuario):
        if (usuario is not None) and isinstance(usuario, Usuario) and isinstance(usuario.login, str):
            # A chave é o login do usuário
            super().add(usuario.login, usuario)

    def get(self, key_login: str):
        if isinstance(key_login, str):
            return super().get(key_login)
