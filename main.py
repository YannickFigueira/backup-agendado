import argparse
import tkinter as tk
from tkinter import ttk, font

from matplotlib.cbook import safe_first_element

## Variáveis principais
version = "4.0.0"
repo = "backup-agendado"
# Medidas
espaco = 5
# Estilo
fonte=("", 11, "normal")

parser = argparse.ArgumentParser(prog="backup-agendado")
parser.add_argument("--version", action="version", version=f"%(prog)s {version}")
args = parser.parse_args()

## Container
def criar_separador_com_texto(janela_container, texto, linha, espacox, espacoy):
    # 1. Criamos um container invisível para envelopar o separador completo
    container = ttk.Frame(janela_container)
    container.grid(row=linha, columnspan=6, sticky="ew", padx=espacox, pady=espacoy)

    # Configura o container para expandir as linhas laterais igualmente
    container.columnconfigure(0, weight=1)
    container.columnconfigure(2, weight=1)

    # 2. Linha da Esquerda
    sep_esquerda = ttk.Separator(container, orient="horizontal")
    sep_esquerda.grid(row=0, column=0, sticky="ew", padx=(0, 10))

    # 3. O Texto Centralizado (com peso Bold/Negrito)
    # Usamos o fundo padrão (background) do root para não dar corte de cor
    label_texto = ttk.Label(container, text=texto, font=("", 10, "bold"))
    label_texto.grid(row=0, column=1, sticky="ne")

    # 4. Linha da Direita
    sep_direita = ttk.Separator(container, orient="horizontal")
    sep_direita.grid(row=0, column=2, sticky="ew", padx=(10, 0))

class BackupAgendado:
    def __init__(self, janela):
        ## Construção da janela
        self.janela = janela
        self.janela.title(f"Backup Agendado {version}")

        ## Painel da janela
        self.frame_controls = ttk.Frame(self.janela)
        self.frame_controls.grid(row=0, column=0, padx=espaco, pady=espaco, sticky="nsew")

        self.frame_andamento = ttk.Frame(self.janela)
        self.frame_andamento.grid(row=0, column=1, sticky="nsew")

        ## Controles do painel esquerdo
        self.lbl_selecao = ttk.Label(self.frame_controls, text="Selecionar Tarefa:", font=fonte)
        self.lbl_selecao.grid(row=0, column=0, padx=espaco, pady=espaco, sticky="nsew")

        self.cmb_selecao = ttk.Combobox(self.frame_controls, font=fonte, state="readonly")
        self.cmb_selecao.grid(row=0, column=1, padx=espaco, pady=espaco, sticky="nsew")

        self.lbl_horario = ttk.Label(self.frame_controls, text="Horário:", font=fonte)
        self.lbl_horario.grid(row=1, column=0, padx=espaco, pady=espaco, sticky="nsew")

        self.lbl_hora_execucao = ttk.Label(self.frame_controls, text="--:--", font=fonte, anchor="center")
        self.lbl_hora_execucao.grid(row=1, column=1, padx=espaco, pady=espaco, sticky="nsew")

        self.btn_executar = ttk.Button(self.frame_controls, text="Executar Tarefa", command="")
        self.btn_executar.grid(row=2, columnspan=2, padx=espaco, pady=espaco, sticky="nsew")

        self.btn_cancelar = ttk.Button(self.frame_controls, text="Cancelar Tarefa", command="")
        self.btn_cancelar.grid(row=3, columnspan=2, padx=espaco, pady=espaco, sticky="nsew")
        self.btn_cancelar.config(state="disabled")

        self.lbl_tamanho = ttk.Label(self.frame_controls, text="Tamanho:", font=fonte, anchor="w")
        self.lbl_tamanho.grid(row=4, column=0, padx=espaco, pady=espaco, sticky="nsew")

        self.lbl_tamanho_exibir = ttk.Label(self.frame_controls, text=(10*"-"), font=fonte, anchor="e")
        self.lbl_tamanho_exibir.grid(row=4, column=1, padx=espaco, pady=espaco, sticky="nsew")

        # Definindo suas variáveis de espaçamento
        espacox = espaco
        espacoy = 15

        # Usando o separador customizado
        criar_separador_com_texto(self.frame_controls, "EM EXECUÇÃO", linha=5, espacox=espacox, espacoy=espacoy)

        self.moldura_borda = ttk.Frame(self.frame_controls, relief="solid", borderwidth=1, padding=10)
        self.moldura_borda.grid(row=6, rowspan=5, columnspan=2, padx=espaco, pady=espaco, sticky="nsew")

        # Texto de exemplo
        texto_longo = (
            "Status do Sistema:\n"
            "- Backup da pasta 'Trabalho' concluído.\n"
            "- Erro ao acessar a unidade E:/ (Dispositivo desconectado).\n"
            "- Próxima verificação agendada para às 20:00."
        )

        self.lbl_multi = ttk.Label(
            self.moldura_borda,
            text=texto_longo,
            justify="left",
            wraplength=350,
            font=fonte
        )
        self.lbl_multi.pack(anchor="w")

        self.btn_encerrar = ttk.Button(self.frame_controls, text="Encerrar Tarefa", command="")
        self.btn_encerrar.grid(row=(7 + 5), columnspan=2, padx=espacox, pady=espacox, sticky="nsew")

        ## Controles do painel direito

if __name__ == "__main__":
    root = tk.Tk()
    app = BackupAgendado(root)
    root.mainloop()