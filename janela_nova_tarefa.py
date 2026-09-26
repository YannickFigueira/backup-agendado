import config
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QFrame,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

import tema
# Importa a barra de título customizada do seu módulo
from barra_titulo_subjanela import BarraTituloSubjanela


class JanelaNovaTarefa(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Configurações de modalidade e janela sem bordas (Frameless)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Dialog
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setModal(True)
        self.setWindowTitle("Nova Tarefa")

        # Identificadores de controle
        self.nome_janela = "nova-tarefa"
        self.janela_controle = "janela_nova_tarefa"
        self.controles = {self.janela_controle: self}

        # Layout Principal (Vertical)
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)

        # 1. Adiciona a Barra de Título Customizada no topo
        self.barra_titulo = BarraTituloSubjanela(
            self, titulo=self.windowTitle()
        )
        self.layout_principal.addWidget(self.barra_titulo)

        # 2. Constrói o corpo/painel de campos
        self._criar_layout()

        tema.conectar_mudanca_tema(self)
        tema.atualizar_tema(self)

    def _criar_layout(self):
        # Frame do Conteúdo (Painel de Campos)
        self.frame_campos = QFrame(self)
        self.layout_principal.addWidget(self.frame_campos)

        # Layout em Grade para alinhar Rótulos, Campos e Botões
        grid = QGridLayout(self.frame_campos)
        grid.setContentsMargins(
            config.ESPACO, config.ESPACO, config.ESPACO, config.ESPACO
        )
        grid.setSpacing(config.ESPACO)

        linha = 0
        largura_texto = 300

        # --- Campo Origem ---
        self.lbl_origem = QLabel("Origem:", self.frame_campos)
        grid.addWidget(self.lbl_origem, linha, 0, Qt.AlignmentFlag.AlignLeft)

        self.txt_origem = QLineEdit(self.frame_campos)
        self.txt_origem.setFixedWidth(largura_texto)
        self.controles["txt_origem"] = self.txt_origem
        grid.addWidget(self.txt_origem, linha, 1)

        self.btn_selecionar_origem = QPushButton("...", self.frame_campos)
        self.btn_selecionar_origem.setObjectName("BtnAcao")
        self.btn_selecionar_origem.setFixedWidth(40)
        self.controles["btn_selecionar_origem"] = self.btn_selecionar_origem
        grid.addWidget(self.btn_selecionar_origem, linha, 2)
        linha += 1

        # --- Campo Destino ---
        self.lbl_destino = QLabel("Destino:", self.frame_campos)
        grid.addWidget(self.lbl_destino, linha, 0, Qt.AlignmentFlag.AlignLeft)

        self.txt_destino = QLineEdit(self.frame_campos)
        self.txt_destino.setFixedWidth(largura_texto)
        self.controles["txt_destino"] = self.txt_destino
        grid.addWidget(self.txt_destino, linha, 1)

        self.btn_selecionar_destino = QPushButton("...", self.frame_campos)
        self.btn_selecionar_destino.setObjectName("BtnAcao")
        self.btn_selecionar_destino.setFixedWidth(40)
        self.controles["btn_selecionar_destino"] = self.btn_selecionar_destino
        grid.addWidget(self.btn_selecionar_destino, linha, 2)
        linha += 1

        # --- Botão Adicionar Pasta ---
        self.btn_adicionar = QPushButton(
            "Adicionar pasta", self.frame_campos
        )
        self.btn_adicionar.setObjectName("BtnAcao")
        self.controles["btn_adicionar"] = self.btn_adicionar
        grid.addWidget(self.btn_adicionar, linha, 0, 1, 3)
        linha += 1

        # --- Botão Salvar Pastas ---
        self.btn_salvar = QPushButton("Salvar pastas", self.frame_campos)
        self.btn_salvar.setObjectName("BtnAcao")
        self.btn_salvar.setEnabled(False)  # Equivalente ao state="disabled"
        self.controles["btn_salvar"] = self.btn_salvar
        grid.addWidget(self.btn_salvar, linha, 0, 1, 3)