import tkinter as tk
from tkinter import ttk

import estilo

class JanelaAlterarPastas:
    def __init__(self, janela):
        self.janela_alterar_pastas = tk.Toplevel(janela)
        self.janela_alterar_pastas.title("Alterar Pastas")
        #self.janela_config.geometry("600x400")
        # Garante que esta janela apareça SEMPRE por cima da principal
        self.janela_alterar_pastas.transient(janela)

        self.nome_janela = "alterar-pastas"  # <-- Identificador para o controlador
        self.controles = {}

        self._criar_layout()

    def _criar_layout(self):
        # --- Controles da janela ---
        self.controles['janela_alterar_pastas'] = self.janela_alterar_pastas
        # Opcional: Bloqueia a janela principal até que esta seja fechada (Modal)
        self.janela_alterar_pastas.grab_set()


        ## Painel da janela
        self.frame_campos = ttk.Frame(self.janela_alterar_pastas)
        self.frame_campos.grid(row=0, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="ew")

        self.frame_adicionar = ttk.Frame(self.janela_alterar_pastas)
        self.frame_adicionar.grid(row=1, column=0, columnspan=3, padx=estilo.ESPACO, pady=(0, estilo.ESPACO), sticky="ew")
        self.frame_adicionar.grid_columnconfigure(0, weight=1)
        self.frame_adicionar.grid_columnconfigure(1, weight=1)

        ## Controles do painel campos
        linha_campo = 0

        self.lbl_selecao = ttk.Label(self.frame_campos, text="Selecionar:", font=estilo.FONTE_ARIAL)
        self.lbl_selecao.grid(row=linha_campo, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")

        self.cmb_selecao = ttk.Combobox(self.frame_campos, font=estilo.FONTE_VAZIA, state="readonly")
        self.cmb_selecao.grid(row=linha_campo, column=1, columnspan=3, padx=estilo.ESPACO, pady=estilo.ESPACO,
                              sticky="nsew")
        self.controles['cmb_selecao'] = self.cmb_selecao
        linha_campo += 1

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

        self.btn_alterar = ttk.Button(self.frame_campos, text="Alterar pasta",
                                     style="Fonte.TButton")
        self.btn_alterar.grid(row=linha_campo, column=0, columnspan=3, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.controles['btn_alterar'] = self.btn_alterar
        linha_campo += 1

        self.btn_excluir_pasta = ttk.Button(self.frame_campos, text="Excluir pasta",
                                      style="Fonte.TButton")
        self.btn_excluir_pasta.grid(row=linha_campo, column=0, columnspan=3, padx=estilo.ESPACO, pady=estilo.ESPACO,
                              sticky="nsew")
        self.controles['btn_excluir_pasta'] = self.btn_excluir_pasta

        self.btn_adicionar_pasta = ttk.Button(self.frame_adicionar, text="Adicionar nova pasta",
                                      style="Fonte.TButton")
        self.btn_adicionar_pasta.grid(row=0, column=0, padx=estilo.ESPACO, pady=(0, estilo.ESPACO),
                              sticky="nsew")
        self.controles['btn_adicionar_pasta'] = self.btn_adicionar_pasta

        self.bnt_gravar_adicionar = ttk.Button(self.frame_adicionar, text="Gravar nova pasta",
                                      style="Fonte.TButton")
        self.bnt_gravar_adicionar.grid(row=0, column=1, padx=estilo.ESPACO, pady=(0, estilo.ESPACO),
                              sticky="nsew")
        self.controles['bnt_gravar_adicionar'] = self.bnt_gravar_adicionar
