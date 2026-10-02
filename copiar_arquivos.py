import os
import platform
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PyQt6.QtCore import QThread, pyqtSignal

import dados_tinydb
from arquivo_log import gerar_arquivo_log, registrar_log
from config import log_files

# Aumenta o buffer interno do Windows no shutil para 16MB
shutil._WINDOWS_INTERNAL_BUFFER_SIZE = 16 * 1024 * 1024
SYSTEM_OS = platform.system()


def formatar_tamanho(tamanho):
    try:
        tamanho = float(tamanho)
    except (ValueError, TypeError):
        return "0.00 B"

    for unidade in ['B', 'KB', 'MB', 'GB', 'TB']:
        if tamanho < 1024.0:
            return f"{tamanho:.2f} {unidade}"
        tamanho /= 1024.0
    return f"{tamanho:.2f} PB"


class WorkerCopia(QThread):
    # --- SINAIS PARA A INTERFACE GRÁFICA ---
    sinal_progresso = pyqtSignal(int, float)            # (porcentagem_int, porcentagem_float)
    sinal_andamento = pyqtSignal(str)                   # Texto exibindo o arquivo atual
    sinal_execucao = pyqtSignal(str)                    # Texto exibindo a tarefa em execução
    sinal_tamanho_copiado = pyqtSignal(str)             # Texto com tamanho somado
    sinal_tamanho_total = pyqtSignal(str)               # Texto com tamanho total calculado
    sinal_estado_botoes = pyqtSignal(bool, bool, bool)  # (cmb/executar_enabled, pausar_enabled, finalizado)
    sinal_alerta = pyqtSignal(str, str)                 # (Título, Mensagem) para dialogs
    sinal_concluido = pyqtSignal(bool, bool)            # (teve_erro, foi_cancelado)

    def __init__(self, nome_tarefa=None, pastas_origem=None, pastas_destino=None, modo_automatizado=False):
        super().__init__()
        self.nome_tarefa = nome_tarefa
        self.pastas_origem = pastas_origem
        self.pastas_destino = pastas_destino
        self.modo_automatizado = modo_automatizado

        # Controle de fluxo da thread
        self.cancelar = False
        self.pausar = False
        self.tamanho_total = 0
        self.soma = 0

    def solicitar_pausa(self):
        self.pausar = True

    def solicitar_cancelamento(self):
        self.cancelar = True

    def run(self):
        """Ponto de entrada executado em segundo plano pela QThread."""
        if self.modo_automatizado:
            self._executar_copia_automatizada()
            return

        # Desabilita botões da interface via sinal
        self.sinal_estado_botoes.emit(False, True, False)
        self.sinal_execucao.emit(f"Executando...\n{self.nome_tarefa}")

        # Carrega tarefas do banco caso não tenham sido passadas manualmente
        if not self.pastas_origem or not self.pastas_destino:
            carregar_dados = dados_tinydb.carregar_dados_tarefa()
            self.pastas_origem = carregar_dados['tarefas'][self.nome_tarefa]['pastas_origem']
            self.pastas_destino = carregar_dados['tarefas'][self.nome_tarefa]['pastas_destino']

        # 1. Calcula o tamanho total antes de iniciar a cópia
        self._calcular_tamanho_total()

        # 2. Executa o fluxo principal de cópia
        self._copiando_pastas()

        # Reabilita botões da interface ao finalizar
        self.sinal_estado_botoes.emit(True, False, True)
        self.sinal_andamento.emit("Concluído cópia!")
        self.sinal_execucao.emit("")
        self.sinal_concluido.emit(False, self.cancelar)

    def _calcular_tamanho_total(self):
        """Calcula o tamanho total dos arquivos para a barra de progresso."""
        self.sinal_tamanho_total.emit("Atualizando...")
        self.tamanho_total = 0

        for pasta in self.pastas_origem:
            ver_pasta = Path(pasta)
            if ver_pasta.exists():
                for item in ver_pasta.rglob("*"):
                    if self.cancelar:
                        return
                    if item.is_file():
                        try:
                            self.tamanho_total += item.stat(follow_symlinks=False).st_size
                        except Exception:
                            pass

        self.sinal_tamanho_total.emit(formatar_tamanho(self.tamanho_total))

    def _copiando_pastas(self):
        """Itera sobre os pares de origem/destino e gerencia a cópia."""
        for i, (origem, destino_base) in enumerate(zip(self.pastas_origem, self.pastas_destino)):
            if self.cancelar:
                return

            caminho_origem = Path(origem)
            pasta_destino_final = Path(destino_base) / caminho_origem.name

            self.sinal_andamento.emit(f"Iniciando cópia... {i + 1}")
            self._copiando_arquivos(str(caminho_origem), pasta_destino_final)

    def _copiando_arquivos(self, origem, destino):
        caminho_log = gerar_arquivo_log(log_files)

        with ThreadPoolExecutor(max_workers=2) as executor:
            for raiz, dirs, files in os.walk(origem, onerror=lambda a: None):
                if self.pausar:
                    self.sinal_alerta.emit("Pausa", "Tarefa pausada")
                    self.pausar = False

                if self.cancelar:
                    return

                destino_final = destino / Path(raiz).relative_to(origem)
                try:
                    if Path(raiz).is_dir():
                        destino_final.mkdir(parents=True, exist_ok=True)

                    for f in files:
                        origem_arquivo = Path(raiz) / f
                        try:
                            tamanho_arq = origem_arquivo.stat(follow_symlinks=False).st_size
                            self.soma += tamanho_arq
                            destino_arquivo = destino / Path(raiz).relative_to(origem) / f

                            # Emite os sinais de atualização para a GUI
                            self.sinal_andamento.emit(f"{formatar_tamanho(tamanho_arq)} -> {origem_arquivo}")
                            self.sinal_tamanho_copiado.emit(formatar_tamanho(self.soma))

                            if self.tamanho_total > 0:
                                pct_float = (self.soma / self.tamanho_total) * 100
                                self.sinal_progresso.emit(int(pct_float), pct_float)

                            executor.submit(self._copiar_arquivo, origem_arquivo, destino_arquivo, caminho_log)
                        except Exception as e:
                            registrar_log(caminho_log, f"[ERRO] Copiando -> {e} -> {origem_arquivo}")

                except Exception as e:
                    registrar_log(caminho_log, f"[ERRO] Criando pasta -> {e}")

    def _executar_copia_automatizada(self):
        """Fluxo sem atualização pesada de interface para rotinas em segundo plano."""
        caminho_log = gerar_arquivo_log(log_files)
        registrar_log(caminho_log, "Iniciando processo de backup automatizado.")

        with ThreadPoolExecutor(max_workers=2) as executor:
            for i, (origem, destino_base) in enumerate(zip(self.pastas_origem, self.pastas_destino)):
                caminho_origem = Path(origem)
                destino = Path(destino_base) / caminho_origem.name

                registrar_log(caminho_log, f"Copiando pasta {origem}")

                for raiz, dirs, files in os.walk(origem, onerror=lambda a: None):
                    destino_final = destino / Path(raiz).relative_to(origem)
                    try:
                        if Path(raiz).is_dir():
                            destino_final.mkdir(parents=True, exist_ok=True)

                        for f in files:
                            origem_arquivo = Path(raiz) / f
                            destino_arquivo = destino / Path(raiz).relative_to(origem) / f
                            try:
                                executor.submit(self._copiar_arquivo, origem_arquivo, destino_arquivo, caminho_log)
                            except Exception as e:
                                registrar_log(caminho_log, f"[ERRO] ao copiar: {e} {origem_arquivo}")
                    except Exception as e:
                        registrar_log(caminho_log, f"[ERRO] Criando pasta -> {e}")

        registrar_log(caminho_log, "Processo finalizado.\n" + ("_" * 40))
        self.sinal_concluido.emit(False, False)

    def _copiar_arquivo(self, origem_arquivo, destino_arquivo, caminho_log):
        """Realiza a cópia física do arquivo tratando o limite de caminhos do Windows."""
        try:
            if SYSTEM_OS == 'Windows':
                str_origem = f"\\\\?\\{origem_arquivo.resolve()}"
                str_destino = f"\\\\?\\{destino_arquivo.resolve()}"
            else:
                str_origem = origem_arquivo
                str_destino = destino_arquivo

            path_destino = Path(str_destino)
            path_origem = Path(str_origem)

            if not path_destino.is_file() or (path_origem.stat().st_mtime > path_destino.stat().st_mtime):
                shutil.copy2(str_origem, str_destino, follow_symlinks=False)
        except shutil.SameFileError:
            pass
        except Exception as e:
            registrar_log(caminho_log, f"[ERRO] Copiando -> {e} -> Origem {origem_arquivo} -> Destino {destino_arquivo}")

class WorkerCalculoTamanho(QThread):
    sinal_tamanho = pyqtSignal(str)

    def __init__(self, pastas_origem):
        super().__init__()
        self.pastas_origem = pastas_origem

    def run(self):
        self.sinal_tamanho.emit("Atualizando...")
        tamanho_total = 0
        for pasta in self.pastas_origem:
            ver_pasta = Path(pasta)
            if ver_pasta.exists():
                for item in ver_pasta.rglob("*"):
                    if item.is_file():
                        try:
                            tamanho_total += item.stat(follow_symlinks=False).st_size
                        except Exception:
                            pass
        self.sinal_tamanho.emit(formatar_tamanho(tamanho_total))

def iniciar_calculo_tamanho(view, pastas_origem, liberar=""):
    """Função compatível para chamar o cálculo de tamanho avulso."""
    global worker_tamanho_global
    worker_tamanho_global = WorkerCalculoTamanho(pastas_origem)
    worker_tamanho_global.sinal_tamanho.connect(
        view.controles['lbl_tamanho_exibir'].setText
    )
    worker_tamanho_global.start()