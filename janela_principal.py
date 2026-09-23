import platform
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QFrame, QLabel, QComboBox,
    QPushButton, QProgressBar, QGridLayout, QHBoxLayout, QVBoxLayout
)
from PyQt6.QtCore import Qt

import config
import barra_menu
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

    def _criar_barra_menu(self):
        pass

    def _criar_layout(self):
        self.controles['janela_principal'] = self

        layout_conteudo = QHBoxLayout(self.conteudo_widget)
        layout_conteudo.setContentsMargins(config.ESPACO, config.ESPACO, config.ESPACO, config.ESPACO)
        layout_conteudo.setSpacing(config.ESPACO)

        # ==================== PAINEL ESQUERDO (CONTROLES) ====================
        self.frame_controls = QFrame()
        layout_controls = QGridLayout(self.frame_controls)
        layout_controls.setContentsMargins(config.ESPACO, config.ESPACO, config.ESPACO, config.ESPACO)
        layout_controls.setSpacing(config.ESPACO)

        layout_conteudo.addWidget(self.frame_controls)
        self.controles['frame_controls'] = self.frame_controls

        linha_esq = 0

        # Seleção de Tarefa
        self.lbl_selecao = QLabel("Selecionar Tarefa:")
        layout_controls.addWidget(self.lbl_selecao, linha_esq, 0)

        self.cmb_selecao = QComboBox()
        layout_controls.addWidget(self.cmb_selecao, linha_esq, 1)
        self.controles['cmb_selecao'] = self.cmb_selecao
        linha_esq += 1

        # Horário
        self.lbl_horario = QLabel("Horário:")
        layout_controls.addWidget(self.lbl_horario, linha_esq, 0)

        self.lbl_hora_execucao = QLabel("--:--")
        self.lbl_hora_execucao.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_controls.addWidget(self.lbl_hora_execucao, linha_esq, 1)
        self.controles['lbl_hora_execucao'] = self.lbl_hora_execucao
        linha_esq += 1

        # Tamanho
        self.lbl_tamanho = QLabel("Tamanho:")
        self.lbl_tamanho.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout_controls.addWidget(self.lbl_tamanho, linha_esq, 0)

        self.lbl_tamanho_exibir = QLabel("-" * 10)
        self.lbl_tamanho_exibir.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_controls.addWidget(self.lbl_tamanho_exibir, linha_esq, 1)
        self.controles['lbl_tamanho_exibir'] = self.lbl_tamanho_exibir
        linha_esq += 1

        # Botão Executar
        self.btn_executar = QPushButton("Executar Tarefa")
        self.btn_executar.setObjectName("BtnAcao")
        layout_controls.addWidget(self.btn_executar, linha_esq, 0, 1, 2)
        self.controles['btn_executar'] = self.btn_executar
        linha_esq += 1

        # Botão Pausar
        self.btn_pausar = QPushButton("Pausar Tarefa")
        self.btn_pausar.setObjectName("BtnAcao")
        self.btn_pausar.setEnabled(False)
        layout_controls.addWidget(self.btn_pausar, linha_esq, 0, 1, 2)
        self.controles['btn_pausar'] = self.btn_pausar
        linha_esq += 1

        self.controles['linha_painel_esquerdo'] = linha_esq

        # Moldura de execução
        linha_esq += 1
        self.moldura_execucao_borda = QFrame()
        self.moldura_execucao_borda.setFixedHeight(110)

        layout_moldura_exec = QVBoxLayout(self.moldura_execucao_borda)
        layout_moldura_exec.setContentsMargins(10, 10, 4, 4)

        self.lbl_multi_execucao = QLabel("")
        self.lbl_multi_execucao.setWordWrap(True)
        self.lbl_multi_execucao.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout_moldura_exec.addWidget(self.lbl_multi_execucao)

        layout_controls.addWidget(self.moldura_execucao_borda, linha_esq, 0, 5, 2)
        self.controles['lbl_multi_execucao'] = self.lbl_multi_execucao
        linha_esq += 5

        # Botão Encerrar
        self.btn_encerrar = QPushButton("Encerrar Tarefa")
        self.btn_encerrar.setObjectName("BtnAcao")
        layout_controls.addWidget(self.btn_encerrar, linha_esq, 0, 1, 2)
        self.controles['btn_encerrar'] = self.btn_encerrar

        # ==================== PAINEL DIREITO (ANDAMENTO) ====================
        self.frame_andamento = QFrame()
        layout_andamento = QGridLayout(self.frame_andamento)
        layout_andamento.setContentsMargins(config.ESPACO, config.ESPACO, config.ESPACO, config.ESPACO)
        layout_andamento.setSpacing(config.ESPACO)

        layout_conteudo.addWidget(self.frame_andamento)

        linha_dir = 0

        # Moldura de andamento atual
        self.moldura_andamento_atual = QFrame()
        self.moldura_andamento_atual.setFixedHeight(360)

        layout_moldura_and = QVBoxLayout(self.moldura_andamento_atual)
        layout_moldura_and.setContentsMargins(10, 10, 4, 4)

        self.lbl_multi_andamento = QLabel("")
        self.lbl_multi_andamento.setWordWrap(True)
        self.lbl_multi_andamento.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout_moldura_and.addWidget(self.lbl_multi_andamento)

        layout_andamento.addWidget(self.moldura_andamento_atual, linha_dir, 0, 2, 3)
        self.controles['lbl_multi_andamento'] = self.lbl_multi_andamento
        linha_dir += 2

        # Rótulos Copiado / Copiado Tamanho
        self.lbl_copiado = QLabel("Copiado:")
        self.lbl_copiado.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout_andamento.addWidget(self.lbl_copiado, linha_dir, 0)

        self.lbl_copiado_tamanho = QLabel("-" * 10)
        self.lbl_copiado_tamanho.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_andamento.addWidget(self.lbl_copiado_tamanho, linha_dir, 1)
        self.controles['lbl_copiado_tamanho'] = self.lbl_copiado_tamanho

        # Barra de Progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedSize(500, 26)
        self.progress_bar.setRange(0, 10000)
        self.progress_bar.setValue(0)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar.setFormat("0.000%")

        layout_andamento.addWidget(self.progress_bar, linha_dir, 2, Qt.AlignmentFlag.AlignRight)

        self.controles['progress_bar'] = self.progress_bar
        self.controles['lbl_porcentagem'] = self.progress_bar