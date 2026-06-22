import tkinter as tk
from tkinter import ttk

import funcoes

# Medidas
espaco = 5
# Estilo
fonte=("", 11, "normal")

class JanelaConfiguracao:
    def __init__(self, janela):
        self.janela_config = tk.Toplevel(janela)
        self.janela_config.title("Configurações")
        #self.janela_config.geometry("600x400")
        # Garante que esta janela apareça SEMPRE por cima da principal
        self.janela_config.transient(janela)

        # Opcional: Bloqueia a janela principal até que esta seja fechada (Modal)
        self.janela_config.grab_set()

        ## Painel da janela
        self.frame_campos = ttk.Frame(self.janela_config)
        self.frame_campos.grid(row=0, column=0, padx=espaco, pady=espaco)

        self.frame_checkbox = ttk.Frame(self.janela_config)
        self.frame_checkbox.grid(row=1, column=0, padx=espaco, pady=espaco)

        self.frame_botoes = ttk.Frame(self.janela_config)
        self.frame_botoes.grid(row=0, column=1, columnspan=2, padx=espaco, pady=espaco)

        ## Controles do painel campos
        linha_campo = 0
        self.lbl_origem = ttk.Label(self.frame_campos, text="Origem:", font=fonte)
        self.lbl_origem.grid(row=linha_campo, column=0, padx=espaco, pady=espaco)

        self.txt_origem = ttk.Entry(self.frame_campos, width=30, font=fonte)
        self.txt_origem.grid(row=linha_campo, column=1, padx=espaco, pady=espaco)

        self.btn_selecionar_origem = ttk.Button(self.frame_campos, text="...", command=lambda: selecionar_origem())
        self.btn_selecionar_origem.grid(row=linha_campo, column=2, padx=espaco, pady=espaco)
        linha_campo += 1

        self.lbl_destino = ttk.Label(self.frame_campos, text="Destino:", font=fonte)
        self.lbl_destino.grid(row=linha_campo, column=0, padx=espaco, pady=espaco)

        self.txt_destino = ttk.Entry(self.frame_campos, width=30, font=fonte)
        self.txt_destino.grid(row=linha_campo, column=1, padx=espaco, pady=espaco)

        self.btn_selecionar_destino = ttk.Button(self.frame_campos, text="...", command=lambda: selecionar_destino())
        self.btn_selecionar_destino.grid(row=linha_campo, column=2, padx=espaco, pady=espaco)
        linha_campo += 1

        self.lbl_horario = ttk.Label(self.frame_campos, text="Horario:", font=fonte)
        self.lbl_horario.grid(row=linha_campo, column=0, padx=espaco, pady=espaco)

        # Container para agrupar os elementos da hora
        self.frame_hora = ttk.Frame(self.frame_campos, padding=20)
        self.frame_hora.grid(row=linha_campo, column=1, padx=espaco, pady=espaco)

        # Spinbox das Horas (00 a 23)
        # format="%02.0f" garante que mostre '01' em vez de '1'
        self.spin_hora = ttk.Spinbox(self.frame_hora, from_=0, to=23, format="%02.0f", width=3, wrap=True, font=("Segoe UI", 12))
        self.spin_hora.set("12")  # Hora padrão
        self.spin_hora.grid(row=0, column=0)

        # Separador dos dois pontos
        self.lbl_dois_pontos = ttk.Label(self.frame_hora, text=":", font=("Segoe UI", 14, "bold"))
        self.lbl_dois_pontos.grid(row=0, column=1, padx=5)

        # Spinbox dos Minutos (00 a 59)
        self.spin_min = ttk.Spinbox(self.frame_hora, from_=0, to=59, format="%02.0f", width=3, wrap=True, font=("Segoe UI", 12))
        self.spin_min.set("00")  # Minuto padrão
        self.spin_min.grid(row=0, column=2)

        ### Comandos ###
        def selecionar_origem():
            self.txt_origem.delete(0, "end")
            self.txt_origem.insert(0, funcoes.selecionar_pasta())

        def selecionar_destino():
            self.txt_destino.delete(0, "end")
            self.txt_destino.insert(0, funcoes.selecionar_pasta())