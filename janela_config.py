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
        # --- Controle da janela ---
        self.controles['janela_configuracao'] = self.janela_configuracao
        # Opcional: Bloqueia a janela principal até que esta seja fechada (Modal)
        self.janela_configuracao.grab_set()

        ## Painel da janela
        self.frame_campos = ttk.Frame(self.janela_configuracao)
        self.frame_campos.grid(row=0, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="ew")

        self.frame_checkbox = ttk.Frame(self.janela_configuracao)
        self.frame_checkbox.grid(row=1, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="ew")

        ## Controles do painel campos
        linha_campo = 0

        self.txt_destino = ttk.Entry(self.frame_campos, width=largura_texto, font=estilo.FONTE_ARIAL)
        self.txt_destino.grid(row=linha_campo, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO)
        self.controles['txt_destino'] = self.txt_destino

        self.btn_selecionar_destino = ttk.Button(self.frame_campos, text="...", style="Fonte.TButton")
        self.btn_selecionar_destino.grid(row=linha_campo, column=2, padx=estilo.ESPACO, pady=estilo.ESPACO)
        self.controles['btn_selecionar_destino'] = self.btn_selecionar_destino
        linha_campo += 1
        """
        self.lbl_selecao = ttk.Label(self.frame_campos, text="Selecionar:", font=estilo.FONTE_ARIAL)
        self.lbl_selecao.grid(row=linha_campo, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")

        self.cmb_selecao = ttk.Combobox(self.frame_campos, font=estilo.FONTE_VAZIA, state="readonly")
        self.cmb_selecao.grid(row=linha_campo, column=1, columnspan=3, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.controles['cmb_selecao'] = self.cmb_selecao
        linha_campo += 1

        self.lbl_tarefa = ttk.Label(self.frame_campos, text="Tarefa:", font=estilo.FONTE_ARIAL)
        self.lbl_tarefa.grid(row=linha_campo, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")

        self.txt_tarefa = ttk.Entry(self.frame_campos, width=40, font=estilo.FONTE_ARIAL)
        self.txt_tarefa.grid(row=linha_campo, column=1, columnspan=2, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="we")
        self.controles['txt_tarefa'] = self.txt_tarefa
        linha_campo += 1

        self.lbl_horario = ttk.Label(self.frame_campos, text="Horario:", font=estilo.FONTE_ARIAL)
        self.lbl_horario.grid(row=linha_campo, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")

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
        self.lbl_dois_pontos = ttk.Label(self.frame_hora, text=":", font=("Segoe UI", 18, "bold"))
        self.lbl_dois_pontos.grid(row=0, column=1, padx=5)

        # Spinbox dos Minutos (00 a 59)
        self.spin_min = ttk.Spinbox(self.frame_hora, from_=0, to=59, format="%02.0f", width=3, wrap=True, font=("Segoe UI", 12))
        self.spin_min.set("00")  # Minuto padrão
        self.spin_min.grid(row=0, column=2)
        self.controles['spin_min'] = self.spin_min

        # --- Painel Checkbutton ---
        linha_check = 0
        self.var_desabilitar = tk.BooleanVar()
        self.chk_desabilitar = ttk.Checkbutton(self.frame_checkbox, text="Desabilitar", style="Tamanho.TCheckbutton", variable=self.var_desabilitar)
        self.chk_desabilitar.grid(row=linha_check, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")
        self.controles['var_desabilitar'] = self.var_desabilitar

        self.var_desligar = tk.BooleanVar()
        self.chk_desligar = ttk.Checkbutton(self.frame_checkbox, text="Desligar", style="Tamanho.TCheckbutton", variable=self.var_desligar)
        self.chk_desligar.grid(row=linha_check, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")
        self.controles['var_desligar'] = self.var_desligar
        linha_check += 1

        self.var_diariamente = tk.BooleanVar(value=True)
        self.chk_diariamente = ttk.Checkbutton(self.frame_checkbox, text="Diariamente", style="Tamanho.TCheckbutton", variable=self.var_diariamente)
        self.chk_diariamente.grid(row=linha_check, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")
        self.controles['var_diariamente'] = self.var_diariamente
        self.controles['chk_diariamente'] = self.chk_diariamente

        self.var_quarta = tk.BooleanVar(value=False)
        self.chk_quarta = ttk.Checkbutton(self.frame_checkbox, text="Quarta-Feira", style="Tamanho.TCheckbutton", variable=self.var_quarta)
        self.chk_quarta.grid(row=linha_check, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")
        self.controles['var_quarta'] = self.var_quarta
        self.controles['chk_quarta'] = self.chk_quarta
        linha_check += 1

        self.var_domingo = tk.BooleanVar(value=False)
        self.chk_domingo = ttk.Checkbutton(self.frame_checkbox, text="Domingo", style="Tamanho.TCheckbutton", variable=self.var_domingo)
        self.chk_domingo.grid(row=linha_check, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")
        self.controles['var_domingo'] = self.var_domingo
        self.controles['chk_domingo'] = self.chk_domingo

        self.var_quinta = tk.BooleanVar(value=False)
        self.chk_quinta = ttk.Checkbutton(self.frame_checkbox, text="Quinta-Feira", style="Tamanho.TCheckbutton", variable=self.var_quinta)
        self.chk_quinta.grid(row=linha_check, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")
        self.controles['var_quinta'] = self.var_quinta
        self.controles['chk_quinta'] = self.chk_quinta
        linha_check += 1

        self.var_segunda = tk.BooleanVar(value=False)
        self.chk_segunda = ttk.Checkbutton(self.frame_checkbox, text="Segunda-Feira", style="Tamanho.TCheckbutton", variable=self.var_segunda)
        self.chk_segunda.grid(row=linha_check, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")
        self.controles['var_segunda'] = self.var_segunda
        self.controles['chk_segunda'] = self.chk_segunda

        self.var_sexta = tk.BooleanVar(value=False)
        self.chk_sexta = ttk.Checkbutton(self.frame_checkbox, text="Sexta-Feira", style="Tamanho.TCheckbutton", variable=self.var_sexta)
        self.chk_sexta.grid(row=linha_check, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")
        self.controles['var_sexta'] = self.var_sexta
        self.controles['chk_sexta'] = self.chk_sexta
        linha_check += 1

        self.var_terca = tk.BooleanVar(value=False)
        self.chk_terca = ttk.Checkbutton(self.frame_checkbox, text="Terça-Feira", style="Tamanho.TCheckbutton", variable=self.var_terca)
        self.chk_terca.grid(row=linha_check, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")
        self.controles['var_terca'] = self.var_terca
        self.controles['chk_terca'] = self.chk_terca

        self.var_sabado = tk.BooleanVar(value=False)
        self.chk_sabado = ttk.Checkbutton(self.frame_checkbox, text="Sábado", style="Tamanho.TCheckbutton", variable=self.var_sabado)
        self.chk_sabado.grid(row=linha_check, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")
        self.controles['var_sabado'] = self.var_sabado
        self.controles['chk_sabado'] = self.chk_sabado
        linha_check += 1

        largura_botao = 20
        self.btn_gravar = ttk.Button(self.frame_checkbox, width=largura_botao, text="Gravar Tarefa", style="Fonte.TButton")
        self.btn_gravar.grid(row=0, rowspan=5, column=2, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")

        # Texto de exemplo
        texto_longo = (
            "Status do Sistema:\n"
            "  Backup da pasta 'Trabalho' concluído.\n"
            "  Erro ao acessar a unidade E:/ (Dispositivo desconectado). extensão de teste!\n"
            "  Próxima verificação agendada para às 20:00."
        )
        self.moldura_pastas = ttk.Frame(self.frame_checkbox, relief="solid", borderwidth=1, padding=10)
        self.moldura_pastas.grid(row=linha_check, column=0,
                                          columnspan=3, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")

        self.lbl_pastas = ttk.Label(
            self.moldura_pastas,
            text=texto_longo,
            justify="left",
            wraplength=370,
            font=estilo.FONTE_VAZIA,
            padding=(10, 4, 10, 4)
        )
        self.lbl_pastas.pack(anchor="w")
        self.controles['lbl_pastas'] = self.lbl_pastas

    def _criar_barra_menu(self):
        self.barra_menu = tk.Menu(self.janela_configuracao)
        self.janela_configuracao.config(menu=self.barra_menu)
        self.controles['barra_menu'] = self.barra_menu
