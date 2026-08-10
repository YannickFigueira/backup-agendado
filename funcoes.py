import logging
import os
import platform
import re
import subprocess

from tkinter import filedialog, ttk, messagebox
from datetime import datetime

import estilo
import verificarversao, dados_tinydb
from janela_config import JanelaConfiguracao
from janela_logs_backup import JanelaLogsBackup
from janela_nova_tarefa import JanelaNovaTarefa

# --- Registro de erros ---
arquivo_erro = estilo.ARQUIVO_ERRO
# Pastas de configuração Linux
home_dir = os.path.expanduser('~')
log_dir = f"{home_dir}/log"
programa_dir = f"{home_dir}/.backup agendado"
notas = f"{home_dir}/.backup agendado/notas"

if not os.path.exists(programa_dir):
    os.mkdir(programa_dir)
# Pastas de configuração Windows

if platform.system() == 'Linux':
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    logging.basicConfig(
        filename=f"{home_dir}/log/{arquivo_erro}",        # nome do arquivo
        level=logging.ERROR,         # nível de log
        format="%(asctime)s - %(levelname)s - %(message)s")

elif platform.system() == 'Windows':
    if not os.path.exists(f"c:/temp"):
        os.mkdir(f"c:/temp")

    logging.basicConfig(
        filename=f"c:/temp/{arquivo_erro}",  # nome do arquivo
        level=logging.ERROR,  # nível de log
        format="%(asctime)s - %(levelname)s - %(message)s")

# --- Inicialização de variáveis ---
carregar_dados = dados_tinydb.carregar_dados_tarefa()
agora = datetime.now()
hora_formatada = agora.strftime("%H:%M:%S")
#index = 0
pasta_origem = []
pasta_destino = []
editando = False

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


def verificar_tarefas_existentes(valores_atuais):
    nova_tarefa = "tarefa"

    # 1. Filtra APENAS os números das strings que começam estritamente com 'tarefa' seguido de dígitos
    numeros_usados = set()
    for item in valores_atuais:
        match = re.match(r"^tarefa(\d+)$", str(item).strip())
        if match:
            numeros_usados.add(int(match.group(1)))
    # 'numeros_usados' agora é um conjunto com inteiros: {1, 2, 3, 5}
    # O item 'usuario' e 'configuracoes' são totalmente ignorados sem causar erros.

    # 2. Encontra o menor número vago a partir do 1
    proximo_indice = 1
    while proximo_indice in numeros_usados:
        proximo_indice += 1

    return f"{nova_tarefa}{proximo_indice}"


