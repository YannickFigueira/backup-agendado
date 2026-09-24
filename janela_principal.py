import platform
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QFrame, QLabel, QComboBox,
    QPushButton, QProgressBar, QGridLayout, QHBoxLayout, QVBoxLayout, QApplication
)
from PyQt6.QtCore import Qt

import config
import tema
from barra_titulo import BarraTituloCustomizada

sistema = platform.system()


class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()  # Inicializa a QMainWindow diretamente sem pai

        # 1. Configurações de janela frameless e comportamentos do sistema
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)

        if sistema in ["Linux", "Linux2"]:
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.Tool)

        self.setWindowTitle(f"{config.NOME_PROGRAMA} {config.VERSION}")

        self.nome_janela = "janela-principal"
        self.controles = {}

        # 2. Estrutura Base usando o Central Widget do QMainWindow
        self.container_principal = QWidget(self)
        self.setCentralWidget(self.container_principal)

        layout_geral = QVBoxLayout(self.container_principal)
        layout_geral.setContentsMargins(1, 1, 1, 1)
        layout_geral.setSpacing(0)

        # 1. Barra de Título Customizada
        titulo_texto = f"{config.NOME_PROGRAMA} {config.VERSION}"
        self.barra_titulo = BarraTituloCustomizada(self, titulo=titulo_texto)
        layout_geral.addWidget(self.barra_titulo)

        # 2. Conteúdo da Janela
        self.conteudo_widget = QWidget()
        layout_geral.addWidget(self.conteudo_widget, stretch=1)

        # 3. Montagem do Layout e Menu
        self._criar_layout()
        self._criar_barra_menu()

        # 4. Integração com o Tema
        tema.conectar_mudanca_tema(self)
        tema.atualizar_tema(self)

        # Trava o tamanho da janela de acordo com o tamanho ideal dos componentes
        self.setFixedSize(self.sizeHint())

        # Centraliza a janela na tela
        self._centralizar_janela()

    def _centralizar_janela(self):
        """Centraliza a janela no monitor ativo."""
        screen = QApplication.primaryScreen()
        if screen:
            geometria_tela = screen.availableGeometry()
            geometria_janela = self.frameGeometry()
            geometria_janela.moveCenter(geometria_tela.center())
            self.move(geometria_janela.topLeft())

    def _criar_barra_menu(self):
        self.menu_arquivo = self.barra_titulo.adicionar_submenu("Arquivo")
        self.controles['menu_arquivo'] = self.menu_arquivo

        self.menu_ajuda = self.barra_titulo.adicionar_submenu("Ajuda")
        self.controles['menu_ajuda'] = self.menu_ajuda

    def _criar_layout(self):
        self.controles['janela_principal'] = self

        # Layout Principal Horizontal (Esquerda vs Direita)
        layout_conteudo = QHBoxLayout(self.conteudo_widget)
        layout_conteudo.setContentsMargins(config.ESPACO, config.ESPACO, config.ESPACO, config.ESPACO)
        layout_conteudo.setSpacing(config.ESPACO)

        # =========================================================================
        # PAINEL ESQUERDO (CONTROLES)
        # =========================================================================
        self.frame_controls = QFrame()
        layout_controls = QVBoxLayout(self.frame_controls)
        layout_controls.setContentsMargins(config.ESPACO, config.ESPACO, config.ESPACO, config.ESPACO)
        layout_controls.setSpacing(config.ESPACO)

        layout_conteudo.addWidget(self.frame_controls)
        self.controles['frame_controls'] = self.frame_controls

        # Grid interno para Seleção, Horário e Tamanho
        grid_esq = QGridLayout()
        grid_esq.setSpacing(8)

        # Seleção de Tarefa
        self.lbl_selecao = QLabel("Selecionar Tarefa:")
        grid_esq.addWidget(self.lbl_selecao, 0, 0)

        self.cmb_selecao = QComboBox()
        grid_esq.addWidget(self.cmb_selecao, 0, 1)
        self.controles['cmb_selecao'] = self.cmb_selecao

        # Horário
        self.lbl_horario = QLabel("Horário:")
        grid_esq.addWidget(self.lbl_horario, 1, 0)

        self.lbl_hora_execucao = QLabel("--:--")
        self.lbl_hora_execucao.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_esq.addWidget(self.lbl_hora_execucao, 1, 1)
        self.controles['lbl_hora_execucao'] = self.lbl_hora_execucao

        # Tamanho
        self.lbl_tamanho = QLabel("Tamanho:")
        self.lbl_tamanho.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        grid_esq.addWidget(self.lbl_tamanho, 2, 0)

        self.lbl_tamanho_exibir = QLabel("-" * 10)
        self.lbl_tamanho_exibir.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_esq.addWidget(self.lbl_tamanho_exibir, 2, 1)
        self.controles['lbl_tamanho_exibir'] = self.lbl_tamanho_exibir

        layout_controls.addLayout(grid_esq)

        # Botão Executar
        self.btn_executar = QPushButton("Executar Tarefa")
        self.btn_executar.setObjectName("BtnAcao")
        layout_controls.addWidget(self.btn_executar)
        self.controles['btn_executar'] = self.btn_executar

        # Botão Pausar
        self.btn_pausar = QPushButton("Pausar Tarefa")
        self.btn_pausar.setObjectName("BtnAcao")
        self.btn_pausar.setEnabled(False)
        layout_controls.addWidget(self.btn_pausar)
        self.controles['btn_pausar'] = self.btn_pausar

        # Divisor / Marcador "EM EXECUÇÃO"
        lbl_divisor = QLabel("───── EM EXECUÇÃO ─────")
        lbl_divisor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_controls.addWidget(lbl_divisor)

        # Moldura de execução (Com Borda Visível)
        self.moldura_execucao_borda = QFrame()
        self.moldura_execucao_borda.setFixedHeight(160)
        self.moldura_execucao_borda.setObjectName("MolduraLog")
        self.moldura_execucao_borda.setFrameShape(QFrame.Shape.StyledPanel)
        self.moldura_execucao_borda.setFrameShadow(QFrame.Shadow.Sunken)

        layout_moldura_exec = QVBoxLayout(self.moldura_execucao_borda)
        layout_moldura_exec.setContentsMargins(10, 10, 4, 4)

        self.lbl_multi_execucao = QLabel("")
        self.lbl_multi_execucao.setWordWrap(True)
        self.lbl_multi_execucao.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout_moldura_exec.addWidget(self.lbl_multi_execucao)

        layout_controls.addWidget(self.moldura_execucao_borda)
        self.controles['lbl_multi_execucao'] = self.lbl_multi_execucao

        # Botão Encerrar
        self.btn_encerrar = QPushButton("Encerrar Tarefa")
        self.btn_encerrar.setObjectName("BtnAcao")
        layout_controls.addWidget(self.btn_encerrar)
        self.controles['btn_encerrar'] = self.btn_encerrar

        # =========================================================================
        # PAINEL DIREITO (ANDAMENTO)
        # =========================================================================
        self.frame_andamento = QFrame()
        layout_andamento = QVBoxLayout(self.frame_andamento)
        layout_andamento.setContentsMargins(config.ESPACO, config.ESPACO, config.ESPACO, config.ESPACO)
        layout_andamento.setSpacing(config.ESPACO)

        layout_conteudo.addWidget(self.frame_andamento, stretch=1)

        # Moldura de andamento atual (Com Borda Visível)
        self.moldura_andamento_atual = QFrame()
        self.moldura_andamento_atual.setObjectName("MolduraLog")
        self.moldura_andamento_atual.setFrameShape(QFrame.Shape.StyledPanel)
        self.moldura_andamento_atual.setFrameShadow(QFrame.Shadow.Sunken)

        layout_moldura_and = QVBoxLayout(self.moldura_andamento_atual)
        layout_moldura_and.setContentsMargins(10, 10, 4, 4)

        self.lbl_multi_andamento = QLabel("")
        self.lbl_multi_andamento.setWordWrap(True)
        self.lbl_multi_andamento.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout_moldura_and.addWidget(self.lbl_multi_andamento)

        layout_andamento.addWidget(self.moldura_andamento_atual, stretch=1)
        self.controles['lbl_multi_andamento'] = self.lbl_multi_andamento

        # Rodapé do Progresso (Copiado + Barra de Progresso)
        layout_progresso_bottom = QHBoxLayout()
        layout_progresso_bottom.setSpacing(config.ESPACO)

        self.lbl_copiado = QLabel("Copiado:")
        self.lbl_copiado.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout_progresso_bottom.addWidget(self.lbl_copiado)

        self.lbl_copiado_tamanho = QLabel("-" * 10)
        self.lbl_copiado_tamanho.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_progresso_bottom.addWidget(self.lbl_copiado_tamanho)
        self.controles['lbl_copiado_tamanho'] = self.lbl_copiado_tamanho

        # Barra de Progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedSize(500, 26)
        self.progress_bar.setRange(0, 10000)
        self.progress_bar.setValue(0)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar.setFormat("0.000%")

        layout_progresso_bottom.addWidget(self.progress_bar, stretch=1)

        layout_andamento.addLayout(layout_progresso_bottom)

        self.controles['progress_bar'] = self.progress_bar
        self.controles['lbl_porcentagem'] = self.progress_bar