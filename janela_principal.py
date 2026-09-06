import platform
import customtkinter as ctk
import barra_menu
import estilo

sistema = platform.system()

## Inicio do Programa
class JanelaPrincipal:
    def __init__(self, janela_principal):
        self.janela_principal = janela_principal

        # 1. Oculta a janela para renderizar o layout sem flickering/delay
        self.janela_principal.withdraw()

        # 2. Configurações de janela frameless e transient X11
        self.janela_principal.overrideredirect(True)

        if sistema in ["Linux", "Linux2"]:
            try:
                self.janela_principal.tk.call('wm', 'transient', self.janela_principal._w, '')
            except Exception:
                pass

        self.janela_principal.title(f"{estilo.NOME_PROGRAMA} {estilo.VERSION}")
        self.janela_principal.resizable(width=False, height=False)

        self.nome_janela = "janela-principal"
        self.controles = {}

        # 3. Monta todo o layout na memória
        self._criar_layout()
        barra_menu.criar_barra_menu(self, f"{estilo.NOME_PROGRAMA} {estilo.VERSION}", 'janela_principal', True)

        # 4. Exibe a janela totalmente carregada
        self.janela_principal.deiconify()
        self.janela_principal.lift()
        self.janela_principal.focus_force()

    def _criar_layout(self):
        self.controles['janela_principal'] = self.janela_principal

        ## Painel da janela
        self.frame_controls = ctk.CTkFrame(self.janela_principal)
        self.frame_controls.grid(row=1, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.controles['frame_controls'] = self.frame_controls

        self.frame_andamento = ctk.CTkFrame(self.janela_principal)
        self.frame_andamento.grid(row=1, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")

        ## Controles do painel esquerdo
        linha_esq = 0

        self.lbl_selecao = ctk.CTkLabel(self.frame_controls, text="Selecionar Tarefa:", font=estilo.FONTE_VAZIA)
        self.lbl_selecao.grid(row=linha_esq, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")

        self.opt_selecao = ctk.CTkOptionMenu(self.frame_controls, font=estilo.FONTE_VAZIA)
        self.opt_selecao.grid(row=linha_esq, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.controles['opt_selecao'] = self.opt_selecao
        linha_esq += 1

        self.lbl_horario = ctk.CTkLabel(self.frame_controls, text="Horário:", font=estilo.FONTE_VAZIA)
        self.lbl_horario.grid(row=linha_esq, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")

        self.lbl_hora_execucao = ctk.CTkLabel(self.frame_controls, text="--:--", font=estilo.FONTE_VAZIA, anchor="center")
        self.lbl_hora_execucao.grid(row=linha_esq, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.controles['lbl_hora_execucao'] = self.lbl_hora_execucao
        linha_esq += 1
        linha_estendida_moldura_andamento = linha_esq

        self.lbl_tamanho = ctk.CTkLabel(self.frame_controls, text="Tamanho:", font=estilo.FONTE_VAZIA, anchor="w")
        self.lbl_tamanho.grid(row=linha_esq, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")

        self.lbl_tamanho_exibir = ctk.CTkLabel(self.frame_controls, text=(10 * "-"), font=estilo.FONTE_VAZIA, anchor="center")
        self.lbl_tamanho_exibir.grid(row=linha_esq, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.controles['lbl_tamanho_exibir'] = self.lbl_tamanho_exibir
        linha_esq += 1

        self.btn_executar = ctk.CTkButton(self.frame_controls, text="Executar Tarefa", command="")
        self.btn_executar.grid(row=linha_esq, columnspan=2, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.controles['btn_executar'] = self.btn_executar
        linha_esq += 1

        self.btn_pausar = ctk.CTkButton(self.frame_controls, text="Pausar Tarefa", command="")
        self.btn_pausar.grid(row=linha_esq, columnspan=2, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.btn_pausar.configure(state="disabled")
        self.controles['btn_pausar'] = self.btn_pausar
        linha_esq += 1

        # REGISTRA A LINHA NECESSÁRIA PELO CONTROLADOR
        self.controles['linha_painel_esquerdo'] = linha_esq

        # Moldura de execução
        linha_esq += 1
        linha_estendida_moldura_execucao = 5
        self.frame_controls.rowconfigure(linha_esq, weight=0)
        self.moldura_execucao_borda = ctk.CTkFrame(self.frame_controls, height=110)
        self.moldura_execucao_borda.grid(
            row=linha_esq,
            rowspan=linha_estendida_moldura_execucao,
            columnspan=2,
            padx=estilo.ESPACO,
            pady=estilo.ESPACO,
            sticky="ew"
        )
        self.moldura_execucao_borda.grid_propagate(False)
        self.moldura_execucao_borda.pack_propagate(False)
        linha_esq += 1 + linha_estendida_moldura_execucao

        self.lbl_multi_execucao = ctk.CTkLabel(
            self.moldura_execucao_borda,
            text="",
            justify="left",
            wraplength=250,
            font=estilo.FONTE_VAZIA
        )
        self.lbl_multi_execucao.pack(anchor="w", padx=(10, 4), pady=(10, 4))
        self.controles['lbl_multi_execucao'] = self.lbl_multi_execucao

        self.btn_encerrar = ctk.CTkButton(self.frame_controls, text="Encerrar Tarefa", command="")
        self.btn_encerrar.grid(row=linha_esq, columnspan=2, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.controles['btn_encerrar'] = self.btn_encerrar

        ## Controles do painel direito
        linha_dir = 0
        self.frame_andamento.rowconfigure(linha_dir, weight=0)
        self.frame_andamento.columnconfigure(linha_dir, weight=1)

        self.moldura_andamento_atual = ctk.CTkFrame(self.frame_andamento, height=360)
        self.moldura_andamento_atual.grid(
            row=linha_dir,
            rowspan=linha_estendida_moldura_andamento,
            column=0,
            columnspan=3,
            padx=estilo.ESPACO,
            pady=estilo.ESPACO,
            sticky="ew"
        )
        self.moldura_andamento_atual.grid_propagate(False)
        self.moldura_andamento_atual.pack_propagate(False)
        linha_dir += linha_estendida_moldura_andamento

        self.lbl_multi_andamento = ctk.CTkLabel(
            self.moldura_andamento_atual,
            text="",
            justify="left",
            wraplength=480,
            font=estilo.FONTE_VAZIA
        )
        self.lbl_multi_andamento.pack(anchor="w", padx=(10, 4), pady=(10, 4))
        self.controles['lbl_multi_andamento'] = self.lbl_multi_andamento

        self.lbl_copiado = ctk.CTkLabel(self.frame_andamento, text="Copiado:", justify="left", font=estilo.FONTE_VAZIA)
        self.lbl_copiado.grid(row=linha_dir, column=0, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")

        self.lbl_copiado_tamanho = ctk.CTkLabel(self.frame_andamento, text=(10 * "-"), justify="center", font=estilo.FONTE_VAZIA)
        self.lbl_copiado_tamanho.grid(row=linha_dir, column=1, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="nsew")
        self.controles['lbl_copiado_tamanho'] = self.lbl_copiado_tamanho

        # Barra de progresso
        self.progress_bar = ctk.CTkProgressBar(self.frame_andamento, width=500, height=26)
        self.progress_bar.grid(row=linha_dir, column=2, padx=estilo.ESPACO, pady=estilo.ESPACO, sticky="e")
        self.progress_bar.set(0)

        self.texto_progresso_id = self.progress_bar._canvas.create_text(
            250, 13,
            text="0.000%",
            fill="white",
            font=("Helvetica", 11, "bold")
        )

        def _centralizar_texto_progresso(event):
            self.progress_bar._canvas.coords(self.texto_progresso_id, event.width / 2, event.height / 2)
            self.progress_bar._canvas.tag_raise(self.texto_progresso_id)

        self.progress_bar._canvas.bind("<Configure>", _centralizar_texto_progresso)

        self.controles['progress_bar'] = self.progress_bar
        self.controles['lbl_porcentagem'] = self.texto_progresso_id