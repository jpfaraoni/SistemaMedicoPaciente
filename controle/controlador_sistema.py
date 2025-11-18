from limite.tela_sistema import TelaSistema
from controle.controlador_pacientes import ControladorPacientes
from controle.controlador_consulta import ControladorConsultas
from controle.controlador_medicos import ControladorMedicos
from controle.controlador_plano_terapia import ControladorPlanoTerapia
import hashlib
from DAO.usuario_dao import UsuarioDAO
from limite.tela_login import TelaLogin
from exceptions.cancel_op_exception import CancelOpException

APP_SECRET_PEPPER = "meu_projeto_didatico_super_secreto"


class ControladorSistema:
    """Fachada principal: centraliza controladores e expõe uma interface única ao main."""

    def __init__(self):
        self.__controlador_pacientes = ControladorPacientes(self)
        self.__controlador_consulta = ControladorConsultas(self)
        self.__controlador_medicos = ControladorMedicos(self)
        self.__controlador_plano_terapia = ControladorPlanoTerapia(self)
        self.__tela_sistema = TelaSistema()
        self.__usuario_dao = UsuarioDAO()
        self.__tela_login = TelaLogin()
        self.__usuario_logado = None

    def __hash_senha(self, senha: str) -> str:
        senha_com_pepper = senha.encode('utf-8') + APP_SECRET_PEPPER.encode('utf-8')
        hash_obj = hashlib.sha256(senha_com_pepper)
        return hash_obj.hexdigest()

    def verificar_senha(self, senha_digitada: str, hash_armazenado: str) -> bool:
        hash_digitado = self.__hash_senha(senha_digitada)
        return hash_digitado == hash_armazenado

    def autenticar(self):
        while True:
            try:
                dados = self.__tela_login.pega_dados_login()
                login = dados["login"]
                senha_digitada = dados["senha"]

                usuario = self.__usuario_dao.get(login)

                if usuario is None:
                    self.__tela_login.mostra_mensagem("Erro", "Usuário não encontrado.")
                elif self.verificar_senha(senha_digitada, usuario.senha_hash):
                    self.__usuario_logado = usuario
                    self.__tela_login.mostra_mensagem("Sucesso", f"Bem-vindo(a), {usuario.login}!")
                    return True
                else:
                    self.__tela_login.mostra_mensagem("Erro", "Senha inválida.")
            
            except CancelOpException:
                return False

    @property
    def controlador_pacientes(self):
        return self.__controlador_pacientes

    @property
    def controlador_consulta(self):
        return self.__controlador_consulta

    @property
    def controlador_medicos(self):
        return self.__controlador_medicos

    @property
    def controlador_plano_terapia(self):
        return self.__controlador_plano_terapia

    @property
    def usuario_logado(self):
        return self.__usuario_logado

    def inicializa_sistema(self):
        while True:
            sucesso_login = self.autenticar()
            if sucesso_login:
                self.abre_tela()
            else:
                self.encerra_sistema()
                break

    def cadastra_paciente(self):
        self.__controlador_pacientes.abre_tela()

    def cadastra_consultas(self):
        self.__controlador_consulta.abre_tela()

    def cadastra_medicos(self):
        self.__controlador_medicos.abre_tela()

    def gerenciar_planos_terapia(self):
        self.__controlador_plano_terapia.abre_tela()

    def encerra_sistema(self):
        exit(0)

    def fazer_logout(self):
        return

    def abre_tela(self):
        while True:
            opcoes = {}
            if self.__usuario_logado.tipo_usuario == 'secretaria':
                opcoes = {1: self.cadastra_paciente,
                          2: self.cadastra_medicos,
                          3: self.cadastra_consultas,
                          0: self.fazer_logout}
            
            elif self.__usuario_logado.tipo_usuario == 'paciente':
                opcoes = {1: self.cadastra_paciente,
                          3: self.cadastra_consultas,
                          4: self.gerenciar_planos_terapia, # Paciente pode ver
                          0: self.fazer_logout}

            elif self.__usuario_logado.tipo_usuario == 'medico':
                opcoes = {2: self.cadastra_medicos,
                          3: self.cadastra_consultas,
                          4: self.gerenciar_planos_terapia, # Médico pode criar/ver
                          0: self.fazer_logout}

            opcoes_disponiveis = list[int](opcoes.keys())
            opcao_escolhida = self.__tela_sistema.tela_opcoes(self.__usuario_logado.tipo_usuario, opcoes_disponiveis)
            
            funcao_escolhida = opcoes.get(opcao_escolhida)
            
            if funcao_escolhida:
                if funcao_escolhida == self.fazer_logout:
                    self.__usuario_logado = None
                    break
                funcao_escolhida()
            else:
                self.__tela_sistema.mostra_mensagem("Erro", "Opção inválida.")