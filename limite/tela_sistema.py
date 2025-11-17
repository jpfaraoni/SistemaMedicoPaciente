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
        sg.ChangeLookAndFeel('Material1')
        layout_esquerda = [
            [sg.Image(filename='limite/imagens/imagem_sistema_pequena..png')]
        ]
        layout_direita = [
            [sg.Button("Gerenciar Pacientes", key=1, size=(11, 2), font=("Helvetica", 13))],
            [sg.Button("Gerenciar Médicos", key=2, size=(11, 2), font=("Helvetica", 13))],
            [sg.Button("Gerenciar Consultas", key=3, size=(11, 2), font=("Helvetica", 13))],
            [sg.Button("Finalizar  Sistema", key=0, size=(11, 2), font=("Helvetica", 13))],
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
