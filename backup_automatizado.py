import threading
from datetime import datetime
from time import sleep

import copiar_arquivos
import dados_tinydb
from copiar_arquivos import copiando_arquivos


# --- Inicialização dos dados ---

def iniciar_monitoramento():
    t = threading.Thread(
        target=conferir_horario,
        daemon=True
    )
    t.start()

def conferir_horario():

    while True:
        agora = datetime.now()
        hora_formatada = agora.strftime("%H:%M")
        t = threading.Thread(
            target=executar_backup,
            args=(hora_formatada,),
            daemon=True
        )
        t.start()
        sleep(60)

def executar_backup(hora_atual):
    carregar_dados = dados_tinydb.carregar_dados_tarefa()
    lista_nomes = list(carregar_dados['tarefas'].keys())
    executar_tarefa = []

    for nome_tarefa in lista_nomes:
        hora = carregar_dados['tarefas'][nome_tarefa]['hora']
        minuto = carregar_dados['tarefas'][nome_tarefa]['minuto']
        print(f"{hora_atual} - {hora}:{minuto}")
        if f"{hora}:{minuto}" == hora_atual:
            executar_tarefa.append(nome_tarefa)


    for nome_tarefa in executar_tarefa:
        pastas_origem = carregar_dados['tarefas'][nome_tarefa]['pastas_origem']
        pastas_destino = carregar_dados['tarefas'][nome_tarefa]['pastas_destino']
        copiar_arquivos.inicar_copia_automatizada(pastas_origem, pastas_destino)
