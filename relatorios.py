import os
import time
import tempfile
from datetime import datetime, date
from PyQt6.QtCore import QThread

import config
import dados_tinydb
import telegrambot
from copiar_arquivos import WorkerCopia
from compactar import WorkerCompactador


class GerenciadorRelatorio:
    def __init__(self):
        self.pastas_origem = config.log_files if isinstance(config.log_files, list) else [config.log_files]
        self.pastas_destino = config.temp if isinstance(config.temp, list) else [config.temp]
        self.worker_copia = None
        self.worker_compactador = None
        self.arquivo_controle = os.path.join(
            tempfile.gettempdir(),
            "relatorio_telegram_enviado.flag"
        )

    def iniciar_processo(self):
        """Inicia o fluxo assíncrono de Cópia -> Compactação -> Envio."""
        self.worker_copia = WorkerCopia(
            pastas_origem=self.pastas_origem,
            pastas_destino=self.pastas_destino,
            modo_automatizado=False
        )
        self.worker_copia.finished.connect(self._ao_concluir_copia)
        self.worker_copia.start()

    def _ao_concluir_copia(self):
        origem = self.pastas_origem[0]
        destino_zip = self.pastas_destino[0]

        self.worker_compactador = WorkerCompactador(origem, destino_zip, parent=None)
        self.worker_compactador.finished.connect(self._ao_concluir_compactacao)
        self.worker_compactador.start()

    def _ao_concluir_compactacao(self):
        destino_zip = self.pastas_destino[0] / f"{self.pastas_origem[0].name}.zip"
        config_dados = dados_tinydb.carregar_dados_telegram()
        telegram, chat_id = dados_tinydb.ler_dados_telegram(config_dados)

        telegrambot.enviar_arquivo(telegram, chat_id, destino_zip)
        self._registrar_envio()

        self.worker_copia = None
        self.worker_compactador = None

    def _eh_primeiro_dia_util(self, data_referencia: date) -> bool:
        if data_referencia.weekday() >= 5:
            return False
        for dia in range(1, data_referencia.day):
            if date(data_referencia.year, data_referencia.month, dia).weekday() < 5:
                return False
        return True

    def _ja_foi_enviado_este_mes(self, hoje: date) -> bool:
        if not os.path.exists(self.arquivo_controle):
            return False
        try:
            with open(self.arquivo_controle, "r", encoding="utf-8") as f:
                return f.read().strip() == hoje.strftime("%Y-%m")
        except IOError:
            return False

    def _registrar_envio(self):
        try:
            with open(self.arquivo_controle, "w", encoding="utf-8") as f:
                f.write(date.today().strftime("%Y-%m"))
        except IOError as e:
            print(f"Erro ao salvar flag de controle: {e}")

    def checar_e_executar(self):
        """Verifica regras de envio mensal."""
        hoje = date.today()
        if self._eh_primeiro_dia_util(hoje) and not self._ja_foi_enviado_este_mes(hoje):
            print(f"[{datetime.now()}] Primeiro dia útil do mês. Iniciando relatório...")
            self.iniciar_processo()


class MonitorRelatorioThread(QThread):
    """Thread que roda em segundo plano monitorando o tempo continuamente."""
    def __init__(self, interval_segundos=3600):
        super().__init__()
        self.intervalo = interval_segundos  # Checa a cada 1 hora por padrão
        self.gerenciador = GerenciadorRelatorio()
        self.executando = True

    def run(self):
        while self.executando:
            # Tenta executar a verificação
            self.gerenciador.checar_e_executar()
            # Aguarda o intervalo antes da próxima checagem
            time.sleep(self.intervalo)

    def parar(self):
        self.executando = False


# Variável global do módulo para manter a referência viva
_monitor_thread = None

def iniciar_monitoramento_relatorio():
    """Função de entrada para iniciar a thread em segundo plano."""
    global _monitor_thread
    if _monitor_thread is None or not _monitor_thread.isRunning():
        _monitor_thread = MonitorRelatorioThread()
        _monitor_thread.start()