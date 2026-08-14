import tkinter as tk
from tkinter import ttk

import estilo

class JanelaNovaTarefa:
    def __init__(self, janela):
        self.janela_nova_tarefa = tk.Toplevel(janela)
        self.janela_nova_tarefa.title("Nova Tarefa")
        #self.janela_config.geometry("600x400")
        # Garante que esta janela apareça SEMPRE por cima da principal
        self.janela_nova_tarefa.transient(janela)

        self.nome_janela = "nova-tarefa"  # <-- Identificador para o controlador
        self.controles = {}

        self._criar_layout()

    def _criar_layout(self):
        # --- Controles da janela ---
        self.controles['janela_nova_tarefa'] = self.janela_nova_tarefa
        # Opcional: Bloqueia a janela principal até que esta seja fechada (Modal)
        self.janela_nova_tarefa.grab_set()

        ## Painel da janela
        self.frame_campos = ttk.Frame(self.janela_nova_tarefa)
        self.frame_campos.grid(row=0, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="ew")

        ## Controles do painel campos
        linha_campo = 0

        self.lbl_origem = ttk.Label(self.frame_campos, text="Origem:", font=estilo.FONTE_ARIAL)
        self.lbl_origem.grid(row=linha_campo, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")

        largura_texto = 30
        self.txt_origem = ttk.Entry(self.frame_campos, width=largura_texto, font=estilo.FONTE_ARIAL)
        self.txt_origem.grid(row=linha_campo, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO)
        self.controles['txt_origem'] = self.txt_origem

        self.btn_selecionar_origem = ttk.Button(self.frame_campos, text="...", style="Fonte.TButton")
        self.btn_selecionar_origem.grid(row=linha_campo, column=2, padx=estilo.ESPACO, pady=estilo.ESPACO)
        self.controles['btn_selecionar_origem'] = self.btn_selecionar_origem
        linha_campo += 1

        self.lbl_destino = ttk.Label(self.frame_campos, text="Destino:", font=estilo.FONTE_ARIAL)
        self.lbl_destino.grid(row=linha_campo, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")

        self.txt_destino = ttk.Entry(self.frame_campos, width=largura_texto, font=estilo.FONTE_ARIAL)
        self.txt_destino.grid(row=linha_campo, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO)
        self.controles['txt_destino'] = self.txt_destino

        self.btn_selecionar_destino = ttk.Button(self.frame_campos, text="...", style="Fonte.TButton")
        self.btn_selecionar_destino.grid(row=linha_campo, column=2, padx=estilo.ESPACO, pady=estilo.ESPACO)
        self.controles['btn_selecionar_destino'] = self.btn_selecionar_destino
        linha_campo += 1

        self.btn_adicionar = ttk.Button(self.frame_campos, text="Adicionar pasta",
                                     style="Fonte.TButton")
        self.btn_adicionar.grid(row=linha_campo, column=0, columnspan=3, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.controles['btn_adicionar'] = self.btn_adicionar
        linha_campo += 1

        self.btn_salvar = ttk.Button(self.frame_campos, text="Salvar pastas",
                                     style="Fonte.TButton")
        self.btn_salvar.grid(row=linha_campo, column=0, columnspan=3, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.btn_salvar.config(state="disabled")
        self.controles['btn_salvar'] = self.btn_salvar