import tkinter as tk
import platform

import customtkinter as ctk

import barra_menu
import estilo
from menu_hamburguer import MenuHamburguer

sistema = platform.system()

## Inicio do Programa
class JanelaPrincipal:
    def __init__(self, janela_principal):
        ## Construção da janela
        self.janela_principal = janela_principal
        self.janela_principal.overrideredirect(True)
        if sistema == "Linux" or sistema == "Linux2":
            self.janela_principal.withdraw()
        self.janela_principal.title(f"{estilo.NOME_PROGRAMA} {estilo.VERSION}")
        self.janela_principal.resizable(width=False, height=False)

        self.nome_janela = "janela-principal"  # <-- Identificador para o controlador
        self.controles = {}

        self._criar_layout()
        barra_menu.criar_barra_menu(self, f"{estilo.NOME_PROGRAMA} {estilo.VERSION}", 'janela_principal', False)

        # --- CORREÇÃO PARA FORÇAR A EXIBIÇÃO NO WINDOWS ---
        self.janela_principal.update_idletasks()
        self.janela_principal.deiconify()  # Restaura a janela na tela
        self.janela_principal.lift()  # Traz para a frente de outras janelas
        self.janela_principal.focus_force()  # Força o foco no Windows

    def _criar_layout(self):
        self.controles['janela_principal'] = self.janela_principal

        ## Painel da janela
        self.frame_controls = ctk.CTkFrame(self.janela_principal)
        self.frame_controls.grid(row=1, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.controles['frame_controls'] = self.frame_controls

        self.frame_andamento = ctk.CTkFrame(self.janela_principal)
        self.frame_andamento.grid(row=1, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")

        ## Controles do painel esquerdo
        self.lbl_selecao = ctk.CTkLabel(self.frame_controls, text="Selecionar Tarefa:", font=estilo.FONTE_VAZIA)
        self.lbl_selecao.grid(row=estilo.LINHA_PAINEL_ESQUERDO, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")

        self.opt_selecao = ctk.CTkOptionMenu(self.frame_controls, font=estilo.FONTE_VAZIA)
        self.opt_selecao.grid(row=estilo.LINHA_PAINEL_ESQUERDO, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.controles['opt_selecao'] = self.opt_selecao
        estilo.LINHA_PAINEL_ESQUERDO += 1

        self.lbl_horario = ctk.CTkLabel(self.frame_controls, text="Horário:", font=estilo.FONTE_VAZIA)
        self.lbl_horario.grid(row=estilo.LINHA_PAINEL_ESQUERDO, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")

        self.lbl_hora_execucao = ctk.CTkLabel(self.frame_controls, text="--:--", font=estilo.FONTE_VAZIA, anchor="center")
        self.lbl_hora_execucao.grid(row=estilo.LINHA_PAINEL_ESQUERDO, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.controles['lbl_hora_execucao'] = self.lbl_hora_execucao
        estilo.LINHA_PAINEL_ESQUERDO += 1
        linha_estendida_moldura_andamento = estilo.LINHA_PAINEL_ESQUERDO

        self.lbl_tamanho = ctk.CTkLabel(self.frame_controls, text="Tamanho:", font=estilo.FONTE_VAZIA, anchor="w")
        self.lbl_tamanho.grid(row=estilo.LINHA_PAINEL_ESQUERDO, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO,
                              sticky="nsew")

        self.lbl_tamanho_exibir = ctk.CTkLabel(self.frame_controls, text=(10 * "-"), font=estilo.FONTE_VAZIA, anchor="center")
        self.lbl_tamanho_exibir.grid(row=estilo.LINHA_PAINEL_ESQUERDO, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO,
                                     sticky="nsew")
        self.controles['lbl_tamanho_exibir'] = self.lbl_tamanho_exibir
        estilo.LINHA_PAINEL_ESQUERDO += 1

        self.btn_executar = ctk.CTkButton(self.frame_controls, text="Executar Tarefa", command="")
        self.btn_executar.grid(row=estilo.LINHA_PAINEL_ESQUERDO, columnspan=2, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.controles['btn_executar'] = self.btn_executar
        estilo.LINHA_PAINEL_ESQUERDO += 1

        self.btn_pausar = ctk.CTkButton(self.frame_controls, text="Pausar Tarefa", command="")
        self.btn_pausar.grid(row=estilo.LINHA_PAINEL_ESQUERDO, columnspan=2, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.btn_pausar.configure(state="disabled")
        self.controles['btn_pausar'] = self.btn_pausar
        estilo.LINHA_PAINEL_ESQUERDO += 1
        self.controles['linha_painel_esquerdo'] = estilo.LINHA_PAINEL_ESQUERDO

        # Usando o separador customizado
        estilo.LINHA_PAINEL_ESQUERDO += 1
        linha_estendida_moldura_execucao = 5
        self.frame_controls.rowconfigure(estilo.LINHA_PAINEL_ESQUERDO, weight=0)
        self.moldura_execucao_borda = ctk.CTkFrame(self.frame_controls, height=110)
        self.moldura_execucao_borda.grid(row=estilo.LINHA_PAINEL_ESQUERDO, rowspan=linha_estendida_moldura_execucao, columnspan=2,
                                         padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="ew")
        self.moldura_execucao_borda.grid_propagate(False)
        self.moldura_execucao_borda.pack_propagate(False)
        estilo.LINHA_PAINEL_ESQUERDO += 1 + linha_estendida_moldura_execucao

        self.frame_controls.update_idletasks()
        largura_moldura = self.moldura_execucao_borda.winfo_width()

        self.lbl_multi_execucao = ctk.CTkLabel(
            self.moldura_execucao_borda,
            text="",
            justify="left",
            wraplength=largura_moldura - 10 * 2,
            font=estilo.FONTE_VAZIA
        )
        self.lbl_multi_execucao.pack(anchor="w", padx=(10, 4), pady=(10, 4))
        self.controles['lbl_multi_execucao'] = self.lbl_multi_execucao

        self.btn_encerrar = ctk.CTkButton(self.frame_controls, text="Encerrar Tarefa", command="")
        self.btn_encerrar.grid(row=estilo.LINHA_PAINEL_ESQUERDO, columnspan=2, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.controles['btn_encerrar'] = self.btn_encerrar

        ## Controles do painel direito
        linha_painel_direito = 0

        self.frame_andamento.rowconfigure(linha_painel_direito, weight=0)
        self.frame_andamento.columnconfigure(linha_painel_direito, weight=1)

        self.moldura_andamento_atual = ctk.CTkFrame(self.frame_andamento, height=360)
        self.moldura_andamento_atual.grid(row=linha_painel_direito, rowspan=linha_estendida_moldura_andamento,
                                          column=0, columnspan=3, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="ew")
        self.moldura_andamento_atual.grid_propagate(False)
        self.moldura_andamento_atual.pack_propagate(False)
        linha_painel_direito += linha_estendida_moldura_andamento

        self.lbl_multi_andamento = ctk.CTkLabel(
            self.moldura_andamento_atual,
            text="",
            justify="left",
            wraplength=500,
            font=estilo.FONTE_VAZIA
        )
        self.lbl_multi_andamento.pack(anchor="w", padx=(10, 4), pady=(10, 4))
        self.controles['lbl_multi_andamento'] = self.lbl_multi_andamento

        self.lbl_copiado = ctk.CTkLabel(self.frame_andamento, text="Copiado:", justify="left", font=estilo.FONTE_VAZIA)
        self.lbl_copiado.grid(row=linha_painel_direito, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")

        self.lbl_copiado_tamanho = ctk.CTkLabel(self.frame_andamento, text=(10*"-"), justify="center", font=estilo.FONTE_VAZIA)
        self.lbl_copiado_tamanho.grid(row=linha_painel_direito, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.controles['lbl_copiado_tamanho'] = self.lbl_copiado_tamanho

        # 1. Cria a barra de progresso normalmente
        self.progress_bar = ctk.CTkProgressBar(self.frame_andamento, width=500, height=26)
        self.progress_bar.grid(row=linha_painel_direito, column=2, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="e")
        self.progress_bar.set(0)

        # 2. Cria o texto DIRETAMENTE dentro do Canvas interno do CTkProgressBar
        # Isso garante transparência real sem o retângulo cinza recortando a barra
        self.texto_progresso_id = self.progress_bar._canvas.create_text(
            0, 0,
            text="0.000%",
            fill="white",
            font=("Helvetica", 11, "bold")
        )

        # Function interna para manter o texto sempre centralizado quando a barra redimensionar
        def _centralizar_texto_progresso(event):
            largura = event.width
            altura = event.height
            self.progress_bar._canvas.coords(self.texto_progresso_id, largura / 2, altura / 2)
            # Garante que o texto fique sempre acima da camada do progresso
            self.progress_bar._canvas.tag_raise(self.texto_progresso_id)

        self.progress_bar._canvas.bind("<Configure>", _centralizar_texto_progresso)

        # Registra as referências
        self.controles['progress_bar'] = self.progress_bar
        self.controles['lbl_porcentagem'] = self.texto_progresso_id  # Guarda o ID do texto