import tkinter as tk
from tkinter import ttk

import estilo

class JanelaExcluirTarefa:
    def __init__(self, janela):
        self.janela_excluir_tarefa = tk.Toplevel(janela)
        self.janela_excluir_tarefa.title("Excluir Tarefa")
        #self.janela_config.geometry("600x400")
        # Garante que esta janela apareça SEMPRE por cima da principal
        self.janela_excluir_tarefa.transient(janela)

        self.nome_janela = "excluir-tarefa"  # <-- Identificador para o controlador
        self.controles = {}

        self._criar_layout()

    def _criar_layout(self):
        # --- Controles da janela ---
        self.controles['janela_excluir_tarefa'] = self.janela_excluir_tarefa
        # Opcional: Bloqueia a janela principal até que esta seja fechada (Modal)
        self.janela_excluir_tarefa.grab_set()

        ## Painel da janela
        self.frame_campos = ttk.Frame(self.janela_excluir_tarefa)
        self.frame_campos.grid(row=0, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="ew")

        ## Controles do painel campos
        linha_campo = 0

        self.lbl_selecao = ttk.Label(self.frame_campos, text="Selecionar:", font=estilo.FONTE_ARIAL)
        self.lbl_selecao.grid(row=linha_campo, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")

        self.cmb_selecao = ttk.Combobox(self.frame_campos, font=estilo.FONTE_VAZIA, state="readonly")
        self.cmb_selecao.grid(row=linha_campo, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO,
                              sticky="nsew")
        self.controles['cmb_selecao'] = self.cmb_selecao
        linha_campo += 1

        self.btn_excluir = ttk.Button(self.frame_campos, text="Excluir Tarefa", style="Fonte.TButton")
        self.btn_excluir.grid(row=linha_campo, column=0, columnspan=2, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.controles['btn_excluir'] = self.btn_excluir