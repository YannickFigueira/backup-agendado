import os
import threading
import time
from pathlib import Path

import dados_tinydb

# Variável
tarefas_executando = []

# --- Execução da cópia dos arquivos
def iniciar_copiar_arquivos(view, nome_tarefa):
    carregar_dados = dados_tinydb.carregar_dados_tarefa()
    pastas_origem = carregar_dados['tarefas'][nome_tarefa]['pastas_origem']
    pastas_destino = carregar_dados['tarefas'][nome_tarefa]['pastas_destino']
    view.controles['lbl_multi_execucao'].config(text=f"Executando...\n{nome_tarefa}")
    iniciar_copia(pastas_origem, pastas_destino, view)

def iniciar_copia(pastas_origem, pastas_destino, view):
    t = threading.Thread(
        target=copiando_pastas,
        args=(pastas_origem, pastas_destino, view),
        daemon=True
    )
    t.start()

def copiando_pastas(pastas_origem, pastas_destino, view):
    # Pegamos um widget do Tkinter do dicionário para usar o método .after()
    lbl_andamento = view.controles['lbl_multi_andamento']
    lbl_execucao = view.controles['lbl_multi_execucao']

    # zip alinha origem/destino; enumerate fornece o índice 'i'
    for i, (origem, destino_base) in enumerate(zip(pastas_origem, pastas_destino)):
        caminho_origem = Path(origem)
        # / une caminhos automaticamente independente do S.O.
        pasta_destino_final = Path(destino_base) / caminho_origem.name

        print(f"Iniciando cópia...{i}\n")

        # Atualização segura do Tkinter vindo de Thread
        lbl_andamento.after(
            0,
            lambda idx=i: lbl_andamento.config(text=f"Iniciando cópia...{idx}")
        )

        copiando_arquivos(str(caminho_origem), str(pasta_destino_final), view)

    # Atualiza a interface ao finalizar todas as cópias
    lbl_andamento.after(0, lambda: view.controles['lbl_multi_andamento'].config(text="Encerrado cópia"))
    lbl_execucao.after(0, lambda: view.controles['lbl_multi_execucao'].config(text=""))

def copiando_arquivos(origem, destino, view):
    print(origem)
    print(destino)
    time.sleep(10)
    print("Executado com sucesso")
