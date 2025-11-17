import PySimpleGUI as sg
from exceptions.cancel_op_exception import CancelOpException
from limite.abstract_tela import AbstractTela


class TelaPacientes(AbstractTela):
    def __init__(self, tela_sistema):
        super().__init__(tela_sistema)

    def tela_opcoes(self):
        sg.change_look_and_feel('Material1')

        layout_esquerda = [
            [sg.Image(filename='limite/imagens/imagem_sistema_pequena..png')]
        ]

        layout_direita = [
            [sg.Button("Adicionar Paciente", key=1, size=(11, 1.15), font=("Helvetica", 13))],
            [sg.Button("Atualizar Dados Paciente", key=2, size=(11, 1.15), font=("Helvetica", 13))],
            [sg.Button("Remover Paciente", key=3, size=(11, 1.15), font=("Helvetica", 13))],
            [sg.Button("Listar    Pacientes", key=4, size=(11, 1.15), font=("Helvetica", 13))],
            [sg.Button("Sair", key=0, size=(11, 1.15), font=("Helvetica", 13))],
        ]

        layout = [
            [sg.Column(layout_direita),
             sg.VSeparator(),
             sg.Column(layout_esquerda)]
        ]

        window = sg.Window("Menu Filme", layout, size=(600, 400), finalize=True)

        event, _ = window.read()
        window.close()
        return event if event is not None else 0

    # --- NOVO MÉTODO PARA O MENU DO PACIENTE ---
    def tela_opcoes_paciente(self):
        """
        Mostra um menu de opções restrito para o paciente logado.
        """
        sg.change_look_and_feel('Material1')
        
        layout_esquerda = [
            [sg.Image(filename='limite/imagens/imagem_sistema_pequena..png')]
        ]
        
        # Menu restrito
        layout_direita = [
            [sg.Button("Ver Meus Dados", key=1, size=(15, 1.15), font=("Helvetica", 13))],
            [sg.Button("Atualizar Meus Dados", key=2, size=(15, 1.15), font=("Helvetica", 13))],
            [sg.Button("Sair", key=0, size=(15, 1.15), font=("Helvetica", 13))],
        ]

        layout = [
            [sg.Column(layout_direita),
             sg.VSeparator(),
             sg.Column(layout_esquerda)]
        ]

        # O key=1 e key=2 vão mapear para ver_meus_dados e atualizar_meus_dados
        # no dicionário 'lista_opcoes' do 'abre_tela_paciente_logado'
        
        window = sg.Window("Meu Perfil", layout, size=(600, 400), finalize=True)
        event, _ = window.read()
        window.close()
        return event if event is not None else 0

    def pega_dados_paciente(self):
        layout = [
            [sg.Text("Nome:"), sg.InputText(key="nome")],
            [sg.Text("Email:"), sg.InputText(key="email")],
            [sg.Text("Cpf:"), sg.InputText(key="cpf")],
            [sg.Text("Contato (telefone):"), sg.InputText(key="contato")],
            [sg.Text("Data de Nascimento(DD/MM/AAAA):"), sg.InputText(key="data_nascimento")],
            [sg.Text("Genero:"), sg.InputText(key="genero")],
            [sg.Text("Convenio:"), sg.InputText(key="convenio")],
            [sg.Checkbox("Deficiente:", key="deficiente")],
            [sg.Text("Tipo Sanguíneo:"), sg.InputText(key="tipo_sanguineo")],
            [sg.Button("Confirmar"), sg.Cancel("Cancelar")],

        ]
        window = sg.Window("Cadastrar Paciente", layout)

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
                "convenio": values["convenio"],
                "deficiente": values["deficiente"],
                "tipo_sanguineo": values["tipo_sanguineo"],
            }
        except ValueError:
            raise ValueError("Dados inválidos.")


    def pega_novos_dados_paciente(self):
        layout = [
            [sg.Text("Novo nome do paciente:"), sg.InputText(key="nome")],
            [sg.Text("Novo email do paciente:"), sg.InputText(key="email")],
            [sg.Text("Novo contato (número) do paciente:"), sg.InputText(key="contato")],
            [sg.Text("Nova data de nascimento do paciente:"), sg.InputText(key="data_nascimento")],
            [sg.Text("Novo gênero do paciente:"), sg.InputText(key="genero")],
            [sg.Text("Novo convenio do paciente:"), sg.InputText(key="convenio")],
            [sg.Checkbox("Deficiente:", key="deficiente")],
            [sg.Checkbox("Novo tipo sanguíneo do paciente:"), sg.InputText(key="tipo_sanguineo")],
            [sg.Button("Confirmar"), sg.Button("Cancelar")],
        ]
        window = sg.Window("Atualizar Paciente", layout)

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
                "convenio": values["convenio"],
                "deficiente": values["deficiente"],
                "tipo_sanguineo": values["tipo_sanguineo"],
            }
        except ValueError:
            raise ValueError("Dados inválidos.")

    def seleciona_paciente(self):
        layout = [
            [sg.Text("Digite o cpf do paciente que deseja selecionar:"), sg.InputText(key="cpf")],
            [sg.Button("Confirmar"), sg.Button("Cancelar")],
        ]
        window = sg.Window("Selecionar Paciente", layout)

        button, values = window.read()
        window.close()

        if button in ("Cancelar", None):
            raise CancelOpException()

        return values["cpf"]


    def exibe_lista_pacientes(self, pacientes, selecionar=False):
        if not pacientes:
            self.__mostra_mensagem("Erro", "Nenhuma paciente cadastrado.")
            return

        layout = [[sg.Text("Pacientes cadastrados:")]]
        for paciente in pacientes:
            if selecionar:
                layout.append([
                    sg.Radio(
                        f"Nome: {paciente['nome']}, Email: {paciente['email']} min, Idade: {paciente['idade']}, "
                        f"Cpf: {paciente['cpf']}",
                        "PACIENTES",
                        key=int(paciente['cpf'])
                    )
                ])
            else:
                layout.append([sg.Text(f"Nome: {paciente['nome']}, Email: {paciente['email']}, Cpf: {paciente['cpf']} Contato: {paciente['contato']} Idade: {paciente['idade']}, Genero: {paciente['genero']}, Convenio: {paciente['convenio']}, Deficiente: {paciente['deficiente']}, Tipo Sanguíneo: {paciente['tipo_sanguineo']}")])
    
        if selecionar:
            layout.append([sg.Button("Confirmar"), sg.Cancel("Cancelar")])
        else:
            layout.append([sg.Button("Fechar")])

        window = sg.Window("Lista de Pacientes", layout)
        button, values = window.read()
        window.close()

        if button in (None, "Cancelar", "Fechar"):
            raise CancelOpException()

        for key, selected in values.items():
            if selected:
                return int(key)
        
        # Se nenhum paciente foi selecionado e o usuário confirmou, levanta exceção
        if selecionar:
            raise CancelOpException()
