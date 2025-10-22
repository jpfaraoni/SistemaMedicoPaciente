import PySimpleGUI as sg
from exceptions.cancel_op_exception import CancelOpException
from limite.abstract_tela import AbstractTela


class TelaConsulta(AbstractTela):
    def __init__(self, tela_sistema):
        super().__init__(tela_sistema)

    def tela_opcoes(self):
        sg.change_look_and_feel('Material1')

        layout_esquerda = [
            [sg.Image(filename='limite/imagens/imagem_sistema_pequena..png')]
        ]

        layout_direita = [
            [sg.Button("Agendar Consulta", key=1, size=(11, 1.15), font=("Helvetica", 13))],
            [sg.Button("Atualizar Dados Consulta", key=2, size=(11, 1.15), font=("Helvetica", 13))],
            [sg.Button("Cancelar Consulta", key=3, size=(11, 1.15), font=("Helvetica", 13))],
            [sg.Button("Listar    Consultas", key=4, size=(11, 1.15), font=("Helvetica", 13))],
            [sg.Button("Sair", key=0, size=(11, 1.15), font=("Helvetica", 13))],
        ]

        layout = [
            [sg.Column(layout_direita),
             sg.VSeparator(),
             sg.Column(layout_esquerda)]
        ]

        window = sg.Window("Menu Consulta", layout, size=(600, 400), finalize=True)

        event, _ = window.read()
        window.close()
        return event if event is not None else 0

    def pega_dados_consulta(self):
        layout = [
            [sg.Text("Data:"), sg.InputText(key="data")],
            [sg.Text("Horário:"), sg.InputText(key="horario")],
            [sg.Button("Confirmar"), sg.Cancel("Cancelar")],
        ]
        window = sg.Window("Agendar Consulta", layout)

        button, values = window.read()
        window.close()

        if button in ("Cancelar", None):
            raise CancelOpException()

        try:
            return {
                "data": values["data"],
                "horario": values["horario"],
            }
        except ValueError:
            raise ValueError("Dados inválidos.")


    # def pega_novos_dados_paciente(self):
    #     layout = [
    #         [sg.Text("Novo nome do paciente:"), sg.InputText(key="nome")],
    #         [sg.Text("Novo email do paciente:"), sg.InputText(key="email")],
    #         [sg.Text("Nova idade do paciente:"), sg.InputText(key="idade")],
    #         [sg.Button("Confirmar"), sg.Button("Cancelar")],
    #     ]
    #     window = sg.Window("Atualizar Paciente", layout)

    #     button, values = window.read()
    #     window.close()

    #     if button in ("Cancelar", None):
    #         raise CancelOpException()

    #     try:
    #         return {
    #             "nome": values["nome"],
    #             "email": values["email"],
    #             "idade": int(values["idade"]),
    #         }
    #     except ValueError:
    #         raise ValueError("Dados inválidos.")

    # def seleciona_consulta(self):
    #     layout = [
    #         [sg.Text("Digite o cpf do paciente que deseja selecionar:"), sg.InputText(key="cpf")],
    #         [sg.Button("Confirmar"), sg.Button("Cancelar")],
    #     ]
    #     window = sg.Window("Selecionar Paciente", layout)

    #     button, values = window.read()
    #     window.close()

    #     if button in ("Cancelar", None):
    #         raise CancelOpException()

    #     return values["cpf"]


    def exibe_lista_consulta(self, consultas, selecionar=False):
        if not consultas:
            self.__mostra_mensagem("Erro", "Nenhuma consulta cadastrada.")
            return

        layout = [[sg.Text("Consultas cadastrados:")]]
        for consulta in consultas:
            if selecionar:
                layout.append([
                    sg.Radio(
                        f"Número: {consulta['numero']}, Paciente: {consulta['paciente']}, Médico: {consulta['medico']}, Data: {consulta['data']}, Horário: {consulta['horario']}",
                        "CONSULTAS",
                        key=int(consulta['numero'])
                    )
                ])
            else:
                layout.append([sg.Text(f"Número: {consulta['numero']}, Paciente: {consulta['paciente']}, Médico: {consulta['medico']}, Data: {consulta['data']}, Horário: {consulta['horario']}")])
    
        if selecionar:
            layout.append([sg.Button("Confirmar"), sg.Cancel("Cancelar")])
        else:
            layout.append([sg.Button("Fechar")])

        window = sg.Window("Lista de Consultas", layout)
        button, values = window.read()
        window.close()

        if button in (None, "Cancelar"):
            raise CancelOpException()

        for key, selected in values.items():
            if selected:
                return int(key)
