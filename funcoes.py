import platform
import re
import subprocess
from tkinter import filedialog, ttk, messagebox

import estilo
import verificarversao, dados_tinydb
from janela_config import JanelaConfiguracao
from janela_logs_backup import JanelaLogsBackup
from janela_nova_tarefa import JanelaNovaTarefa

# --- Inicialização de variáveis ---
carregar_dados = dados_tinydb.carregar_dados_tarefa()
# --- Funções de controle geral ---
def selecionar_pasta():
    pasta = filedialog.askdirectory(title="Selecione uma pasta")
    if pasta:  # se o usuário não cancelar
        return pasta
    else:
        return ""

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

## Notas da versão
def extrair_ultima_versao_changelog():
    caminho_arquivo = "CHANGELOG.md"
    if platform.system() == "Windows":
        caminho_arquivo = "C:\\Programa Igreja\\doc\\CHANGELOG.md"
        #subprocess.run(["notepad", caminho_arquivo])
    elif platform.system() == "Linux":
        caminho_arquivo = "/usr/share/doc/programaigreja/CHANGELOG.md"
        #subprocess.run(["xdg-open", caminho_arquivo])  # ou "gedit"
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

def visitar_site():
    pagina = f"https://github.com/YannickFigueira"
    resposta = messagebox.askyesno("Sobre", f"{estilo.NOME_PROGRAMA} {estilo.VERSION}\n"
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

class Funcoes:
    def __init__(self, view):
        self.view = view

        # Teste dos dados
        # Exemplo de como você leria isso no seu script de automação:
        #dados_tinydb.atualizar_campo_tarefa('tarefa6', 'hora', '17')
        #dados_tinydb.apagar_dados_tarefa('tarefa4')
        #dados_tinydb.gravar_dados_geral()
        """
        carregar_dados = dados_tinydb.carregar_dados_tarefa()
        for nome_tarefa, leitura in carregar_dados['tarefas'].items():
            print(f"A {nome_tarefa} está agendada para as {leitura['hora']}:{leitura['minuto']}")
            print(f"A {nome_tarefa} está executando {leitura['executando']}")
            print(f"Listar as pastas configuradas origem {leitura['pastas_origem']}, destino {leitura['pastas_destino']}")
            # Saída: A tarefa1 está agendada para as 10:45
            # Saída: A tarefa2 está agendada para as 12:30...
"""
        # O controlador se adapta automaticamente baseando-se em qual janela o chamou
        if hasattr(view, 'nome_janela'):
            if view.nome_janela == "janela-principal":
                self._vincular_janela_principal()
            elif view.nome_janela == "configuracao":
                self._vincular_configuracoes()
            elif view.nome_janela == "log-backup":
                self._vincular_logs_backup()


    # --- LÓGICA DA JANELA PRINCIPAL ---
    def _vincular_janela_principal(self):
        # --- Inicialização dos dados ---

        lista_nomes = list(carregar_dados['tarefas'].keys())
        self.view.controles['cmb_selecao'].config(values=list(lista_nomes))
        self.view.controles['cmb_selecao'].current(0)
        nome_tarefa = self.view.controles['cmb_selecao'].get()
        hora = carregar_dados['tarefas'][nome_tarefa]['hora']
        minuto = carregar_dados['tarefas'][nome_tarefa]['minuto']
        self.view.controles['lbl_hora_execucao'].config(text=f"{hora}:{minuto}")

        # --- Controle do Menu ---
        # -- Menu Arquivo --
        self.view.controles['menu_arquivo'].add_command(label="Configurações",
                                    command=lambda: self.abrir_configuracoes(self.view.controles['janela_principal']))
        self.view.controles['menu_arquivo'].add_command(label="Logs",
                                    command=lambda: self.abrir_logs_backup(self.view.controles['janela_principal']))
        # Mudar comado para withdraw
        self.view.controles['menu_arquivo'].add_command(label="Sair",
                                                        command=lambda: self.view.controles['janela_principal'].quit()) # Mudar para withdraw

        # -- Menu Ajuda --
        self.view.controles['menu_ajuda'].add_command(label="Verificar atualização",
                                      command=lambda: verificarversao.consultar_lancamento(estilo.REPO, estilo.VERSION))
        self.view.controles['menu_ajuda'].add_command(label="Notas da versão",
              command=lambda: self.view.controles['lbl_multi_andamento'].config(text=extrair_ultima_versao_changelog()))
        self.view.controles['menu_ajuda'].add_command(label="Sobre", command=lambda: visitar_site())

        # --- Controle da Janela Principal ---
        criar_separador_com_texto(self.view.controles['frame_controls'], "EM EXECUÇÃO", linha=self.view.controles['linha_painel_esquerdo'],
                                  espacox=estilo.ESPACOX, espacoy=estilo.ESPACOY)

        # --- Controle da janela ---
        self.view.controles['cmb_selecao'].bind("<<ComboboxSelected>>", self.atualizar_horario)


    # --- LÓGICA DA JANELA DE NOVA TAREFA ---
    def _vincular_configuracoes(self):
        self.view.controles['btn_selecionar_origem'].config(command=lambda: self.selecionar_origem())
        self.view.controles['btn_selecionar_destino'].config(command=lambda: self.selecionar_destino())

    # Ações da janela
    def selecionar_origem(self):
        self.view.controles['txt_origem'].delete(0, "end")
        self.view.controles['txt_origem'].insert(0, selecionar_pasta())

    def selecionar_destino(self):
        self.view.controles['txt_destino'].delete(0, "end")
        self.view.controles['txt_destino'].insert(0, selecionar_pasta())

    # --- LÓGICA DA JANELA DE CONFIGURAÇÕES ---
    def _vincular_logs_backup(self):
        pass

    # --- Funções das janelas ---
    def abrir_configuracoes(self, janela_principal):
        # 1. Cria a parte visual
        visual = JanelaConfiguracao(self.view.controles['janela_principal'])

        # 2. Cria a lógica e passa a visão para ela controlar
        logica = Funcoes(visual)

    def abrir_logs_backup(self, janela_principal):
        # 1. Cria a parte visual
        visual = JanelaLogsBackup(self.view.controles['janela_principal'])

        # 2. Cria a lógica e passa a visão para ela controlar
        logica = Funcoes(visual)

    def abrir_nova_tarefa(self, janela_principal):
        # 1. Cria a parte visual
        visual = JanelaNovaTarefa(self.view.controles['janela_principal'])

        # 2. Cria a lógica e passa a visão para ela controlar
        logica = Funcoes(visual)

    # --- Funções da Janela Principal ---
    def atualizar_horario(self, event = None):
        nome_tarefa = self.view.controles['cmb_selecao'].get()
        hora_atualizada = carregar_dados['tarefas'][nome_tarefa]['hora']
        minuto_atualizado = carregar_dados['tarefas'][nome_tarefa]['minuto']
        self.view.controles['lbl_hora_execucao'].config(text=f"{hora_atualizada}:{minuto_atualizado}")