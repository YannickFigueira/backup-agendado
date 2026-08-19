import tkinter as tk
from tkinter import ttk

import estilo

class JanelaLogsBackup:
    def __init__(self, janela):
        self.janela_logs_backup = tk.Toplevel(janela)
        self.janela_logs_backup.title("Logs backup")
        #self.janela_config.geometry("600x400")
        # Garante que esta janela apareça SEMPRE por cima da principal
        self.janela_logs_backup.transient(janela)

        self.nome_janela = "log-backup"  # <-- Identificador para o controlador
        self.controles = {}

        self._criar_layout()

    def _criar_layout(self):
        self.controles['janela_logs_backup'] = self.janela_logs_backup

        altura_linha = 10
        self.moldura_log_lista = ttk.Frame(self.janela_logs_backup, width=200, height=220, relief="solid", borderwidth=1)
        self.moldura_log_lista.grid(row=0, rowspan=altura_linha, columnspan=2,
                                         padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="ew")
        self.moldura_log_lista.grid_propagate(False)
        self.moldura_log_lista.pack_propagate(False)

        self.janela_logs_backup.update_idletasks()
        largura_moldura = self.moldura_log_lista.winfo_width()

        self.lbl_logs = ttk.Label(
            self.moldura_log_lista,
            text="",
            justify="left",
            wraplength=largura_moldura - 10 * 2,
            font=estilo.FONTE_VAZIA,
            padding=(10, 4, 10, 0)
        )
        self.lbl_logs.pack(anchor="w")
        self.controles['lbl_logs'] = self.lbl_logs

        altura_linha += 1
        self.lbl_logs_backup = ttk.Label(self.janela_logs_backup, text="Selecionar logs: ", font=estilo.FONTE_VAZIA)
        self.lbl_logs_backup.grid(row=altura_linha, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="ew")

        self.cmb_selecao = ttk.Combobox(self.janela_logs_backup, font=estilo.FONTE_VAZIA, state="readonly",)
        self.cmb_selecao.grid(column=1, row=altura_linha, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="ew")
        self.controles['cmb_selecao'] = self.cmb_selecao
        altura_linha += 1

        self.btn_abrir_logs = ttk.Button(self.janela_logs_backup, text="Abrir log")
        self.btn_abrir_logs.grid(row=altura_linha, columnspan=2, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="ew")
        self.controles['btn_abrir_logs'] = self.btn_abrir_logs
