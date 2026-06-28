import tkinter as tk
from tkinter import ttk

import estilo

## Inicio do Programa
class JanelaPrincipal:
    def __init__(self, janela_principal):
        ## Construção da janela
        self.janela_principal = janela_principal
        self.janela_principal.title(f"{estilo.NOME_PROGRAMA} {estilo.VERSION}")
        self.janela_principal.resizable(width=False, height=False)

        self.nome_janela = "janela-principal"  # <-- Identificador para o controlador
        self.controles = {}

        self._criar_layout()
        self._criar_barra_menu()

    def _criar_layout(self):
        self.controles['janela_principal'] = self.janela_principal

        ## Painel da janela
        self.frame_controls = ttk.Frame(self.janela_principal)
        self.frame_controls.grid(row=0, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.controles['frame_controls'] = self.frame_controls

        self.frame_andamento = ttk.Frame(self.janela_principal)
        self.frame_andamento.grid(row=0, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")

        ## Controles do painel esquerdo
        self.lbl_selecao = ttk.Label(self.frame_controls, text="Selecionar Tarefa:", font=estilo.FONTE_VAZIA)
        self.lbl_selecao.grid(row=estilo.LINHA_PAINEL_ESQUERDO, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")

        self.cmb_selecao = ttk.Combobox(self.frame_controls, font=estilo.FONTE_VAZIA, state="readonly")
        self.cmb_selecao.grid(row=estilo.LINHA_PAINEL_ESQUERDO, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        estilo.LINHA_PAINEL_ESQUERDO += 1

        self.lbl_horario = ttk.Label(self.frame_controls, text="Horário:", font=estilo.FONTE_VAZIA)
        self.lbl_horario.grid(row=estilo.LINHA_PAINEL_ESQUERDO, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")

        self.lbl_hora_execucao = ttk.Label(self.frame_controls, text="--:--", font=estilo.FONTE_VAZIA, anchor="center")
        self.lbl_hora_execucao.grid(row=estilo.LINHA_PAINEL_ESQUERDO, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        estilo.LINHA_PAINEL_ESQUERDO += 1
        linha_estendida_moldura_andamento = estilo.LINHA_PAINEL_ESQUERDO

        self.btn_executar = ttk.Button(self.frame_controls, text="Executar Tarefa", command="")
        self.btn_executar.grid(row=estilo.LINHA_PAINEL_ESQUERDO, columnspan=2, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        estilo.LINHA_PAINEL_ESQUERDO += 1

        self.btn_cancelar = ttk.Button(self.frame_controls, text="Cancelar Tarefa", command="")
        self.btn_cancelar.grid(row=estilo.LINHA_PAINEL_ESQUERDO, columnspan=2, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.btn_cancelar.config(state="disabled")
        estilo.LINHA_PAINEL_ESQUERDO += 1

        self.lbl_tamanho = ttk.Label(self.frame_controls, text="Tamanho:", font=estilo.FONTE_VAZIA, anchor="w")
        self.lbl_tamanho.grid(row=estilo.LINHA_PAINEL_ESQUERDO, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")

        self.controles['linha_painel_esquerdo'] = estilo.LINHA_PAINEL_ESQUERDO

        self.lbl_tamanho_exibir = ttk.Label(self.frame_controls, text=(10*"-"), font=estilo.FONTE_VAZIA, anchor="e")
        self.lbl_tamanho_exibir.grid(row=estilo.LINHA_PAINEL_ESQUERDO, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        estilo.LINHA_PAINEL_ESQUERDO += 1
        # Usando o separador customizado

        estilo.LINHA_PAINEL_ESQUERDO += 1

        linha_estendida_moldura_execucao = 5
        self.frame_controls.rowconfigure(estilo.LINHA_PAINEL_ESQUERDO, weight=0)
        self.moldura_execucao_borda = ttk.Frame(self.frame_controls, height=110, relief="solid", borderwidth=1)
        self.moldura_execucao_borda.grid(row=estilo.LINHA_PAINEL_ESQUERDO, rowspan=linha_estendida_moldura_execucao, columnspan=2,
                                         padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="ew")
        self.moldura_execucao_borda.grid_propagate(False)
        self.moldura_execucao_borda.pack_propagate(False)
        estilo.LINHA_PAINEL_ESQUERDO += 1 + linha_estendida_moldura_execucao

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
            font=estilo.FONTE_VAZIA,
            padding=(10, 4, 10, 0)
        )
        self.lbl_multi_execucao.pack(anchor="w")

        self.btn_encerrar = ttk.Button(self.frame_controls, text="Encerrar Tarefa", command="")
        self.btn_encerrar.grid(row=estilo.LINHA_PAINEL_ESQUERDO, columnspan=2, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")

        ## Controles do painel direito
        linha_painel_direito = 0

        self.frame_andamento.rowconfigure(linha_painel_direito, weight=0)
        self.frame_andamento.columnconfigure(linha_painel_direito, weight=1)

        self.moldura_andamento_atual = ttk.Frame(self.frame_andamento, height=339, relief="solid", borderwidth=1, padding=10)
        self.moldura_andamento_atual.grid(row=linha_painel_direito, rowspan=linha_estendida_moldura_andamento,
                                          column=0, columnspan=3, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="ew")
        self.moldura_andamento_atual.grid_propagate(False)
        self.moldura_andamento_atual.pack_propagate(False)
        linha_painel_direito += linha_estendida_moldura_andamento

        self.lbl_multi_andamento = ttk.Label(
            self.moldura_andamento_atual,
            text=texto_longo,
            justify="left",
            wraplength=500,
            font=estilo.FONTE_VAZIA,
            padding=(10, 4, 10, 0)
        )
        self.lbl_multi_andamento.pack(anchor="w")
        self.controles['lbl_multi_andamento'] = self.lbl_multi_andamento

        self.lbl_copiado = ttk.Label(self.frame_andamento, text="Copiado:", justify="left", font=estilo.FONTE_VAZIA)
        self.lbl_copiado.grid(row=linha_painel_direito, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")

        self.lbl_copiado_tamanho = ttk.Label(self.frame_andamento, text=(8*"-"), justify="center", font=estilo.FONTE_VAZIA)
        self.lbl_copiado_tamanho.grid(row=linha_painel_direito, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")

        self.progress_canvas = tk.Canvas(self.frame_andamento, height=25, bg="white", highlightthickness=1,
                                    highlightbackground="black")
        self.progress_canvas.grid(row=linha_painel_direito, column=2, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="e")

        ## Carregar Menus
        #criar_barra_menu(self.janela_principal, self.lbl_multi_andamento)
    def _criar_barra_menu(self):
        self.barra_menu = tk.Menu(self.janela_principal)
        self.janela_principal.config(menu=self.barra_menu)

        # Menu Arquivo
        self.menu_arquivo = tk.Menu(self.barra_menu, tearoff=0)
        self.barra_menu.add_cascade(label="Arquivo", menu=self.menu_arquivo)
        self.controles['menu_arquivo'] = self.menu_arquivo

        # Menu Ajuda
        self.menu_ajuda = tk.Menu(self.barra_menu, tearoff=0)
        self.barra_menu.add_cascade(label="Ajuda", menu=self.menu_ajuda)
        self.controles['menu_ajuda'] = self.menu_ajuda