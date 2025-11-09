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
            # Primeiro, pega os dados do médico (sem sala)
            dados_medico = self.__telamedico.pega_dados_medicos()

            crm = dados_medico["crm"]
            nome = dados_medico["nome"]
            especialidade = dados_medico["especialidade"]
            expediente_inicial = dados_medico["expediente_inicial"]
            expediente_final = dados_medico["expediente_final"]

            # Validações básicas
            if not isinstance(crm, int):
                raise ValueError("CRM inválido.")

            if not isinstance(nome, str):
                raise ValueError("Nome inválido.")

            if not isinstance(especialidade, str):
                raise ValueError("Especialidade inválida.")

            # Verifica se médico já existe
            try:
                self.busca_medico(crm)
                self.__telamedico.mostra_mensagem("Erro", f"Médico com CRM {crm} já está cadastrado.")
                return
            except MedicoNaoEncontrado:
                pass  # Médico não existe, pode criar

            # Busca todas as salas e permite seleção
            salas = self.__sala_DAO.get_all()
            if not salas:
                self.__telamedico.mostra_mensagem("Erro", "Nenhuma sala cadastrada. Crie salas primeiro.")
                return

            # Prepara lista de salas para exibição
            salas_info = [{"numero": sala.numero, "andar": sala.andar, "capacidade": sala.capacidade}
                         for sala in salas]

            # Seleciona sala usando interface gráfica com radio buttons
            numero_sala = self.__telamedico.seleciona_sala(salas_info)

            # Busca o objeto sala pelo número
            sala = self.__sala_DAO.get(numero_sala)
            if sala is None:
                self.__telamedico.mostra_mensagem("Erro", f"Sala {numero_sala} não encontrada.")
                return

            # Cria novo médico
            novo_medico = Medico(crm, nome, especialidade, expediente_inicial, expediente_final, sala)
            self.__medico_DAO.add(novo_medico)
            self.__telamedico.mostra_mensagem("Confirmação", f"Médico '{nome}' foi adicionado com sucesso!")
        
        except ValueError as ve:
            self.__telamedico.mostra_mensagem("Erro", f"{ve}")
        except CancelOpException:
            pass  # Usuário cancelou - não faz nada
        except Exception as e:
            self.__telamedico.mostra_mensagem("Erro", f"Erro inesperado: {e}")
            

    def atualizar_medico(self):
        try:
            # Listar médicos para seleção
            crm = self.listar_medicos(selecionar=True)
            
            if crm is None:
                return
            
            medico = self.busca_medico(crm)
            
            novos_dados = self.__telamedico.pega_novos_dados_medicos()  
            nome = novos_dados["nome"]
            especialidade = novos_dados["especialidade"]
            expediente_inicial = novos_dados["expediente_inicial"]
            expediente_final = novos_dados["expediente_final"]
            
    
            if nome is None or especialidade is None or expediente_inicial is None or expediente_final is None:
                raise ValueError("Erro", "Todos os campos são obrigatórios.")

            if not isinstance(nome, str):
                raise ValueError("Erro", "Nome inválido.")

            if not isinstance(especialidade, str):
                raise ValueError("Erro", "Especialidade inválida.")

            if not isinstance(expediente_inicial, str):
                raise ValueError("Erro", "Expediente inicial inválido.")
            
            self.__medico_DAO.update(medico)
            self.listar_medicos()
            self.__telamedico.mostra_mensagem("Confirmação", f"Médico CRM '{crm}' atualizado com sucesso!")
            
        except MedicoNaoEncontrado as e:
            self.__telamedico.mostra_mensagem("Erro:", f"{e}")
        except ValueError as ve:
            self.__telamedico.mostra_mensagem("Erro:", f"{ve}")
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

        medicos_info = [{"crm": medico.crm, "nome": medico.nome, "especialidade": medico.especialidade,
                           "expediente_inicial": medico.expediente_inicial, "expediente_final": medico.expediente_final,
                           "sala": medico.sala}
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
        lista_opcoes = {1: self.adicionar_medico, 2: self.atualizar_medico, 3: self.remover_medico, 4: self.listar_medicos, 0: self.retornar}

        continua = True
        while continua:
            lista_opcoes[self.__telamedico.tela_opcoes()]()
