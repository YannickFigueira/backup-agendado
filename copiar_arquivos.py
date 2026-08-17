import os
import shutil
import threading
import time
from pathlib import Path
from tkinter import messagebox

import dados_tinydb

# Variável
tarefas_executando = []
cancelar = False
pausar = False
liberar_total = False
total_arquivos = 0
contador = 1
soma = 0

def pausar_copia():
    global pausar
    pausar = True

def cancelar_copia():
    resposta = messagebox.askyesno("Cancelar", "Quer realmente cancelar?")
    if resposta:
        global cancelar
        cancelar = True

### Atualiza a barra de progresso ###
def atualizar_barra(valor, total, progress_canvas):
    progress_canvas.delete("all")
    largura = int((valor / total) * progress_canvas.winfo_width())
    # desenha a barra preenchida
    progress_canvas.create_rectangle(0, 0, largura, 25, fill="green")
    # escreve a porcentagem dentro da barra
    porcentagem = (valor / total) * 100
    x = progress_canvas.winfo_width() // 2
    progress_canvas.create_text(x, 12, text=f"{porcentagem:.3f}%", fill="black", font=("Arial", 10, "bold"))

# --- Inicio de todo o procedimento
def iniciar_calculo_tamanho(view, pastas_origem, liberar):
    t = threading.Thread(
        target=tamanho_pasta,
        args=(view, pastas_origem, liberar),
        daemon=True
    )
    t.start()

def tamanho_pasta(view, pastas_origem, liberar):
    global total_arquivos, liberar_total
    lbl_tamanho_exibir = view.controles['lbl_tamanho_exibir']
    lbl_tamanho_exibir.after(0, lambda: view.controles['lbl_tamanho_exibir'].config(text="Atualizando..."))
    tamanho_total = 0
    total_arquivos = 0
    for pasta in pastas_origem:
        ver_pasta = Path(pasta)

        # Iteramos pelos arquivos para contar e somar o tamanho simultaneamente
        for item in ver_pasta.rglob("*"):
            if item.is_file():
                total_arquivos += 1
                tamanho_total += item.stat().st_size

    lbl_tamanho_exibir.after(0, lambda: view.controles['lbl_tamanho_exibir'].config(text=formatar_tamanho(tamanho_total)))

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
    view.controles['cmb_selecao'].config(state="disabled")
    view.controles['btn_executar'].config(state="disabled")
    view.controles['btn_pausar'].config(state="normal")
    carregar_dados = dados_tinydb.carregar_dados_tarefa()
    pastas_origem = carregar_dados['tarefas'][nome_tarefa]['pastas_origem']
    pastas_destino = carregar_dados['tarefas'][nome_tarefa]['pastas_destino']
    view.controles['lbl_multi_execucao'].config(text=f"Executando...\n{nome_tarefa}")
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
    # Pegamos um widget do Tkinter do dicionário para usar o método .after()
    lbl_andamento = view.controles['lbl_multi_andamento']
    lbl_execucao = view.controles['lbl_multi_execucao']

    # zip alinha origem/destino; enumerate fornece o índice 'i'
    for i, (origem, destino_base) in enumerate(zip(pastas_origem, pastas_destino)):
        caminho_origem = Path(origem)
        # / une caminhos automaticamente independente do S.O.
        pasta_destino_final = Path(destino_base) / caminho_origem.name

        print(f"Iniciando cópia...{i}\n")

        # Atualização segura do Tkinter vindo de Thread
        lbl_andamento.after(
            0,
            lambda idx=i: lbl_andamento.config(text=f"Iniciando cópia...{idx}")
        )

        copiando_arquivos(str(caminho_origem), str(pasta_destino_final), view)

    # Atualiza a interface ao finalizar todas as cópias
    view.controles['cmb_selecao'].config(state="readonly")
    view.controles['btn_executar'].config(state="normal")
    view.controles['btn_pausar'].config(state="disabled")
    lbl_andamento.after(0, lambda: view.controles['lbl_multi_andamento'].config(text="Concluído cópia!"))
    lbl_execucao.after(0, lambda: view.controles['lbl_multi_execucao'].config(text=""))

def copiando_arquivos(origem, destino, view):
    global cancelar, pausar, contador, total_arquivos, soma
    lbl_andamento = view.controles['lbl_multi_andamento']
    lbl_copiado_tamanho = view.controles['lbl_copiado_tamanho']
    if pausar:
        messagebox.showinfo("Pausa", "Tarefa pausada")
        pausar = False

    if cancelar:
        print("Tarefa encerrada")
        return

    # lista todos os arquivos e subpastas
    arquivos = []
    for raiz, dirs, files in os.walk(origem, onerror=lambda a: None):
        #print(f"Diretorio: {Path(raiz)}")
        destino_final = destino / Path(raiz).relative_to(origem)
        if Path(raiz).is_dir():
            #print(f"{destino_final}")
            destino_final.mkdir(parents=True, exist_ok=True)

        for f in files:
            #arquivos.append(Path(raiz) / f)
            origem_arquivo = Path(raiz) / f
            soma += origem_arquivo.stat().st_size
            print(f"Tamanhos -> {contador}")
            destino_arquivo = destino / Path(raiz).relative_to(origem) / f
            lbl_andamento.after(0, lambda: view.controles['lbl_multi_andamento'].config(text=f"{formatar_tamanho(origem_arquivo.stat().st_size)} -> {origem_arquivo}"))
            lbl_copiado_tamanho.after(0, lambda: view.controles['lbl_copiado_tamanho'].config(text=formatar_tamanho(soma)))

            # 1. Se o arquivo não existe no destino, copia direto
            if not destino_arquivo.is_file():
                shutil.copy2(origem_arquivo, destino_arquivo)

            # 2. Se ele existe, compara as datas de modificação
            elif origem_arquivo.stat().st_mtime > destino_arquivo.stat().st_mtime:
                shutil.copy2(origem_arquivo, destino_arquivo)
            #print(f"Origem -- {Path(raiz) / f}")
            #print(f"Destino -- {destino / Path(raiz).relative_to(origem) / f}")

            if liberar_total:
                atualizar_barra(contador, total_arquivos, view.controles['progress_canvas'])
            contador += 1

    #time.sleep(5)
    print("Executado com sucesso")
