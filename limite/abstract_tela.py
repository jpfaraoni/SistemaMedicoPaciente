from abc import ABC, abstractmethod
import PySimpleGUI as sg
from exceptions.cancel_op_exception import CancelOpException

class AbstractTela(ABC):
    @abstractmethod
    def __init__(self, tela_sistema) -> None:
        self.tela_sistema = tela_sistema
    @abstractmethod
    def tela_opcoes(self):
        pass

    def mostra_mensagem(self, titulo: str, msg: str):
        sg.popup(titulo, msg)

    def confirma_acao(self, titulo: str, msg: str):
        resultado = sg.popup_yes_no(msg, title=titulo)
        return resultado == 'Yes'

    def seleciona_entidade_por_id(self, titulo: str, texto_prompt: str, chave_input: str):
        layout = [
            [sg.Text(texto_promp), sg.InputText(key="id")],
            [sg.Button("Confirmar"), sg.Button("Cancelar")],
        ]
        window = sg.Window(titulo, layout)

        button, values = window.read()
        window.close()

        if button in ("Cancelar", None):
            raise CancelOpException()

        return values["id"]