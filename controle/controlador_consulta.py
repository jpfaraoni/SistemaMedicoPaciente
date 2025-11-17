from exceptions.cancel_op_exception import CancelOpException
from exceptions.sala_nao_encontrada_exception import SalaNaoEncontrada
from datetime import datetime, timedelta
from exceptions.horario_invalido_exception import HorarioInvalido
from limite.tela_consulta import TelaConsulta
from entidades.paciente import Paciente
from controle.controlador_entidade_abstrata import ControladorEntidadeAbstrata
from DAO.consulta_dao import ConsultaDAO
from random import randint
from exceptions.consulta_nao_encontrada_exception import ConsultaNaoEncontrada
from entidades.consulta import Consulta
# from controle.controlador_medicos import ControladorMedicos


class ControladorConsultas(ControladorEntidadeAbstrata):
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, controlador_sistema):
        super().__init__(controlador_sistema)
        self.__telaconsulta = TelaConsulta(controlador_sistema)
        self.__consulta_DAO = ConsultaDAO()
        #TODO instanciar os dao's de medicos e pacientes para a consulta de banco de dados 
       

        """
        Controlador responsável por gerenciar as Consultas.
        """

    def horario_disponivel(self, nova_consulta:Consulta):
        """
        Verifica se há conflito entre a data/horário da nova consulta e as consultas já cadastradas.
        Considera que cada consulta dura sempre 1 hora.
        Verifica conflitos na mesma data e horário para sala, médico e paciente.
        """
        # Valida o horário da nova consulta
        if not self.validar_horario(nova_consulta.horario):
            raise HorarioInvalido(nova_consulta.horario)

        # Valida a data da nova consulta
        if not self.validar_data(nova_consulta.data):
            raise ValueError("Data inválida. Use o formato DD/MM/AAAA")

        # Combina data e horário para criar datetime completo
        novo_datetime_inicio = datetime.strptime(f"{nova_consulta.data} {nova_consulta.horario}", "%d/%m/%Y %H:%M")
        # Consulta sempre dura 1 hora
        novo_datetime_termino = novo_datetime_inicio + timedelta(hours=1)

        consultas = self.__consulta_DAO.get_all()
        for consulta in consultas:
            # Só verifica conflitos se for na mesma data
            if consulta.data == nova_consulta.data:
                # Combina data e horário da consulta existente
                datetime_inicio_existente = datetime.strptime(f"{consulta.data} {consulta.horario}", "%d/%m/%Y %H:%M")
                # Consulta existente também dura 1 hora
                datetime_termino_existente = datetime_inicio_existente + timedelta(hours=1)

                # Verifica conflito na mesma sala
                if consulta.sala.numero == nova_consulta.sala.numero:
                    # Verifica se há sobreposição de horários entre as consultas na mesma sala
                    if (novo_datetime_inicio < datetime_termino_existente and
                            novo_datetime_termino > datetime_inicio_existente):
                        return False  # Conflito de horário na sala
                
                # Verifica conflito com o mesmo médico
                if consulta.medico == nova_consulta.medico:
                    # Verifica se há sobreposição de horários para o mesmo médico
                    if (novo_datetime_inicio < datetime_termino_existente and
                            novo_datetime_termino > datetime_inicio_existente):
                        return False  # Conflito de horário para o médico
                
                # Verifica conflito com o mesmo paciente
                if consulta.paciente == nova_consulta.paciente:
                    # Verifica se há sobreposição de horários para o mesmo paciente
                    if (novo_datetime_inicio < datetime_termino_existente and
                            novo_datetime_termino > datetime_inicio_existente):
                        return False  # Conflito de horário para o paciente
                    
        return True  # Horário disponível

    def validar_horario(self, horario):
        """
        Valida se o horário está no formato HH:MM.
        Retorna True se o horário for válido, caso contrário, False.
        """
        try:
            datetime.strptime(horario, "%H:%M")
            return True
        except ValueError:
            return False

    def validar_data(self, data):
        """
        Valida se a data está no formato DD/MM/AAAA.
        Retorna True se a data for válida, caso contrário, False.
        """
        try:
            datetime.strptime(data, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def adicionar_consultas(self):
        try:
            # Listar pacientes e medicos para auxiliar o usuário na escolha
            cpf_paciente = self._controlador_sistema.controlador_pacientes.listar_pacientes(selecionar=True)
            if cpf_paciente is None:
                pass
            crm_medico = self._controlador_sistema.controlador_medicos.listar_medicos(selecionar=True)
            if crm_medico is None:
                pass

            paciente = self._controlador_sistema.controlador_pacientes.busca_paciente(cpf_paciente)
            medico = self._controlador_sistema.controlador_medicos.busca_medico(crm_medico)
            # Obter dados da consulta a partir da visão
            dados_consulta = self.__telaconsulta.pega_dados_consulta()
            data = dados_consulta["data"]
            horario = dados_consulta["horario"]

            # Buscar o médico e paciente pelos dados fornecidos
            # medico = self._controlador_sistema.controlador_medico.busca_medico(dados_consulta["medico"])
            # paciente = self._controlador_sistema.controlador_pacientes.busca_paciente(dados_consulta["paciente"])

            # Validar o horário
            if not self.validar_horario(horario):
                raise HorarioInvalido(horario)
    
            # Criar uma nova consulta e verificar conflitos de horário
            nova_consulta = Consulta(randint(0, 1000), paciente, medico, data, horario, medico.sala)
            if not self.horario_disponivel(nova_consulta):
                raise Exception(f"Erro: Conflito de horário na sala {medico.sala.numero} para o horário {horario}.")

            # Adicionar a consulta ao banco de dados
            self.__consulta_DAO.add(nova_consulta)
            self.__telaconsulta.mostra_mensagem("Confirmação", f"Consulta com o médico '{medico.nome}' adicionada com sucesso!")

        except HorarioInvalido as e:
            self.__telaconsulta.mostra_mensagem("Erro", f"Erro: {e}")
        except ValueError as ve:
            self.__telaconsulta.mostra_mensagem("Erro", f"Erro: {ve}")
        except CancelOpException:
            pass
        except Exception as ex:
            self.__telaconsulta.mostra_mensagem("Erro", f"Erro inesperado: {ex}")

    def atualizar_consulta(self):
        try:
            nmr_consulta = self.listar_consultas(selecionar=True)
            if nmr_consulta is not None:
                consulta = self.busca_consulta(nmr_consulta)

            cpf_paciente = self._controlador_sistema.controlador_pacientes.listar_pacientes(selecionar=True)
            crm_medico = self._controlador_sistema.controlador_medicos.listar_medicos(selecionar=True)
            
            #TODO usar metodo get de abstrato.dao para retornar o objeto do banco de dados respectivo
            paciente = self._controlador_sistema.controlador_pacientes.busca_paciente(cpf_paciente)
            medico = self._controlador_sistema.controlador_medicos.busca_medico(crm_medico)

            # paciente = self._controlador_sistema.controlador_pacientes.busca_paciente(novos_dados_consulta["paciente"])
            # medicos = self._controlador_sistema.medico_controlador.busca_medico(novos_dados_consulta["medico"])
            novos_dados = self.__telaconsulta.pega_dados_consulta()
            data = novos_dados["data"]
            horario = novos_dados["horario"]

            if not self.validar_horario(horario):
                raise HorarioInvalido(horario)

            consulta.paciente = paciente
            consulta.medico = medico
            consulta.data = data
            consulta.horario = horario
            consulta.sala = medico.sala

            self.__consulta_DAO.update(consulta)
            self.listar_consultas()
            self.__telaconsulta.mostra_mensagem("Confirmação", f"Consulta número {consulta.numero} atualizada com sucesso!")
        
        except HorarioInvalido as e:
            self.__telaconsulta.mostra_mensagem("Erro", f"Erro: {e}")
        except ConsultaNaoEncontrada as e:
            self.__telaconsulta.mostra_mensagem("Erro", f"Erro: {e}")
        except ValueError as ve:
            self.__telaconsulta.mostra_mensagem("Erro", f"Erro de valor: {ve}")
        except CancelOpException:
            pass

    def remover_consulta(self):
        try:
            nmr_consulta = self.listar_consultas(selecionar=True)

            self.__consulta_DAO.remove(nmr_consulta)
            self.listar_consultas(selecionar=False)
        except CancelOpException:
            pass
        except ValueError as ve:
            self.__telaconsulta.mostra_mensagem("Erro", f"{ve}")

    def busca_consulta(self, nmr_consulta: int):
        consulta = self.__consulta_DAO.get(nmr_consulta)
        if consulta is not None:
            return consulta
        else:
            raise ConsultaNaoEncontrada(nmr_consulta)

    def listar_consultas(self, selecionar = False):
        consultas = self.__consulta_DAO.get_all()
        if not consultas:
            self.__telaconsulta.mostra_mensagem("Erro", "Nenhuma consulta cadastrada.")
            return None 

        consulta_info = [{"numero": consulta.numero,
                                            "paciente": consulta.paciente.nome,
                                            "medico": consulta.medico.nome,
                                            "data": consulta.data,
                                            "horario": consulta.horario,}
                                            for consulta in consultas]
                            
        try:
            return self.__telaconsulta.exibe_lista_consulta(consulta_info, selecionar)
        except CancelOpException:
            return None

    def abre_tela(self):
        lista_opcoes = {1: self.adicionar_consultas, 2: self.atualizar_consulta, 3: self.remover_consulta,
                        4: self.listar_consultas, 0: self.retornar}

        continua = True
        while continua:
            lista_opcoes[self.__telaconsulta.tela_opcoes()]()
