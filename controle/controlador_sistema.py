from limite.tela_sistema import TelaSistema
from controle.controlador_pacientes import ControladorPacientes
from controle.controlador_consulta import ControladorConsultas
from controle.controlador_medicos import ControladorMedicos
from controle.controlador_plano_terapia import ControladorPlanoTerapia
import hashlib # Importe a biblioteca de hash
from DAO.usuario_dao import UsuarioDAO
from limite.tela_login import TelaLogin
from exceptions.cancel_op_exception import CancelOpException

# Adicione uma constante "secreta" no topo do arquivo.
# Isso é o nosso "pepper" - um segredo do app.
APP_SECRET_PEPPER = "meu_projeto_didatico_super_secreto"

class ControladorSistema:

    def __init__(self):
        self.__controlador_pacientes = ControladorPacientes(self)
        self.__controlador_consulta = ControladorConsultas(self)
        self.__controlador_medicos = ControladorMedicos(self)
        self.__controlador_plano_terapia = ControladorPlanoTerapia(self)
        self.__tela_sistema = TelaSistema()
        # --- NOVOS ITENS PARA LOGIN ---
        self.__usuario_dao = UsuarioDAO()
        self.__tela_login = TelaLogin() # Você precisará criar esta classe
        self.__usuario_logado = None # Guarda quem está logado
        # --- FIM DOS NOVOS ITENS ---

    # --- NOVO MÉTODO DE HASH ---
    def __hash_senha(self, senha: str) -> str:
        """Cria um hash SHA256 da senha com um pepper."""
        # Converte a senha e o pepper para bytes e os concatena
        senha_com_pepper = senha.encode('utf-8') + APP_SECRET_PEPPER.encode('utf-8')
        # Cria o hash
        hash_obj = hashlib.sha256(senha_com_pepper)
        # Retorna a representação hexadecimal do hash
        return hash_obj.hexdigest()

    # --- NOVO MÉTODO DE VERIFICAÇÃO ---
    def verificar_senha(self, senha_digitada: str, hash_armazenado: str) -> bool:
        """Verifica se a senha digitada corresponde ao hash salvo."""
        hash_digitado = self.__hash_senha(senha_digitada)
        return hash_digitado == hash_armazenado

    # --- NOVO MÉTODO DE AUTENTICAÇÃO ---
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
        """Retorna o objeto do usuário que fez login."""
        return self.__usuario_logado
    # --- FIM DA ADIÇÃO ---

    def inicializa_sistema(self):
        # Loop principal: continua mostrando login até o usuário fechar
        while True:
            sucesso_login = self.autenticar()
            
            # Se o login for bem-sucedido, abre o menu principal
            if sucesso_login:
                self.abre_tela() # Este método agora retorna quando o usuário clica em "Sair"
                # Quando abre_tela retorna, o usuário já foi limpo pelo fazer_logout()
                # Volta para o loop e mostra o login novamente
            else:
                # Se autenticar retornar False (usuário clicou em Sair no login), encerra
                self.encerra_sistema()
                break

    def cadastra_paciente(self):
        # A lógica de permissão está em ControladorPacientes.abre_tela().
        # Nós apenas precisamos chamar esse método.
        self.__controlador_pacientes.abre_tela()

    def cadastra_consultas(self):
        # A lógica de permissão está em ControladorConsultas.abre_tela().
        # Nós apenas precisamos chamar esse método.
        self.__controlador_consulta.abre_tela()

    def cadastra_medicos(self):
        # A lógica de permissão está em ControladorMedicos.abre_tela().
        # Nós apenas precisamos chamar esse método.
        self.__controlador_medicos.abre_tela()

    def gerenciar_planos_terapia(self):
        # A lógica de permissão já está no 'abre_tela' do controlador de planos
        self.__controlador_plano_terapia.abre_tela()

    def encerra_sistema(self):
        exit(0)

    def fazer_logout(self):
        """Faz logout e retorna ao login. Chamado quando o usuário clica em 'Sair' no menu principal."""
        # Apenas marca que deve fazer logout - não limpa ainda para evitar erros
        return

    def abre_tela(self):
        # 5. ADICIONAR OPÇÃO 4 no dicionário 'opcoes'
        
        while True:
            # Recria o dicionário de opções a cada iteração para garantir que está atualizado
            opcoes = {}
            if self.__usuario_logado.tipo_usuario == 'secretaria':
                opcoes = {1: self.cadastra_paciente,
                          2: self.cadastra_medicos,
                          3: self.cadastra_consultas,
                          # 4: self.gerenciar_planos_terapia, # Secretaria não gerencia planos
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

            # 6. ATUALIZAR a tela_sistema para ela saber quais botões mostrar
            opcoes_disponiveis = list[int](opcoes.keys())
            opcao_escolhida = self.__tela_sistema.tela_opcoes(self.__usuario_logado.tipo_usuario, opcoes_disponiveis)
            
            funcao_escolhida = opcoes.get(opcao_escolhida)
            
            if funcao_escolhida:
                if funcao_escolhida == self.fazer_logout:
                    # Limpa o usuário logado e sai do loop
                    self.__usuario_logado = None
                    break # Sai do loop do menu principal (e volta para o loop de login em inicializa_sistema)
                funcao_escolhida()
            else:
                self.__tela_sistema.mostra_mensagem("Erro", "Opção inválida.")