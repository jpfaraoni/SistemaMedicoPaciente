# Arquivo: controle/controlador_plano_terapia.py

from controle.controlador_entidade_abstrata import ControladorEntidadeAbstrata
from limite.tela_plano_terapia import TelaPlanoTerapia
from DAO.plano_terapia_dao import PlanoDeTerapiaDAO
from entidades.plano_terapia import PlanoDeTerapia
from exceptions.cancel_op_exception import CancelOpException
from exceptions.paciente_nao_encontrado_exception import PacienteNaoEncontrado
from exceptions.medico_nao_encontrado_exception import MedicoNaoEncontrado
from random import randint
from datetime import datetime

class ControladorPlanoTerapia(ControladorEntidadeAbstrata):
    def __init__(self, controlador_sistema):
        super().__init__(controlador_sistema)
        self.__tela_plano = TelaPlanoTerapia(controlador_sistema)
        self.__plano_DAO = PlanoDeTerapiaDAO()

    def criar_plano_terapia(self, crm_logado: int):
        """ (Lógica do Médico) """
        try:
            # 1. Buscar o objeto Medico que está criando o plano
            medico = self._controlador_sistema.controlador_medicos.busca_medico(crm_logado)
            if medico is None:
                raise MedicoNaoEncontrado(crm_logado)
            
            # 2. Selecionar o Paciente para quem é o plano
            cpf_paciente = self._controlador_sistema.controlador_pacientes.listar_pacientes(selecionar=True)
            if cpf_paciente is None:
                raise CancelOpException()
            
            paciente = self._controlador_sistema.controlador_pacientes.busca_paciente(cpf_paciente)
            if paciente is None:
                raise PacienteNaoEncontrado(cpf_paciente)

            # 3. Pegar o texto do plano
            dados = self.__tela_plano.pega_dados_plano()
            texto_plano = dados["texto_plano"]

            if not texto_plano or texto_plano.strip() == "":
                raise ValueError("O texto do plano não pode estar vazio.")

            # 4. Criar e salvar o plano
            data_hoje = datetime.now().strftime("%d/%m/%Y")
            novo_plano = PlanoDeTerapia(
                id_plano=randint(0, 100000),
                paciente=paciente,
                medico=medico,
                data_criacao=data_hoje,
                texto_plano=texto_plano
            )

            self.__plano_DAO.add(novo_plano)
            self.__tela_plano.mostra_mensagem("Sucesso", "Plano de terapia criado e salvo.")

        except (ValueError, PacienteNaoEncontrado, MedicoNaoEncontrado) as e:
            self.__tela_plano.mostra_mensagem("Erro", f"{e}")
        except CancelOpException:
            pass # Usuário cancelou
            
    def listar_planos_paciente(self, cpf_logado: int):
        """ (Lógica do Paciente) Mostra lista e permite ler """
        todos_planos = self.__plano_DAO.get_all()
        planos_filtrados = [p for p in todos_planos if p.paciente.cpf == cpf_logado]
        
        self.logica_visualizacao_lista(planos_filtrados)
        
    def listar_planos_medico(self, crm_logado: int):
        """ (Lógica do Médico) Mostra lista dos planos que ele criou """
        todos_planos = self.__plano_DAO.get_all()
        planos_filtrados = [p for p in todos_planos if p.medico.crm == crm_logado]
        
        self.logica_visualizacao_lista(planos_filtrados)

    def logica_visualizacao_lista(self, lista_planos: list):
        """ Lógica interna para exibir a lista e mostrar detalhes """
        try:
            while True:
                planos_info = [{
                    "id_plano": plano.id_plano,
                    "paciente_nome": plano.paciente.nome,
                    "medico_nome": plano.medico.nome,
                    "data_criacao": plano.data_criacao
                } for plano in lista_planos]

                id_plano_selecionado = self.__tela_plano.exibe_lista_planos(planos_info)
                
                if id_plano_selecionado is None:
                    break # Usuário fechou a lista
                
                plano_obj = self.__plano_DAO.get(id_plano_selecionado)
                if plano_obj:
                    self.__tela_plano.mostra_plano_detalhado(
                        plano_obj.data_criacao,
                        plano_obj.medico.nome,
                        plano_obj.texto_plano
                    )
        except CancelOpException:
            pass

    def abre_tela(self):
        usuario_logado = self._controlador_sistema.usuario_logado
        
        opcoes = {}
        if usuario_logado.tipo_usuario == 'paciente':
            cpf_logado = usuario_logado.id_entidade
            opcoes = {1: lambda: self.listar_planos_paciente(cpf_logado),
                      0: self.retornar}
        elif usuario_logado.tipo_usuario == 'medico':
            crm_logado = usuario_logado.id_entidade
            opcoes = {2: lambda: self.criar_plano_terapia(crm_logado),
                      3: lambda: self.listar_planos_medico(crm_logado),
                      0: self.retornar}
        
        continua = True
        while continua:
            opcao = self.__tela_plano.tela_opcoes(usuario_logado.tipo_usuario)
            funcao_escolhida = opcoes.get(opcao)
            
            if funcao_escolhida:
                if funcao_escolhida == self.retornar:
                    continua = False
                else:
                    funcao_escolhida()
            else:
                self.__tela_plano.mostra_mensagem("Aviso", "Opção inválida.")