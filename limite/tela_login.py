import PySimpleGUI as sg
from exceptions.cancel_op_exception import CancelOpException
from limite.abstract_tela import AbstractTela

class TelaLogin(AbstractTela):
    def __init__(self):
        # Não precisa do controlador_sistema
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