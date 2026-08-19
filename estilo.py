# estilo.py
import os
from pathlib import Path

# Versão e repositório
VERSION = "v4.0.0"
REPO= "backup-agendado"
NOME_PROGRAMA = "Backup Agendado"

# Pastas de configuração Linux
home_dir = os.path.expanduser('~')
programa_dir = f"{home_dir}/.backup agendado"
notas = f"{home_dir}/.backup agendado/notas"
log_files = Path(f"{home_dir}/.backup agendado/logs")

if not os.path.exists(programa_dir):
    os.mkdir(programa_dir)
if not os.path.exists(notas):
    os.mkdir(notas)
if not os.path.exists(log_files):
    os.mkdir(log_files)

# Margens padrão para janelas e frames
# Medidas
ESPACO = 5
LINHA_PAINEL_ESQUERDO = 0

# Container
ESPACOX = ESPACO
ESPACOY = 15

# Arquivo de log
ARQUIVO_ERRO = "backup_agendado.log"

# Estilo
FONTE_VAZIA=("", 11, "normal")
FONTE_ARIAL=("Arial", 11, "normal")
