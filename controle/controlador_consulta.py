# Arquivo: controle/controlador_consulta.py

from exceptions.cancel_op_exception import CancelOpException
from exceptions.sala_nao_encontrada_exception import SalaNaoEncontrada
from datetime import datetime, timedelta
from exceptions.horario_invalido_exception import HorarioInvalido
from limite.tela_consulta import TelaConsulta
from entidades.paciente import Paciente
from entidades.medico import Medico
from controle.controlador_entidade_abstrata import ControladorEntidadeAbstrata
from DAO.consulta_dao import ConsultaDAO
from random import randint
from exceptions.consulta_nao_encontrada_exception import ConsultaNaoEncontrada
from entidades.consulta import Consulta
from exceptions.medico_nao_encontrado_exception import MedicoNaoEncontrado
from exceptions.paciente_nao_encontrado_exception import PacienteNaoEncontrado
# from controle.controlador_medicos import ControladorMedicos


class ControladorConsultas(ControladorEntidadeAbstrata):

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
            # Ignora a própria consulta se estivermos atualizando
            if consulta.numero == nova_consulta.numero:
                continue
                
            # Só verifica conflitos se for na mesma data
            if consulta.data == nova_consulta.data:
                # Combina data e horário da consulta existente
                datetime_inicio_existente = datetime.strptime(f"{consulta.data} {consulta.horario}", "%d/%m/%Y %H:%M")
                # Consulta existente também dura 1 hora
                datetime_termino_existente = datetime_inicio_existente + timedelta(hours=1)

                # Verifica conflito na mesma sala
                if consulta.sala.numero == nova_consulta.sala.numero:
                    if (novo_datetime_inicio < datetime_termino_existente and
                            novo_datetime_termino > datetime_inicio_existente):
                        return False  # Conflito de horário na sala
                
                # Verifica conflito com o mesmo médico
                if consulta.medico.crm == nova_consulta.medico.crm:
                    if (novo_datetime_inicio < datetime_termino_existente and
                            novo_datetime_termino > datetime_inicio_existente):
                        return False  # Conflito de horário para o médico
                
                # Verifica conflito com o mesmo paciente
                if consulta.paciente.cpf == nova_consulta.paciente.cpf:
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

    def pode_cancelar_consulta(self, consulta: Consulta) -> bool:
        """
        Valida se uma consulta pode ser cancelada respeitando a antecedência mínima de 1 hora.
        
        Regra: O paciente não pode cancelar se:
        - A data da consulta for igual à data atual E
        - O horário atual + 1 hora for maior ou igual ao horário da consulta
        
        Retorna True se pode cancelar, False caso contrário.
        """
        # Obtém data e horário atuais de forma simples e clara
        agora = datetime.now()
        
        # Combina data e horário da consulta para criar datetime completo
        datetime_consulta = datetime.strptime(f"{consulta.data} {consulta.horario}", "%d/%m/%Y %H:%M")
        
        # Se a consulta for em data/horário passado, não pode cancelar
        if datetime_consulta < agora:
            return False
        
        # Se a consulta for em data futura (não é hoje), pode cancelar
        data_atual_str = agora.strftime("%d/%m/%Y")
        if consulta.data != data_atual_str:
            return True
        
        # Se for na data atual, verifica a antecedência de 1 hora
        # Calcula o horário mínimo permitido (agora + 1 hora)
        horario_minimo_permitido = agora + timedelta(hours=1)
        
        # Pode cancelar apenas se o horário da consulta for depois do horário mínimo permitido
        return datetime_consulta > horario_minimo_permitido

    def validar_triagem(self, paciente: Paciente, medico: Medico) -> bool:
        """
        Valida regras de triagem durante o agendamento.
        
        Regra RF09: Pacientes com idade menor que 16 anos só podem agendar consultas
        com médicos que tenham especialidade = "pediatra".
        
        Retorna True se a triagem é válida (pode agendar), False caso contrário.
        """
        # Verifica se o paciente tem menos de 16 anos
        if paciente.idade < 16:
            # Verifica se o médico é ortopedista (comparação case-insensitive)
            if medico.especialidade.lower() != "pediatria":
                return False
        
        return True

    # --- Lógica de Agendamento ---
    
    def agendar_consulta_logica(self, paciente: Paciente, medico: Medico):
        """
        Lógica central de agendamento, reutilizada por Secretaria e Paciente.
        Recebe os objetos Paciente e Medico e cuida do resto.
        """
        try:
            # Validar regras de triagem antes de prosseguir
            if not self.validar_triagem(paciente, medico):
                self.__telaconsulta.mostra_mensagem(
                    "Erro de Triagem",
                    f"Pacientes com idade menor que 16 anos só podem agendar consultas com médicos pediatras.\n"
                    f"O paciente '{paciente.nome}' tem {paciente.idade} anos e o médico selecionado "
                    f"'{medico.nome}' é especialista em '{medico.especialidade}'.\n"
                    f"Por favor, selecione um médico pediatra."
                )
                return
            
            # Obter dados da consulta a partir da visão
            dados_consulta = self.__telaconsulta.pega_dados_consulta()
            data = dados_consulta["data"]
            horario = dados_consulta["horario"]

            # Validar o horário e data
            if not self.validar_horario(horario):
                raise HorarioInvalido(horario)
            if not self.validar_data(data):
                raise ValueError("Data inválida. Use o formato DD/MM/AAAA")

            # Criar uma nova consulta (temporária) para verificar
            nova_consulta = Consulta(randint(0, 100000), paciente, medico, data, horario, medico.sala)
            
            # Verificar conflitos de horário
            if not self.horario_disponivel(nova_consulta):
                # A exceção aqui é muito genérica, vamos ser mais específicos
                raise ValueError(f"Erro: Conflito de horário detectado para {horario} no dia {data}.")

            # Adicionar a consulta ao banco de dados
            self.__consulta_DAO.add(nova_consulta)
            self.__telaconsulta.mostra_mensagem("Confirmação", f"Consulta com o médico '{medico.nome}' adicionada com sucesso!")
        except ValueError as ve:
            self.__telaconsulta.mostra_mensagem("Erro", f"{ve}")
        except CancelOpException:
            pass
    # --- Métodos de SECRETÁRIA ---

    def adicionar_consultas_secretaria(self):
        try:
            # 1. Secretária seleciona AMBOS
            cpf_paciente = self._controlador_sistema.controlador_pacientes.listar_pacientes(selecionar=True)
            if cpf_paciente is None: raise CancelOpException()
            
            crm_medico = self._controlador_sistema.controlador_medicos.listar_medicos(selecionar=True)
            if crm_medico is None: raise CancelOpException()

            paciente = self._controlador_sistema.controlador_pacientes.busca_paciente(cpf_paciente)
            medico = self._controlador_sistema.controlador_medicos.busca_medico(crm_medico)
            
            # 2. Chama a lógica central de agendamento
            self.agendar_consulta_logica(paciente, medico)

        except (HorarioInvalido, ValueError, PacienteNaoEncontrado, MedicoNaoEncontrado) as e:
            self.__telaconsulta.mostra_mensagem("Erro", f"{e}")
        except CancelOpException:
            pass # Usuário cancelou
        except Exception as ex:
            self.__telaconsulta.mostra_mensagem("Erro", f"Erro inesperado: {ex}")

    def atualizar_consulta_secretaria(self):
        """
        Lógica de atualização completa para a secretária.
        Permite selecionar a consulta e alterar tudo.
        """
        try:
            # 1. Secretária seleciona a consulta para editar
            nmr_consulta = self.listar_consultas(selecionar=True)
            if nmr_consulta is None:
                return # Cancelou
            
            consulta = self.busca_consulta(nmr_consulta)

            # 2. Secretária seleciona o NOVO paciente (ou o mesmo)
            cpf_paciente = self._controlador_sistema.controlador_pacientes.listar_pacientes(selecionar=True)
            if cpf_paciente is None: raise CancelOpException()

            # 3. Secretária seleciona o NOVO médico (ou o mesmo)
            crm_medico = self._controlador_sistema.controlador_medicos.listar_medicos(selecionar=True)
            if crm_medico is None: raise CancelOpException()
            
            paciente = self._controlador_sistema.controlador_pacientes.busca_paciente(cpf_paciente)
            medico = self._controlador_sistema.controlador_medicos.busca_medico(crm_medico)

            # 4. Pega nova data e horário
            novos_dados = self.__telaconsulta.pega_dados_consulta()
            data = novos_dados["data"]
            horario = novos_dados["horario"]

            # 5. Valida data e horário
            if not self.validar_horario(horario):
                raise HorarioInvalido(horario)
            if not self.validar_data(data):
                raise ValueError("Data inválida.")

            # 6. Atualiza o objeto 'consulta'
            consulta.paciente = paciente
            consulta.medico = medico
            consulta.data = data
            consulta.horario = horario
            consulta.sala = medico.sala # Sala é sempre atrelada ao médico

            # 7. Verifica disponibilidade (importante!)
            if not self.horario_disponivel(consulta):
                 raise ValueError(f"Erro: Conflito de horário detectado para {horario} no dia {data}.")

            self.__consulta_DAO.update(consulta)
            self.listar_consultas(selecionar=False) # Mostra lista atualizada
            self.__telaconsulta.mostra_mensagem("Confirmação", f"Consulta número {consulta.numero} atualizada com sucesso!")
        
        except (HorarioInvalido, ConsultaNaoEncontrada, PacienteNaoEncontrado, MedicoNaoEncontrado, ValueError) as e:
            self.__telaconsulta.mostra_mensagem("Erro", f"{e}")
        except CancelOpException:
            pass

    def remover_consulta_secretaria(self):
        """ Lógica de remoção para a secretária. """
        try:
            nmr_consulta = self.listar_consultas(selecionar=True)
            if nmr_consulta is None:
                return # Cancelou

            self.__consulta_DAO.remove(nmr_consulta)
            self.listar_consultas(selecionar=False) # Mostra lista atualizada
            self.__telaconsulta.mostra_mensagem("Confirmação", "Consulta removida com sucesso.")
        except CancelOpException:
            pass
        except ValueError as ve:
            self.__telaconsulta.mostra_mensagem("Erro", f"{ve}")

    # --- Métodos de PACIENTE ---

    def adicionar_consultas_paciente(self, cpf_logado: int):
        try:
            # 1. Paciente já é conhecido
            paciente = self._controlador_sistema.controlador_pacientes.busca_paciente(cpf_logado)
            
            # 2. Paciente SÓ seleciona o MÉDICO
            crm_medico = self._controlador_sistema.controlador_medicos.listar_medicos(selecionar=True)
            if crm_medico is None: raise CancelOpException()
            
            medico = self._controlador_sistema.controlador_medicos.busca_medico(crm_medico)

            # 3. Chama a lógica central de agendamento
            self.agendar_consulta_logica(paciente, medico)
            
        except (HorarioInvalido, ValueError, MedicoNaoEncontrado) as e:
            self.__telaconsulta.mostra_mensagem("Erro", f"{e}")
        except CancelOpException:
            pass

    def atualizar_consulta_paciente(self, cpf_logado: int):
        """
        Lógica de atualização restrita para o paciente.
        Só pode alterar data, horário ou médico de suas próprias consultas.
        """
        try:
            # 1. Lista APENAS as consultas do paciente logado
            nmr_consulta = self.listar_consultas_paciente(cpf_logado, selecionar=True)
            if nmr_consulta is None:
                return # Cancelou
            
            consulta = self.busca_consulta(nmr_consulta)
            paciente = consulta.paciente # O paciente é fixo

            # 2. Paciente seleciona o NOVO médico (ou o mesmo)
            crm_medico = self._controlador_sistema.controlador_medicos.listar_medicos(selecionar=True)
            if crm_medico is None: raise CancelOpException()
            
            medico = self._controlador_sistema.controlador_medicos.busca_medico(crm_medico)

            # 3. Pega nova data e horário
            novos_dados = self.__telaconsulta.pega_dados_consulta()
            data = novos_dados["data"]
            horario = novos_dados["horario"]

            # 4. Valida data e horário
            if not self.validar_horario(horario):
                raise HorarioInvalido(horario)
            if not self.validar_data(data):
                raise ValueError("Data inválida.")

            # 5. Atualiza o objeto 'consulta'
            consulta.paciente = paciente # Continua o mesmo
            consulta.medico = medico
            consulta.data = data
            consulta.horario = horario
            consulta.sala = medico.sala

            # 6. Verifica disponibilidade
            if not self.horario_disponivel(consulta):
                 raise ValueError(f"Erro: Conflito de horário detectado para {horario} no dia {data}.")

            self.__consulta_DAO.update(consulta)
            self.listar_consultas_paciente(cpf_logado, selecionar=False) # Mostra lista atualizada
            self.__telaconsulta.mostra_mensagem("Confirmação", f"Consulta número {consulta.numero} atualizada com sucesso!")
        
        except (HorarioInvalido, ConsultaNaoEncontrada, MedicoNaoEncontrado, ValueError) as e:
            self.__telaconsulta.mostra_mensagem("Erro", f"{e}")
        except CancelOpException:
            pass

    def remover_consulta_paciente(self, cpf_logado: int):
        """ Lógica de remoção restrita para o paciente com validação de antecedência mínima. """
        try:
            # 1. Lista APENAS as consultas do paciente logado
            nmr_consulta = self.listar_consultas_paciente(cpf_logado, selecionar=True)
            if nmr_consulta is None:
                return # Cancelou

            # 2. Busca a consulta para validar a antecedência
            consulta = self.busca_consulta(nmr_consulta)
            
            # 3. Valida se pode cancelar respeitando a antecedência mínima de 1 hora
            if not self.pode_cancelar_consulta(consulta):
                self.__telaconsulta.mostra_mensagem(
                    "Erro", 
                    "Não é possível cancelar esta consulta. É necessário cancelar com pelo menos 1 hora de antecedência."
                )
                return

            # 4. Remove a consulta selecionada
            self.__consulta_DAO.remove(nmr_consulta)
            self.listar_consultas_paciente(cpf_logado, selecionar=False) # Mostra lista atualizada
            self.__telaconsulta.mostra_mensagem("Confirmação", "Consulta removida com sucesso.")
        except ConsultaNaoEncontrada as e:
            self.__telaconsulta.mostra_mensagem("Erro", f"{e}")
        except CancelOpException:
            pass
        except ValueError as ve:
            self.__telaconsulta.mostra_mensagem("Erro", f"{ve}")

    # --- Métodos de Listagem (Genéricos e Restritos) ---

    def busca_consulta(self, nmr_consulta: int):
        consulta = self.__consulta_DAO.get(nmr_consulta)
        if consulta is not None:
            return consulta
        else:
            raise ConsultaNaoEncontrada(nmr_consulta)

    def listar_consultas(self, selecionar = False):
        """ Lista TODAS as consultas (Visão da Secretária). """
        consultas = self.__consulta_DAO.get_all()
        if not consultas:
            self.__telaconsulta.mostra_mensagem("Erro", "Nenhuma consulta cadastrada.")
            return None 

        # Formata os dados para a tela
        consulta_info = [{"numero": consulta.numero,
                          "paciente": consulta.paciente.nome,
                          "medico": consulta.medico.nome,
                          "data": consulta.data,
                          "horario": consulta.horario}
                         for consulta in consultas]
                            
        try:
            return self.__telaconsulta.exibe_lista_consulta(consulta_info, selecionar)
        except CancelOpException:
            return None

    def listar_consultas_paciente(self, cpf_logado: int, selecionar=False):
        """ Lista APENAS as consultas do paciente logado. """
        consultas_todas = self.__consulta_DAO.get_all()
        
        # Filtra a lista
        consultas_filtradas = [c for c in consultas_todas if c.paciente.cpf == cpf_logado]
        
        if not consultas_filtradas:
            self.__telaconsulta.mostra_mensagem("Aviso", "Você não possui nenhuma consulta agendada.")
            return None 

        # Formata os dados para a tela
        consulta_info = [{"numero": consulta.numero,
                          "paciente": consulta.paciente.nome,
                          "medico": consulta.medico.nome,
                          "data": consulta.data,
                          "horario": consulta.horario}
                         for consulta in consultas_filtradas]
                            
        try:
            return self.__telaconsulta.exibe_lista_consulta(consulta_info, selecionar)
        except CancelOpException:
            return None

    def listar_consultas_medico(self, crm_logado: int, selecionar=False):
        """ Lista APENAS as consultas (agenda) do médico logado. """
        consultas_todas = self.__consulta_DAO.get_all()
        
        # Filtra a lista
        consultas_filtradas = [c for c in consultas_todas if c.medico.crm == crm_logado]
        
        if not consultas_filtradas:
            self.__telaconsulta.mostra_mensagem("Aviso", "Você não possui nenhuma consulta em sua agenda.")
            return None 

        # Formata os dados para a tela
        consulta_info = [{"numero": consulta.numero,
                          "paciente": consulta.paciente.nome,
                          "medico": consulta.medico.nome,
                          "data": consulta.data,
                          "horario": consulta.horario}
                         for consulta in consultas_filtradas]
                            
        try:
            return self.__telaconsulta.exibe_lista_consulta(consulta_info, selecionar)
        except CancelOpException:
            return None

    # --- Ponto de Entrada Principal ---

    def abre_tela(self):
        # Este método é chamado pelo ControladorSistema,
        # que JÁ filtrou o usuário.
        
        # Busca o usuário logado no ControladorSistema
        usuario_logado = self._controlador_sistema.usuario_logado
        
        opcoes = {}
        if usuario_logado.tipo_usuario == 'secretaria':
            opcoes = {1: self.adicionar_consultas_secretaria, 
                      2: self.atualizar_consulta_secretaria, # Nome atualizado
                      3: self.remover_consulta_secretaria,   # Nome atualizado
                      4: self.listar_consultas, 
                      0: self.retornar}
                      
        elif usuario_logado.tipo_usuario == 'paciente':
            cpf_logado = usuario_logado.id_entidade
            opcoes = {1: lambda: self.adicionar_consultas_paciente(cpf_logado), 
                      2: lambda: self.atualizar_consulta_paciente(cpf_logado),
                      3: lambda: self.remover_consulta_paciente(cpf_logado),
                      4: lambda: self.listar_consultas_paciente(cpf_logado, selecionar=False), # Adicionado selecionar=False
                      0: self.retornar}
        
        elif usuario_logado.tipo_usuario == 'medico':
            crm_logado = usuario_logado.id_entidade
            opcoes = {
                      4: lambda: self.listar_consultas_medico(crm_logado, selecionar=False), # Adicionado selecionar=False
                      # 5: self.sugerir_plano_terapia (futuro)
                      0: self.retornar}

        continua = True
        while continua:
            # A tela de consulta agora é dinâmica
            opcao = self.__telaconsulta.tela_opcoes(usuario_logado.tipo_usuario)
            
            if opcao == 0:
                self.retornar()
                continua = False
            else:
                funcao_escolhida = opcoes.get(opcao)
                if funcao_escolhida:
                    funcao_escolhida()
                else:
                    # Se a opção não for 0 e não estiver no dicionário (ex: Paciente clica 2 e não há 2)
                    self.__telaconsulta.mostra_mensagem("Aviso", "Opção não disponível para este tipo de usuário.")