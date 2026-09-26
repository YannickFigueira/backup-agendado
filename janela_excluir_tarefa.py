import config
import tema
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QFrame,
    QGridLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

# Importa a barra de título customizada
from barra_titulo_subjanela import BarraTituloSubjanela


class JanelaExcluirTarefa(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Configurações de janela sem bordas (Frameless) e modal
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Dialog
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setModal(True)
        self.setWindowTitle("Excluir Tarefa")

        # Identificadores de controle
        self.nome_janela = "excluir-tarefa"
        self.janela_controle = "janela_excluir_tarefa"
        self.controles = {self.janela_controle: self}

        # Layout Principal da Janela (Vertical, sem margens para a barra colar no topo)
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)

        # 1. Adiciona a Barra de Título Customizada
        self.barra_titulo = BarraTituloSubjanela(
            self, titulo=self.windowTitle()
        )
        self.layout_principal.addWidget(self.barra_titulo)

        # 2. Painel Interno de Conteúdo
        self.frame_conteudo = QFrame(self)
        self.layout_principal.addWidget(self.frame_conteudo)

        # 3. Conecta e aplica o Tema
        tema.conectar_mudanca_tema(self)
        tema.atualizar_tema(self)

        # 4. Constrói o layout interno dos campos
        self._criar_layout()

    def _criar_layout(self):
        # Layout principal do conteúdo interno
        layout_conteudo = QVBoxLayout(self.frame_conteudo)
        layout_conteudo.setContentsMargins(
            config.ESPACO, config.ESPACO, config.ESPACO, config.ESPACO
        )
        layout_conteudo.setSpacing(config.ESPACO)

        # Frame dos Campos em Grid
        self.frame_campos = QFrame(self.frame_conteudo)
        grid_campos = QGridLayout(self.frame_campos)
        grid_campos.setContentsMargins(0, 0, 0, 0)
        grid_campos.setSpacing(config.ESPACO)

        linha = 0

        # Rótulo "Selecionar:"
        self.lbl_selecao = QLabel("Selecionar:", self.frame_campos)
        grid_campos.addWidget(
            self.lbl_selecao, linha, 0, Qt.AlignmentFlag.AlignLeft
        )

        # ComboBox de Seleção de Tarefa
        self.cmb_selecao = QComboBox(self.frame_campos)
        self.controles["cmb_selecao"] = self.cmb_selecao
        grid_campos.addWidget(self.cmb_selecao, linha, 1)
        linha += 1

        # Botão Excluir Tarefa (ocupando 2 colunas)
        self.btn_excluir = QPushButton("Excluir Tarefa", self.frame_campos)
        self.btn_excluir.setObjectName("BtnAcao")
        self.controles["btn_excluir"] = self.btn_excluir
        grid_campos.addWidget(self.btn_excluir, linha, 0, 1, 2)

        layout_conteudo.addWidget(self.frame_campos)