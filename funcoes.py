"""Módulo funcoes do sistema de Backup Agendado.

Este módulo gerencia toda a funcionalidade do programa
"""
import os
import platform
import re
import sys
import threading
import tkinter as tk
from time import sleep

from tkinter import filedialog, ttk, messagebox
from datetime import datetime
from screeninfo import get_monitors

import verificarversao, dados_tinydb, copiar_arquivos, estilo
from arquivo_log import abrir_logs, ler_pasta_log, gerar_arquivo_log
from janela_alterar_pastas import JanelaAlterarPastas
from janela_config import JanelaConfiguracao
from janela_logs_backup import JanelaLogsBackup
from janela_nova_tarefa import JanelaNovaTarefa
from janela_excluir_tarefa import JanelaExcluirTarefa

# --- Inicialização de variáveis ---
carregar_dados = dados_tinydb.carregar_dados_tarefa()
pasta_origem = []
pasta_destino = []
editando_dados = False
editando_novos_dados = False
editando_excluir_dados = False
editando_adicionar_pasta = False
atualizado_pastas = False
nova_tarefa_gravada = False
# Variaveis alterar pastas
origem_pasta = []
destino_pasta = []
# Verificar janelas
configuracao_aberta = False
nova_tarefa_aberta = False
alterar_pasta_aberta = False
excluir_tarefa_aberta = False

# --- Funções de controle geral ---
def selecionar_pasta():
    """
    :return:
    """
    pasta = filedialog.askdirectory(title="Selecione uma pasta")
    if pasta:  # se o usuário não cancelar
        return pasta
    else:
        return ""

## Container
def criar_separador_com_texto(janela_container, texto, linha, espacox, espacoy):
    """
    :param janela_container:
    :param texto:
    :param linha:
    :param espacox:
    :param espacoy:
    """
    # 1. Criamos um container invisível para envelopar o separador completo
    container = ttk.Frame(janela_container)
    container.grid(row=linha, columnspan=6, sticky="ew", padx=espacox, pady=espacoy)

    # Configura o container para expandir as linhas laterais igualmente
    container.columnconfigure(0, weight=1)
    container.columnconfigure(2, weight=1)

    # 2. Linha da Esquerda
    sep_esquerda = ttk.Separator(container)
    sep_esquerda.grid(row=0, column=0, sticky="ew", padx=(0, 10))

    # 3. O Texto Centralizado (com peso Bold/Negrito)
    # Usamos o fundo padrão (background) do root para não dar corte de cor
    label_texto = ttk.Label(container, text=texto, font=("", 10, "bold"))
    label_texto.grid(row=0, column=1, sticky="ne")

    # 4. Linha da Direita
    sep_direita = ttk.Separator(container)
    sep_direita.grid(row=0, column=2, sticky="ew", padx=(10, 0))

## Notas da versão
def extrair_ultima_versao_changelog():
    """
    :return:
    """
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
        with open(caminho_arquivo, encoding="utf-8") as f:
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
    """Gera mensagem para visitar a página"""
    pagina = f"https://github.com/YannickFigueira"
    resposta = messagebox.askyesno("Sobre", f"{estilo.NOME_PROGRAMA} {estilo.VERSION}\n"
                                            f"Desenvolvedor YannickFigueira\n"
                                            f"chronostimeinchain@gmail.com\n"
                                            f"Deseja visitar a página")
    if resposta:
        verificarversao.webbrowser.open(pagina)

def verificar_tarefas_existentes(valores_atuais):
    """
    :param valores_atuais:
    :return:
    """
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

def pegar_resolucao():
    """:return:"""
    monitors = get_monitors()
    first = None

    for m in monitors:
        # 1. Tenta obter o atributo is_primary com segurança
        is_primary = getattr(m, 'is_primary', False)

        # 2. Se não existir, verifica se a posição é a origem (0, 0)
        if is_primary or (m.x == 0 and m.y == 0):
            first = m
            break

    # Fallback caso nada seja identificado
    if not first and monitors:
        first = monitors[0]

    return first

