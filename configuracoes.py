import tkinter as tk
from tkinter import ttk

import funcoes

# Medidas
espaco = 5
# Estilo
fonte=("Arial", 11, "normal")

class JanelaConfiguracao:
    def __init__(self, janela):
        self.janela_config = tk.Toplevel(janela)
        self.janela_config.title("Configurações")
        #self.janela_config.geometry("600x400")
        # Garante que esta janela apareça SEMPRE por cima da principal
        self.janela_config.transient(janela)
        self.style = ttk.Style(self.janela_config)
        self.style.configure("Tamanho.TCheckbutton", font=fonte)
        self.style.configure("Fonte.TButton", font=fonte)

        self.style.map(
            "Tamanho.TCheckbutton",
            #background=[('selected', 'white'), ('active', 'white'), ('!selected', 'white')],
            indicatorcolor=[('selected', '#0078D7'), ('!selected', 'white')],
            # Azul quando marcado, branco quando desmarcado
            foreground=[('active', 'black')]
        )

        # Opcional: Bloqueia a janela principal até que esta seja fechada (Modal)
        self.janela_config.grab_set()

        ## Painel da janela
        self.frame_campos = ttk.Frame(self.janela_config)
        self.frame_campos.grid(row=0, column=0, padx=espaco, pady=espaco, sticky="ew")

        self.frame_checkbox = ttk.Frame(self.janela_config)
        self.frame_checkbox.grid(row=1, column=0, padx=espaco, pady=espaco, sticky="ew")

        ## Controles do painel campos
        linha_campo = 0
        self.lbl_origem = ttk.Label(self.frame_campos, text="Origem:", font=fonte)
        self.lbl_origem.grid(row=linha_campo, column=0, padx=espaco, pady=espaco)

        largura_texto = 30
        self.txt_origem = ttk.Entry(self.frame_campos, width=largura_texto, font=fonte)
        self.txt_origem.grid(row=linha_campo, column=1, padx=espaco, pady=espaco)

        self.btn_selecionar_origem = ttk.Button(self.frame_campos, text="...", style="Fonte.TButton", command=lambda: selecionar_origem())
        self.btn_selecionar_origem.grid(row=linha_campo, column=2, padx=espaco, pady=espaco)
        linha_campo += 1

        self.lbl_destino = ttk.Label(self.frame_campos, text="Destino:", font=fonte)
        self.lbl_destino.grid(row=linha_campo, column=0, padx=espaco, pady=espaco)

        self.txt_destino = ttk.Entry(self.frame_campos, width=largura_texto, font=fonte)
        self.txt_destino.grid(row=linha_campo, column=1, padx=espaco, pady=espaco)

        self.btn_selecionar_destino = ttk.Button(self.frame_campos, text="...", style="Fonte.TButton", command=lambda: selecionar_destino())
        self.btn_selecionar_destino.grid(row=linha_campo, column=2, padx=espaco, pady=espaco)
        linha_campo += 1

        self.lbl_horario = ttk.Label(self.frame_campos, text="Horario:", font=fonte)
        self.lbl_horario.grid(row=linha_campo, column=0, padx=espaco, pady=espaco)

        # Container para agrupar os elementos da hora
        self.frame_hora = ttk.Frame(self.frame_campos, padding=0)
        self.frame_hora.grid(row=linha_campo, column=1)

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

        self.chk_desligar = ttk.Checkbutton(self.frame_campos, text="Desligar", style="Tamanho.TCheckbutton")
        self.chk_desligar.grid(row=linha_campo, column=2, columnspan=2, padx=espaco, pady=espaco, sticky="e")

        ## Painel Checkbutton
        linha_check = 0
        self.var_diariamente = tk.BooleanVar(value=True)
        self.chk_diariamente = ttk.Checkbutton(self.frame_checkbox, text="Diariamente", style="Tamanho.TCheckbutton", variable=self.var_diariamente)
        self.chk_diariamente.grid(row=linha_check, column=0, padx=espaco, pady=espaco, sticky="w")

        self.chk_quarta = ttk.Checkbutton(self.frame_checkbox, text="Quarta-Feira", style="Tamanho.TCheckbutton")
        self.chk_quarta.grid(row=linha_check, column=1, padx=espaco, pady=espaco, sticky="w")
        linha_check += 1

        self.chk_domingo = ttk.Checkbutton(self.frame_checkbox, text="Domingo", style="Tamanho.TCheckbutton")
        self.chk_domingo.grid(row=linha_check, column=0, padx=espaco, pady=espaco, sticky="w")

        self.chk_quinta = ttk.Checkbutton(self.frame_checkbox, text="Quinta-Feira", style="Tamanho.TCheckbutton")
        self.chk_quinta.grid(row=linha_check, column=1, padx=espaco, pady=espaco, sticky="w")
        linha_check += 1

        self.chk_segunda = ttk.Checkbutton(self.frame_checkbox, text="Segunda-Feira", style="Tamanho.TCheckbutton")
        self.chk_segunda.grid(row=linha_check, column=0, padx=espaco, pady=espaco, sticky="w")

        self.chk_sexta = ttk.Checkbutton(self.frame_checkbox, text="Sexta-Feira", style="Tamanho.TCheckbutton")
        self.chk_sexta.grid(row=linha_check, column=1, padx=espaco, pady=espaco, sticky="w")
        linha_check += 1

        self.chk_terca = ttk.Checkbutton(self.frame_checkbox, text="Terça-Feira", style="Tamanho.TCheckbutton")
        self.chk_terca.grid(row=linha_check, column=0, padx=espaco, pady=espaco, sticky="w")

        self.chk_sabado = ttk.Checkbutton(self.frame_checkbox, text="Sábado", style="Tamanho.TCheckbutton")
        self.chk_sabado.grid(row=linha_check, column=1, padx=espaco, pady=espaco, sticky="w")

        largura_botao = 20
        self.btn_add_pasta = ttk.Button(self.frame_checkbox, width=largura_botao, text="Add Pasta", style="Fonte.TButton")
        self.btn_add_pasta.grid(row=0, rowspan=2, column=2, padx=espaco, pady=espaco, sticky="nsew")

        self.btn_gravar = ttk.Button(self.frame_checkbox, width=largura_botao, text="Gravar Tarefa", style="Fonte.TButton")
        self.btn_gravar.grid(row=2, rowspan=2, column=2, padx=espaco, pady=espaco, sticky="nsew")
        self.btn_gravar.configure(state="disabled")

        ### Comandos ###
        def selecionar_origem():
            self.txt_origem.delete(0, "end")
            self.txt_origem.insert(0, funcoes.selecionar_pasta())

        def selecionar_destino():
            self.txt_destino.delete(0, "end")
            self.txt_destino.insert(0, funcoes.selecionar_pasta())