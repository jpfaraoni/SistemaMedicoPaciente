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
            [sg.Button("Remover      Médico", key=3, size=(11, 1.15), font=("Helvetica", 13))],
            [sg.Button("Listar      Médicos", key=4, size=(11, 1.15), font=("Helvetica", 13))],
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

    def pega_dados_medicos(self):
        layout = [
            [sg.Text("CRM:"), sg.InputText(key="crm")],
            [sg.Text("Nome:"), sg.InputText(key="nome")],
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
                "crm": int(values["crm"]),
                "nome": values["nome"],
                "especialidade": values["especialidade"],
                "expediente_inicial": values["expediente_inicial"],
                "expediente_final": values["expediente_final"],
            }
        except ValueError:
            raise ValueError("Dados inválidos.")

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
        
        # Se nenhuma sala foi selecionada e o usuário confirmou, levanta exceção
        raise CancelOpException()


    def pega_novos_dados_medicos(self):
        layout = [
            [sg.Text("Novo nome do médico:"), sg.InputText(key="nome")],
            [sg.Text("Novo especialidade do médico:"), sg.InputText(key="especialidade")],
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

        return values["cpf"]


    def exibe_lista_medicos(self, medicos, selecionar=False):
        if not medicos:
            self.__mostra_mensagem("Erro", "Nenhuma médico cadastrado.")
            return

        layout = [[sg.Text("Médicos cadastrados:")]]
        for medico in medicos:
            if selecionar:
                layout.append([
                    sg.Radio(
                        f"CRM: {medico['crm']}, Nome: {medico['nome']}, Especialidade: {medico['especialidade']}, Expediente: {medico['expediente_inicial']}-{medico['expediente_final']}, Sala: {medico['sala']}",
                        "MÉDICOS",
                        key=int(medico['crm'])
                    )
                ])
            else:
                layout.append([sg.Text(f"CRM: {medico['crm']}, Nome: {medico['nome']}, Especialidade: {medico['especialidade']}, Expediente: {medico['expediente_inicial']}-{medico['expediente_final']}, Sala: {medico['sala']}")])
    
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
        
        # Se nenhum médico foi selecionado e o usuário confirmou, levanta exceção
        if selecionar:
            raise CancelOpException()
