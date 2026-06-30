import tkinter as tk
from tkinter import ttk

import estilo

class JanelaConfiguracao:
    def __init__(self, janela):
        self.janela_configuracao = tk.Toplevel(janela)
        self.janela_configuracao.title("Configurações")
        #self.janela_config.geometry("600x400")
        # Garante que esta janela apareça SEMPRE por cima da principal
        self.janela_configuracao.transient(janela)
        self.style = ttk.Style(self.janela_configuracao)
        self.style.configure("Tamanho.TCheckbutton", font=estilo.FONTE_ARIAL)
        self.style.configure("Fonte.TButton", font=estilo.FONTE_ARIAL)

        self.nome_janela = "configuracao"  # <-- Identificador para o controlador
        self.controles = {}

        self.style.map(
            "Tamanho.TCheckbutton",
            #background=[('selected', 'white'), ('active', 'white'), ('!selected', 'white')],
            indicatorcolor=[('selected', '#0078D7'), ('!selected', 'white')],
            # Azul quando marcado, branco quando desmarcado
            foreground=[('active', 'black')]
        )

        self._criar_layout()
        self._criar_barra_menu()

    def _criar_layout(self):
        # Opcional: Bloqueia a janela principal até que esta seja fechada (Modal)
        self.janela_configuracao.grab_set()

        ## Painel da janela
        self.frame_campos = ttk.Frame(self.janela_configuracao)
        self.frame_campos.grid(row=0, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="ew")

        self.frame_checkbox = ttk.Frame(self.janela_configuracao)
        self.frame_checkbox.grid(row=1, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="ew")

        self.frame_alterar = ttk.Frame(self.janela_configuracao)
        self.frame_alterar.grid(row=2, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="ew")

        ## Controles do painel campos
        linha_campo = 0
        self.lbl_origem = ttk.Label(self.frame_campos, text="Origem:", font=estilo.FONTE_ARIAL)
        self.lbl_origem.grid(row=linha_campo, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO)

        largura_texto = 30
        self.txt_origem = ttk.Entry(self.frame_campos, width=largura_texto, font=estilo.FONTE_ARIAL)
        self.txt_origem.grid(row=linha_campo, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO)
        self.controles['txt_origem'] = self.txt_origem

        self.btn_selecionar_origem = ttk.Button(self.frame_campos, text="...", style="Fonte.TButton")
        self.btn_selecionar_origem.grid(row=linha_campo, column=2, padx=estilo.ESPACO, pady=estilo.ESPACO)
        self.controles['btn_selecionar_origem'] = self.btn_selecionar_origem
        linha_campo += 1

        self.lbl_destino = ttk.Label(self.frame_campos, text="Destino:", font=estilo.FONTE_ARIAL)
        self.lbl_destino.grid(row=linha_campo, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO)

        self.txt_destino = ttk.Entry(self.frame_campos, width=largura_texto, font=estilo.FONTE_ARIAL)
        self.txt_destino.grid(row=linha_campo, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO)
        self.controles['txt_destino'] = self.txt_destino

        self.btn_selecionar_destino = ttk.Button(self.frame_campos, text="...", style="Fonte.TButton")
        self.btn_selecionar_destino.grid(row=linha_campo, column=2, padx=estilo.ESPACO, pady=estilo.ESPACO)
        self.controles['btn_selecionar_destino'] = self.btn_selecionar_destino
        linha_campo += 1

        self.lbl_tarefa = ttk.Label(self.frame_campos, text="Tarefa:", font=estilo.FONTE_ARIAL)
        self.lbl_tarefa.grid(row=linha_campo, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO)

        self.txt_tarefa = ttk.Entry(self.frame_campos, font=estilo.FONTE_ARIAL)
        self.txt_tarefa.grid(row=linha_campo, column=1, columnspan=2, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="we")
        self.controles['txt_tarefa'] = self.txt_tarefa
        linha_campo += 1

        self.lbl_horario = ttk.Label(self.frame_campos, text="Horario:", font=estilo.FONTE_ARIAL)
        self.lbl_horario.grid(row=linha_campo, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO)

        # Container para agrupar os elementos da hora
        self.frame_hora = ttk.Frame(self.frame_campos, padding=0)
        self.frame_hora.grid(row=linha_campo, column=1)

        # Spinbox das Horas (00 a 23)
        # format="%02.0f" garante que mostre '01' em vez de '1'
        self.spin_hora = ttk.Spinbox(self.frame_hora, from_=0, to=23, format="%02.0f", width=3, wrap=True, font=("Segoe UI", 12))
        self.spin_hora.set("17")  # Hora padrão
        self.spin_hora.grid(row=0, column=0)
        self.controles['spin_hora'] = self.spin_hora

        # Separador dos dois pontos
        self.lbl_dois_pontos = ttk.Label(self.frame_hora, text=":", font=("Segoe UI", 14, "bold"))
        self.lbl_dois_pontos.grid(row=0, column=1, padx=5)

        # Spinbox dos Minutos (00 a 59)
        self.spin_min = ttk.Spinbox(self.frame_hora, from_=0, to=59, format="%02.0f", width=3, wrap=True, font=("Segoe UI", 12))
        self.spin_min.set("00")  # Minuto padrão
        self.spin_min.grid(row=0, column=2)

        self.chk_desligar = ttk.Checkbutton(self.frame_campos, text="Desligar", style="Tamanho.TCheckbutton")
        self.chk_desligar.grid(row=linha_campo, column=2, columnspan=2, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="e")

        # --- Painel Checkbutton ---
        linha_check = 0
        self.var_diariamente = tk.BooleanVar(value=True)
        self.chk_diariamente = ttk.Checkbutton(self.frame_checkbox, text="Diariamente", style="Tamanho.TCheckbutton", variable=self.var_diariamente)
        self.chk_diariamente.grid(row=linha_check, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")

        self.chk_quarta = ttk.Checkbutton(self.frame_checkbox, text="Quarta-Feira", style="Tamanho.TCheckbutton")
        self.chk_quarta.grid(row=linha_check, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")
        linha_check += 1

        self.chk_domingo = ttk.Checkbutton(self.frame_checkbox, text="Domingo", style="Tamanho.TCheckbutton")
        self.chk_domingo.grid(row=linha_check, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")

        self.chk_quinta = ttk.Checkbutton(self.frame_checkbox, text="Quinta-Feira", style="Tamanho.TCheckbutton")
        self.chk_quinta.grid(row=linha_check, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")
        linha_check += 1

        self.chk_segunda = ttk.Checkbutton(self.frame_checkbox, text="Segunda-Feira", style="Tamanho.TCheckbutton")
        self.chk_segunda.grid(row=linha_check, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")

        self.chk_sexta = ttk.Checkbutton(self.frame_checkbox, text="Sexta-Feira", style="Tamanho.TCheckbutton")
        self.chk_sexta.grid(row=linha_check, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")
        linha_check += 1

        self.chk_terca = ttk.Checkbutton(self.frame_checkbox, text="Terça-Feira", style="Tamanho.TCheckbutton")
        self.chk_terca.grid(row=linha_check, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")

        self.chk_sabado = ttk.Checkbutton(self.frame_checkbox, text="Sábado", style="Tamanho.TCheckbutton")
        self.chk_sabado.grid(row=linha_check, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")

        largura_botao = 20
        self.btn_add_pasta = ttk.Button(self.frame_checkbox, width=largura_botao, text="Add Pasta", style="Fonte.TButton")
        self.btn_add_pasta.grid(row=0, rowspan=2, column=2, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")

        self.btn_gravar = ttk.Button(self.frame_checkbox, width=largura_botao, text="Gravar Tarefa", style="Fonte.TButton")
        self.btn_gravar.grid(row=2, rowspan=2, column=2, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.btn_gravar.configure(state="disabled")

        # --- Painel Alterar ---
        self.lbl_selecao = ttk.Label(self.frame_alterar, text="Selecionar Tarefa:", font=estilo.FONTE_VAZIA)
        self.lbl_selecao.grid(row=0, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")

        self.cmb_selecao = ttk.Combobox(self.frame_alterar, font=estilo.FONTE_VAZIA, state="readonly")
        self.cmb_selecao.grid(row=0, column=1, columnspan=3, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")

        largura_btn_alterar = 15
        self.btn_alterar = ttk.Button(self.frame_alterar, width=largura_btn_alterar, text="Alterar Tarefa",
                                     style="Fonte.TButton")
        self.btn_alterar.grid(row=1, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.btn_alterar.configure(state="disabled")

        self.btn_adicionar = ttk.Button(self.frame_alterar, width=largura_btn_alterar, text="Adicionar Tarefa",
                                     style="Fonte.TButton")
        self.btn_adicionar.grid(row=1, column=1, padx=(estilo.ESPACO - 1), pady=estilo.ESPACO, sticky="nsew")
        self.btn_adicionar.configure(state="disabled")

        self.btn_remover = ttk.Button(self.frame_alterar, width=largura_btn_alterar, text="Remover Tarefa",
                                     style="Fonte.TButton")
        self.btn_remover.grid(row=1, column=2, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.btn_remover.configure(state="disabled")

    def _criar_barra_menu(self):
        pass