import PySimpleGUI as sg

class TelaSistema:
    def __init__(self):
        pass

    def tela_opcoes(self, tipo_usuario: str, opcoes_disponiveis: list): # 1. Aceita lista de opções
        sg.ChangeLookAndFeel('Material1')
        layout_esquerda = [
            [sg.Image(filename='limite/imagens/imagem_sistema_pequena..png')]
        ]
        
        layout_direita = []
        
        # 2. Constrói botões dinamicamente
        if 1 in opcoes_disponiveis:
            texto = "Gerenciar Pacientes" if tipo_usuario == 'secretaria' else "Meus Dados"
            layout_direita.append([sg.Button(texto, key=1, size=(15, 1.15), font=("Helvetica", 13))])
        
        if 2 in opcoes_disponiveis:
            texto = "Gerenciar Médicos" if tipo_usuario == 'secretaria' else "Meus Dados"
            layout_direita.append([sg.Button(texto, key=2, size=(15, 1.15), font=("Helvetica", 13))])

        if 3 in opcoes_disponiveis:
            texto = "Gerenciar Consultas" if tipo_usuario == 'secretaria' else "Minhas Consultas"
            layout_direita.append([sg.Button(texto, key=3, size=(15, 1.15), font=("Helvetica", 13))])

        if 4 in opcoes_disponiveis:
            texto = "Planos de Terapia"
            layout_direita.append([sg.Button(texto, key=4, size=(15, 1.15), font=("Helvetica", 13))])
        
        layout_direita.append([sg.Button("Sair", key=0, size=(15, 1.15), font=("Helvetica", 13))])

        layout = [
            [sg.Column(layout_direita),
             sg.VSeparator(),
             sg.Column(layout_esquerda)]
            ]
        
        window = sg.Window("Menu Principal", layout, finalize=True)
        event, _ = window.read()
        window.close()
        
        return event if isinstance(event, int) else 0