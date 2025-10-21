from entidades.medico import Medico
from DAO.medico_dao import MedicoDAO
from DAO.sala_dao import SalaDAO
from exceptions.medico_nao_encontrado_exception import MedicoNaoEncontrado
from exceptions.cancel_op_exception import CancelOpException

class ControladorMedicos:
    def __init__(self, controlador_sistema):
        self.__sistema_controlador = controlador_sistema
        self.__medico_DAO = MedicoDAO()
        self.__sala_DAO = SalaDAO()

    def adicionar_medico(self):
        try:
            # Obter dados do médico
            crm = int(input("Digite o CRM do médico: "))
            nome = input("Digite o nome do médico: ")
            especialidade = input("Digite a especialidade: ")
            expediente_inicial = input("Digite o horário de início do expediente (HH:MM): ")
            expediente_final = input("Digite o horário de fim do expediente (HH:MM): ")
            
            # Listar salas disponíveis
            print("\nSalas disponíveis:")
            self.listar_salas()
            numero_sala = int(input("Digite o número da sala: "))
            
            # Buscar a sala
            sala = self.__sala_DAO.get(numero_sala)
            if sala is None:
                print(f"Sala {numero_sala} não encontrada.")
                return
            
            # Verificar se médico já existe
            try:
                self.busca_medico(crm)
                print(f"Médico com CRM {crm} já está cadastrado.")
                return
            except MedicoNaoEncontrado:
                pass  # Médico não existe, pode criar
            
            # Criar novo médico
            novo_medico = Medico(crm, nome, especialidade, expediente_inicial, expediente_final, sala)
            self.__medico_DAO.add(novo_medico)
            print(f"Médico '{nome}' foi adicionado com sucesso!")
            
        except ValueError as ve:
            print(f"Erro: {ve}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def atualizar_medico(self):
        try:
            # Listar médicos para seleção
            medicos = self.listar_medicos(selecionar=True)
            if medicos is None:
                return
            
            crm = medicos
            medico = self.busca_medico(crm)
            
            print(f"\nAtualizando dados do médico: {medico}")
            
            # Obter novos dados
            novo_nome = input(f"Nome atual ({medico.nome}): ") or medico.nome
            nova_especialidade = input(f"Especialidade atual ({medico.especialidade}): ") or medico.especialidade
            novo_expediente_inicial = input(f"Expediente inicial atual ({medico.expediente_inicial}): ") or medico.expediente_inicial
            novo_expediente_final = input(f"Expediente final atual ({medico.expediente_final}): ") or medico.expediente_final
            
            # Atualizar dados
            medico.nome = novo_nome
            medico.especialidade = nova_especialidade
            medico.expediente_inicial = novo_expediente_inicial
            medico.expediente_final = novo_expediente_final
            
            self.__medico_DAO.update(medico)
            print(f"Médico CRM '{crm}' atualizado com sucesso!")
            
        except MedicoNaoEncontrado as e:
            print(f"Erro: {e}")
        except ValueError as ve:
            print(f"Erro: {ve}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def remover_medico(self):
        try:
            # Listar médicos para seleção
            medicos = self.listar_medicos(selecionar=True)
            if medicos is None:
                return
            
            crm = medicos
            medico = self.busca_medico(crm)
            
            confirmacao = input(f"Tem certeza que deseja remover o médico {medico.nome} (CRM: {crm})? (s/n): ")
            if confirmacao.lower() == 's':
                self.__medico_DAO.remove(crm)
                print(f"Médico CRM '{crm}' foi removido com sucesso.")
            else:
                print("Operação cancelada.")
                
        except MedicoNaoEncontrado as e:
            print(f"Erro: {e}")
        except ValueError as ve:
            print(f"Erro: {ve}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def busca_medico(self, crm: int):
        medicos = self.__medico_DAO.get_all()
        for medico in medicos:
            if medico.crm == crm:
                return medico
        raise MedicoNaoEncontrado(crm)

    def listar_medicos(self, selecionar=False):
        medicos = self.__medico_DAO.get_all()
        if not medicos:
            print("Nenhum médico cadastrado.")
            return None

        medicos_info = []
        for i, medico in enumerate(medicos, 1):
            info = {
                "crm": medico.crm,
                "nome": medico.nome,
                "especialidade": medico.especialidade,
                "expediente_inicial": medico.expediente_inicial,
                "expediente_final": medico.expediente_final,
                "sala": medico.sala.numero
            }
            medicos_info.append(info)
            
            if selecionar:
                print(f"{i}. {medico}")
            else:
                print(f"{i}. {medico}")

        if selecionar:
            try:
                escolha = int(input("\nDigite o número do médico (ou 0 para cancelar): "))
                if escolha == 0:
                    return None
                elif 1 <= escolha <= len(medicos_info):
                    return medicos_info[escolha - 1]["crm"]
                else:
                    print("Opção inválida.")
                    return None
            except ValueError:
                print("Opção inválida.")
                return None
        
        return medicos_info

    def listar_salas(self):
        """Lista todas as salas disponíveis"""
        salas = self.__sala_DAO.get_all()
        if not salas:
            print("Nenhuma sala cadastrada.")
            return
        
        for sala in salas:
            print(f"Sala {sala.numero} - Andar {sala.andar} (Capacidade: {sala.capacidade})")

    def listar_medicos_por_especialidade(self, especialidade: str):
        """Lista médicos de uma especialidade específica"""
        medicos = self.__medico_DAO.get_all()
        medicos_especialidade = [m for m in medicos if m.especialidade.lower() == especialidade.lower()]
        
        if not medicos_especialidade:
            print(f"Nenhum médico encontrado para a especialidade '{especialidade}'.")
            return []
        
        print(f"\nMédicos da especialidade '{especialidade}':")
        for medico in medicos_especialidade:
            print(f"- {medico}")
        
        return medicos_especialidade

    def listar_medicos_por_sala(self, numero_sala: int):
        """Lista médicos de uma sala específica"""
        medicos = self.__medico_DAO.get_all()
        medicos_sala = [m for m in medicos if m.sala.numero == numero_sala]
        
        if not medicos_sala:
            print(f"Nenhum médico encontrado na sala {numero_sala}.")
            return []
        
        print(f"\nMédicos da sala {numero_sala}:")
        for medico in medicos_sala:
            print(f"- {medico}")
        
        return medicos_sala

    def verificar_disponibilidade_medico(self, crm: int, horario: str):
        """Verifica se um médico está disponível em um horário específico"""
        try:
            medico = self.busca_medico(crm)
            
            # Verificar se o horário está dentro do expediente
            from datetime import datetime
            horario_consulta = datetime.strptime(horario, "%H:%M").time()
            expediente_inicio = datetime.strptime(medico.expediente_inicial, "%H:%M").time()
            expediente_fim = datetime.strptime(medico.expediente_final, "%H:%M").time()
            
            if expediente_inicio <= horario_consulta < expediente_fim:
                return True
            else:
                return False
                
        except MedicoNaoEncontrado:
            return False
        except ValueError:
            return False

    def popular_medicos_iniciais(self):
        """Popula o arquivo medicos.pkl com médicos iniciais"""
        print("=== Populando arquivo medicos.pkl ===")
        print("Criando médicos iniciais...\n")
        
        try:
            medicos_criados = Medico.popular_medicos()
            
            if medicos_criados > 0:
                print(f"\n✅ Sucesso! {medicos_criados} médicos foram criados e salvos em medicos.pkl")
            else:
                print("\nℹ️  Todos os médicos já existem no arquivo medicos.pkl")
                
        except Exception as e:
            print(f"\n❌ Erro ao popular médicos: {e}")
            print("Verifique se as salas foram criadas primeiro.")

    def menu_medicos(self):
        """Menu principal para gerenciar médicos"""
        while True:
            print("\n" + "="*50)
            print("MENU MÉDICOS")
            print("="*50)
            print("1. Adicionar Médico")
            print("2. Atualizar Médico")
            print("3. Remover Médico")
            print("4. Listar Médicos")
            print("5. Listar por Especialidade")
            print("6. Listar por Sala")
            print("7. Popular Médicos Iniciais")
            print("0. Voltar")
            
            try:
                opcao = int(input("\nEscolha uma opção: "))
                
                if opcao == 1:
                    self.adicionar_medico()
                elif opcao == 2:
                    self.atualizar_medico()
                elif opcao == 3:
                    self.remover_medico()
                elif opcao == 4:
                    self.listar_medicos()
                elif opcao == 5:
                    especialidade = input("Digite a especialidade: ")
                    self.listar_medicos_por_especialidade(especialidade)
                elif opcao == 6:
                    numero_sala = int(input("Digite o número da sala: "))
                    self.listar_medicos_por_sala(numero_sala)
                elif opcao == 7:
                    self.popular_medicos_iniciais()
                elif opcao == 0:
                    break
                else:
                    print("Opção inválida.")
                    
            except ValueError:
                print("Opção inválida.")
            except KeyboardInterrupt:
                print("\nOperação cancelada.")
                break