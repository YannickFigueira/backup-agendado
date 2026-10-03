import faulthandler
import sys
import os
import argparse
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

import config
import backup_automatizado
import relatorios  # Importa o módulo do relatório
from arquivo_log import gerar_arquivo_log
from funcoes import Funcoes, registrar_log
from janela_principal import JanelaPrincipal

# Ativa o faulthandler para capturar erros fatais do C++
faulthandler.enable()

def capturar_excecoes(exctype, value, tb):
    """Exibe o traceback completo no terminal antes do crash."""
    print("=== EXCEÇÃO NÃO TRATADA DETECTADA ===", file=sys.stderr)
    import traceback
    traceback.print_exception(exctype, value, tb)
    sys.exit(1)

# Redireciona o tratamento de exceções do Python/Qt
sys.excepthook = capturar_excecoes

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
args, _ = parser.parse_known_args()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName(config.NOME_PROGRAMA)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_icone = os.path.join(base_dir, "imagens", "backup.png")
    if os.path.exists(caminho_icone):
        app.setWindowIcon(QIcon(caminho_icone))

    window = JanelaPrincipal()
    # window.show()  <-- Se for rodar totalmente invisível/oculto na bandeja

    logica = Funcoes(window)

    # --- SERVIÇOS EM SEGUNDO PLANO ---
    backup_automatizado.iniciar_monitoramento()
    relatorios.iniciar_monitoramento_relatorio()  # Módulo isolado iniciado!

    sys.exit(app.exec())