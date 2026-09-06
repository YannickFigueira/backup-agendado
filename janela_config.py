import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

import estilo
from seletor_tempo import TimeSelector


class JanelaConfiguracao:
    def __init__(self, janela):
        self.janela_configuracao = ctk.CTkToplevel(janela)
        self.janela_configuracao.title("Configurações")
        #self.janela_config.geometry("600x400")
        # Garante que esta janela apareça SEMPRE por cima da principal
        self.janela_configuracao.transient(janela)

        self.nome_janela = "configuracao"  # <-- Identificador para o controlador
        self.controles = {}

        self._criar_layout()
        self._criar_barra_menu()

    def _criar_layout(self):
        # --- Controle da janela ---
        self.controles['janela_configuracao'] = self.janela_configuracao
        # Opcional: Bloqueia a janela principal até que esta seja fechada (Modal)
        self.janela_configuracao.grab_set()
        self.janela_configuracao.focus_force()

        # 3. Intercepta o clique no botão 'X' de fechar a Toplevel
        def ao_fechar():
            # Libera o bloqueio antes de destruir
            self.janela_configuracao.grab_release()
            self.janela_configuracao.destroy()

        self.janela_configuracao.protocol("WM_DELETE_WINDOW", ao_fechar)

        ## Painel da janela
        self.frame_campos = ctk.CTkFrame(self.janela_configuracao)
        self.frame_campos.grid(row=0, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="ew")

        self.frame_checkbox = ctk.CTkFrame(self.janela_configuracao)
        self.frame_checkbox.grid(row=1, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="ew")

        ## Controles do painel campos
        linha_campo = 0

        self.lbl_selecao = ctk.CTkLabel(self.frame_campos, text="Selecionar:", font=estilo.FONTE_ARIAL)
        self.lbl_selecao.grid(row=linha_campo, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")

        self.cmb_selecao = ctk.CTkOptionMenu(self.frame_campos, font=estilo.FONTE_VAZIA)
        self.cmb_selecao.grid(row=linha_campo, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.controles['opt_selecao'] = self.cmb_selecao

        # Container para agrupar os elementos da hora
        self.frame_hora = ctk.CTkFrame(self.frame_campos, fg_color="transparent")
        self.frame_hora.grid(row=linha_campo, rowspan=2, column=2, sticky="w")

        self.lbl_horario = ctk.CTkLabel(self.frame_hora, text="Horário", font=estilo.FONTE_ARIAL)
        self.lbl_horario.pack(side="top", anchor="center")
        linha_campo += 1

        self.lbl_tarefa = ctk.CTkLabel(self.frame_campos, text="Tarefa:", font=estilo.FONTE_ARIAL)
        self.lbl_tarefa.grid(row=linha_campo, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")

        self.txt_tarefa = ctk.CTkEntry(self.frame_campos, width=100, font=estilo.FONTE_ARIAL)
        self.txt_tarefa.grid(row=linha_campo, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="we")
        self.controles['txt_tarefa'] = self.txt_tarefa
        linha_campo += 1

        # Seletor de Horas
        self.spin_hora = TimeSelector(
            self.frame_hora,
            values=[f"{h:02d}" for h in range(24)],
            initial_value="17",
            width=70,
            font=estilo.FONTE_VAZIA
        )
        self.spin_hora.pack(side="left", padx=2)

        # Separador ":"
        lbl_pontos = ctk.CTkLabel(self.frame_hora, text=":", font=("Arial", 16, "bold"))
        lbl_pontos.pack(side="left", padx=2)

        # Seletor de Minutos
        self.spin_min = TimeSelector(
            self.frame_hora,
            values=[f"{m:02d}" for m in range(0, 60, 5)],
            initial_value="00",
            width=70,
            font=estilo.FONTE_VAZIA
        )
        self.spin_min.pack(side="left", padx=2)

        self.controles['spin_hora'] = self.spin_hora
        self.controles['spin_min'] = self.spin_min

        # --- Painel Checkbutton ---
        linha_check = 0
        self.var_desabilitar = tk.BooleanVar()
        self.chk_desabilitar = ctk.CTkCheckBox(self.frame_checkbox, text="Desabilitar", variable=self.var_desabilitar)
        self.chk_desabilitar.grid(row=linha_check, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")
        self.controles['var_desabilitar'] = self.var_desabilitar

        self.var_desligar = tk.BooleanVar()
        self.chk_desligar = ctk.CTkCheckBox(self.frame_checkbox, text="Desligar", variable=self.var_desligar)
        self.chk_desligar.grid(row=linha_check, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")
        self.controles['var_desligar'] = self.var_desligar
        linha_check += 1

        self.var_diariamente = tk.BooleanVar(value=True)
        self.chk_diariamente = ctk.CTkCheckBox(self.frame_checkbox, text="Diariamente", variable=self.var_diariamente)
        self.chk_diariamente.grid(row=linha_check, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")
        self.controles['var_diariamente'] = self.var_diariamente
        self.controles['chk_diariamente'] = self.chk_diariamente

        self.var_quarta = tk.BooleanVar(value=False)
        self.chk_quarta = ctk.CTkCheckBox(self.frame_checkbox, text="Quarta-Feira", variable=self.var_quarta)
        self.chk_quarta.grid(row=linha_check, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")
        self.controles['var_quarta'] = self.var_quarta
        self.controles['chk_quarta'] = self.chk_quarta
        linha_check += 1

        self.var_domingo = tk.BooleanVar(value=False)
        self.chk_domingo = ctk.CTkCheckBox(self.frame_checkbox, text="Domingo", variable=self.var_domingo)
        self.chk_domingo.grid(row=linha_check, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")
        self.controles['var_domingo'] = self.var_domingo
        self.controles['chk_domingo'] = self.chk_domingo

        self.var_quinta = tk.BooleanVar(value=False)
        self.chk_quinta = ctk.CTkCheckBox(self.frame_checkbox, text="Quinta-Feira", variable=self.var_quinta)
        self.chk_quinta.grid(row=linha_check, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")
        self.controles['var_quinta'] = self.var_quinta
        self.controles['chk_quinta'] = self.chk_quinta
        linha_check += 1

        self.var_segunda = tk.BooleanVar(value=False)
        self.chk_segunda = ctk.CTkCheckBox(self.frame_checkbox, text="Segunda-Feira", variable=self.var_segunda)
        self.chk_segunda.grid(row=linha_check, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")
        self.controles['var_segunda'] = self.var_segunda
        self.controles['chk_segunda'] = self.chk_segunda

        self.var_sexta = tk.BooleanVar(value=False)
        self.chk_sexta = ctk.CTkCheckBox(self.frame_checkbox, text="Sexta-Feira", variable=self.var_sexta)
        self.chk_sexta.grid(row=linha_check, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")
        self.controles['var_sexta'] = self.var_sexta
        self.controles['chk_sexta'] = self.chk_sexta
        linha_check += 1

        self.var_terca = tk.BooleanVar(value=False)
        self.chk_terca = ctk.CTkCheckBox(self.frame_checkbox, text="Terça-Feira", variable=self.var_terca)
        self.chk_terca.grid(row=linha_check, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")
        self.controles['var_terca'] = self.var_terca
        self.controles['chk_terca'] = self.chk_terca

        self.var_sabado = tk.BooleanVar(value=False)
        self.chk_sabado = ctk.CTkCheckBox(self.frame_checkbox, text="Sábado", variable=self.var_sabado)
        self.chk_sabado.grid(row=linha_check, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")
        self.controles['var_sabado'] = self.var_sabado
        self.controles['chk_sabado'] = self.chk_sabado
        linha_check += 1

        largura_botao = 20
        self.btn_gravar = ctk.CTkButton(self.frame_checkbox, text="Gravar Tarefa")
        self.btn_gravar.grid(row=0, rowspan=5, column=2, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.controles['btn_gravar'] = self.btn_gravar
        
        self.moldura_pastas = ctk.CTkFrame(self.frame_checkbox)
        self.moldura_pastas.grid(row=linha_check, column=0,
                                          columnspan=3, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")

        self.lbl_pastas = ctk.CTkLabel(
            self.moldura_pastas,
            justify="left",
            wraplength=370,
            font=estilo.FONTE_VAZIA
        )
        self.lbl_pastas.pack(anchor="w", padx=(10, 4), pady=(10, 4))
        self.controles['lbl_pastas'] = self.lbl_pastas

    def _criar_barra_menu(self):
        self.barra_menu = tk.Menu(self.janela_configuracao)
        self.janela_configuracao.config(menu=self.barra_menu)
        self.controles['barra_menu'] = self.barra_menu
