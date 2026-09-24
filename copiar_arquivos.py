import os
import shutil
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import platform

import caixa_mensagem
import dados_tinydb
from arquivo_log import gerar_arquivo_log, registrar_log
from config import log_files

# Aumenta o buffer interno do Windows no shutil para 16MB (o padrão é 64KB)
# Isso reduz as chamadas de sistema e evita que o cache esvazie, mitigando as pausas.
shutil._WINDOWS_INTERNAL_BUFFER_SIZE = 16 * 1024 * 1024

# Variável
sistema = platform.system()
tarefas_executando = []
cancelar = False
pausar = False
liberar_total = False
tamanho_total = 0
contador = 1
soma = 0

def pausar_copia():
    global pausar
    pausar = True

def cancelar_copia():
    resposta = caixa_mensagem.sim_nao("Cancelar", "Quer realmente cancelar?")
    if resposta == "Sim":
        global cancelar
        cancelar = True

### Atualiza a barra de progresso ###
def atualizar_barra(view, valor, total):
    porcentagem = (valor / total)
    view.controles['progress_bar'].set(porcentagem)
    #self.view.controles['lbl_porcentagem'].configure(text=f"{(porcentagem * 100):.3f}%")
    # 2. Atualiza o texto do canvas
    texto_id = view.controles['lbl_porcentagem']
    view.controles['progress_bar']._canvas.itemconfig(texto_id, text=f"{(porcentagem * 100):.3f}%")

# --- Inicio do procedimento
def iniciar_calculo_tamanho(view, pastas_origem, liberar):
    t = threading.Thread(
        target=tamanho_pasta,
        args=(view, pastas_origem, liberar),
        daemon=True
    )
    t.start()

def tamanho_pasta(view, pastas_origem, liberar):
    global tamanho_total, liberar_total
    lbl_tamanho_exibir = view.controles['lbl_tamanho_exibir']
    view.controles['lbl_tamanho_exibir'].setText("Atualizando...")
    tamanho_total = 0
    for pasta in pastas_origem:
        ver_pasta = Path(pasta)

        # Iteramos pelos arquivos para contar e somar o tamanho simultaneamente
        for item in ver_pasta.rglob("*"):
            if item.is_file():
                tamanho_total += item.stat(follow_symlinks=False).st_size

    view.controles['lbl_tamanho_exibir'].setText(formatar_tamanho(tamanho_total))

    match liberar:
        case "execucao":
            liberar_total = True
        case _:
            return

def formatar_tamanho(tamanho):
    # Converte o valor para float com segurança
    try:
        tamanho = float(tamanho)
    except (ValueError, TypeError):
        return "0.00 B"

    for unidade in ['B', 'KB', 'MB', 'GB', 'TB']:
        if tamanho < 1024.0:
            return f"{tamanho:.2f} {unidade}"
        tamanho /= 1024.0
    return f"{tamanho:.2f} PB"

# --- Execução da cópia dos arquivos ---
def iniciar_copiar_arquivos(view, nome_tarefa):
    global contador, soma
    contador = 1
    soma = 0
    view.controles['cmb_selecao'].setEnabled(False)
    view.controles['btn_executar'].setEnabled(False)
    view.controles['btn_pausar'].setEnabled(True)
    carregar_dados = dados_tinydb.carregar_dados_tarefa()
    pastas_origem = carregar_dados['tarefas'][nome_tarefa]['pastas_origem']
    pastas_destino = carregar_dados['tarefas'][nome_tarefa]['pastas_destino']
    view.controles['lbl_multi_execucao'].setText(f"Executando...\n{nome_tarefa}")

    iniciar_calculo_tamanho(view, pastas_origem, "execucao")
    iniciar_copia(pastas_origem, pastas_destino, view)

def iniciar_copia(pastas_origem, pastas_destino, view):
    t = threading.Thread(
        target=copiando_pastas,
        args=(pastas_origem, pastas_destino, view),
        daemon=True
    )
    t.start()

def copiando_pastas(pastas_origem, pastas_destino, view):
    # Pegamos um widget do Tkinter do dicionário para usar o procedimento .after()
    lbl_andamento = view.controles['lbl_multi_andamento']
    lbl_execucao = view.controles['lbl_multi_execucao']

    # zip alinha origem/destino; enumerate fornece o índice 'i'
    for i, (origem, destino_base) in enumerate(zip(pastas_origem, pastas_destino)):
        caminho_origem = Path(origem)
        # / une caminhos automaticamente independente do S.O.
        pasta_destino_final = Path(destino_base) / caminho_origem.name

        # Atualização segura do Tkinter vindo de Thread
        lbl_andamento.setText(f"Iniciando cópia...{i}")

        copiando_arquivos(str(caminho_origem), str(pasta_destino_final), view)

    # Atualiza a interface ao finalizar todas as cópias
    view.controles['cmb_selecao'].configure(state="normal")
    view.controles['btn_executar'].configure(state="normal")
    view.controles['btn_pausar'].configure(state="disabled")
    lbl_andamento.after(0, lambda: view.controles['lbl_multi_andamento'].configure(text="Concluído cópia!"))
    lbl_execucao.after(0, lambda: view.controles['lbl_multi_execucao'].configure(text=""))

