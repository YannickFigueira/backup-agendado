import json
import os

import estilo

desmontar_chave = 10 # Mudar para o número desejado

# Dados iniciais
dados_chave = {
    "app": {
        "name": f"{estilo.NOME_PROGRAMA}",
        "version": f"{estilo.VERSION}"
    },
    "crypto": {
        "key": ""
    }
}

dados_config = {
    "app": {
        "name": f"{estilo.NOME_PROGRAMA}",
        "version": f"{estilo.VERSION}"
    },
    "database": {
        "tarefa": [
            "tarefa1",
            "tarefa2",
            "tarefa3"
        ],
        "hora": "10",
        "minuto": "45",
        "pastas_origem": {
            "tarefa1": ["pasta1, pasta2"],
            "tarefa2": ["pasta1, pasta2"],
            "tarefa3": ["pasta1, pasta2"],
        },
        "pastas_destino": {
            "tarefa1": ["pasta1, pasta2"],
            "tarefa2": ["pasta1, pasta2"],
            "tarefa3": ["pasta1, pasta2"],
        },
        "execucao": "True, False, False, False, False, False, False, False",
        "tarefa_executando": [
            "False",
            "False",
            "False"
        ],
        "desligar": "False",
        "desabilitar_tarefa": "False",
        "ultima_nota_nfce": "",
        "relatorio": "True",
        "segundo_sistema": "False",
        "segundo_sis_pasta": "",
        "modoenvio": "Telegram",
        "telegrambot": "",
        "chat_id": ""
    }}

# Diretórios base
dados_dir = "dados"

if not os.path.exists(dados_dir):
    os.makedirs(dados_dir)

    with open(f"{dados_dir}/chave.json", "w", encoding="utf-8") as c:
        json.dump(dados_chave, c, indent=4, ensure_ascii=False)

    with open(f"{dados_dir}/config.json", "w", encoding="utf-8") as c:
        json.dump(dados_config, c, indent=4, ensure_ascii=False)

# --- Gravação ---
def gravar_dados(campo, valor):
    with open(f"{dados_dir}/config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    if campo == "pastas_destino":
        horas_separate = valor.split("\n")
        config["database"]["pastas_destino"].clear()
        for separate in horas_separate:
            if separate != "":
                config["database"]["pastas_destino"].append(separate)
    else:
        config["database"][campo] = valor

    with open(f"{dados_dir}/config.json", "w", encoding="utf-8") as fw:
        json.dump(config, fw, indent=4, ensure_ascii=False)

def ler_dados(dados):
    with open(f"{dados_dir}/config.json", "r", encoding="utf-8") as d:
        config = json.load(d)

    # Acessando dados
    tarefa = config["database"]["tarefa"]
    hora = config["database"]["hora"]
    caminho = config["database"]["pastas_origem"]
    horas = config["database"]["pastas_destino"]
    relatorio_str = config["database"]["relatorio"]
    relatorio = relatorio_str.strip().lower() == "true"
    segundo_sis_str = config["database"]["segundo_sistema"]
    segundo_sis = segundo_sis_str.strip().lower() == "true"
    segundo_sis_pasta = config["database"]["segundo_sis_pasta"]
    desligar = config["database"]["desligar"]
    modoenvio = config["database"]["modoenvio"]

    execucao = config["database"]["execucao"]
    tarefa_executando_str = config["database"]["tarefa_executando"]  # exemplo: "False"
    tarefa_executando = tarefa_executando_str.strip().lower() == "true"

    if dados == "tarefa":
        return tarefa
    elif dados == "hora":
        return hora
    elif dados == "caminho":
        return caminho
    elif dados == "pastas_destino":
        return horas
    elif dados == "relatorio":
        return relatorio
    elif dados == "segundo_sistema":
        return segundo_sis
    elif dados == "desligar":
        return desligar
    elif dados == "segundo_sis_pasta":
        return segundo_sis_pasta
    elif dados == "modoenvio":
        return modoenvio
    elif dados == "execucao":
        return int(execucao)
    elif dados == "tarefa_executando":
        return tarefa_executando
    return None


