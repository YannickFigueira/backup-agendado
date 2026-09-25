import threading
from datetime import datetime
from time import sleep

import dados_tinydb
from copiar_arquivos import WorkerCopia

# Guardamos as threads ativas em memória para não serem coletadas pelo Garbage Collector
workers_agendados = []


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

        # Formata para garantir dois dígitos (ex: "07:05")
        horario_tarefa = f"{int(hora):02d}:{int(minuto):02d}"

        if horario_tarefa == hora_atual:
            executar_tarefa.append(nome_tarefa)

    for nome_tarefa in executar_tarefa:
        desabilitar = carregar_dados['tarefas'][nome_tarefa]['desabilitar_tarefa']
        if not desabilitar:
            dados_tinydb.atualizar_campo_tarefa(nome_tarefa, 'executando', True)
            pastas_origem = carregar_dados['tarefas'][nome_tarefa]['pastas_origem']
            pastas_destino = carregar_dados['tarefas'][nome_tarefa]['pastas_destino']

            # Instancia a WorkerCopia no modo automatizado
            worker = WorkerCopia(
                pastas_origem=pastas_origem,
                pastas_destino=pastas_destino,
                modo_automatizado=True
            )

            # Atualiza o banco quando a thread concluir
            def ao_concluir(erro, cancelado):
                dados_tinydb.atualizar_campo_tarefa(nome_tarefa, 'executando', False)

            worker.sinal_concluido.connect(ao_concluir)

            # Mantém a referência da thread e inicia
            workers_agendados.append(worker)
            worker.start()