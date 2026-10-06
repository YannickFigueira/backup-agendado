import os
import configparser

from PyQt6.QtWidgets import QMessageBox

import dados_tinydb


def migrar_configuracoes_ini(diretorio_config=r"C:\Copia\Config"):
    """
    Lê os arquivos ini (arquivos.ini e config.ini) no diretório especificado
    e migra as tarefas encontradas para o TinyDB via dados_tinydb.py.
    """
    caminho_arquivos = os.path.join(diretorio_config, "arquivos.ini")
    caminho_config = os.path.join(diretorio_config, "config.ini")

    if not os.path.exists(caminho_config):
        print(f"Erro: Arquivo não encontrado em '{caminho_config}'")
        return False

    # 1. Instancia o leitor do config.ini
    ini_config = configparser.ConfigParser(strict=False)
    ini_config.read(caminho_config, encoding='utf-8')

    # 2. Instancia o leitor do arquivos.ini (se existir)
    ini_arquivos = configparser.ConfigParser(strict=False)
    if os.path.exists(caminho_arquivos):
        ini_arquivos.read(caminho_arquivos, encoding='utf-8')

    # 3. Mapeamento de Tarefas
    # Lê a seção [tarefa] que mapeia índices para nomes: ex: tarefa0 = Tarefa1
    mapeamento_tarefas = {}
    if ini_config.has_section("tarefa"):
        for chave, nome in ini_config.items("tarefa"):
            if chave.startswith("tarefa"):
                idx = chave.replace("tarefa", "")  # ex: '0'
                mapeamento_tarefas[idx] = nome

    # 4. Processa cada tarefa identificada
    # Se não houver seção [tarefa], assume pelo menos o índice '0'
    indices = list(mapeamento_tarefas.keys()) if mapeamento_tarefas else ['0']

    for idx in indices:
        nome_tarefa = mapeamento_tarefas.get(idx, f"Tarefa_{idx}")

        # --- LENDO ORIGENS E DESTINOS ---
        origens = []
        destinos = []

        chave_origem = f"origem0{idx}" if len(idx) == 1 else f"origem{idx}"
        chave_destino = f"destino0{idx}" if len(idx) == 1 else f"destino{idx}"

        # Tenta ler do arquivos.ini primeiro; se não achar, busca no config.ini
        if ini_arquivos.has_section("arquivo"):
            if ini_arquivos.has_option("arquivo", chave_origem):
                origens.append(ini_arquivos.get("arquivo", chave_origem))
            if ini_arquivos.has_option("arquivo", chave_destino):
                destinos.append(ini_arquivos.get("arquivo", chave_destino))

        if not origens and ini_config.has_section("arquivo"):
            if ini_config.has_option("arquivo", chave_origem):
                origens.append(ini_config.get("arquivo", chave_origem))
            if ini_config.has_option("arquivo", chave_destino):
                destinos.append(ini_config.get("arquivo", chave_destino))

        # --- LENDO HORÁRIO ---
        chave_hora = f"hora{idx}"
        chave_minuto = f"minuto{idx}"
        hora = ini_config.get("configuration", chave_hora, fallback="17")
        minuto = ini_config.get("configuration", chave_minuto, fallback="00")

        # Formata com 2 dígitos (ex: '9' -> '09')
        hora = hora.zfill(2)
        minuto = minuto.zfill(2)

        # --- LENDO DIAS DA SEMANA (execucao) ---
        chave_semana = f"semana{idx}"
        semana_str = ini_config.get("configuration", chave_semana, fallback="")
        if semana_str:
            # Converte a string 'true,true,...' em lista de booleanos [True, True, ...]
            execucao = [item.strip().lower() == 'true' for item in semana_str.split(',')]
        else:
            execucao = [True] * 8

        # --- LENDO CONFIGURAÇÕES COMPLEMENTARES ---
        chave_desligar = f"desligar{idx}"
        desligar = ini_config.getboolean("configuration", chave_desligar, fallback=False)

        chave_executar = f"executar{idx}"
        executar_flag = ini_config.getboolean("configuration", chave_executar, fallback=True)
        desabilitar_tarefa = not executar_flag  # Inverte a lógica

        # --- MONTA O PACOTE DE DADOS ---
        # Ordem esperada por gravar_nova_tarefa:
        # dados[0] -> hora
        # dados[1] -> minuto
        # dados[2] -> pastas_origem (lista)
        # dados[3] -> pastas_destino (lista)
        # dados[4] -> execucao (lista de booleans)
        # dados[5] -> desligar (bool)
        # dados[6] -> desabilitar_tarefa (bool)
        dados = [
            hora,
            minuto,
            origens if origens else ["C:\\"],
            destinos if destinos else ["C:\\temp"],
            execucao,
            desligar,
            desabilitar_tarefa
        ]

        # 5. Grava no TinyDB usando a função do módulo
        sucesso = dados_tinydb.gravar_nova_tarefa(nome_tarefa, dados)
        if not sucesso:
            print(f"Atualizando campos da tarefa existente '{nome_tarefa}'...")
            dados_tinydb.atualizar_campo_tarefa(nome_tarefa, "hora", hora)
            dados_tinydb.atualizar_campo_tarefa(nome_tarefa, "minuto", minuto)
            dados_tinydb.atualizar_campo_tarefa(nome_tarefa, "pastas_origem", origens)
            dados_tinydb.atualizar_campo_tarefa(nome_tarefa, "pastas_destino", destinos)
            dados_tinydb.atualizar_campo_tarefa(nome_tarefa, "execucao", execucao)
            dados_tinydb.atualizar_campo_tarefa(nome_tarefa, "desligar", desligar)
            dados_tinydb.atualizar_campo_tarefa(nome_tarefa, "desabilitar_tarefa", desabilitar_tarefa)

    # Limpa a tarefa de exemplo 'inicial' criada por padrão se novas tarefas foram lidas
    if mapeamento_tarefas and "inicial" in dados_tinydb.carregar_dados_tarefa()['tarefas']:
        dados_tinydb.apagar_dados_tarefa("inicial")

    QMessageBox.information(None, "Aviso", "Migração concluída com sucesso!")
    return True
