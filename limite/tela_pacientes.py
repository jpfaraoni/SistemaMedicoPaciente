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

    def pega_dados_paciente(self):
        layout = [
            [sg.Text("Nome:"), sg.InputText(key="nome")],
            [sg.Text("Email:"), sg.InputText(key="email")],
            [sg.Text("Idade:"), sg.InputText(key="idade")],
            [sg.Text("Cpf:"), sg.InputText(key="cpf")],
            [sg.Button("Confirmar"), sg.Cancel("Cancelar")],
        ]
        window = sg.Window("Cadastrar Usuario", layout)

        button, values = window.read()
        window.close()

        if button in ("Cancelar", None):
            raise CancelOpException()

        try:
            return {
                "nome": values["nome"],
                "email": values["email"],
                "idade": int(values["idade"]),
                "cpf": int(values["cpf"]),
            }
        except ValueError:
            raise ValueError("Dados inválidos.")


    def pega_novos_dados_paciente(self):
        layout = [
            [sg.Text("Novo nome do paciente:"), sg.InputText(key="nome")],
            [sg.Text("Novo email do paciente:"), sg.InputText(key="email")],
            [sg.Text("Nova idade do paciente:"), sg.InputText(key="idade")],
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
                "idade": int(values["idade"]),
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
                layout.append([sg.Text(f"Nome: {paciente['nome']}, Email: {paciente['email']}, Idade: {paciente['idade']}, Cpf: {paciente['cpf']}")])
    
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