def registrar_log(caminho_log, mensagem):
    """Abre o arquivo no modo append ('a') e escreve a mensagem com timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 'a' abre o arquivo para escrita sem apagar o conteúdo existente
    # encoding='utf-8' previne erros de acentuação no arquivo
    with open(caminho_log, mode="a", encoding="utf-8") as arquivo:
        arquivo.write(f"[{timestamp}] {mensagem}\n")


def obter_caminho_recurso(caminho_relativo: str) -> str:
    """
    Retorna o caminho absoluto para recursos, funcionando em ambiente de
    desenvolvimento, empacotado via PyInstaller ou instalado via .deb no Linux.
    """
    # 1. Se estiver rodando empacotado via PyInstaller
    if getattr(sys, 'frozen', False):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        caminho_embutido = os.path.join(base_path, caminho_relativo)
        if os.path.exists(caminho_embutido):
            return caminho_embutido

    # 2. Se for o pacote .deb instalado no Linux (/usr/share)
    caminho_sistema = os.path.join("/usr/share/backup-agendado", os.path.basename(caminho_relativo))
    if os.path.exists(caminho_sistema):
        return caminho_sistema

    # 3. Fallback: Desenvolvimento local (caminho relativo à pasta do script)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, caminho_relativo)

class Funcoes:
    """Classe da função principal"""
    def __init__(self, view):
        self.icon_tray = None
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
            elif view.nome_janela == "alterar-pastas":
                self._vincular_alterar_pastas()
            elif view.nome_janela == "excluir-tarefa":
                self._vincular_excluir_tarefa()


    # --- LÓGICA DA JANELA PRINCIPAL ---
    def _vincular_janela_principal(self):
        # --- Inicialização dos dados ---
        nome_tarefa = self.carregar_cmb_selecao()
        self.atualizar_informacoes(nome_tarefa)
        if not nome_tarefa == "inicial":
            self.verificar_tarefa_executando()
            self.esconder_janela()

        self.criar_bandeja()

        # --- Posição da janela principal ---
        largura = 342
        altura = 305

        first = pegar_resolucao()

        if first is not None:
            largura_tela = first.width
            altura_tela = first.height
        else:
            # Defina um valor padrão de fallback caso não encontre o monitor
            largura_tela = 1920
            altura_tela = 1080

        # Calcula as posições X e Y para centralizar
        pos_x = int((largura_tela / 2) - largura)
        pos_y = int((altura_tela / 2) - altura)

        # Passa apenas +X+Y (ou -X-Y para borda direita/inferior)
        self.view.controles['janela_principal'].geometry(f"+{pos_x}+{pos_y}")

        # --- Controle do Menu ---
        # -- Menu Arquivo --
        self.view.controles['menu_arquivo'].add_command(label="Configurações",
                                    command=lambda: self.abrir_janela_configuracoes(nome_tarefa))
        self.view.controles['menu_arquivo'].add_command(label="Logs",
                                    command=lambda: self.abrir_janela_logs_backup())
        # Mudar comado para withdraw
        self.view.controles['menu_arquivo'].add_command(label="Sair",
                                                        command=lambda: self.fechar_programa()) # Mudar para withdraw

        # -- Menu Ajuda --
        self.view.controles['menu_ajuda'].add_command(label="Verificar atualização",
                                      command=lambda: verificarversao.consultar_lancamento(estilo.REPO, estilo.VERSION))
        self.view.controles['menu_ajuda'].add_command(label="Notas da versão",
              command=lambda: self.view.controles['lbl_multi_andamento'].config(text=extrair_ultima_versao_changelog()))
        self.view.controles['menu_ajuda'].add_command(label="Sobre", command=lambda: visitar_site())

        # --- Controle da Janela Principal ---
        self.view.controles['janela_principal'].protocol("WM_DELETE_WINDOW",lambda: self.esconder_janela())
        criar_separador_com_texto(self.view.controles['frame_controls'], "EM EXECUÇÃO", linha=self.view.controles['linha_painel_esquerdo'],
                                  espacox=estilo.ESPACOX, espacoy=estilo.ESPACOY)

        # --- Controle da janela ---
        self.view.controles['btn_executar'].config(command=lambda:  copiar_arquivos.iniciar_copiar_arquivos(self.view, self.view.controles['cmb_selecao'].get()))
        self.view.controles['btn_pausar'].config(command=lambda: copiar_arquivos.pausar_copia())
        self.view.controles['btn_encerrar'].config(command=lambda: copiar_arquivos.cancelar_copia())
        self.view.controles['cmb_selecao'].bind("<<ComboboxSelected>>",lambda _: self.atualizar_informacoes(self.view.controles['cmb_selecao'].get()))

        if nome_tarefa == "inicial":
            messagebox.showinfo("Aviso", "Insira a primeira tarefa")
            self.abrir_janela_configuracoes(nome_tarefa)

    # --- LÓGICA DA JANELA DE CONFIGURAÇÕES ---
    def _vincular_configuracoes(self):
        # --- Inicialização ---
        self.carregar_cmb_selecao()
        self.atualizar_configuracao()

        # --- Controles da Janela Configurações ---
        self.view.controles['janela_configuracao'].protocol("WM_DELETE_WINDOW",
                                                         lambda: self.fechar_janelas('janela_configuracao'))
        self.view.controles['cmb_selecao'].bind("<<ComboboxSelected>>",lambda _: self.atualizar_configuracao())
        self.view.controles['chk_diariamente'].configure(command=lambda: self.atualizar_checkbox())
        self.view.controles['btn_gravar'].config(command=lambda: self.gravar_tarefa())

        # --- Controle dos Menus ---
        self.view.controles['barra_menu'].add_command(label="Editar Tarefa",
                                                      command=lambda: self.habilitar_edicao())
        self.view.controles['barra_menu'].add_command(label="Nova Tarefa",
                                                       command=lambda: self.abrir_janela_nova_tarefa())
        self.view.controles['barra_menu'].add_command(label="Alterar Pastas",
                                                      command=lambda: self.abrir_janela_alterar_pastas())
        self.view.controles['barra_menu'].add_command(label="Excluir Tarefa",
                                                      command=lambda: self.abrir_janela_excluir_tarefa())

    # --- LÓGICA DA JANELA DE NOVA TAREFA ---
    def _vincular_nova_tarefa(self):
        # --- Controles da janela Nova Tarefa ---
        self.view.controles['janela_nova_tarefa'].protocol("WM_DELETE_WINDOW",
                                                            lambda: self.fechar_janelas('janela_nova_tarefa'))
        self.view.controles['btn_selecionar_origem'].config(command=lambda: self.selecionar_pastas('txt_origem'))
        self.view.controles['btn_selecionar_destino'].config(command=lambda: self.selecionar_pastas('txt_destino'))
        self.view.controles['btn_adicionar'].config(command=lambda: self.adicionar_nova_tarefa())
        self.view.controles['btn_salvar'].config(command=lambda: self.gravar_pastas())

    # --- LÓGICA DA JANELA ALTERAR PASTAS ---
    def _vincular_alterar_pastas(self):
        # --- Controles da janela Alterar Pastas ---
        self.view.controles['janela_alterar_pastas'].protocol("WM_DELETE_WINDOW",
                                                           lambda: self.fechar_janelas('janela_alterar_pastas'))
        self.view.controles['btn_selecionar_origem'].config(command=lambda: self.selecionar_pastas('txt_origem'))
        self.view.controles['btn_selecionar_destino'].config(command=lambda: self.selecionar_pastas('txt_destino'))

    # --- LÓGICA DA JANELA EXCLUIR TAREFA ---
    def _vincular_excluir_tarefa(self):
        self.view.controles['btn_excluir'].config(command=lambda: self.excluir_tarefa())

    # --- LÓGICA DA JANELA DE LOGS ---
    def _vincular_logs_backup(self):
        # --- Inicialização da janela logs ---
        arquivos_log = ler_pasta_log()
        texto_log = "\n".join([f"{item}" for item in arquivos_log])

        # --- Controles da janela de logs
        self.view.controles['janela_logs_backup'].protocol("WM_DELETE_WINDOW",
                                                              lambda: self.fechar_janelas('janela_logs_backup'))

        self.view.controles['lbl_logs'].config(text=texto_log)
        self.view.controles['cmb_selecao'].config(values=arquivos_log)
        self.view.controles['cmb_selecao'].current(0)
        self.view.controles['btn_abrir_logs'].config(command=lambda: abrir_logs(self.view))

    # --- Execução das janelas ---
    def abrir_janela_configuracoes(self, nome_tarefa):
        global editando_novos_dados, configuracao_aberta, carregar_dados
        configuracao_aberta = True
        # 1. Cria a parte visual
        visual = JanelaConfiguracao(self.view.controles['janela_principal'])

        # 2. Cria a lógica e passa a visão para ela controlar
        logica = Funcoes(visual)

        logica.centralizar_janela("janela_configuracao", self.view.controles['janela_principal'])

        # --- Inicialização ---
        #nome_tarefa = logica.carregar_cmb_selecao()
        if nome_tarefa == "inicial":
            logica.desabiliatar_menus_configuracao()
        else:
            logica.view.controles['barra_menu'].entryconfig("Editar Tarefa", state="normal")
            logica.view.controles['barra_menu'].entryconfig("Alterar Pastas", state="normal")
            logica.view.controles['barra_menu'].entryconfig("Excluir Tarefa", state="normal")

        logica.view.controles['btn_gravar'].config(state="disabled")
        qtd_origem = len(self.view.controles['cmb_selecao']['values'])
        qtd_destino = len(logica.view.controles['cmb_selecao']['values'])
        if qtd_origem < qtd_destino:
            logica.view.controles['cmb_selecao'].config(state="readonly")
            logica.carregar_cmb_selecao()
            editando_novos_dados = False
            logica.atualizar_configuracao()

        logica.view.controles['janela_configuracao'].wait_window()
        carregar_dados = dados_tinydb.carregar_dados_tarefa()
        nome_tarefa = self.carregar_cmb_selecao()
        if nome_tarefa == "inicial":
            messagebox.showinfo("Aviso", "Nenhuma tarefa foi criada e o programa será encerrado!")
            self.fechar_programa()
        else:
            configuracao_aberta = False
            nome_tarefa = self.carregar_cmb_selecao()
            hora = carregar_dados['tarefas'][nome_tarefa]['hora']
            minuto = carregar_dados['tarefas'][nome_tarefa]['minuto']
            self.view.controles['lbl_hora_execucao'].config(text=f"{hora}:{minuto}")

    def abrir_janela_nova_tarefa(self):
        global pasta_origem, pasta_destino, nova_tarefa_aberta
        nova_tarefa_aberta = True
        # 1. Cria a parte visual
        visual = JanelaNovaTarefa(self.view.controles['janela_configuracao'])

        # 2. Cria a lógica e passa a visão para ela controlar
        logica = Funcoes(visual)
        logica.centralizar_janela("janela_nova_tarefa", self.view.controles['janela_configuracao'])
        if len(pasta_origem) > 0:
            pasta_origem = []
            pasta_destino = []

        logica.view.controles['janela_nova_tarefa'].wait_window()
        nova_tarefa_aberta = False
        if atualizado_pastas:
            self.view.controles['barra_menu'].entryconfig("Editar Tarefa", state="disabled")
            self.view.controles['barra_menu'].entryconfig("Nova Tarefa", state="disabled")
            self.view.controles['barra_menu'].entryconfig("Alterar Pastas", state="disabled")
            self.view.controles['barra_menu'].entryconfig("Excluir Tarefa", state="disabled")

        if editando_novos_dados:
            self.view.controles['btn_gravar'].config(state="normal")
        # 3. Atualiza os valores do Combobox
        self.atualizar_configuracao()

    def abrir_janela_alterar_pastas(self):
        global alterar_pasta_aberta, origem_pasta, destino_pasta
        alterar_pasta_aberta = True
        # 1. Cria a parte visual
        visual = JanelaAlterarPastas(self.view.controles['janela_configuracao'])

        # 2. Cria a lógica e passa a visão para ela controlar
        logica = Funcoes(visual)
        logica.centralizar_janela("janela_alterar_pastas", self.view.controles['janela_configuracao'])

        # Carregar configuração
        nome_tarefa = self.view.controles['cmb_selecao'].get()
        quantidade_pastas = carregar_dados['tarefas'][nome_tarefa]['pastas_origem']
        index = 1
        pastas = []
        for i in range(len(quantidade_pastas)):
            pastas.append(f"Pasta{index}")
            index += 1
        logica.view.controles['btn_gravar_adicionar'].config(state="disabled")
        logica.view.controles['cmb_selecao'].config(values=list(pastas))
        logica.view.controles['cmb_selecao'].current(0)
        origem_pasta = carregar_dados['tarefas'][nome_tarefa]['pastas_origem']
        destino_pasta = carregar_dados['tarefas'][nome_tarefa]['pastas_destino']
        # --- Controles ---
        logica.view.controles['cmb_selecao'].bind("<<ComboboxSelected>>", lambda _: logica.carregar_pastas())
        logica.view.controles['btn_alterar'].config(command=lambda: logica.gravar_alterar_pastas(nome_tarefa))
        logica.view.controles['btn_excluir_pasta'].config(command=lambda: logica.excluir_pasta(nome_tarefa))
        logica.view.controles['btn_adicionar_pasta'].config(command=lambda: logica.adicionar_pasta())
        logica.view.controles['btn_gravar_adicionar'].config(command=lambda: logica.gravar_alterar_pastas(nome_tarefa))

        # --- inicialização ---
        logica.carregar_pastas()
        logica.view.controles['janela_alterar_pastas'].wait_window()
        self.atualizar_configuracao()
        alterar_pasta_aberta = False

    def abrir_janela_excluir_tarefa(self):
        global excluir_tarefa_aberta
        excluir_tarefa_aberta = True
        # 1. Cria a parte vsual
        visual = JanelaExcluirTarefa(self.view.controles['janela_configuracao'])

        # 2. Cria a lógica e passa a visão para ela controlar
        logica = Funcoes(visual)
        logica.centralizar_janela("janela_excluir_tarefa", self.view.controles['janela_configuracao'])

        logica.carregar_cmb_selecao()
        logica.view.controles['janela_excluir_tarefa'].wait_window()
        nome_tarefa = self.carregar_cmb_selecao()
        self.atualizar_configuracao()
        if nome_tarefa == "inicial":
            self.desabiliatar_menus_configuracao()
        excluir_tarefa_aberta = False

    def abrir_janela_logs_backup(self):
        arquivos_log = ler_pasta_log()
        if len(arquivos_log) > 0:
            print("Arquivos logs backup")
            print(len(arquivos_log))
            # 1. Cria a parte visual
            visual = JanelaLogsBackup(self.view.controles['janela_principal'])

            # 2. Cria a lógica e passa a visão para ela controlar
            logica = Funcoes(visual)
            logica.centralizar_janela("janela_logs_backup", self.view.controles['janela_principal'])

            logica.view.controles['janela_logs_backup'].wait_window()
        else:
            messagebox.showinfo("Aviso", "Nenhum log foi gerado ainda")

    # --- Funções Gerais ---
    def verificar_tarefa_executando(self):
        executando = threading.Thread(
            target=self.tarefa_executando,
            daemon=True,
        )
        executando.start()

    def tarefa_executando(self):
        global carregar_dados
        while True:
            try:
                # 1. Verifica se o widget ainda existe na interface
                lbl_multi_execucao = self.view.controles.get('lbl_multi_execucao')
                if not lbl_multi_execucao or not lbl_multi_execucao.winfo_exists():
                    break  # Encerra o loop da thread se a janela foi destruída

                carregar_dados = dados_tinydb.carregar_dados_tarefa()
                lista_nomes = list(carregar_dados['tarefas'].keys())
                tarefas_executando = []

                for nome_tarefa in lista_nomes:
                    executando = carregar_dados['tarefas'][nome_tarefa]['executando']
                    if executando:
                        tarefas_executando.append(nome_tarefa)

                lista_executando = "\n".join([f"{item}" for item in tarefas_executando])

                # 2. Protege o agendamento no Tkinter contra encerramentos repentinos
                try:
                    lbl_multi_execucao.after(
                        0,
                        lambda texto=lista_executando: self.view.controles['lbl_multi_execucao'].config(text=texto)
                    )
                except (tk.TclError, RuntimeError):
                    break  # Tkinter foi fechado, interrompe a thread

            except Exception as e:
                erros_log = gerar_arquivo_log(estilo.log_erros)
                registrar_log(erros_log, f"[ERRO] Monitoramento das tarefas -> {e}")

                # 3. Dorme 60 segundos
            sleep(60)

    def fechar_janelas(self, janela):
        global configuracao_aberta, nova_tarefa_aberta, excluir_tarefa_aberta, editando_dados

        match janela:
            case 'janela_principal':
                if configuracao_aberta:
                    return
            case 'janela_configuracao':
                editando_dados = False
                if nova_tarefa_aberta or alterar_pasta_aberta or excluir_tarefa_aberta:
                    return

        self.view.controles[f'{janela}'].destroy()

    def carregar_cmb_selecao(self):
        lista_nomes = list(carregar_dados['tarefas'].keys())
        self.view.controles['cmb_selecao'].config(values=list(lista_nomes))
        self.view.controles['cmb_selecao'].current(0)
        nome_tarefa = self.view.controles['cmb_selecao'].get()

        return nome_tarefa

    def verificar_pastas_existentes(self):
        verificar_origem = self.view.controles['txt_origem'].get().strip()
        verificar_destino = self.view.controles['txt_destino'].get().strip()
        if verificar_origem != "":
            if verificar_destino != "":
                if os.path.exists(verificar_origem):
                    if os.path.exists(verificar_destino):
                        return True
                    else:
                        messagebox.showinfo("Aviso", "Pasta de destino não existe!")
                        return False
                else:
                    messagebox.showinfo("Aviso", "Pasta de origem não existe!")
                    return False
            else:
                messagebox.showinfo("Aviso", "Selecione uma pasta de destino")
                self.view.controles['txt_destino'].focus_set()
                return False
        else:
            messagebox.showinfo("Aviso", "Selecione uma pasta de origem")
            self.view.controles['txt_origem'].focus_set()
            return False

    def selecionar_pastas(self, controle):
        self.view.controles[controle].delete(0, "end")
        self.view.controles[controle].insert(0, selecionar_pasta())

    def esconder_janela(self):
        self.view.controles['janela_principal'].withdraw()

    def restaurar_janela(self):
        self.view.controles['janela_principal'].deiconify()

    def fechar_programa(self, icon=None):
        resposta = messagebox.askokcancel("Alerta",
    "Fechando o programa o backup não será mais executado até que seja iniciado novamente",
            icon="warning")
        if resposta:
            sistema = platform.system()

            if sistema == "Linux":
                # 1. Oculta e destrói os objetos Qt no Linux
                if hasattr(self, 'qt_tray') and self.qt_tray is not None:
                    self.qt_tray.hide()
                    self.qt_tray.deleteLater()
                    self.qt_tray = None

                if hasattr(self, 'qt_app') and self.qt_app is not None:
                    self.qt_app.quit()
                    self.qt_app = None

            else:
                # Lógica exclusiva para o Windows (pystray + Tkinter)
                janela_principal = self.view.controles.get('janela_principal')

                # 1. Função interna para encerrar o Tkinter e o processo de forma limpa
                def encerrar_windows():
                    if janela_principal and janela_principal.winfo_exists():
                        try:
                            janela_principal.quit()
                            janela_principal.destroy()
                        except Exception:
                            pass
                    os._exit(0)

                # 2. Agenda a destruição da janela para a Thread Principal do Tkinter
                if janela_principal and janela_principal.winfo_exists():
                    janela_principal.after(50, encerrar_windows)

                # 3. Encerra o pystray para remover o ícone da barra de tarefas
                tray_obj = icon or getattr(self, 'icon_tray', None)
                if tray_obj and hasattr(tray_obj, 'stop'):
                    try:
                        tray_obj.stop()
                    except Exception:
                        pass

                # Caso a janela principal já estivesse fechada, mata o processo com um pequeno delay
                if not (janela_principal and janela_principal.winfo_exists()):
                    import threading
                    threading.Timer(0.1, lambda: os._exit(0)).start()

    def _processar_eventos_qt(self):
        """Processa a fila do Qt dentro do loop do Tkinter de forma não-bloqueante."""
        if hasattr(self, 'qt_app') and self.qt_app is not None:
            self.qt_app.processEvents()

            # Pega a janela principal do Tkinter
            janela = self.view.controles.get('janela_principal')
            if janela and janela.winfo_exists():
                janela.after(150, self._processar_eventos_qt)

    def criar_bandeja(self):
        sistema = platform.system()
        caminho_imagem = obter_caminho_recurso("imagens/backup.png")

        if sistema == "Linux":
            from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
            from PyQt6.QtGui import QIcon

            # 1. Cria/Recupera a instância do Qt na THREAD PRINCIPAL
            self.qt_app = QApplication.instance() or QApplication(sys.argv)
            self.qt_app.setQuitOnLastWindowClosed(False)

            # 2. Instancia o ícone
            self.qt_tray = QSystemTrayIcon(QIcon(caminho_imagem))
            menu = QMenu()

            acao1 = menu.addAction("Janela Principal")
            acao1.triggered.connect(self.restaurar_janela)

            acao2 = menu.addAction("Sair")
            acao2.triggered.connect(self.fechar_programa)

            self.qt_tray.setContextMenu(menu)
            self.qt_tray.show()

            # 3. Processa os eventos do Qt periodicamente via Tkinter (Sem travar!)
            self._processar_eventos_qt()

            return self.qt_tray

        else:
            # Mantém pystray para Windows
            print('systray')
            from pystray import Icon, MenuItem, Menu
            from PIL import Image

            image = Image.open(caminho_imagem)
            menu = Menu(
                MenuItem("Janela Principal", self.restaurar_janela),
                MenuItem("Sair", self.fechar_programa),
            )
            self.icon_tray = Icon("BackupAgendado", image, estilo.NOME_PROGRAMA, menu)
            self.icon_tray.run_detached()
            return self.icon_tray

    def centralizar_janela(self, janela, parent):
        """Centraliza a janela 'child' no centro da janela 'parent'."""
        parent.update_idletasks()
        self.view.controles[janela].update_idletasks()

        # Dimensões e posição da janela principal
        p_width = parent.winfo_width()
        p_height = parent.winfo_height()
        p_x = parent.winfo_rootx()
        p_y = parent.winfo_rooty()

        # Dimensões da janela filha
        c_width = self.view.controles[janela].winfo_reqwidth()
        c_height = self.view.controles[janela].winfo_reqheight()

        # Cálculo das coordenadas X e Y
        x = p_x + (p_width // 2) - (c_width // 2)
        y = p_y + (p_height // 2) - (c_height // 2)

        # Aplica a geometria (Largura x Altura + X + Y)
        self.view.controles[janela].geometry(f"{c_width}x{c_height}+{x}+{y}")

    # --- Funções da Janela Principal ---
    def atualizar_informacoes(self, nome_tarefa):
        pastas_origem = carregar_dados['tarefas'][nome_tarefa]['pastas_origem']
        self.atualizar_horario(nome_tarefa)
        if nome_tarefa != "inicial":
            copiar_arquivos.iniciar_calculo_tamanho(self.view, pastas_origem, "")

    def atualizar_horario(self, nome_tarefa):
        hora_atualizada = carregar_dados['tarefas'][nome_tarefa]['hora']
        minuto_atualizado = carregar_dados['tarefas'][nome_tarefa]['minuto']
        self.view.controles['lbl_hora_execucao'].config(text=f"{hora_atualizada}:{minuto_atualizado}")

    # --- Funções da Janela Configurações ---
    def desabiliatar_menus_configuracao(self):
        self.view.controles['barra_menu'].entryconfig("Editar Tarefa", state="disabled")
        self.view.controles['barra_menu'].entryconfig("Alterar Pastas", state="disabled")
        self.view.controles['barra_menu'].entryconfig("Excluir Tarefa", state="disabled")

    def habilitar_edicao(self):
        global editando_dados
        editando_dados = True
        self.view.controles['btn_gravar'].config(state="normal")
        messagebox.showinfo("Aviso", "Edição habilitada")

    def atualizar_configuracao(self):
        global editando_excluir_dados
        if not editando_novos_dados or editando_dados:
            if editando_excluir_dados:
                nome_tarefa = self.carregar_cmb_selecao()
                editando_excluir_dados = False
            else:
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

    def gravar_tarefa(self):
        # Novos dados
        global editando_dados, editando_novos_dados, atualizado_pastas, pasta_origem, pasta_destino, carregar_dados
        nome_tarefa = self.view.controles['txt_tarefa'].get().strip()
        if nome_tarefa == "inicial":
            messagebox.showinfo("Aviso", "Nome reservado e não pode ser usado!")
            pasta_origem = []
            pasta_destino = []
            self.view.controles['cmb_selecao'].current(0)
            self.carregar_cmb_selecao()
        else:
            hora = self.view.controles['spin_hora'].get()
            minuto = self.view.controles['spin_min'].get()

            if len(hora) > 2:
                messagebox.showwarning("Aviso", "Formato de hora inválido!\nRedigite ou use as setas")
                return

            if len(minuto) > 2:
                messagebox.showwarning("Aviso", "Formato de minuto inválido!\nRedigite ou use as setas")
                return

            if len(nome_tarefa) > 2:
                if nome_tarefa != "":
                    if not atualizado_pastas:
                        pasta_origem = []
                        pasta_destino = []
                        editando_novos_dados = False

                    # Captura os dados
                    self.view.controles['cmb_selecao'].config(state="readonly")
                    nome_tarefa = self.view.controles['cmb_selecao'].get()
                    tarefa = self.view.controles['txt_tarefa'].get().strip()
                    if len(hora) == 1:
                        hora = f"0{hora}"
                    if len(minuto) == 1:
                        minuto = f"0{minuto}"
                    semanas = ['diariamente', 'domingo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado']
                    diario = self.view.controles['var_diariamente'].get()
                    index = 0
                    execusao = []
                    if diario:
                        execusao = [True] * len(semanas)
                    else:
                        for i in range(len(semanas)):
                            execusao.append(self.view.controles[f'var_{semanas[index]}'].get())
                            index += 1
                    desligar = self.view.controles['var_desligar'].get()
                    desabilitar = self.view.controles['var_desabilitar'].get()

                    if editando_novos_dados:
                        # Verificar dados
                        dados = [hora, minuto, pasta_origem, pasta_destino, execusao, desligar, desabilitar]
                        dados_tinydb.gravar_nova_tarefa(tarefa, dados)
                        editando_novos_dados = False
                        atualizado_pastas = False
                        self.carregar_cmb_selecao()
                        self.atualizar_configuracao()
                        messagebox.showinfo("Aviso", "Novos dados gravados com sucesso!")
                        qtd_origem = len(self.view.controles['cmb_selecao']['values'])
                        if qtd_origem > 1:
                            if self.view.controles['cmb_selecao'].get() == "inicial":
                                dados_tinydb.apagar_dados_tarefa("inicial")
                                carregar_dados = dados_tinydb.carregar_dados_tarefa()
                                self.carregar_cmb_selecao()
                                self.atualizar_configuracao()

                    elif editando_dados:
                        if nome_tarefa != tarefa:
                            dados_tinydb.renomear_tarefa(nome_tarefa, tarefa)

                        dados_tinydb.atualizar_campo_tarefa(tarefa, 'hora', hora)
                        dados_tinydb.atualizar_campo_tarefa(tarefa, 'minuto', minuto)
                        dados_tinydb.atualizar_campo_tarefa(tarefa, 'execucao', execusao)
                        dados_tinydb.atualizar_campo_tarefa(tarefa, 'desligar', desligar)
                        dados_tinydb.atualizar_campo_tarefa(tarefa, 'desabilitar_tarefa', desabilitar)
                        carregar_dados = dados_tinydb.carregar_dados_tarefa()
                        editando_dados = False
                        self.carregar_cmb_selecao()
                        self.atualizar_configuracao()
                        messagebox.showinfo("Aviso", "Dados alterados com sucesso!")
                    else:
                        messagebox.showinfo("Aviso", "Nenhum dados foi alterado!\nHabilite a edição ou insira novos dados.")
                else:
                    messagebox.showinfo("Aviso", "Nome da tarefa não pode estar vazio!")
            else:
                messagebox.showinfo("Aviso", "Minimo de 3 letras!")

            # Habilitar menus
            self.view.controles['barra_menu'].entryconfig("Editar Tarefa", state="normal")
            self.view.controles['barra_menu'].entryconfig("Alterar Pastas", state="normal")
            self.view.controles['barra_menu'].entryconfig("Excluir Tarefa", state="normal")

        self.view.controles['btn_gravar'].config(state="disabled")
        self.view.controles['barra_menu'].entryconfig("Nova Tarefa", state="normal")

    # --- Funções da janela Nova tarefa ---
    def adicionar_nova_tarefa(self):
        existe = self.verificar_pastas_existentes()
        if existe:
            origem = self.view.controles['txt_origem'].get().strip()
            pasta_origem.append(origem)
            # Extrai o nome da última pasta ("Development")
            #nome_pasta = os.path.basename(origem.rstrip("/")) Pegar o nome da pasta de origem
            pasta_destino.append(self.view.controles['txt_destino'].get().strip())

            self.view.controles['txt_origem'].delete(0, "end")
            self.view.controles['btn_salvar'].config(state="normal")

    def gravar_pastas(self):
        global editando_novos_dados, atualizado_pastas
        if len(pasta_origem) != 0:
            atualizado_pastas = True
            self.view.controles['txt_destino'].delete(0, "end")
            editando_novos_dados = True
            messagebox.showinfo("Aviso", "Nova tarefa pronta para ser gravada")
            self.view.controles['janela_nova_tarefa'].destroy()
        else:
            messagebox.showinfo("Aviso", "Adicione ao menos uma pasta")

    # --- Funcões da Janela Alterar Pastas ---
    def carregar_pastas(self):
        global origem_pasta, destino_pasta
        self.view.controles['txt_origem'].delete(0, "end")
        self.view.controles['txt_origem'].insert(0, origem_pasta[self.view.controles['cmb_selecao'].current()])
        self.view.controles['txt_destino'].delete(0, "end")
        self.view.controles['txt_destino'].insert(0, destino_pasta[self.view.controles['cmb_selecao'].current()])

    def gravar_alterar_pastas(self, nome_tarefa):
        global origem_pasta, destino_pasta, carregar_dados, editando_adicionar_pasta
        existe = self.verificar_pastas_existentes()
        if existe:
            if not editando_adicionar_pasta:
                origem_pasta[self.view.controles['cmb_selecao'].current()] = self.view.controles['txt_origem'].get().strip()
                destino_pasta[self.view.controles['cmb_selecao'].current()] = self.view.controles['txt_destino'].get().strip()
            else:
                origem_pasta.append(self.view.controles['txt_origem'].get().strip())
                destino_pasta.append(self.view.controles['txt_destino'].get().strip())
                self.view.controles['btn_adicionar_pasta'].config(state="normal")
                self.view.controles['btn_gravar_adicionar'].config(state="disabled")

            dados_tinydb.atualizar_campo_tarefa(nome_tarefa, 'pastas_origem', origem_pasta)
            dados_tinydb.atualizar_campo_tarefa(nome_tarefa, 'pastas_destino', destino_pasta)
            carregar_dados = dados_tinydb.carregar_dados_tarefa()

            messagebox.showinfo("Aviso", "Pastas alteradas com sucesso!")

    def adicionar_pasta(self):
        global editando_adicionar_pasta
        existe = self.verificar_pastas_existentes()
        if existe:
            valores_atuais = list(self.view.controles['cmb_selecao']['values'])
            index = 1
            pastas = []
            for i in range(len(valores_atuais) + 1):
                pastas.append(f"Pasta{index}")
                index += 1
            self.view.controles['cmb_selecao']['values'] = pastas
            self.view.controles['cmb_selecao'].current(len(pastas) - 1)
            self.view.controles['txt_origem'].delete(0, "end")
            editando_adicionar_pasta = True
            self.view.controles['btn_adicionar_pasta'].config(state="disabled")
            self.view.controles['btn_gravar_adicionar'].config(state="normal")

    def excluir_pasta(self, nome_tarefa):
        global origem_pasta, destino_pasta, carregar_dados
        qtd_origem = len(self.view.controles['cmb_selecao']['values'])
        if qtd_origem > 1:
            resposta = messagebox.askyesno("Atenção", "Pasta será excluída!")
            if resposta:
                valores_atuais = list(self.view.controles['cmb_selecao']['values'])
                valores_novos_pasta_origem = []
                valores_novos_pasta_destino = []
                for i in range(len(valores_atuais)):
                    if i != self.view.controles['cmb_selecao'].current():
                        valores_novos_pasta_origem.append(origem_pasta[i])
                        valores_novos_pasta_destino.append(destino_pasta[i])

                origem_pasta.clear()
                destino_pasta.clear()
                origem_pasta = valores_novos_pasta_origem
                destino_pasta = valores_novos_pasta_destino
                self.view.controles['cmb_selecao'].current(0)
                self.carregar_pastas()

                index = 1
                pastas = []
                for i in range(len(valores_novos_pasta_origem)):
                    pastas.append(f"Pasta{index}")
                    index += 1

                self.view.controles['cmb_selecao']['values'] = pastas
                self.view.controles['cmb_selecao'].current(0)

                dados_tinydb.atualizar_campo_tarefa(nome_tarefa, 'pastas_origem', origem_pasta)
                dados_tinydb.atualizar_campo_tarefa(nome_tarefa, 'pastas_destino', destino_pasta)
                carregar_dados = dados_tinydb.carregar_dados_tarefa()

                messagebox.showinfo("Aviso", "Pastas excluida com sucesso!")
        else:
            messagebox.showinfo("Aviso", "Existe somente uma pasta, para excluir deve apagar a tarefa!")


    # --- Funções da Janela Excluir Tarefa ---
    def excluir_tarefa(self):
        global editando_excluir_dados, carregar_dados
        resposta = messagebox.askyesno("Atenção", "Tarefa será excluída!")
        if resposta:
            nome_tarefa = self.view.controles['cmb_selecao'].get()
            qtd_tarefa = len(self.view.controles['cmb_selecao']['values'])
            dados_tinydb.apagar_dados_tarefa(nome_tarefa)

            if qtd_tarefa == 1:
                    dados = ["17", "00", [], [], [True, True, True, True, True, True, True, True], False, False]
                    dados_tinydb.gravar_nova_tarefa("inicial", dados)

            carregar_dados = dados_tinydb.carregar_dados_tarefa()
            editando_excluir_dados = True
            self.fechar_janelas("janela_excluir_tarefa")
