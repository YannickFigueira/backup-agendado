import platform
from PyQt6.QtWidgets import (
    QDialog, QWidget, QFrame, QLabel, QComboBox, QLineEdit,
    QPushButton, QCheckBox, QSpinBox, QGridLayout, QHBoxLayout, QVBoxLayout, QSizePolicy
)
from PyQt6.QtCore import Qt

import config
import tema
from barra_titulo import BarraTituloCustomizada

sistema = platform.system()


class JanelaConfiguracao(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 1. Configurações de Janela Frameless e Comportamento
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)

        if sistema in ["Linux", "Linux2"]:
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.Tool)

        self.setWindowTitle("Configurações")
        self.nome_janela = "configuracao"  # Identificador para o controlador
        self.controles = {}

        # 2. Estrutura Base Layout Geral
        layout_geral = QVBoxLayout(self)
        layout_geral.setContentsMargins(1, 1, 1, 1)
        layout_geral.setSpacing(0)

        # 3. Barra de Título Customizada
        self.barra_titulo = BarraTituloCustomizada(self, titulo="Configurações")
        layout_geral.addWidget(self.barra_titulo)

        # 4. Conteúdo Central
        self.conteudo_widget = QWidget()
        layout_geral.addWidget(self.conteudo_widget, stretch=1)

        # 5. Montagem da Interface e Tema
        self._criar_layout()
        self._criar_barra_menu()

        tema.conectar_mudanca_tema(self)
        tema.atualizar_tema(self)

        # Trava o tamanho de acordo com os componentes organizados
        self.adjustSize()
        self.setFixedSize(self.sizeHint())

    def _criar_barra_menu(self):
        pass

    def _criar_layout(self):
        self.controles['janela_configuracao'] = self

        layout_conteudo = QVBoxLayout(self.conteudo_widget)
        layout_conteudo.setContentsMargins(config.ESPACO, config.ESPACO, config.ESPACO, config.ESPACO)
        layout_conteudo.setSpacing(config.ESPACO)

        # =========================================================================
        # FRAME DE CAMPOS (Seleção, Tarefa e Horário)
        # =========================================================================
        self.frame_campos = QFrame()
        grid_campos = QGridLayout(self.frame_campos)
        grid_campos.setContentsMargins(0, 0, 0, 0)
        grid_campos.setSpacing(config.ESPACO)

        # Selecionar
        self.lbl_selecao = QLabel("Selecionar:")
        grid_campos.addWidget(self.lbl_selecao, 0, 0)

        self.cmb_selecao = QComboBox()
        grid_campos.addWidget(self.cmb_selecao, 0, 1)
        self.controles['cmb_selecao'] = self.cmb_selecao
        self.controles['cmb_selecao'] = self.cmb_selecao  # Atalho direto para o controle

        # Tarefa
        self.lbl_tarefa = QLabel("Tarefa:")
        grid_campos.addWidget(self.lbl_tarefa, 1, 0)

        self.txt_tarefa = QLineEdit()
        grid_campos.addWidget(self.txt_tarefa, 1, 1)
        self.controles['txt_tarefa'] = self.txt_tarefa

        # Seletor de Horário (Sub-frame com 2 SpinBoxes em linha)
        self.frame_hora = QFrame()
        layout_hora = QVBoxLayout(self.frame_hora)
        layout_hora.setContentsMargins(0, 0, 0, 0)
        layout_hora.setSpacing(2)

        self.lbl_horario = QLabel("Horário")
        self.lbl_horario.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_hora.addWidget(self.lbl_horario)

        # Container horizontal para Hora : Minuto
        box_time = QHBoxLayout()
        box_time.setContentsMargins(0, 0, 0, 0)
        box_time.setSpacing(4)

        self.spin_hora = QSpinBox()
        self.spin_hora.setRange(0, 23)
        self.spin_hora.setValue(17)
        self.spin_hora.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self.spin_hora.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lbl_dois_pontos = QLabel(":")
        self.lbl_dois_pontos.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.spin_min = QSpinBox()
        self.spin_min.setRange(0, 59)
        self.spin_min.setValue(0)
        self.spin_min.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self.spin_min.setAlignment(Qt.AlignmentFlag.AlignCenter)

        box_time.addWidget(self.spin_hora)
        box_time.addWidget(self.lbl_dois_pontos)
        box_time.addWidget(self.spin_min)

        layout_hora.addLayout(box_time)

        # Adiciona o agrupador de horário estendendo pelas 2 linhas do Grid
        grid_campos.addWidget(self.frame_hora, 0, 2, 2, 1, Qt.AlignmentFlag.AlignCenter)

        self.controles['spin_hora'] = self.spin_hora
        self.controles['spin_min'] = self.spin_min

        layout_conteudo.addWidget(self.frame_campos)

        # =========================================================================
        # FRAME CHECKBOXES E BOTÃO
        # =========================================================================
        self.frame_checkbox = QFrame()
        grid_check = QGridLayout(self.frame_checkbox)
        grid_check.setContentsMargins(0, 0, 0, 0)
        grid_check.setSpacing(config.ESPACO)

        # Linha 0: Desabilitar / Desligar
        self.chk_desabilitar = QCheckBox("Desabilitar")
        grid_check.addWidget(self.chk_desabilitar, 0, 0)
        self.controles['var_desabilitar'] = self.chk_desabilitar

        self.chk_desligar = QCheckBox("Desligar")
        grid_check.addWidget(self.chk_desligar, 0, 1)
        self.controles['var_desligar'] = self.chk_desligar

        # Linha 1: Diariamente / Quarta-Feira
        self.chk_diariamente = QCheckBox("Diariamente")
        self.chk_diariamente.setChecked(True)
        grid_check.addWidget(self.chk_diariamente, 1, 0)
        self.controles['var_diariamente'] = self.chk_diariamente
        self.controles['chk_diariamente'] = self.chk_diariamente

        self.chk_quarta = QCheckBox("Quarta-Feira")
        grid_check.addWidget(self.chk_quarta, 1, 1)
        self.controles['var_quarta'] = self.chk_quarta
        self.controles['chk_quarta'] = self.chk_quarta

        # Linha 2: Domingo / Quinta-Feira
        self.chk_domingo = QCheckBox("Domingo")
        grid_check.addWidget(self.chk_domingo, 2, 0)
        self.controles['var_domingo'] = self.chk_domingo
        self.controles['chk_domingo'] = self.chk_domingo

        self.chk_quinta = QCheckBox("Quinta-Feira")
        grid_check.addWidget(self.chk_quinta, 2, 1)
        self.controles['var_quinta'] = self.chk_quinta
        self.controles['chk_quinta'] = self.chk_quinta

        # Linha 3: Segunda-Feira / Sexta-Feira
        self.chk_segunda = QCheckBox("Segunda-Feira")
        grid_check.addWidget(self.chk_segunda, 3, 0)
        self.controles['var_segunda'] = self.chk_segunda
        self.controles['chk_segunda'] = self.chk_segunda

        self.chk_sexta = QCheckBox("Sexta-Feira")
        grid_check.addWidget(self.chk_sexta, 3, 1)
        self.controles['var_sexta'] = self.chk_sexta
        self.controles['chk_sexta'] = self.chk_sexta

        # Linha 4: Terça-Feira / Sábado
        self.chk_terca = QCheckBox("Terça-Feira")
        grid_check.addWidget(self.chk_terca, 4, 0)
        self.controles['var_terca'] = self.chk_terca
        self.controles['chk_terca'] = self.chk_terca

        self.chk_sabado = QCheckBox("Sábado")
        grid_check.addWidget(self.chk_sabado, 4, 1)
        self.controles['var_sabado'] = self.chk_sabado
        self.controles['chk_sabado'] = self.chk_sabado

        # Botão Gravar Tarefa (Ocupa as 5 linhas ao lado dos checkboxes)
        self.btn_gravar = QPushButton("Gravar Tarefa")
        self.btn_gravar.setObjectName("BtnAcao")

        # Permite que o botão expanda na vertical sem limite
        self.btn_gravar.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding
        )
        grid_check.addWidget(self.btn_gravar, 0, 2, 5, 1)
        self.controles['btn_gravar'] = self.btn_gravar

        # Moldura inferior de informações/pastas
        self.moldura_pastas = QFrame()
        self.moldura_pastas.setObjectName("MolduraLog")
        self.moldura_pastas.setFrameShape(QFrame.Shape.StyledPanel)
        self.moldura_pastas.setFrameShadow(QFrame.Shadow.Sunken)

        layout_pastas = QVBoxLayout(self.moldura_pastas)
        layout_pastas.setContentsMargins(10, 10, 10, 10)

        self.lbl_pastas = QLabel("")
        self.lbl_pastas.setWordWrap(True)
        self.lbl_pastas.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout_pastas.addWidget(self.lbl_pastas)

        grid_check.addWidget(self.moldura_pastas, 5, 0, 1, 3)
        self.controles['lbl_pastas'] = self.lbl_pastas

        layout_conteudo.addWidget(self.frame_checkbox)