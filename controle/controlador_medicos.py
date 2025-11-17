from controle.controlador_entidade_abstrata import ControladorEntidadeAbstrata
from entidades.medico import Medico
from DAO.medico_dao import MedicoDAO
from DAO.sala_dao import SalaDAO
from exceptions.medico_nao_encontrado_exception import MedicoNaoEncontrado
from exceptions.cancel_op_exception import CancelOpException
from limite.tela_medicos import TelaMedicos
import PySimpleGUI as sg

class ControladorMedicos(ControladorEntidadeAbstrata):
    def __init__(self, controlador_sistema):
        super().__init__(controlador_sistema)
        self.__telamedico = TelaMedicos(controlador_sistema)
        self.__medico_DAO = MedicoDAO()
        self.__sala_DAO = SalaDAO()

    def adicionar_medico(self):
        try:
            dados_medico = self.__telamedico.pega_dados_medicos()

            # Dados de Pessoa
            nome = dados_medico["nome"]
            email = dados_medico["email"]
            cpf = dados_medico["cpf"] # Já vem como int
            contato = dados_medico["contato"]
            data_nascimento = dados_medico["data_nascimento"]
            genero = dados_medico["genero"]
            
            # Dados de Medico
            crm = dados_medico["crm"] # Já vem como int
            especialidade = dados_medico["especialidade"]
            expediente_inicial = dados_medico["expediente_inicial"]
            expediente_final = dados_medico["expediente_final"]

            # Validações básicas
            if not all([nome, email, cpf, contato, data_nascimento, genero, crm, especialidade, expediente_inicial, expediente_final]):
                raise ValueError("Erro", "Todos os campos são obrigatórios.")

            if not isinstance(nome, str):
                raise ValueError("Nome inválido.")

            if not isinstance(email, str):
                raise ValueError("Email inválido.")

            if not isinstance(crm, int):
                raise ValueError("CRM inválido.")

            try:
                self.busca_medico(crm)
                self.__telamedico.mostra_mensagem("Erro", f"Médico com CRM {crm} já está cadastrado.")
                return
            except MedicoNaoEncontrado:

                salas = self.__sala_DAO.get_all()
                if not salas:
                    self.__telamedico.mostra_mensagem("Erro", "Nenhuma sala cadastrada. Crie salas primeiro.")
                    return

                salas_info = [{"numero": sala.numero, "andar": sala.andar, "capacidade": sala.capacidade}
                            for sala in salas]

                numero_sala = self.__telamedico.seleciona_sala(salas_info)

                sala = self.__sala_DAO.get(numero_sala)
                if sala is None:
                    self.__telamedico.mostra_mensagem("Erro", f"Sala {numero_sala} não encontrada.")
                    return

                novo_medico = Medico(nome, email, cpf, contato, data_nascimento, genero,
                crm, especialidade, expediente_inicial, expediente_final, sala)
                self.__medico_DAO.add(novo_medico)
                self.__telamedico.mostra_mensagem("Confirmação", f"Médico '{nome}' foi adicionado com sucesso!")
        
        except ValueError as ve:
            self.__telamedico.mostra_mensagem("Erro", f"{ve}")
        except CancelOpException:
            pass  # Usuário cancelou - não faz nada
        except Exception as e:
            self.__telamedico.mostra_mensagem("Erro", f"Erro inesperado: {e}")
        
    # --- MÉTODO ATUALIZADO (PARA SECRETÁRIA) ---
    def atualizar_medico_secretaria(self):
        # Este é o seu 'atualizar_paciente' original
        # A secretária precisa selecionar o paciente primeiro
        try:
            crm = self.listar_medicos(selecionar=True)
            if crm is None:
                return  # Secretária cancelou
            
            # Chama o método de lógica de atualização
            self.atualizar_medico_com_crm(crm) 

        except (MedicoNaoEncontrado, ValueError) as e:
            self.__telamedico.mostra_mensagem("Erro:", f"{e}")
        except CancelOpException:
            pass

     # --- NOVO MÉTODO (PARA PACIENTE LOGADO) ---
    def atualizar_meus_dados(self, crm_logado: int):
        # Este método não lista pacientes. Ele já sabe qual paciente editar.
        try:
            # Chama o método de lógica de atualização diretamente
            self.atualizar_medico_com_crm(crm_logado)
            
        except (MedicoNaoEncontrado, ValueError) as e:
            self.__telamedico.mostra_mensagem("Erro:", f"{e}")
        except CancelOpException:
            pass

    def atualizar_medico_com_crm(self, crm: int):
        try:

            if crm is None:
                return
            
            medico = self.busca_medico(crm)
            
            novos_dados = self.__telamedico.pega_novos_dados_medicos()

            nome = novos_dados["nome"]
            email = novos_dados["email"]
            contato = novos_dados["contato"]
            data_nascimento = novos_dados["data_nascimento"]
            genero = novos_dados["genero"]
            
            especialidade = novos_dados["especialidade"]
            expediente_inicial = novos_dados["expediente_inicial"]
            expediente_final = novos_dados["expediente_final"]
            
    
            if not all([nome, email, contato, data_nascimento, genero, especialidade, expediente_inicial, expediente_final]):
                raise ValueError("Erro", "Todos os campos são obrigatórios.")

            if not isinstance(nome, str):
                raise ValueError("Erro", "Nome inválido.")

            if not isinstance(email, str):
                raise ValueError("Erro", "Email inválido.")

            if not isinstance(crm, int):
                raise ValueError("Erro", "CRM inválido.")

            medico.nome = nome
            medico.email = email
            medico.contato = contato
            medico.data_nascimento = data_nascimento
            medico.genero = genero
            medico.especialidade = especialidade
            medico.expediente_inicial = expediente_inicial
            medico.expediente_final = expediente_final
            
            self.__medico_DAO.update(medico)
            self.listar_medicos(selecionar=False)
            self.__telamedico.mostra_mensagem("Confirmação", f"Médico CRM '{crm}' atualizado com sucesso!")
            
        except MedicoNaoEncontrado as e:
            self.__telamedico.mostra_mensagem("Erro:", f"{e}")
        except ValueError as ve:
            self.__telamedico.mostra_mensagem("Erro:", f"{ve}")
        except CancelOpException:
            pass

    def ver_meus_dados(self, crm_logado: int):
        """
        Mostra os dados apenas do médico logado.
        """
        try:
            medico = self.busca_medico(crm_logado)
            
            # Formata os dados para a tela de listagem (mas com apenas 1 paciente)
            medicos_info = [{
                 # Atributos de Pessoa
                "nome": medico.nome,
                "email": medico.email,
                "cpf": medico.cpf,
                "contato": medico.contato,
                "data_nascimento": medico.data_nascimento,
                "genero": medico.genero,
                "idade": medico.idade, # A IDADE CALCULADA!
                
                # Atributos específicos de Medico
                "crm": medico.crm,
                "especialidade": medico.especialidade,
                "expediente_inicial": medico.expediente_inicial,
                "expediente_final": medico.expediente_final,
                "sala": medico.sala # Passa o objeto Sala inteiro
            }]
            
            # Reutiliza a 'exibe_lista_pacientes' sem seleção
            self.__telamedico.exibe_lista_medicos(medicos_info, selecionar=False)
            
        except MedicoNaoEncontrado as e:
            self.__telamedico.mostra_mensagem("Erro:", f"{e}")
        except CancelOpException:
            pass

    def remover_medico(self):
        try:
            # Listar médicos para seleção
            crm = self.listar_medicos(selecionar=True)
            
            if crm is None:
                return
    
            medico = self.busca_medico(crm)
            self.__medico_DAO.remove(crm)
            self.listar_medicos()
            self.__telamedico.mostra_mensagem("Confirmação", f"Médico CRM '{crm}' foi removido com sucesso!")
                
        except MedicoNaoEncontrado as e:
            self.__telamedico.mostra_mensagem("Erro:", f"{e}")
        except ValueError as ve:
            self.__telamedico.mostra_mensagem("Erro:", f"{ve}")
        except CancelOpException:
            pass

    def busca_medico(self, crm: int):
        medico = self.__medico_DAO.get(crm)
        if medico is not None:
            return medico
        raise MedicoNaoEncontrado(crm)

    def listar_medicos(self, selecionar=False):
        medicos = self.__medico_DAO.get_all()
        if not medicos:
            self.__telamedico.mostra_mensagem("Erro", "Nenhum médico cadastrado.")
            return None

        medicos_info = [{
                    # Atributos de Pessoa
                    "nome": medico.nome,
                    "email": medico.email,
                    "cpf": medico.cpf,
                    "contato": medico.contato,
                    "data_nascimento": medico.data_nascimento,
                    "genero": medico.genero,
                    "idade": medico.idade, # A IDADE CALCULADA!
                    
                    # Atributos específicos de Medico
                    "crm": medico.crm,
                    "especialidade": medico.especialidade,
                    "expediente_inicial": medico.expediente_inicial,
                    "expediente_final": medico.expediente_final,
                    "sala": medico.sala # Passa o objeto Sala inteiro
                }
                          for medico in medicos]
        try:
            return self.__telamedico.exibe_lista_medicos(medicos_info, selecionar)
        except CancelOpException:
            return None

    def listar_salas(self):
        """Lista todas as salas disponíveis"""
        salas = self.__sala_DAO.get_all()
        if not salas:
            self.__telamedico.mostra_mensagem("Erro", "Nenhuma sala cadastrada.")
            return
        
        for sala in salas:
            self.__telamedico.mostra_mensagem(f"Sala {sala.numero} - Andar {sala.andar} (Capacidade: {sala.capacidade})")

    def abre_tela(self):
        lista_opcoes = {1: self.adicionar_medico, 2: self.atualizar_medico_secretaria, 3: self.remover_medico, 4: self.listar_medicos, 0: self.retornar}

        continua = True
        while continua:
            lista_opcoes[self.__telamedico.tela_opcoes()]()

    # --- NOVO MÉTODO (PARA MÉDICO LOGADO) ---
    def abre_tela_medico_logado(self, crm_logado: int):
        # Este é o novo menu restrito para o Medico
        # Note que passamos o 'crm_logado' para os métodos
        lista_opcoes = {
            1: lambda: self.ver_meus_dados(crm_logado),
            2: lambda: self.atualizar_meus_dados(crm_logado),
            0: self.retornar
        }
        
        continua = True
        while continua:
            # Você precisa criar este novo método de tela em TelaPacientes
            # que mostra apenas os botões "Ver Meus Dados", "Atualizar Meus Dados" e "Sair"
            opcao = self.__telamedico.tela_opcoes_medico() 
            
            if opcao == 0:
                continua = False
            else:
                funcao_escolhida = lista_opcoes.get(opcao)
                if funcao_escolhida:
                    funcao_escolhida()