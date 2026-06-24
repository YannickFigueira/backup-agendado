import argparse
import platform
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import re

import verificarversao
from funcoes import Controles
from janela_config import JanelaConfiguracao
from janela_nova_tarefa import JanelaNovaTarefa

def abrir_nova_tarefa(janela_principal):
    # 1. Cria a parte visual
    visual = JanelaNovaTarefa(janela_principal)

    # 2. Cria a lógica e passa a visão para ela controlar
    logica = Controles(visual)

def abrir_configuracoes(janela_principal):
    # 1. Cria a parte visual
    visual = JanelaConfiguracao(janela_principal)

    # 2. Cria a lógica e passa a visão para ela controlar
    logica = Controles(visual)

## Variáveis principais
version = "4.0.0"
repo = "backup-agendado"
programa_title = "Backup Agendado"
# Medidas
espaco = 5
# Estilo
fonte=("", 11, "normal")

parser = argparse.ArgumentParser(prog="backup-agendado")
parser.add_argument("--version", action="version", version=f"%(prog)s {version}")
args = parser.parse_args()

## Container
def criar_separador_com_texto(janela_container, texto, linha, espacox, espacoy):
    # 1. Criamos um container invisível para envelopar o separador completo
    container = ttk.Frame(janela_container)
    container.grid(row=linha, columnspan=6, sticky="ew", padx=espacox, pady=espacoy)

    # Configura o container para expandir as linhas laterais igualmente
    container.columnconfigure(0, weight=1)
    container.columnconfigure(2, weight=1)

    # 2. Linha da Esquerda
    sep_esquerda = ttk.Separator(container, orient="horizontal")
    sep_esquerda.grid(row=0, column=0, sticky="ew", padx=(0, 10))

    # 3. O Texto Centralizado (com peso Bold/Negrito)
    # Usamos o fundo padrão (background) do root para não dar corte de cor
    label_texto = ttk.Label(container, text=texto, font=("", 10, "bold"))
    label_texto.grid(row=0, column=1, sticky="ne")

    # 4. Linha da Direita
    sep_direita = ttk.Separator(container, orient="horizontal")
    sep_direita.grid(row=0, column=2, sticky="ew", padx=(10, 0))

## Barra de Menus
def criar_barra_menu(janela, lbl_log):
    # Criar barra de menu
    barra_menu = tk.Menu(janela)
    janela.config(menu=barra_menu)

    def visitar_site():
        pagina = f"https://github.com/YannickFigueira"
        resposta = messagebox.askyesno("Sobre", f"{programa_title} v{version}\n"
                                                f"Desenvolvedor YannickFigueira\n"
                                                f"chronostimeinchain@gmail.com\n"
                                                f"Deseja visitar a página")
        if resposta:
            verificarversao.webbrowser.open(pagina)

    def abrir_logs():
        if platform.system() == "Windows":
            arquivo = "C:\\Programa Igreja\\doc\\CHANGELOG.md"
            subprocess.run(["notepad", arquivo])
        elif platform.system() == "Linux":
            arquivo = "/usr/share/doc/programaigreja/CHANGELOG.md"
            subprocess.run(["xdg-open", arquivo])  # ou "gedit"
        else:
            print("Sistema não suportado")

    ## Notas da versão
    def extrair_ultima_versao_changelog():
        caminho_arquivo = "CHANGELOG.md"
        if platform.system() == "Windows":
            caminho_arquivo = "C:\\Programa Igreja\\doc\\CHANGELOG.md"
            subprocess.run(["notepad", caminho_arquivo])
        elif platform.system() == "Linux":
            caminho_arquivo = "/usr/share/doc/programaigreja/CHANGELOG.md"
            subprocess.run(["xdg-open", caminho_arquivo])  # ou "gedit"
        else:
            print("Sistema não suportado")

        try:
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                conteudo = f.read()

            # Expressão Regular explicada:
            # (##\s*\[\d+\.\d+\.\d+\].*?) -> Grupo 1: Captura o cabeçalho da versão (ex: ## [0.4.1] - ...)
            # (?=##\s*\[\d+\.\d+\.\d+\]|$) -> Lookahead: Para de capturar assim que encontrar OUTRO cabeçalho '## [X.X.X]' ou o fim do arquivo ($)
            padrao = r"(##\s*\[\d+\.\d+\.\d+\].*?)(?=##\s*\[\d+\.\d+\.\d+\]|$)"

            # re.DOTALL faz o ponto (.) capturar quebras de linha (\n) também
            versoes = re.findall(padrao, conteudo, re.DOTALL)

            if versoes:
                # Pega o ÚLTIMO elemento da lista encontrada no arquivo
                ultima_versao_texto = versoes[-1].strip()
                return ultima_versao_texto
            else:
                return "Nenhuma versão no formato '## [X.X.X]' foi encontrada."

        except FileNotFoundError:
            return "Arquivo changelog.md não encontrado."

    # --- COMO USAR NO SEU PROGRAMA ---
    # Se o seu arquivo se chamar 'changelog.md':
    #arquivo = "/usr/share/doc/programaigreja/CHANGELOG.md"
    #texto_da_ultima_versao = extrair_ultima_versao_changelog(arquivo)
    #print(texto_da_ultima_versao)

    # Manu Arquivo
    menu_arquivo = tk.Menu(barra_menu, tearoff=0)
    #menu_arquivo.add_command(label="Nova Tarefa", command=lambda: JanelaConfiguracao(janela))
    menu_arquivo.add_command(label="Nova Tarefa", command=lambda: abrir_nova_tarefa(janela))
    menu_arquivo.add_command(label="Configurações", command=lambda: abrir_configuracoes(janela))
    menu_arquivo.add_command(label="Sair", command=janela.quit)
    barra_menu.add_cascade(label="Arquivo", menu=menu_arquivo)

    # Menu Ajuda
    menu_ajuda = tk.Menu(barra_menu, tearoff=0)
    menu_ajuda.add_command(label="Verificar atualização",
                           command=lambda: verificarversao.consultar_lancamento(repo, version))
    menu_ajuda.add_command(label="Notas da versão",
                           command=lambda: lbl_log.config(text=extrair_ultima_versao_changelog()))
    menu_ajuda.add_command(label="Sobre",
                           command=lambda: visitar_site())
    barra_menu.add_cascade(label="Ajuda", menu=menu_ajuda)

