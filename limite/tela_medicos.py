# Arquivo: limite/tela_medicos.py
import PySimpleGUI as sg
from exceptions.cancel_op_exception import CancelOpException
from limite.abstract_tela import AbstractTela


class TelaMedicos(AbstractTela):
    def __init__(self, tela_sistema):
        super().__init__(tela_sistema)

    def tela_opcoes(self):
        sg.change_look_and_feel('Material1')

        layout_esquerda = [
            [sg.Image(filename='limite/imagens/imagem_sistema_pequena..png')]
        ]

        layout_direita = [
            [sg.Button("Adicionar Médico", key=1, size=(11, 1.15), font=("Helvetica", 13))],
            [sg.Button("Atualizar Dados Médico", key=2, size=(11, 1.15), font=("Helvetica", 13))],
            [sg.Button("Remover Médico", key=3, size=(11, 1.15), font=("Helvetica", 13))],
            [sg.Button("Listar    Médicos", key=4, size=(11, 1.15), font=("Helvetica", 13))],
            [sg.Button("Sair", key=0, size=(11, 1.15), font=("Helvetica", 13))],
        ]

        layout = [
            [sg.Column(layout_direita),
             sg.VSeparator(),
             sg.Column(layout_esquerda)]
        ]

        window = sg.Window("Menu Médicos", layout, size=(600, 400), finalize=True)

        event, _ = window.read()
        window.close()
        return event if event is not None else 0

    # --- NOVO MÉTODO PARA O MENU DO MÉDICO ---
    def tela_opcoes_medico(self):
        """
        Mostra um menu de opções restrito para o médico logado.
        """
        sg.change_look_and_feel('Material1')
        
        layout_esquerda = [
            [sg.Image(filename='limite/imagens/imagem_sistema_pequena..png')]
        ]
        
        # Menu restrito
        layout_direita = [
            [sg.Button("Ver Meus Dados", key=1, size=(15, 1.15), font=("Helvetica", 13))],
            [sg.Button("Atualizar Meus Dados", key=2, size=(15, 1.15), font=("Helvetica", 13))],
            # Adicione aqui o botão 5 para "Sugerir Terapia" se quiser
            [sg.Button("Sair", key=0, size=(15, 1.15), font=("Helvetica", 13))],
        ]

        layout = [
            [sg.Column(layout_direita),
             sg.VSeparator(),
             sg.Column(layout_esquerda)]
        ]
        
        window = sg.Window("Meu Perfil Médico", layout, size=(600, 400), finalize=True)
        event, _ = window.read()
        window.close()
        return event if event is not None else 0

    def pega_dados_medicos(self):
        layout = [
            [sg.Text("Nome:"), sg.InputText(key="nome")],
            [sg.Text("Email:"), sg.InputText(key="email")],
            [sg.Text("CPF:"), sg.InputText(key="cpf")],
            [sg.Text("Contato (telefone):"), sg.InputText(key="contato")],
            [sg.Text("Data de Nascimento(DD/MM/AAAA):"), sg.InputText(key="data_nascimento")],
            [sg.Text("Gênero:"), sg.InputText(key="genero")],
            [sg.HorizontalSeparator()],
            [sg.Text("CRM:"), sg.InputText(key="crm")],
            [sg.Text("Especialidade:"), sg.InputText(key="especialidade")],
            [sg.Text("Expediente Inicial (HH:MM):"), sg.InputText(key="expediente_inicial")],
            [sg.Text("Expediente Final (HH:MM):"), sg.InputText(key="expediente_final")],
            [sg.Button("Confirmar"), sg.Cancel("Cancelar")],
        ]
        window = sg.Window("Cadastrar Médico", layout)

        button, values = window.read()
        window.close()

        if button in ("Cancelar", None):
            raise CancelOpException()

        try:
            return {
                "nome": values["nome"],
                "email": values["email"],
                "cpf": int(values["cpf"]),
                "contato": values["contato"],
                "data_nascimento": values["data_nascimento"],
                "genero": values["genero"],
                "crm": int(values["crm"]),
                "especialidade": values["especialidade"],
                "expediente_inicial": values["expediente_inicial"],
                "expediente_final": values["expediente_final"],
            }
        except ValueError:
            raise ValueError("Dados inválidos (CPF e CRM devem ser números).")

    def seleciona_sala(self, salas):
        """
        Exibe lista de salas usando PySimpleGUI com botões radio para seleção.
        Retorna o número da sala selecionada ou None se cancelar.
        """
        if not salas:
            sg.popup("Erro", "Nenhuma sala cadastrada.")
            raise CancelOpException()

        layout = [[sg.Text("Selecione uma sala:")]]
        for sala in salas:
            layout.append([
                sg.Radio(
                    f"Sala {sala['numero']} - Andar {sala['andar']} (Capacidade: {sala['capacidade']})",
                    "SALAS",
                    key=int(sala['numero'])
                )
            ])
        
        layout.append([sg.Button("Confirmar"), sg.Cancel("Cancelar")])

        window = sg.Window("Selecionar Sala", layout)
        button, values = window.read()
        window.close()

        if button in (None, "Cancelar", "Fechar"):
            raise CancelOpException()

        for key, selected in values.items():
            if selected:
                return int(key)
        
        raise CancelOpException()


    def pega_novos_dados_medicos(self):
        layout = [
            [sg.Text("Novo nome do médico:"), sg.InputText(key="nome")],
            [sg.Text("Novo email do médico:"), sg.InputText(key="email")],
            [sg.Text("Novo contato (telefone):"), sg.InputText(key="contato")],
            [sg.Text("Nova data de nascimento (DD/MM/AAAA):"), sg.InputText(key="data_nascimento")],
            [sg.Text("Novo gênero:"), sg.InputText(key="genero")],
            [sg.HorizontalSeparator()],
            [sg.Text("Nova especialidade do médico:"), sg.InputText(key="especialidade")],
            [sg.Text("Nova expediente inicial do médico:"), sg.InputText(key="expediente_inicial")],
            [sg.Text("Nova expediente final do médico:"), sg.InputText(key="expediente_final")],
            [sg.Button("Confirmar"), sg.Button("Cancelar")],
        ]
        window = sg.Window("Atualizar Médico", layout)

        button, values = window.read()
        window.close()

        if button in ("Cancelar", None):
            raise CancelOpException()

        try:
            return {
                "nome": values["nome"],
                "email": values["email"],
                "contato": values["contato"],
                "data_nascimento": values["data_nascimento"],
                "genero": values["genero"],
                "especialidade": values["especialidade"],
                "expediente_inicial": values["expediente_inicial"],
                "expediente_final": values["expediente_final"],
            }
        except ValueError:
            raise ValueError("Dados inválidos.")

    def seleciona_medico(self):
        layout = [
            [sg.Text("Digite o crm do médico que deseja selecionar:"), sg.InputText(key="crm")],
            [sg.Button("Confirmar"), sg.Button("Cancelar")],
        ]
        window = sg.Window("Selecionar Médico", layout)

        button, values = window.read()
        window.close()

        if button in ("Cancelar", None):
            raise CancelOpException()

        return values["crm"] 


    def exibe_lista_medicos(self, medicos, selecionar=False):
        if not medicos:
            self.__mostra_mensagem("Erro", "Nenhum médico cadastrado.")
            return

        layout = [[sg.Text("Médicos cadastrados:")]]
        for medico in medicos:
            if selecionar:
                layout.append([
                    sg.Radio(
                        # Exibe nome, email, idade (calculada), CRM (chave) e especialidade.
                        f"Nome: {medico['nome']}, Email: {medico['email']}, Idade: {medico['idade']}, CRM: {medico['crm']}, Especialidade: {medico['especialidade']}",
                        "MEDICOS",
                        key=int(medico['crm'])
                    )
                ])
            else:
                layout.append([sg.Text(
                    f"Nome: {medico['nome']}, Email: {medico['email']}, Cpf: {medico['cpf']}, Contato: {medico['contato']}, "
                    f"Idade: {medico['idade']}, Genero: {medico['genero']}, CRM: {medico['crm']}, "
                    f"Especialidade: {medico['especialidade']}, Expediente: {medico['expediente_inicial']}-{medico['expediente_final']}, "
                    f"Sala: {medico['sala'].numero}" # Acessa o atributo 'numero' do objeto Sala
                )])
    
        if selecionar:
            layout.append([sg.Button("Confirmar"), sg.Cancel("Cancelar")])
        else:
            layout.append([sg.Button("Fechar")])

        window = sg.Window("Lista de Médicos", layout)
        button, values = window.read()
        window.close()

        if button in (None, "Cancelar", "Fechar"):
            raise CancelOpException()

        for key, selected in values.items():
            if selected:
                return int(key)
        
        if selecionar:
            raise CancelOpException()