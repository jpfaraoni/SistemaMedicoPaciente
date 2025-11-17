# Arquivo: limite/tela_login.py

import PySimpleGUI as sg
from exceptions.cancel_op_exception import CancelOpException
# Remova a importação de AbstractTela
# from limite.abstract_tela import AbstractTela 

# 1. Mude a definição da classe para não herdar de ninguém
class TelaLogin:
    def __init__(self):
        # 2. Remova a chamada super().__init__()
        pass

    def pega_dados_login(self):
        sg.ChangeLookAndFeel('Material1')
        layout = [
            [sg.Text("Login:", size=(10, 1)), sg.InputText(key="login")],
            [sg.Text("Senha:", size=(10, 1)), sg.InputText(key="senha", password_char='*')],
            [sg.Button("Entrar"), sg.Button("Sair")]
        ]
        
        window = sg.Window("Login do Sistema", layout)
        
        button, values = window.read()
        window.close()
        
        if button in ("Sair", None):
            raise CancelOpException()
            
        return values # Retorna {"login": "...", "senha": "..."}
    
    # 3. Adicione este método (copiado da AbstractTela)
    #    para que o ControladorSistema possa usá-lo.
    def mostra_mensagem(self, titulo: str, msg: str):
        sg.popup(titulo, msg)