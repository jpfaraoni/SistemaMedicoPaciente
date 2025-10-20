import PySimpleGUI as sg

class TelaSistema:
    def __init__(self):
        pass

    def tela_opcoes(self):
        """
        Exibe a interface gráfica do menu principal do sistema.

        Retorna:
            int: Código da opção selecionada pelo usuário.
        """
        sg.ChangeLookAndFeel('LightGrey1')
        layout_esquerda = [
            [sg.Image(filename='limite/imagens/imagemmedicopaciente.png')]
        ]
        layout_direita = [
            [sg.Button("Espaço Paciente", key=1, size=(9, 1), font=("Helvetica", 12))],
            [sg.Button("Espaço Médico", key=2, size=(9, 1), font=("Helvetica", 12))],
            [sg.Button("Relatórios", key=3, size=(9, 1), font=("Helvetica", 12))],
            [sg.Button("Prescrições", key=4, size=(9, 1), font=("Helvetica", 12))],
            [sg.Button("Finalizar Sistema", size=(9, 1), font=("Helvetica", 12))],
        ]

        layout = [
            [sg.Column(layout_direita),
            sg.VSeparator(),
            sg.Column(layout_esquerda)]
            ]
        # Cria a janela com o layout definido
        window = sg.Window("Menu Principal", layout, finalize=True)

        # Lê o evento do botão pressionado
        event, _ = window.read()
        window.close()

        # Retorna o código da opção selecionada
        return event if isinstance(event, int) else 0
