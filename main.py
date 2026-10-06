import faulthandler
import sys
import os
import argparse

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtNetwork import QLocalServer, QLocalSocket

import config
import backup_automatizado
import relatorios  # Importa o módulo do relatório
from arquivo_log import gerar_arquivo_log
from funcoes import Funcoes, registrar_log
from janela_principal import JanelaPrincipal

# Garante um destino para o faulthandler mesmo sem terminal
if sys.stderr is None:
    # Em modo GUI sem console, salva o log de crash fatal em um arquivo
    config.log_erros = open("crash_faulthandler.log", "a", encoding="utf-8")
    faulthandler.enable(file=config.log_erros)
else:
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

# --- LÓGICA DE INSTÂNCIA ÚNICA ---
SERVER_NAME = f"{config.NOME_PROGRAMA}_instancia_unica"


def verificar_instancia_unica():
    """
    Verifica se já existe uma instância em execução.
    Retorna True se puder continuar, ou False se outra instância já estiver rodando.
    """
    socket = QLocalSocket()
    socket.connectToServer(SERVER_NAME)

    # Se conseguir conectar ao servidor local em até 500ms, outra instância já está rodando
    if socket.waitForConnected(500):
        # Envia uma mensagem para avisar a instância existente para focar na tela (opcional)
        socket.write(b"RESTAURAR")
        socket.waitForBytesWritten(1000)
        socket.disconnectFromServer()
        return False
    return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName(config.NOME_PROGRAMA)

    # 1. Checa se o programa já está aberto
    if not verificar_instancia_unica():
        QMessageBox.information(None, "Aviso", "O programa já está em execução")
        sys.exit(0)

    # 2. Cria o servidor local para bloquear futuras novas instâncias
    local_server = QLocalServer()
    # Remove resíduos do servidor caso a aplicação anterior tenha encerrado de forma abrupta
    QLocalServer.removeServer(SERVER_NAME)
    local_server.listen(SERVER_NAME)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_icone = os.path.join(base_dir, "imagens", "backup.png")
    if os.path.exists(caminho_icone):
        app.setWindowIcon(QIcon(caminho_icone))

    window = JanelaPrincipal()


    # window.show()  <-- Se for rodar totalmente invisível/oculto na bandeja

    # Trata conexões vindas de tentativas de abrir uma segunda instância
    def ao_receber_conexao():
        client_socket = local_server.nextPendingConnection()
        if client_socket:
            if client_socket.waitForReadyRead(1000):
                msg = client_socket.readAll().data().decode("utf-8")
                if msg == "RESTAURAR":
                    # Restaura e traz a janela para o foco principal
                    window.show()
                    window.setWindowState(
                        window.windowState() & Qt.WindowState.WindowMinimized | Qt.WindowState.WindowActive
                    )
                    window.raise_()
                    window.activateWindow()
            client_socket.disconnectFromServer()


    local_server.newConnection.connect(ao_receber_conexao)

    logica = Funcoes(window)

    # --- SERVIÇOS EM SEGUNDO PLANO ---
    backup_automatizado.iniciar_monitoramento()
    relatorios.iniciar_monitoramento_relatorio()

    sys.exit(app.exec())