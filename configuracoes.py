import tkinter as tk
from tkinter import ttk

class JanelaConfiguracao:
    def __init__(self, janela):
        self.janela_config = tk.Toplevel(janela)
        self.janela_config.title("Configurações")
        self.janela_config.geometry("600x400")
        # Garante que esta janela apareça SEMPRE por cima da principal
        self.janela_config.transient(janela)

        # Opcional: Bloqueia a janela principal até que esta seja fechada (Modal)
        self.janela_config.grab_set()

        ## Painel da janela
        espaco = 5
        self.frame_campos = tk.Frame(self.janela_config)
        self.frame_campos.grid(row=0, column=0, padx=espaco, pady=espaco)

        self.frame_checkbox = tk.Frame(self.janela_config)
        self.frame_checkbox.grid(row=1, column=0, padx=espaco, pady=espaco)

        self.frame_botoes = tk.Frame(self.janela_config)
        self.frame_botoes.grid(row=0, column=1, columnspan=2, padx=espaco, pady=espaco)

        ##