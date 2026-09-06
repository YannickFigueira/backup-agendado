import tkinter as tk
import customtkinter as ctk

import barra_menu
import estilo

class JanelaNovaTarefa:
    def __init__(self, janela):
        self.janela_nova_tarefa = ctk.CTkToplevel(janela)
        self.janela_nova_tarefa.title("Nova Tarefa")
        self.janela_nova_tarefa.overrideredirect(True)
        #self.janela_config.geometry("600x400")
        # Garante que esta janela apareça SEMPRE por cima da principal
        self.janela_nova_tarefa.transient(janela)

        self.nome_janela = "nova-tarefa"  # <-- Identificador para o controlador
        self.janela_controle = "janela_nova_tarefa"
        self.controles = {}

        self._criar_layout()
        barra_menu.criar_barra_menu(self, self.janela_nova_tarefa.title(), self.janela_controle, True)

    def _criar_layout(self):
        # --- Controles da janela ---
        self.controles[self.janela_controle] = self.janela_nova_tarefa
        # Opcional: Bloqueia a janela principal até que esta seja fechada (Modal)
        self.janela_nova_tarefa.grab_set()
        self.janela_nova_tarefa.focus_force()

        ## Painel da janela
        self.frame_campos = ctk.CTkFrame(self.janela_nova_tarefa)
        self.frame_campos.grid(row=1, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="ew")

        ## Controles do painel campos
        linha_campo = 0

        self.lbl_origem = ctk.CTkLabel(self.frame_campos, text="Origem:", font=estilo.FONTE_ARIAL)
        self.lbl_origem.grid(row=linha_campo, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")

        largura_texto = 300
        self.txt_origem = ctk.CTkEntry(self.frame_campos, width=largura_texto, font=estilo.FONTE_ARIAL)
        self.txt_origem.grid(row=linha_campo, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO)
        self.controles['txt_origem'] = self.txt_origem

        self.btn_selecionar_origem = ctk.CTkButton(self.frame_campos, text="...", width=40)
        self.btn_selecionar_origem.grid(row=linha_campo, column=2, padx=estilo.ESPACO, pady=estilo.ESPACO)
        self.controles['btn_selecionar_origem'] = self.btn_selecionar_origem
        linha_campo += 1

        self.lbl_destino = ctk.CTkLabel(self.frame_campos, text="Destino:", font=estilo.FONTE_ARIAL)
        self.lbl_destino.grid(row=linha_campo, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="w")

        self.txt_destino = ctk.CTkEntry(self.frame_campos, width=largura_texto, font=estilo.FONTE_ARIAL)
        self.txt_destino.grid(row=linha_campo, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO)
        self.controles['txt_destino'] = self.txt_destino

        self.btn_selecionar_destino = ctk.CTkButton(self.frame_campos, text="...", width=40)
        self.btn_selecionar_destino.grid(row=linha_campo, column=2, padx=estilo.ESPACO, pady=estilo.ESPACO)
        self.controles['btn_selecionar_destino'] = self.btn_selecionar_destino
        linha_campo += 1

        self.btn_adicionar = ctk.CTkButton(self.frame_campos, text="Adicionar pasta")
        self.btn_adicionar.grid(row=linha_campo, column=0, columnspan=3, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.controles['btn_adicionar'] = self.btn_adicionar
        linha_campo += 1

        self.btn_salvar = ctk.CTkButton(self.frame_campos, text="Salvar pastas")
        self.btn_salvar.grid(row=linha_campo, column=0, columnspan=3, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.btn_salvar.configure(state="disabled")
        self.controles['btn_salvar'] = self.btn_salvar