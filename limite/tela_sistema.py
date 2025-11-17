import PySimpleGUI as sg

class TelaSistema:
    def __init__(self):
        pass
    
    def tela_opcoes(self, tipo_usuario: str): # Recebe o tipo de usuário
        """
        Exibe a interface gráfica do menu principal do sistema.

        Retorna:
            int: Código da opção selecionada pelo usuário.
        """
        sg.ChangeLookAndFeel('Material1')
        layout_esquerda = [
            [sg.Image(filename='limite/imagens/imagem_sistema_pequena..png')] #
        ]
        # --- MONTAGEM DINÂMICA DO MENU ---
        layout_direita = []
        if tipo_usuario == 'secretaria':
            layout_direita = [
                [sg.Button("Gerenciar Pacientes", key=1, size=(11, 2), font=("Helvetica", 13))],
                [sg.Button("Gerenciar Médicos", key=2, size=(11, 2), font=("Helvetica", 13))],
                [sg.Button("Gerenciar Consultas", key=3, size=(11, 2), font=("Helvetica", 13))],
            ]
        elif tipo_usuario == 'paciente':
            layout_direita = [
                [sg.Button("Meus Dados", key=1, size=(11, 2), font=("Helvetica", 13))], # Botão 1
                [sg.Button("Minhas Consultas", key=3, size=(11, 2), font=("Helvetica", 13))], # Botão 3
            ]
        elif tipo_usuario == 'medico':
            layout_direita = [
                [sg.Button("Meus Dados", key=2, size=(11, 2), font=("Helvetica", 13))], # Botão 2
                [sg.Button("Minhas Consultas", key=3, size=(11, 2), font=("Helvetica", 13))], # Botão 3
            ]
        # Botão de Sair/Logout é comum a todos
        layout_direita.append([sg.Button("Sair", key=0, size=(11, 2), font=("Helvetica", 13))])
        # --- FIM DA MONTAGEM ---
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
