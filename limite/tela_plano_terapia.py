# Arquivo: limite/tela_plano_terapia.py

import PySimpleGUI as sg
from exceptions.cancel_op_exception import CancelOpException
from limite.abstract_tela import AbstractTela

class TelaPlanoTerapia(AbstractTela):
    def __init__(self, tela_sistema):
        super().__init__(tela_sistema)

    def tela_opcoes(self, tipo_usuario: str):
        """
        Mostra o menu de opções dinâmico para Pacientes ou Médicos.
        """
        sg.change_look_and_feel('Material1')
        
        layout_esquerda = [
            [sg.Image(filename='limite/imagens/imagem_sistema_pequena..png')]
        ]

        layout_direita = []
        if tipo_usuario == 'paciente':
            layout_direita = [
                [sg.Button("Ver Meus Planos de Terapia", key=1, size=(20, 1.15), font=("Helvetica", 13))],
            ]
        elif tipo_usuario == 'medico':
            layout_direita = [
                [sg.Button("Criar Novo Plano de Terapia", key=2, size=(20, 1.15), font=("Helvetica", 13))],
                [sg.Button("Ver Planos Criados por Mim", key=3, size=(20, 1.15), font=("Helvetica", 13))],
            ]
        
        layout_direita.append([sg.Button("Sair", key=0, size=(20, 1.15), font=("Helvetica", 13))])

        layout = [
            [sg.Column(layout_direita),
             sg.VSeparator(),
             sg.Column(layout_esquerda)]
        ]
        
        window = sg.Window("Planos de Terapia", layout, size=(600, 400), finalize=True)
        event, _ = window.read()
        window.close()
        return event if event is not None else 0

    def pega_dados_plano(self):
        """
        Tela para o médico escrever o plano.
        Usa sg.Multiline para permitir textos longos.
        """
        layout = [
            [sg.Text("Escreva o texto do plano de terapia:")],
            [sg.Multiline(key="texto_plano", size=(60, 15))],
            [sg.Button("Salvar Plano"), sg.Cancel("Cancelar")]
        ]
        
        window = sg.Window("Criar Plano de Terapia", layout)
        button, values = window.read()
        window.close()
        
        if button in ("Cancelar", None):
            raise CancelOpException()
            
        return values # Retorna {"texto_plano": "..."}

    def exibe_lista_planos(self, planos_info: list):
        """
        Mostra uma lista de planos para o usuário. 
        O paciente clica para LER. O médico clica para LER ou ATUALIZAR.
        """
        if not planos_info:
            self.mostra_mensagem("Aviso", "Nenhum plano de terapia encontrado.")
            return None

        # Para este caso simples, vamos apenas listar e permitir clicar para ver
        layout = [[sg.Text("Seus Planos de Terapia (clique para ler):")]]
        for plano in planos_info:
            layout.append([
                sg.Button(f"Plano para: {plano['paciente_nome']} (Criado em: {plano['data_criacao']} por Dr(a). {plano['medico_nome']})", 
                          key=plano['id_plano'], # A chave é o ID do plano
                          size=(60, 1))
            ])
        
        layout.append([sg.Button("Fechar", key=0)])

        window = sg.Window("Lista de Planos", layout)
        event, _ = window.read()
        window.close()

        if event in (None, 0, "Fechar"):
            return None
        
        return event # Retorna o ID do plano que foi clicado

    def mostra_plano_detalhado(self, data: str, medico_nome: str, texto_plano: str):
        """
        Exibe o texto completo de um plano de terapia em um popup.
        """
        layout = [
            [sg.Text(f"Criado em: {data} por Dr(a). {medico_nome}")],
            [sg.Multiline(texto_plano, size=(70, 20), disabled=True)],
            [sg.Button("Fechar")]
        ]
        window = sg.Window("Detalhes do Plano", layout)
        window.read()
        window.close()