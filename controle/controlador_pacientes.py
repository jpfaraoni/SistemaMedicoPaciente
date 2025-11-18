from entidades.paciente import Paciente
from limite.tela_pacientes import TelaPacientes
from controle.controlador_entidade_abstrata import ControladorEntidadeAbstrata
from exceptions.paciente_nao_encontrado_exception import PacienteNaoEncontrado
from exceptions.cancel_op_exception import CancelOpException
from DAO.paciente_dao import PacienteDAO

class ControladorPacientes(ControladorEntidadeAbstrata):
    """Participa da fachada delegando regras de paciente às telas e DAOs."""

    def __init__(self, controlador_sistema):
        super().__init__(controlador_sistema)
        self.__telapacientes = TelaPacientes(controlador_sistema)
        self.__paciente_DAO = PacienteDAO()

    def adicionar_paciente(self):
        try:
            dados_paciente = self.__telapacientes.pega_dados_paciente()
            nome = dados_paciente["nome"]
            email = dados_paciente["email"]
            cpf = dados_paciente["cpf"]

            contato = dados_paciente["contato"]
            data_nascimento = dados_paciente["data_nascimento"]
            genero = dados_paciente["genero"]

            convenio = dados_paciente["convenio"]
            deficiente = dados_paciente["deficiente"]
            tipo_sanguineo = dados_paciente["tipo_sanguineo"]

            if not all([nome, email, cpf, contato, data_nascimento, genero, convenio, deficiente, tipo_sanguineo]):
                raise ValueError("Todos os campos são obrigatórios.")

            if not isinstance(nome, str):
                raise ValueError("Nome inválido.")

            if not isinstance(email, str):
                raise ValueError("Email inválido.")

            if not isinstance(cpf, int):
                raise ValueError("Cpf inválido.")

            try:
                self.busca_paciente(cpf)  
                raise ValueError(f"Paciente com cpf '{cpf}' já está cadastrado.")
            except PacienteNaoEncontrado:
                novo_paciente = Paciente(
                    nome, email, cpf, contato, data_nascimento, genero,
                    convenio, deficiente, tipo_sanguineo
                )
                self.__paciente_DAO.add(novo_paciente)
                self.__telapacientes.mostra_mensagem("Confirmação", f"Paciente '{nome}' foi adicionado com sucesso!")

        except ValueError as ve:
            self.__telapacientes.mostra_mensagem("Erro:", f"{ve}")
        except CancelOpException:
            pass

    def atualizar_paciente_secretaria(self):
        try:
            cpf = self.listar_pacientes(selecionar=True)
            if cpf is None:
                return
            self.atualizar_paciente_com_cpf(cpf)
        except (PacienteNaoEncontrado, ValueError) as e:
            self.__telapacientes.mostra_mensagem("Erro:", f"{e}")
        except CancelOpException:
            pass

    def atualizar_meus_dados(self, cpf_logado: int):
        try:
            self.atualizar_paciente_com_cpf(cpf_logado)
        except (PacienteNaoEncontrado, ValueError) as e:
            self.__telapacientes.mostra_mensagem("Erro:", f"{e}")
        except CancelOpException:
            pass

    def atualizar_paciente_com_cpf(self, cpf: int):
        try:
            if cpf is None:
                return
            paciente = self.busca_paciente(cpf)
            novos_dados = self.__telapacientes.pega_novos_dados_paciente()

            nome = novos_dados["nome"]
            email = novos_dados["email"]
            contato = novos_dados["contato"]
            data_nascimento = novos_dados["data_nascimento"]
            genero = novos_dados["genero"]
            convenio = novos_dados["convenio"]
            deficiente = novos_dados["deficiente"]
            tipo_sanguineo = novos_dados["tipo_sanguineo"]

            if nome is None or email is None:
                raise ValueError("Erro", "Todos os campos são obrigatórios.")

            if not isinstance(nome, str):
                raise ValueError("Erro", "Nome inválido.")

            if not isinstance(email, str):
                raise ValueError("Erro", "Email inválido.")

            paciente.nome = nome
            paciente.email = email
            paciente.contato = contato
            paciente.data_nascimento = data_nascimento
            paciente.genero = genero
            paciente.convenio = convenio
            paciente.deficiente = deficiente
            paciente.tipo_sanguineo = tipo_sanguineo

            self.__paciente_DAO.update(paciente)
            self.listar_pacientes()

            self.__telapacientes.mostra_mensagem("Confirmação", f"Paciente com CPF '{cpf}' atualizado com sucesso!")
        except PacienteNaoEncontrado as e:
            self.__telapacientes.mostra_mensagem("Erro:", f"{e}")
        except ValueError as ve:
            self.__telapacientes.mostra_mensagem("Erro:", f"{ve}")
        except CancelOpException:
            pass

    def ver_meus_dados(self, cpf_logado: int):
        try:
            paciente = self.busca_paciente(cpf_logado)
            paciente_info = [{
                "nome": paciente.nome,
                "email": paciente.email,
                "cpf": paciente.cpf,
                "contato": paciente.contato,
                "data_nascimento": paciente.data_nascimento,
                "genero": paciente.genero,
                "convenio": paciente.convenio,
                "deficiente": paciente.deficiente,
                "tipo_sanguineo": paciente.tipo_sanguineo,
                "idade": paciente.idade
            }]
            
            self.__telapacientes.exibe_lista_pacientes(paciente_info, selecionar=False)
        except PacienteNaoEncontrado as e:
            self.__telapacientes.mostra_mensagem("Erro:", f"{e}")
        except CancelOpException:
            pass

    def busca_paciente(self, cpf):
        paciente = self.__paciente_DAO.get(cpf)
        if paciente is not None:
            return paciente
        else:
            raise PacienteNaoEncontrado(cpf)

    def remover_paciente(self):
        try:
            cpf = self.listar_pacientes(selecionar=True)

            if cpf is None:
                return

            self.__paciente_DAO.remove(cpf)
            self.__telapacientes.mostra_mensagem("Confirmação", f"Paciente com cpf '{cpf}' foi removido com sucesso.")

        except PacienteNaoEncontrado as e:
            self.__telapacientes.mostra_mensagem(f"Erro:", f"{e}")
        except CancelOpException:
            pass

    def listar_pacientes(self, selecionar=False):
        pacientes = self.__paciente_DAO.get_all()
        if not pacientes:
            self.__telapacientes.mostra_mensagem("Erro", "Nenhum paciente cadastrado.")
            return None

        pacientes_info = [{
                "nome": paciente.nome,
                "email": paciente.email,
                "cpf": paciente.cpf,
                "contato": paciente.contato,
                "data_nascimento": paciente.data_nascimento,
                "genero": paciente.genero,
                "convenio": paciente.convenio,
                "deficiente": paciente.deficiente,
                "tipo_sanguineo": paciente.tipo_sanguineo,
                "idade": paciente.idade 
            }
                          for paciente in pacientes]
        try:
            return self.__telapacientes.exibe_lista_pacientes(pacientes_info, selecionar)
        except CancelOpException:
            return None
    def abre_tela(self):
        """
        Método principal que verifica o tipo de usuário logado e abre a tela apropriada.
        A lógica de permissão está aqui, delegada do ControladorSistema.
        """
        usuario_logado = self._controlador_sistema.usuario_logado
        
        if usuario_logado.tipo_usuario == 'secretaria':
            self.abre_tela_secretaria()
        elif usuario_logado.tipo_usuario == 'paciente':
            cpf_logado = usuario_logado.id_entidade
            self.abre_tela_paciente_logado(cpf_logado)
        else:
            self.__telapacientes.mostra_mensagem("Erro", "Acesso Negado.")

    def abre_tela_secretaria(self):
        """Menu completo para secretaria gerenciar pacientes."""
        lista_opcoes = {1: self.adicionar_paciente, 2: self.atualizar_paciente_secretaria, 3: self.remover_paciente, 4: self.listar_pacientes, 0: self.retornar}

        continua = True
        while continua:
            opcao = self.__telapacientes.tela_opcoes()
            if opcao == 0:
                self.retornar()
                continua = False
            else:
                funcao_escolhida = lista_opcoes.get(opcao)
                if funcao_escolhida:
                    funcao_escolhida()

    def abre_tela_paciente_logado(self, cpf_logado: int):
  
        lista_opcoes = {
            1: lambda: self.ver_meus_dados(cpf_logado),
            2: lambda: self.atualizar_meus_dados(cpf_logado),
            0: self.retornar
        }
        
        continua = True
        while continua:

            opcao = self.__telapacientes.tela_opcoes_paciente() 
            
            if opcao == 0:
                continua = False
            else:
                funcao_escolhida = lista_opcoes.get(opcao)
                if funcao_escolhida:
                    funcao_escolhida()



