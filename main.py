import sys
import os
import argparse
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

import config, backup_automatizado
from arquivo_log import gerar_arquivo_log
from funcoes import Funcoes, registrar_log
from janela_principal import JanelaPrincipal

# TRATAMENTO DE ÍCONE PARA WINDOWS
if sys.platform.startswith("win"):
    try:
        import ctypes

        app_id = f'{config.NOME_PROGRAMA}.app.{config.VERSION}'

        if hasattr(ctypes, 'windll'):
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except Exception as e:
        caminho_log = gerar_arquivo_log(config.log_erros)
        registrar_log(caminho_log, e)

parser = argparse.ArgumentParser(prog="backup-agendado")
parser.add_argument("--version", action="version", version=f"%(prog)s {config.VERSION}")
args = parser.parse_args()

if __name__ == "__main__":
    # 1. Instância do QApplication (necessária antes de qualquer widget no Qt)
    app = QApplication(sys.argv)
    app.setApplicationName(config.NOME_PROGRAMA)

    # Definir ícone da aplicação
    base_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_icone = os.path.join(base_dir, "imagens", "backup.png")

    if os.path.exists(caminho_icone):
        icone = QIcon(caminho_icone)
        app.setWindowIcon(icone)

    # 2. Cria a janela principal
    # Nota: No PyQt, a classe JanelaPrincipal geralmente herda de QMainWindow ou QWidget
    window = JanelaPrincipal()

    if os.path.exists(caminho_icone):
        window.setWindowIcon(QIcon(caminho_icone))

    window.show()

    # 3. Passa a visão para a classe de Lógica controlar
    logica = Funcoes(window)
    backup_automatizado.iniciar_monitoramento()

    # 4. Inicia o loop de eventos do Qt
    sys.exit(app.exec())