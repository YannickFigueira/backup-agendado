import customtkinter as ctk


class MenuHamburguer(ctk.CTkButton):
    def __init__(self, master, width=40, height=32, **kwargs):
        super().__init__(
            master,
            text="☰",
            width=width,
            height=height,
            command=self._toggle_popup,
            **kwargs
        )
        self.itens = []
        self.popup = None
        self.active_submenu_popup = None
        # Dicionário para guardar as referências de estado dos itens
        self.estados = {}

    def adicionar_item(self, texto, comando, estado="normal"):
        """Adiciona um item simples que executa um comando."""
        self.itens.append({"tipo": "item", "texto": texto, "comando": comando})
        self.estados[texto] = estado

    def alterar_estado_item(self, texto, estado):
        """Altera o estado de um item para 'normal' ou 'disabled'."""
        self.estados[texto] = estado
        # Se o pop-up estiver aberto no momento, atualiza a interface imediatamente
        if self.popup and self.popup.winfo_exists():
            for child in self.popup.winfo_children():
                for btn in child.winfo_children():
                    if isinstance(btn, ctk.CTkButton) and btn.cget("text") == texto:
                        btn.configure(state=estado)

    def adicionar_submenu(self, texto):
        """Cria e retorna uma instância de Submenu vinculada a este item."""
        submenu = Submenu(texto)
        self.itens.append({"tipo": "submenu", "texto": texto, "objeto": submenu})
        return submenu

    def _toggle_popup(self):
        if self.popup and self.popup.winfo_exists():
            self._destruir_popups()
            return

        self.popup = ctk.CTkToplevel(self)
        self.popup.overrideredirect(True)
        self.popup.attributes("-topmost", True)

        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height() + 2
        largura_popup = max(160, self.winfo_width())

        self.popup.geometry(f"{largura_popup}x{len(self.itens) * 35}+{x}+{y}")

        frame_itens = ctk.CTkFrame(self.popup, corner_radius=6)
        frame_itens.pack(fill="both", expand=True)

        for item in self.itens:
            if item["tipo"] == "item":
                estado_atual = self.estados.get(item["texto"], "normal")
                btn = ctk.CTkButton(
                    frame_itens,
                    text=item["texto"],
                    height=30,
                    anchor="w",
                    fg_color="transparent",
                    text_color=("gray10", "gray90"),
                    hover_color=("gray70", "gray30"),
                    state=estado_atual,  # Aplica o estado registrado
                    command=lambda cmd=item["comando"]: self._executar_acao(cmd)
                )
                btn.bind("<Enter>", lambda e: self._fechar_active_submenu())
                btn.pack(fill="x", padx=4, pady=2)

            elif item["tipo"] == "submenu":
                btn = ctk.CTkButton(
                    frame_itens,
                    text=f"{item['texto']}  ▶",
                    height=30,
                    anchor="w",
                    fg_color="transparent",
                    text_color=("gray10", "gray90"),
                    hover_color=("gray70", "gray30")
                )
                sub_obj = item["objeto"]
                btn.configure(command=lambda b=btn, s=sub_obj: self._abrir_submenu_lateral(b, s))
                btn.bind("<Enter>", lambda e, b=btn, s=sub_obj: self._abrir_submenu_lateral(b, s))
                btn.pack(fill="x", padx=4, pady=2)

        self.winfo_toplevel().bind("<Button-1>", self._check_click_outside, add="+")

    def _abrir_submenu_lateral(self, btn_widget, submenu_obj):
        self._fechar_active_submenu()

        # Janela do submenu lateral
        sub_popup = ctk.CTkToplevel(self.popup)
        sub_popup.overrideredirect(True)
        sub_popup.attributes("-topmost", True)

        # Posiciona à direita do item correspondente
        x = btn_widget.winfo_rootx() + btn_widget.winfo_width() + 4
        y = btn_widget.winfo_rooty()

        largura_sub = 180
        altura_sub = len(submenu_obj.itens) * 35
        sub_popup.geometry(f"{largura_sub}x{altura_sub}+{x}+{y}")

        frame_sub = ctk.CTkFrame(sub_popup, corner_radius=6)
        frame_sub.pack(fill="both", expand=True)

        for sub_item in submenu_obj.itens:
            b = ctk.CTkButton(
                frame_sub,
                text=sub_item["texto"],
                height=30,
                anchor="w",
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                command=lambda cmd=sub_item["comando"]: self._executar_acao(cmd)
            )
            b.pack(fill="x", padx=4, pady=2)

        self.active_submenu_popup = sub_popup

    def _fechar_active_submenu(self):
        if self.active_submenu_popup and self.active_submenu_popup.winfo_exists():
            self.active_submenu_popup.destroy()
            self.active_submenu_popup = None

    def _destruir_popups(self):
        self._fechar_active_submenu()
        if self.popup and self.popup.winfo_exists():
            self.popup.destroy()
            self.popup = None

    def _executar_acao(self, comando):
        self._destruir_popups()
        if comando:
            comando()

    def _check_click_outside(self, event):
        if self.popup and self.popup.winfo_exists():
            # Coordenadas do menu principal
            px, py = self.popup.winfo_rootx(), self.popup.winfo_rooty()
            pw, ph = self.popup.winfo_width(), self.popup.winfo_height()

            fora_menu_principal = not (px <= event.x_root <= px + pw and py <= event.y_root <= py + ph)
            fora_submenu = True

            # Coordenadas do submenu lateral
            if self.active_submenu_popup and self.active_submenu_popup.winfo_exists():
                sx, sy = self.active_submenu_popup.winfo_rootx(), self.active_submenu_popup.winfo_rooty()
                sw, sh = self.active_submenu_popup.winfo_width(), self.active_submenu_popup.winfo_height()
                fora_submenu = not (sx <= event.x_root <= sx + sw and sy <= event.y_root <= sy + sh)

            if fora_menu_principal and fora_submenu and event.widget != self:
                self._destruir_popups()


class Submenu:
    def __init__(self, titulo):
        self.titulo = titulo
        self.itens = []

    def add_command(self, label, command):
        """Interface idêntica ao tk.Menu para registrar opções."""
        self.itens.append({"texto": label, "comando": command})
