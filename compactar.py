import os
import zipfile
from pathlib import Path
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QMessageBox

from arquivo_log import gerar_arquivo_log, registrar_log


# Assumindo que suas funções de log existem no projeto
# from log import gerar_arquivo_log, registrar_log


class WorkerCompactador(QThread):
    # Sinais para comunicação segura entre a Thread de Fundo e a GUI
    progresso = pyqtSignal(int, int)        # Envia (contador, total)
    mensagem = pyqtSignal(str, str, str)    # Envia (tipo, titulo, conteudo)
    finalizado = pyqtSignal()               # Sinaliza término

    def __init__(self, origem, destino_zip, parent=None):
        super().__init__(parent)
        self.origem = origem
        self.destino_zip = destino_zip

    def run(self):
        caminho_log = gerar_arquivo_log()
        registrar_log(caminho_log, "Iniciado processo de compactação")

        pasta_origem = Path(self.origem)
        caminho_destino = Path(self.destino_zip)

        if caminho_destino.is_dir() or not caminho_destino.suffix:
            arquivo_final = caminho_destino / f"{pasta_origem.name}.zip"
        else:
            arquivo_final = caminho_destino

        destino_zip_str = str(arquivo_final)

        try:
            with zipfile.ZipFile(destino_zip_str, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Contagem prévia de arquivos
                total = sum(len(arquivos) for _, _, arquivos in os.walk(self.origem))
                contador = 0

                if total == 0:
                    self.progresso.emit(1, 1)
                else:
                    for raiz, _, arquivos in os.walk(self.origem):
                        for arquivo in arquivos:
                            try:
                                caminho_completo = Path(raiz) / arquivo
                                caminho_relativo = caminho_completo.relative_to(self.origem)
                                zipf.write(caminho_completo, caminho_relativo)

                                contador += 1
                                self.progresso.emit(contador, total)
                            except Exception as e:
                                registrar_log(caminho_log, f"Erro ao compactar {caminho_completo}: {e}")

            registrar_log(caminho_log, "Finalizado compactação!")
            self.mensagem.emit("info", "Completo", "Finalizado com êxito.")

        except Exception as e:
            registrar_log(caminho_log, f"Erro crítico na compactação: {e}")
            self.mensagem.emit("critical", "Erro", f"Ocorreu um erro ao compactar: {e}")

        finally:
            self.finalizado.emit()