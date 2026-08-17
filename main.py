import argparse
import tkinter as tk

import estilo, backup_automatizado
from funcoes import Funcoes
from janela_principal import JanelaPrincipal

parser = argparse.ArgumentParser(prog="backup-agendado")
parser.add_argument("--version", action="version", version=f"%(prog)s {estilo.VERSION}")
args = parser.parse_args()

if __name__ == "__main__":
    # 1. Inicia a janela base do Tkinter
    root = tk.Tk()

    # 2. Cria a parte visual (passando o root e a versão)
    visual = JanelaPrincipal(root)

    # 3. Passa a visão para a sua classe de Lógica controlar
    logica = Funcoes(visual)
    backup_automatizado.iniciar_monitoramento()

    # 4. Inicia o programa
    root.mainloop()