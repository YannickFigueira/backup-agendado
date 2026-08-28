import argparse
import os
import sys
import tkinter as tk

import estilo, backup_automatizado
from arquivo_log import gerar_arquivo_log
from funcoes import Funcoes, registrar_log
from janela_principal import JanelaPrincipal

# TRATAMENTO DE ÍCONE PARA WINDOWS
if sys.platform.startswith("win"):
    try:
        import ctypes

        app_id = f'{estilo.NOME_PROGRAMA}.app.{estilo.VERSION}'

        # Só acessa o windll se estiver comprovadamente no Windows
        if hasattr(ctypes, 'windll'):
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except Exception as e:
        caminho_log = gerar_arquivo_log()
        registrar_log(caminho_log, e)

parser = argparse.ArgumentParser(prog="backup-agendado")
parser.add_argument("--version", action="version", version=f"%(prog)s {estilo.VERSION}")
args = parser.parse_args()

if __name__ == "__main__":
    # 1. Passe o className diretamente no construtor do Tk (resolve o aviso do className)
    root = tk.Tk(className=estilo.NOME_PROGRAMA)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_icone = os.path.join(base_dir, "imagens", "backup.png")

    if os.path.exists(caminho_icone):
        # Usando PhotoImage nativo para Linux com argumento de arquivo
        foto = tk.PhotoImage(file=caminho_icone)

        # O primeiro parâmetro False força a aplicar especificamente na janela atual
        root.iconphoto(False, foto)
        setattr(root, "_icone_ref", foto)

    # 2. Cria a parte visual (passando o root e a versão)
    visual = JanelaPrincipal(root)

    # 3. Passa a visão para a sua classe de Lógica controlar
    logica = Funcoes(visual)
    backup_automatizado.iniciar_monitoramento()

    # 4. Inicia o programa
    root.mainloop()