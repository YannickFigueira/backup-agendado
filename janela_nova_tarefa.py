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