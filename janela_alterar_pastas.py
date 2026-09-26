import config
import tema  # Importação do gerenciador de temas do seu projeto
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

# Importa a barra de título customizada
from barra_titulo_subjanela import BarraTituloSubjanela


class JanelaAlterarPastas(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        # 1. Configuração de Janela Frameless e Modal
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Dialog
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setModal(True)
        self.setWindowTitle("Alterar Pastas")

        # Identificadores de controle
        self.nome_janela = "alterar-pastas"
        self.janela_controle = "janela_alterar_pastas"
        self.controles = {self.janela_controle: self}

        # 2. Layout Principal da Janela
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)

        # 3. Adiciona a Barra de Título Customizada
        self.barra_titulo = BarraTituloSubjanela(
            self, titulo=self.windowTitle()
        )
        self.layout_principal.addWidget(self.barra_titulo)

        # 4. Painel Interno de Conteúdo
        self.frame_conteudo = QFrame(self)
        self.layout_principal.addWidget(self.frame_conteudo)

        # 5. Aplica o Tema usando as funções do seu módulo
        tema.conectar_mudanca_tema(self)
        tema.atualizar_tema(self)

        # 6. Constrói os campos e botões
        self._criar_layout()

    def _criar_layout(self):
        # Layout vertical principal do conteúdo interno
        layout_conteudo = QVBoxLayout(self.frame_conteudo)
        layout_conteudo.setContentsMargins(
            config.ESPACO, config.ESPACO, config.ESPACO, config.ESPACO
        )
        layout_conteudo.setSpacing(config.ESPACO)

        # --- Frame Campos (Grid Layout) ---
        self.frame_campos = QFrame(self.frame_conteudo)
        grid_campos = QGridLayout(self.frame_campos)
        grid_campos.setContentsMargins(0, 0, 0, 0)
        grid_campos.setSpacing(config.ESPACO)

        linha = 0

        # Selecionar (ComboBox)
        self.lbl_selecao = QLabel("Selecionar:", self.frame_campos)
        grid_campos.addWidget(
            self.lbl_selecao, linha, 0, Qt.AlignmentFlag.AlignLeft
        )

        self.cmb_selecao = QComboBox(self.frame_campos)
        self.controles["cmb_selecao"] = self.cmb_selecao
        grid_campos.addWidget(self.cmb_selecao, linha, 1, 1, 2)
        linha += 1

        # Origem
        self.lbl_origem = QLabel("Origem:", self.frame_campos)
        grid_campos.addWidget(
            self.lbl_origem, linha, 0, Qt.AlignmentFlag.AlignLeft
        )

        self.txt_origem = QLineEdit(self.frame_campos)
        self.controles["txt_origem"] = self.txt_origem
        grid_campos.addWidget(self.txt_origem, linha, 1)

        self.btn_selecionar_origem = QPushButton("...", self.frame_campos)
        self.btn_selecionar_origem.setObjectName("BtnAcao")
        self.btn_selecionar_origem.setFixedWidth(40)
        self.controles["btn_selecionar_origem"] = self.btn_selecionar_origem
        grid_campos.addWidget(self.btn_selecionar_origem, linha, 2)
        linha += 1

        # Destino
        self.lbl_destino = QLabel("Destino:", self.frame_campos)
        grid_campos.addWidget(
            self.lbl_destino, linha, 0, Qt.AlignmentFlag.AlignLeft
        )

        self.txt_destino = QLineEdit(self.frame_campos)
        self.controles["txt_destino"] = self.txt_destino
        grid_campos.addWidget(self.txt_destino, linha, 1)

        self.btn_selecionar_destino = QPushButton("...", self.frame_campos)
        self.btn_selecionar_destino.setObjectName("BtnAcao")
        self.btn_selecionar_destino.setFixedWidth(40)
        self.controles["btn_selecionar_destino"] = self.btn_selecionar_destino
        grid_campos.addWidget(self.btn_selecionar_destino, linha, 2)
        linha += 1

        # Botão Alterar Pasta
        self.btn_alterar = QPushButton("Alterar pasta", self.frame_campos)
        self.btn_alterar.setObjectName("BtnAcao")
        self.controles["btn_alterar"] = self.btn_alterar
        grid_campos.addWidget(self.btn_alterar, linha, 0, 1, 3)
        linha += 1

        # Botão Excluir Pasta
        self.btn_excluir_pasta = QPushButton(
            "Excluir pasta", self.frame_campos
        )
        self.btn_excluir_pasta.setObjectName("BtnAcao")
        self.controles["btn_excluir_pasta"] = self.btn_excluir_pasta
        grid_campos.addWidget(self.btn_excluir_pasta, linha, 0, 1, 3)

        layout_conteudo.addWidget(self.frame_campos)

        # --- Frame Adicionar (Layout Horizontal com 2 colunas) ---
        self.frame_adicionar = QFrame(self.frame_conteudo)
        layout_adicionar = QHBoxLayout(self.frame_adicionar)
        layout_adicionar.setContentsMargins(0, 0, 0, 0)
        layout_adicionar.setSpacing(config.ESPACO)

        self.btn_adicionar_pasta = QPushButton(
            "Adicionar nova pasta", self.frame_adicionar
        )
        self.btn_adicionar_pasta.setObjectName("BtnAcao")
        self.controles["btn_adicionar_pasta"] = self.btn_adicionar_pasta
        layout_adicionar.addWidget(self.btn_adicionar_pasta, stretch=1)

        self.btn_gravar_adicionar = QPushButton(
            "Gravar nova pasta", self.frame_adicionar
        )
        self.btn_gravar_adicionar.setObjectName("BtnAcao")
        self.controles["btn_gravar_adicionar"] = self.btn_gravar_adicionar
        layout_adicionar.addWidget(self.btn_gravar_adicionar, stretch=1)

        layout_conteudo.addWidget(self.frame_adicionar)