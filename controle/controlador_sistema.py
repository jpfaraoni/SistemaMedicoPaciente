from limite.tela_sistema import TelaSistema
from limite.tela_login import TelaLogin
from controle.controlador_pacientes import ControladorPacientes
from controle.controlador_consulta import ControladorConsultas
from controle.controlador_medicos import ControladorMedicos
from DAO.usuario_dao import UsuarioDAO
from exceptions.cancel_op_exception import CancelOpException
import hashlib # Importe a biblioteca de hash

APP_SECRET_PEPPER = "meu_projeto_didatico_super_secreto"

class ControladorSistema:
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.__controlador_pacientes = ControladorPacientes(self)
        self.__controlador_consulta = ControladorConsultas(self)
        self.__controlador_medicos = ControladorMedicos(self)
        self.__tela_sistema = TelaSistema()
        self.__usuario_dao = UsuarioDAO()
        self.__tela_login = TelaLogin()
        self.__usuario_logado = None # Guarda quem está logado

    def autenticar(self):
        """
        Loop de login. Só sai quando o login for bem-sucedido
        ou o usuário cancelar.
        """
        while True:
            try:
                dados = self.__tela_login.pega_dados_login()
                login = dados["login"]
                senha_digitada = dados["senha"]
                usuario = self.__usuario_dao.get(login)
                if usuario is None:
                    self.__tela_login.mostra_mensagem("Erro", "Usuário não encontrado.")
                elif self.verificar_senha(senha_digitada, usuario.senha_hash):
                    self.__usuario_logado = usuario # Salva o usuário logado
                    self.__tela_login.mostra_mensagem("Sucesso", f"Bem-vindo(a), {usuario.login}!")
                    return True # Sucesso, sai do método
                else:
                    self.__tela_login.mostra_mensagem("Erro", "Senha inválida.")
            except CancelOpException:
                return False # Usuário cancelou, sinaliza para fechar
            
    def __hash_senha(self, senha: str) -> str:
        """Cria um hash SHA256 da senha com um pepper."""
        # Converte a senha e o pepper para bytes e os concatena
        senha_com_pepper = senha.encode('utf-8') + APP_SECRET_PEPPER.encode('utf-8')
        # Cria o hash
        hash_obj = hashlib.sha256(senha_com_pepper)
        # Retorna a representação hexadecimal do hash
        return hash_obj.hexdigest()
    
    def verificar_senha(self, senha_digitada: str, hash_armazenado: str) -> bool:
        """Verifica se a senha digitada corresponde ao hash salvo."""
        hash_digitado = self.__hash_senha(senha_digitada)
        return hash_digitado == hash_armazenado

    @property
    def controlador_pacientes(self):
        return self.__controlador_pacientes

    @property
    def controlador_consulta(self):
        return self.__controlador_consulta

    @property
    def controlador_medicos(self):
        return self.__controlador_medicos
    
    def inicializa_sistema(self):
        sucesso_login = self.autenticar()

        if sucesso_login:
            self.abre_tela()
        else:
            self.encerra_sistema()

    def cadastra_paciente(self):
        #self.__controlador_pacientes.abre_tela()
        if self.__usuario_logado.tipo_usuario == 'secretaria':
            self.__controlador_pacientes.abre_tela()
        elif self.__usuario_logado.tipo_usuario == 'paciente':
            # O paciente só pode editar seus próprios dados
            # (Você precisará adaptar abre_tela de ControladorPacientes)
            #self.__controlador_pacientes.abre_tela_paciente_logado(self.__usuario_logado.id_entidade)
            pass
        else:
            self.__tela_sistema.mostra_mensagem("Erro", "Acesso Negado.")

    def cadastra_consultas(self):
        #self.__controlador_consulta.abre_tela()
        if self.__usuario_logado.tipo_usuario == 'secretaria':
            self.__controlador_pacientes.abre_tela()
        elif self.__usuario_logado.tipo_usuario == 'paciente':
            # O paciente só pode editar seus próprios dados
            # (Você precisará adaptar abre_tela de ControladorPacientes)
            #self.__controlador_pacientes.abre_tela_paciente_logado(self.__usuario_logado.id_entidade)
            pass
        else:
            self.__tela_sistema.mostra_mensagem("Erro", "Acesso Negado.")

    def cadastra_medicos(self):
        #self.__controlador_medicos.abre_tela()
        if self.__usuario_logado.tipo_usuario == 'secretaria':
            self.__controlador_pacientes.abre_tela()
        elif self.__usuario_logado.tipo_usuario == 'medico':
            # O paciente só pode editar seus próprios dados
            # (Você precisará adaptar abre_tela de ControladorPacientes)
            #self.__controlador_medico.abre_tela_medico_logado(self.__usuario_logado.id_entidade)
            pass
        else:
            self.__tela_sistema.mostra_mensagem("Erro", "Acesso Negado.")

    def encerra_sistema(self):
        exit(0)

    def abre_tela(self):
        # Este é o seu método original que mostra o menu
        # Agora ele precisa montar as opções com base no usuário logado
        opcoes = {}
        if self.__usuario_logado.tipo_usuario == 'secretaria':
            opcoes = {1: self.cadastra_paciente,
                      2: self.cadastra_medicos,
                      3: self.cadastra_consultas,
                      0: self.encerra_sistema}
        elif self.__usuario_logado.tipo_usuario == 'paciente':
            opcoes = {1: self.cadastra_paciente, # (Renomear botão para "Meus Dados")
                      3: self.cadastra_consultas, # (Renomear botão para "Minhas Consultas")
                      0: self.encerra_sistema}
        elif self.__usuario_logado.tipo_usuario == 'medico':
            opcoes = {2: self.cadastra_medicos, # (Renomear botão para "Meus Dados")
                      3: self.cadastra_consultas, # (Renomear botão para "Minhas Consultas")
                      0: self.encerra_sistema}
        while True:
            # Passa o tipo de usuário para a tela poder mostrar os botões certos
            opcao_escolhida = self.__tela_sistema.tela_opcoes(self.__usuario_logado.tipo_usuario)
            funcao_escolhida = opcoes.get(opcao_escolhida)
            if funcao_escolhida:
                if funcao_escolhida == self.encerra_sistema:
                    break # Sai do loop do menu principal (e volta para o inicializa_sistema)
                funcao_escolhida()
            else:
                self.__tela_sistema.mostra_mensagem("Erro", "Opção inválida.")