## Inicio do Programa
class BackupAgendado:
    def __init__(self, janela):
        ## Construção da janela
        self.janela = janela
        self.janela.title(f"{programa_title} {version}")
        self.janela.resizable(width=False, height=False)

        ## Painel da janela
        self.frame_controls = ttk.Frame(self.janela)
        self.frame_controls.grid(row=0, column=0, padx=espaco, pady=espaco, sticky="nsew")

        self.frame_andamento = ttk.Frame(self.janela)
        self.frame_andamento.grid(row=0, column=1, padx=espaco, pady=espaco, sticky="nsew")

        ## Controles do painel esquerdo
        linha_painel_esquerdo = 0
        self.lbl_selecao = ttk.Label(self.frame_controls, text="Selecionar Tarefa:", font=fonte)
        self.lbl_selecao.grid(row=linha_painel_esquerdo, column=0, padx=espaco, pady=espaco, sticky="nsew")

        self.cmb_selecao = ttk.Combobox(self.frame_controls, font=fonte, state="readonly")
        self.cmb_selecao.grid(row=linha_painel_esquerdo, column=1, padx=espaco, pady=espaco, sticky="nsew")
        linha_painel_esquerdo += 1

        self.lbl_horario = ttk.Label(self.frame_controls, text="Horário:", font=fonte)
        self.lbl_horario.grid(row=linha_painel_esquerdo, column=0, padx=espaco, pady=espaco, sticky="nsew")

        self.lbl_hora_execucao = ttk.Label(self.frame_controls, text="--:--", font=fonte, anchor="center")
        self.lbl_hora_execucao.grid(row=linha_painel_esquerdo, column=1, padx=espaco, pady=espaco, sticky="nsew")
        linha_painel_esquerdo += 1

        self.btn_executar = ttk.Button(self.frame_controls, text="Executar Tarefa", command="")
        self.btn_executar.grid(row=linha_painel_esquerdo, columnspan=2, padx=espaco, pady=espaco, sticky="nsew")
        linha_painel_esquerdo += 1

        self.btn_cancelar = ttk.Button(self.frame_controls, text="Cancelar Tarefa", command="")
        self.btn_cancelar.grid(row=linha_painel_esquerdo, columnspan=2, padx=espaco, pady=espaco, sticky="nsew")
        self.btn_cancelar.config(state="disabled")
        linha_painel_esquerdo += 1

        self.lbl_tamanho = ttk.Label(self.frame_controls, text="Tamanho:", font=fonte, anchor="w")
        self.lbl_tamanho.grid(row=linha_painel_esquerdo, column=0, padx=espaco, pady=espaco, sticky="nsew")

        self.lbl_tamanho_exibir = ttk.Label(self.frame_controls, text=(10*"-"), font=fonte, anchor="e")
        self.lbl_tamanho_exibir.grid(row=linha_painel_esquerdo, column=1, padx=espaco, pady=espaco, sticky="nsew")
        linha_painel_esquerdo += 1

        # Definindo suas variáveis de espaçamento
        espacox = espaco
        espacoy = 15

        # Usando o separador customizado
        criar_separador_com_texto(self.frame_controls, "EM EXECUÇÃO", linha=linha_painel_esquerdo, espacox=espacox, espacoy=espacoy)
        linha_painel_esquerdo += 1

        linha_estendida_moldura_execucao = 5
        self.frame_controls.rowconfigure(linha_painel_esquerdo, weight=0)
        self.moldura_execucao_borda = ttk.Frame(self.frame_controls, height=110, relief="solid", borderwidth=1)
        self.moldura_execucao_borda.grid(row=linha_painel_esquerdo, rowspan=linha_estendida_moldura_execucao, columnspan=2,
                                         padx=espaco, pady=espaco, sticky="ew")
        self.moldura_execucao_borda.grid_propagate(False)
        self.moldura_execucao_borda.pack_propagate(False)
        linha_painel_esquerdo += 1 + linha_estendida_moldura_execucao

        # Texto de exemplo
        texto_longo = (
            "Status do Sistema:\n"
            "- Backup da pasta 'Trabalho' concluído.\n"
            "- Erro ao acessar a unidade E:/ (Dispositivo desconectado).\n"
            "- Próxima verificação agendada para às 20:00."
        )

        self.frame_controls.update_idletasks()
        largura_moldura = self.moldura_execucao_borda.winfo_width()

        self.lbl_multi_execucao = ttk.Label(
            self.moldura_execucao_borda,
            text=texto_longo,
            justify="left",
            wraplength=largura_moldura - 10 * 2,
            font=fonte,
            padding=(10, 4, 10, 0)
        )
        self.lbl_multi_execucao.pack(anchor="w")

        self.btn_encerrar = ttk.Button(self.frame_controls, text="Encerrar Tarefa", command="")
        self.btn_encerrar.grid(row=linha_painel_esquerdo, columnspan=2, padx=espaco, pady=espaco, sticky="nsew")

        ## Controles do painel direito
        linha_painel_direito = 0
        linha_estendida_moldura_andamento = 7
        self.frame_andamento.rowconfigure(linha_painel_direito, weight=0)
        self.frame_andamento.columnconfigure(linha_painel_direito, weight=1)

        self.moldura_andamento_atual = ttk.Frame(self.frame_andamento, height=336, relief="solid", borderwidth=1, padding=10)
        self.moldura_andamento_atual.grid(row=linha_painel_direito, rowspan=linha_estendida_moldura_andamento,
                                          column=0, columnspan=3, padx=espaco, pady=espaco, sticky="ew")
        self.moldura_andamento_atual.grid_propagate(False)
        self.moldura_andamento_atual.pack_propagate(False)
        linha_painel_direito += linha_estendida_moldura_andamento

        self.lbl_multi_andamento = ttk.Label(
            self.moldura_andamento_atual,
            text=texto_longo,
            justify="left",
            wraplength=500,
            font=fonte,
            padding=(10, 4, 10, 0)
        )
        self.lbl_multi_andamento.pack(anchor="w")

        self.lbl_copiado = ttk.Label(self.frame_andamento, text="Copiado:", justify="left", font=fonte)
        self.lbl_copiado.grid(row=linha_painel_direito, column=0, padx=espaco, pady=espaco, sticky="nsew")

        self.lbl_copiado_tamanho = ttk.Label(self.frame_andamento, text=(8*"-"), justify="center", font=fonte)
        self.lbl_copiado_tamanho.grid(row=linha_painel_direito, column=1, padx=espaco, pady=espaco, sticky="nsew")

        self.progress_canvas = tk.Canvas(self.frame_andamento, height=25, bg="white", highlightthickness=1,
                                    highlightbackground="black")
        self.progress_canvas.grid(row=linha_painel_direito, column=2, padx=espaco, pady=espaco, sticky="e")

        ## Carregar Menus
        criar_barra_menu(self.janela, self.lbl_multi_andamento)

if __name__ == "__main__":
    root = tk.Tk()
    app = BackupAgendado(root)
    root.mainloop()