class Funcoes:
    def __init__(self, view):
        self.view = view

        # Teste dos dados
        # Exemplo de como você leria isso no seu script de automação:
        #dados_tinydb.atualizar_campo_tarefa('tarefa6', 'hora', '17')
        #dados_tinydb.apagar_dados_tarefa('tarefa4')

        # O controlador se adapta automaticamente baseando-se em qual janela o chamou
        if hasattr(view, 'nome_janela'):
            if view.nome_janela == "janela-principal":
                self._vincular_janela_principal()
            elif view.nome_janela == "configuracao":
                self._vincular_configuracoes()
            elif view.nome_janela == "log-backup":
                self._vincular_logs_backup()
            elif view.nome_janela == "nova-tarefa":
                self._vincular_nova_tarefa()


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


    # --- LÓGICA DA JANELA DE CONFIGURAÇÕES ---
    def _vincular_configuracoes(self):
        # --- Inicialização ---
        lista_nomes = list(carregar_dados['tarefas'].keys())
        self.view.controles['cmb_selecao'].config(values=list(lista_nomes))
        self.view.controles['cmb_selecao'].current(0)
        self.atualizar_configuracao()

        # --- Controles da Janela Configurações ---
        #self.view.controles['btn_selecionar_origem'].config(command=lambda: self.selecionar_origem())
        #self.view.controles['btn_selecionar_destino'].config(command=lambda: self.selecionar_destino())
        self.view.controles['cmb_selecao'].bind("<<ComboboxSelected>>", self.atualizar_configuracao)
        self.view.controles['chk_diariamente'].configure(command=lambda: self.atualizar_checkbox())
        self.view.controles['btn_gravar'].config(command=lambda: self.gravar_nova_tarefa())

        # --- Controle dos Menus ---
        self.view.controles['barra_menu'].add_command(label="Nova Tarefa",
                                                       command=lambda: self.abrir_nova_tarefa())
        self.view.controles['barra_menu'].add_command(label="Alterar Pastas")

    # --- LÓGICA DA JANELA DE CONFIGURAÇÕES ---
    def _vincular_logs_backup(self):
        pass

    # --- LÓGICA DA JANELA DE NOVA TAREFA ---
    def _vincular_nova_tarefa(self):
        # --- Controles da janela Nova Tarefa ---
        self.view.controles['btn_selecionar_origem'].config(command=lambda: self.selecionar_origem())
        self.view.controles['btn_selecionar_destino'].config(command=lambda: self.selecionar_destino())
        self.view.controles['btn_adicionar'].config(command=lambda: self.adicionar_pastas())
        self.view.controles['btn_salvar'].config(command=lambda: self.gravar_pastas())
        pass

    # --- Funcionalidade geral ---
    # Ações da janela
    def selecionar_origem(self):
        self.view.controles['txt_origem'].delete(0, "end")
        self.view.controles['txt_origem'].insert(0, selecionar_pasta())

    def selecionar_destino(self):
        self.view.controles['txt_destino'].delete(0, "end")
        self.view.controles['txt_destino'].insert(0, selecionar_pasta())

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

    def abrir_nova_tarefa(self):
        # 1. Cria a parte visual
        visual = JanelaNovaTarefa(self.view.controles['janela_configuracao'])

        # 2. Cria a lógica e passa a visão para ela controlar
        logica = Funcoes(visual)
        logica.view.controles['janela_nova_tarefa'].wait_window()
        # 3. Atualiza os valores do Combobox
        self.atualizar_configuracao()


    # --- Funções da Janela Principal ---
    def atualizar_horario(self, event = None):
        nome_tarefa = self.view.controles['cmb_selecao'].get()
        hora_atualizada = carregar_dados['tarefas'][nome_tarefa]['hora']
        minuto_atualizado = carregar_dados['tarefas'][nome_tarefa]['minuto']
        self.view.controles['lbl_hora_execucao'].config(text=f"{hora_atualizada}:{minuto_atualizado}")

    # --- Funções da Janela Configurações ---
    def habilitar_edicao(self):
        #print("Edição habilitada")
        editando = True

    def atualizar_configuracao(self, event = None):
        if not editando:
            nome_tarefa = self.view.controles['cmb_selecao'].get()
            self.view.controles['txt_tarefa'].delete(0, "end")
            self.view.controles['txt_tarefa'].insert(0, nome_tarefa)
            hora_atualizada = carregar_dados['tarefas'][nome_tarefa]['hora']
            minuto_atualizado = carregar_dados['tarefas'][nome_tarefa]['minuto']
            desabilitar = carregar_dados['tarefas'][nome_tarefa]['desabilitar_tarefa']
            desligar = carregar_dados['tarefas'][nome_tarefa]['desligar']
            self.view.controles['spin_hora'].set(hora_atualizada)
            self.view.controles['spin_min'].set(minuto_atualizado)
            self.view.controles['var_desabilitar'].set(desabilitar)
            self.view.controles['var_desligar'].set(desligar)
            semanas =  ['diariamente', 'domingo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado']
            chk_boxes = carregar_dados['tarefas'][nome_tarefa]['execucao']
            for i in range(len(chk_boxes)):
                self.view.controles[f'var_{semanas[i]}'].set(chk_boxes[i])

            diario = self.view.controles['var_diariamente'].get()
            index = 1
            if diario:
                for i in range (len(chk_boxes) - 1):
                    self.view.controles[f'chk_{semanas[index]}'].configure(state="disabled")
                    index += 1
            else:
                for i in range (len(chk_boxes) - 1):
                    self.view.controles[f'chk_{semanas[index]}'].configure(state="normal")
                    index += 1

            pastas_origem = carregar_dados['tarefas'][nome_tarefa]['pastas_origem']
            pastas_destino = carregar_dados['tarefas'][nome_tarefa]['pastas_destino']
            origem = ""
            destino = ""
            for i in range(len(pastas_origem)):
                origem += f"   {pastas_origem[i]}\n"
                destino += f"   {pastas_destino[i]}\n"
            self.view.controles['lbl_pastas'].config(text=f"Pastas de origem{8*"-"}\n{origem}\nPastas de destino{8*"-"}\n{destino}")
        else:
            # 1. Obtém a lista de valores atuais (converte para lista para poder alterar)
            valores_atuais = list(self.view.controles['cmb_selecao']['values'])

            # 2. Adiciona o novo item
            nova_tarefa = verificar_tarefas_existentes(valores_atuais)

            valores_atuais.append(nova_tarefa)
            self.view.controles['cmb_selecao']['values'] = valores_atuais
            self.view.controles['cmb_selecao'].current(len(valores_atuais) - 1)
            self.view.controles['cmb_selecao'].config(state="disabled")
            self.view.controles['txt_tarefa'].delete(0, "end")
            self.view.controles['txt_tarefa'].insert(0, nova_tarefa)
            self.view.controles['spin_hora'].set("17")
            self.view.controles['spin_min'].set("00")
            self.view.controles['var_diariamente'].set(True)
            self.atualizar_checkbox()
            self.view.controles['var_desabilitar'].set(False)
            self.view.controles['var_desligar'].set(False)

    def atualizar_checkbox(self):
        diario = self.view.controles['var_diariamente'].get()

        # Lista com as chaves dos dias para o código ficar limpo
        dias = ['domingo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado']

        if diario:
            for dia in dias:
                # 1. Altera apenas o estado para desabilitado (SEM mexer no parâmetro variable)
                self.view.controles[f'chk_{dia}'].configure(state="disabled")
                # 2. Atualiza o valor da variável original correspondente para True (marcado)
                self.view.controles[f'var_{dia}'].set(True)
        else:
            for dia in dias:
                # 1. Altera o estado de volta para normal
                self.view.controles[f'chk_{dia}'].configure(state="normal")
                # 2. Atualiza o valor da variável original correspondente para False (desmarcado)
                self.view.controles[f'var_{dia}'].set(False)

    def adicionar_pastas(self):

        if self.view.controles['txt_origem'].get() != "":
            if self.view.controles['txt_destino'].get() != "":
                origem = self.view.controles['txt_origem'].get().strip().replace("\\","/")
                pasta_origem.append(origem)
                # Extrai o nome da última pasta ("Development")
                nome_pasta = os.path.basename(origem.rstrip("/"))
                pasta_destino.append(f"{os.path.join(self.view.controles['txt_destino'].get().strip().replace("\\", " / "), nome_pasta)}")

                self.view.controles['txt_origem'].delete(0, "end")
                self.view.controles['btn_salvar'].config(state="normal")
                #self.view.controles['txt_destino'].delete(0, "end")
            else:
                messagebox.showinfo("Aviso", "Selecione uma pasta de destino")
                self.view.controles['txt_destino'].focus_set()
        else:
            messagebox.showinfo("Aviso", "Selecione uma pasta de origem")
            self.view.controles['txt_origem'].focus_set()

    def gravar_pastas(self):
        if len(pasta_origem) != 0:
            global editando
            self.view.controles['txt_destino'].delete(0, "end")
            for i, caminho in enumerate(pasta_origem):
                print(f"Índice {i}: {caminho}")
            for i, caminho in enumerate(pasta_destino):
                print(f"indice {i}: {caminho}")
            editando = True
            self.view.controles['janela_nova_tarefa'].destroy()
        else:
            messagebox.showinfo("Aviso", "Adicione ao menos uma pasta")

    def gravar_nova_tarefa(self):
        global editando
        editando = False
        self.view.controles['cmb_selecao'].config(state="readonly")