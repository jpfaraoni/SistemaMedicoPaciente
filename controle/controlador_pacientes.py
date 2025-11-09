from entidades.paciente import Paciente
from limite.tela_pacientes import TelaPacientes
from controle.controlador_entidade_abstrata import ControladorEntidadeAbstrata
from exceptions.paciente_nao_encontrado_exception import PacienteNaoEncontrado
from exceptions.cancel_op_exception import CancelOpException
from DAO.paciente_dao import PacienteDAO

class ControladorPacientes(ControladorEntidadeAbstrata):
    def __init__(self, controlador_sistema):
        super().__init__(controlador_sistema)
        self.__telapacientes = TelaPacientes(controlador_sistema)
        self.__paciente_DAO = PacienteDAO()

    def adicionar_paciente(self):
        try:
            dados_paciente = self.__telapacientes.pega_dados_paciente()
            nome = dados_paciente["nome"]
            email = dados_paciente["email"]
            idade = int(dados_paciente["idade"])
            cpf = dados_paciente["cpf"]

            if nome is None or email is None or idade is None or cpf is None:
                raise ValueError("Todos os campos são obrigatórios.")

            if not isinstance(nome, str):
                raise ValueError("Nome inválido.")

            if not isinstance(email, str):
                raise ValueError("Email inválido.")

            if not isinstance(idade, int):
                raise ValueError("Idade inválida.")

            if not isinstance(cpf, int):
                raise ValueError("Cpf inválido.")

            try:
                self.busca_paciente(cpf)  
                raise ValueError(f"Paciente com cpf '{cpf}' já está cadastrado.")
            except PacienteNaoEncontrado:
                novo_paciente = Paciente(
                    nome,
                    email,
                    idade,
                    cpf
                )
                self.__paciente_DAO.add(novo_paciente)
                self.__telapacientes.mostra_mensagem("Confirmação", f"Paciente '{nome}' foi adicionado com sucesso!")

        except ValueError as ve:
            self.__telapacientes.mostra_mensagem("Erro:", f"{ve}")
        except CancelOpException:
                pass
        # except Exception as e:
        #     self.__telapacientes.mostra_mensagem(f"Erro: {e}", f"{e}")

    def atualizar_paciente(self):
        #TODO implementar um metodo update na classe DAO abstrata e realizar o update apos atualizar o objeto para o db refletir a nova instancia.
        try:
            cpf = self.listar_pacientes(selecionar=True)

            # Verifica se o usuário cancelou a seleção do paciente
            if cpf is None:
                return  # Retorna silenciosamente se o usuário cancelou

            paciente = self.busca_paciente(cpf)
            
            # Agora tenta pegar os novos dados - se cancelar aqui, a exceção será capturada
            novos_dados = self.__telapacientes.pega_novos_dados_paciente()

            nome = novos_dados["nome"]
            email = novos_dados["email"]
            idade = novos_dados["idade"]

            if nome is None or email is None or idade is None:
                raise ValueError("Erro", "Todos os campos são obrigatórios.")

            if not isinstance(nome, str):
                raise ValueError("Erro", "Nome inválido.")

            if not isinstance(email, str):
                raise ValueError("Erro", "Email inválido.")

            if not isinstance(idade, int):
                raise ValueError("Erro", "Idade inválida.")

            paciente.nome = novos_dados["nome"]
            paciente.email = novos_dados["email"]
            paciente.idade = novos_dados["idade"]

            self.__paciente_DAO.update(paciente)
            self.listar_pacientes()

            self.__telapacientes.mostra_mensagem("Confirmação", f"Paciente com CPF '{cpf}' atualizado com sucesso!")
        except PacienteNaoEncontrado as e:
            self.__telapacientes.mostra_mensagem("Erro:", f"{e}")
        except ValueError as ve:
            self.__telapacientes.mostra_mensagem("Erro:", f"{ve}")
        except CancelOpException:
            pass  # Usuário cancelou - não faz nada

    def busca_paciente(self, cpf):
        paciente = self.__paciente_DAO.get(cpf)
        if paciente is not None:
            return paciente
        else:
            raise PacienteNaoEncontrado(cpf)

    def remover_paciente(self):
        try:
            cpf = self.listar_pacientes(selecionar=True)

            # Verifica se o usuário cancelou a seleção do paciente
            if cpf is None:
                return  # Retorna silenciosamente se o usuário cancelou

            self.__paciente_DAO.remove(cpf)
            self.__telapacientes.mostra_mensagem("Confirmação", f"Paciente com cpf '{cpf}' foi removido com sucesso.")

        except PacienteNaoEncontrado as e:
            self.__telapacientes.mostra_mensagem(f"Erro:", f"{e}")
        except CancelOpException:
            pass  # Usuário cancelou - não faz nada

    def listar_pacientes(self, selecionar=False):

        pacientes = self.__paciente_DAO.get_all()
        if not pacientes:
            self.__telapacientes.mostra_mensagem("Erro", "Nenhum paciente cadastrado.")
            return None

        pacientes_info = [{"nome": paciente.nome, "email": paciente.email, "idade": paciente.idade,
                           "cpf": paciente.cpf}
                          for paciente in pacientes]
        try:
            return self.__telapacientes.exibe_lista_pacientes(pacientes_info, selecionar)
        except CancelOpException:
            return None  # Retorna None explicitamente quando o usuário cancela


    def abre_tela(self):
        lista_opcoes = {1: self.adicionar_paciente, 2: self.atualizar_paciente, 3: self.remover_paciente, 4: self.listar_pacientes, 0: self.retornar}

        continua = True
        while continua:
            lista_opcoes[self.__telapacientes.tela_opcoes()]()



