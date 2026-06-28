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

        altura_linha = 10
        self.moldura_log_lista = ttk.Frame(self.janela_logs_backup, width=200, height=220, relief="solid", borderwidth=1)
        self.moldura_log_lista.grid(row=0, rowspan=altura_linha, columnspan=2,
                                         padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="ew")
        self.moldura_log_lista.grid_propagate(False)
        self.moldura_log_lista.pack_propagate(False)

        # Texto de exemplo
        texto_longo = (
            "Status do Sistema:\n"
            "- Backup da pasta 'Trabalho' concluído.\n"
            "- Erro ao acessar a unidade E:/ (Dispositivo desconectado).\n"
            "- Próxima verificação agendada para às 20:00.\n"
            "linha 5\n"
            "linha 6\n"
            "linha 7\n"
            "linha 8\n"
            "linha 9\n"
            "linha 10\n"
        )

        self.janela_logs_backup.update_idletasks()
        largura_moldura = self.moldura_log_lista.winfo_width()

        self.lbl_logs = ttk.Label(
            self.moldura_log_lista,
            text=texto_longo,
            justify="left",
            wraplength=largura_moldura - 10 * 2,
            font=estilo.FONTE_VAZIA,
            padding=(10, 4, 10, 0)
        )
        self.lbl_logs.pack(anchor="w")

        altura_linha += 1
        self.lbl_logs_backup = ttk.Label(self.janela_logs_backup, text="Selecionar logs: ", font=estilo.FONTE_VAZIA)
        self.lbl_logs_backup.grid(row=altura_linha, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO)

        self.cmb_logs = ttk.Combobox(self.janela_logs_backup, font=estilo.FONTE_VAZIA, state="readonly",)
        self.cmb_logs.grid(column=1, row=altura_linha, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="ew")
        altura_linha += 1

        self.btn_logs = ttk.Button(self.janela_logs_backup, text="Abrir log")
        self.btn_logs.grid(row=altura_linha, columnspan=2, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="ew")

        # Combo para selecionar os logs
        # Botão para abrir os logs
        # Text area para mostrar os logs
        #