def copiando_arquivos(origem, destino, view):
    caminho_log = gerar_arquivo_log(log_files)
    global cancelar, pausar, tamanho_total, soma
    lbl_andamento = view.controles['lbl_multi_andamento']
    lbl_copiado_tamanho = view.controles['lbl_copiado_tamanho']

    with ThreadPoolExecutor(max_workers=2) as executor:
        for raiz, dirs, files in os.walk(origem, onerror=lambda a: None):
            if pausar:
                caixa_mensagem.info("Pausa", "Tarefa pausada")
                pausar = False

            if cancelar:
                print("Tarefa encerrada")
                return

            destino_final = destino / Path(raiz).relative_to(origem)
            try:
                if Path(raiz).is_dir():
                    destino_final.mkdir(parents=True, exist_ok=True)

                for f in files:
                    origem_arquivo = Path(raiz) / f
                    try:
                        # follow_symlinks=False evita tentar resolver atalhos/symlinks quebrados
                        soma += origem_arquivo.stat(follow_symlinks=False).st_size
                        destino_arquivo = destino / Path(raiz).relative_to(origem) / f
                        lbl_andamento.after(0, lambda: view.controles['lbl_multi_andamento'].configure(text=f"{formatar_tamanho(origem_arquivo.stat().st_size)} -> {origem_arquivo}"))
                        lbl_copiado_tamanho.after(0, lambda: view.controles['lbl_copiado_tamanho'].configure(text=formatar_tamanho(soma)))

                        executor.submit(copiar, origem_arquivo, destino_arquivo, caminho_log)
                    except Exception as e:
                        erro_encontrado = True
                        registrar_log(caminho_log, f"[ERRO] Copiando -> {e} -> {origem_arquivo}")

                    if liberar_total:
                        atualizar_barra(view, soma, tamanho_total)
            except Exception as e:
                registrar_log(caminho_log, f"[ERRO] Criando pasta -> {e}")

# --- Procedimento de cópia automatizada ---
def inicar_copia_automatizada(pastas_origem, pastas_destino):
    caminho_log = gerar_arquivo_log(log_files)
    registrar_log(caminho_log, "Iniciando processo de backup.")

    # Executa a cópia concorrente
    with ThreadPoolExecutor(max_workers=2) as executor:
        # zip alinha origem/destino; enumerate fornece o índice 'i'
        for i, (origem, destino_base) in enumerate(zip(pastas_origem, pastas_destino)):
            caminho_origem = Path(origem)
            # / une caminhos automaticamente independente do S.O.
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
                            executor.submit(copiar, origem_arquivo, destino_arquivo, caminho_log)
                        except Exception as e:
                            registrar_log(caminho_log, f"[ERRO] ao copiar: {e} {origem_arquivo}")
                except Exception as e:
                    registrar_log(caminho_log, f"[ERRO] Criando pasta -> {e}")

        registrar_log(caminho_log, "Processo finalizado.\n" + ("_" * 40))

def copiar(origem_arquivo, destino_arquivo, caminho_log):

    try:
        # --- ADICIONE ESTAS LINHAS PARA TRATAR O ERRO 206 ---
        if sistema == 'Windows':
            # Resolve o caminho absoluto e aplica o prefixo UNICODE para caminhos longos
            str_origem = f"\\\\?\\{origem_arquivo.resolve()}"
            str_destino = f"\\\\?\\{destino_arquivo.resolve()}"
        else:
            str_origem = origem_arquivo
            str_destino = destino_arquivo
        # ----------------------------------------------------

        # Atualize as verificações e o shutil.copy2 usando as strings formatadas
        path_destino = Path(str_destino)
        path_origem = Path(str_origem)

        if not path_destino.is_file() or (path_origem.stat().st_mtime > path_destino.stat().st_mtime):
            # shutil.copy2 aceita as strings com o prefixo \\?\
            shutil.copy2(str_origem, str_destino, follow_symlinks=False)
    except shutil.SameFileError:
        pass
    except Exception as e:
        erro_encontrado = True
        registrar_log(caminho_log, f"[ERRO] Copiando -> {e} -> Origem {origem_arquivo} -> Destino {destino_arquivo}")
