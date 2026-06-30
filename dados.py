import os

from tinydb import TinyDB, Query

dados_dir = "dados"

if not os.path.exists(dados_dir):
    os.makedirs(dados_dir)

db = TinyDB('dados/backup_config.json')
tabela_config = db.table('configuracoes')
Config = Query()

# 1. Nova estrutura ideal (cada tarefa contém seus próprios dados)
dados_backup = {
    "id_config": "global",
    # Centralizamos tudo o que pertence às tarefas aqui dentro
    "tarefas": {
        "tarefa1": {
            "hora": "10",
            "minuto": "45",
            "pastas_origem": ["pasta1", "pasta2"],
            "pastas_destino": ["pasta1", "pasta2"],
            "executando": False,
            "execucao": [True, False, False, False, False, False, False, False],  # Dias da semana, por exemplo
            "desligar": False,
            "desabilitar_tarefa": False,
        },
        "tarefa2": {
            "hora": "12",
            "minuto": "30",
            "pastas_origem": ["pasta1", "pasta2"],
            "pastas_destino": ["pasta1", "pasta2"],
            "executando": False,
            "execucao": [True, False, False, False, False, False, False, False],  # Dias da semana, por exemplo
            "desligar": False,
            "desabilitar_tarefa": False,
        },
        "tarefa3": {
            "hora": "16",
            "minuto": "00",
            "pastas_origem": ["pasta1", "pasta2"],
            "pastas_destino": ["pasta1", "pasta2"],
            "executando": False,
            "execucao": [True, False, False, False, False, False, False, False],  # Dias da semana, por exemplo
            "desligar": False,
            "desabilitar_tarefa": False,
        }
    }
}

# Inicializa o banco se estiver vazio
if not tabela_config.all():
    tabela_config.insert(dados_backup)

# --- COMO ADICIONAR A TAREFA 4 NESTA NOVA ESTRUTURA ---

# 1. Buscamos as configurações atuais
config_atual = tabela_config.search(Config.id_config == "global")[0]

# 2. Adicionamos a tarefa4 com todos os seus dados exclusivos de forma organizada
config_atual['tarefas']['tarefa4'] = {
    "hora": "22",
    "minuto": "15",
    "pastas_origem": ["pasta_nova_1"],
    "pastas_destino": ["pasta_backup_4"],
    "executando": False
}

# 3. Salvamos de volta no TinyDB
tabela_config.update(config_atual, Config.id_config == "global")

print("Tarefa 4 com horário exclusivo adicionada com sucesso!")