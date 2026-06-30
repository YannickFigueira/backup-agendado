import os
from tinydb import TinyDB, Query

dados_dir = "dados"
if not os.path.exists(dados_dir):
    os.makedirs(dados_dir)

db = TinyDB('dados/backup_config.json')
tabela_config = db.table('configuracoes')
Config = Query()

# 1. Estrutura inicial padrão (Criada apenas na primeira vez que o script roda)
dados_backup = {
    "id_config": "global",
    "tarefas": {
        "tarefa1": {
            "hora": "10", "minuto": "45",
            "pastas_origem": ["pasta1", "pasta2"], "pastas_destino": ["pasta1", "pasta2"],
            "executando": False, "execucao": [True, False, False, False, False, False, False, False],
            "desligar": False, "desabilitar_tarefa": False,
        }
    }
}

# Inicializa o banco se estiver vazio
if not tabela_config.all():
    tabela_config.insert(dados_backup)

# --- FUNÇÃO PRINCIPAL DE MANIPULAÇÃO ---
# --- GRAVAR OS DADOS ---
def gravar_nova_tarefa(nome_tarefa):
    # 1. Busca o estado mais recente do banco
    config_atual = tabela_config.search(Config.id_config == "global")[0]

    # 2. Verifica se a tarefa já existe para não sobrescrever dados
    if nome_tarefa in config_atual['tarefas']:
        print(f"Aviso: A tarefa '{nome_tarefa}' já existe!")
        return False

    # 3. Define a estrutura com os valores padrão para a nova tarefa
    config_atual['tarefas'][nome_tarefa] = {
        "hora": "00",
        "minuto": "00",
        "pastas_origem": [],
        "pastas_destino": [],
        "executando": False,
        "execucao": [False, False, False, False, False, False, False, False],
        "desligar": False,
        "desabilitar_tarefa": False,
    }

    # 4. Salva de volta no TinyDB
    tabela_config.update(config_atual, Config.id_config == "global")
    print(f"Tarefa '{nome_tarefa}' adicionada com sucesso!")
    return True

def atualizar_campo_tarefa(nome_tarefa, campo, valor):
    # 1. Busca o estado mais recente do banco de dados
    config_atual = tabela_config.search(Config.id_config == "global")[0]

    # 2. Verifica se a tarefa existe para evitar erros de chave (KeyError)
    if nome_tarefa in config_atual['tarefas']:
        # 3. Altera cirurgicamente apenas o campo desejado na memória
        config_atual['tarefas'][nome_tarefa][campo] = valor

        # 4. Grava de volta o documento inteiro atualizado
        tabela_config.update(config_atual, Config.id_config == "global")
    else:
        print(f"Erro: A {nome_tarefa} não existe nas configurações globais.")

def renomear_tarefa(nome_antigo, nome_novo):
    # 1. Busca o estado mais recente do banco
    config_atual = tabela_config.search(Config.id_config == "global")[0]

    # 2. Verifica se a tarefa antiga realmente existe e se o nome novo já não está em uso
    if nome_antigo in config_atual['tarefas']:
        if nome_novo in config_atual['tarefas']:
            print(f"Erro: Já existe uma tarefa chamada '{nome_novo}'.")
            return

        # 3. Copia os dados para a nova chave e remove a antiga
        config_atual['tarefas'][nome_novo] = config_atual['tarefas'][nome_antigo]
        del config_atual['tarefas'][nome_antigo]

        # 4. Grava a alteração no TinyDB
        tabela_config.update(config_atual, Config.id_config == "global")
        print(f"Tarefa '{nome_antigo}' renomeada com sucesso para '{nome_novo}'!")
    else:
        print(f"Erro: A tarefa '{nome_antigo}' não foi encontrada.")

# --- LEITURA DOS DADOS ---
def carregar_dados_tarefa():
    config_atual = tabela_config.search(Config.id_config == "global")[0]

    return config_atual

# --- REMOVER OS DADOS ---
def apagar_dados_tarefa(nome_tarefa):
    # 1. Busca o estado mais recente do banco
    config_atual = tabela_config.search(Config.id_config == "global")[0]

    # 2. Verifica se a tarefa realmente existe antes de tentar deletar
    if nome_tarefa in config_atual['tarefas']:
        # 3. Remove a tarefa inteira do dicionário
        del config_atual['tarefas'][nome_tarefa]

        # 4. Salva o documento atualizado de volta no TinyDB
        tabela_config.update(config_atual, Config.id_config == "global")
        print(f"Tarefa '{nome_tarefa}' removida com sucesso!")
        return True
    else:
        print(f"Erro: A tarefa '{nome_tarefa}' não foi encontrada para remoção.")
        return False