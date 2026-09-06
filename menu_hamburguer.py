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
        self.estados = {}

    def adicionar_item(self, texto, comando, estado="normal"):
        """Adiciona um item simples que executa um comando."""
        self.itens.append({"tipo": "item", "texto": texto, "comando": comando})
        self.estados[texto] = estado

    def alterar_estado_item(self, texto, estado):
        """Altera o estado de um item para 'normal' ou 'disabled'."""
        self.estados[texto] = estado
        if self.popup and self.popup.winfo_exists():
            for child in self.popup.winfo_children():
                if isinstance(child, ctk.CTkButton) and child.cget("text") == texto:
                    child.configure(state=estado)

    def adicionar_submenu(self, texto):
        """Cria e retorna uma instância de Submenu vinculada a este item."""
        submenu = Submenu(texto)
        self.itens.append({"tipo": "submenu", "texto": texto, "objeto": submenu})
        return submenu

    def _toggle_popup(self):
        if self.popup and self.popup.winfo_exists():
            self._destruir_popups()
            return

        # Pega a janela principal raiz para desenhar o menu por cima de tudo
        root_window = self.winfo_toplevel()

        # Calcula a posição relativa do botão em relação à janela principal
        bx = self.winfo_rootx() - root_window.winfo_rootx()
        by = self.winfo_rooty() - root_window.winfo_rooty() + self.winfo_height() + 2
        largura_popup = max(160, self.winfo_width())

        # Cria um CTkFrame interno no lugar do CTkToplevel
        self.popup = ctk.CTkFrame(
            root_window,
            width=largura_popup,
            height=len(self.itens) * 35,
            corner_radius=6,
            border_width=1,
            border_color=("gray70", "gray30")
        )
        self.popup.place(x=bx, y=by)
        self.popup.lift()  # Traz para a frente de todos os widgets na mesma janela

        for item in self.itens:
            if item["tipo"] == "item":
                estado_atual = self.estados.get(item["texto"], "normal")
                btn = ctk.CTkButton(
                    self.popup,
                    text=item["texto"],
                    height=30,
                    anchor="w",
                    fg_color="transparent",
                    text_color=("gray10", "gray90"),
                    hover_color=("gray70", "gray30"),
                    state=estado_atual,
                    command=lambda cmd=item["comando"]: self._executar_acao(cmd)
                )
                btn.bind("<Enter>", lambda e: self._fechar_active_submenu())
                btn.pack(fill="x", padx=4, pady=2)

            elif item["tipo"] == "submenu":
                btn = ctk.CTkButton(
                    self.popup,
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

        root_window.bind("<Button-1>", self._check_click_outside, add="+")

    def _abrir_submenu_lateral(self, btn_widget, submenu_obj):
        self._fechar_active_submenu()

        root_window = self.winfo_toplevel()

        # Posicionamento relativo ao item pai
        sx = btn_widget.winfo_rootx() - root_window.winfo_rootx() + btn_widget.winfo_width() + 4
        sy = btn_widget.winfo_rooty() - root_window.winfo_rooty()

        largura_sub = 180
        altura_sub = len(submenu_obj.itens) * 35

        # Submenu também é um CTkFrame flutuante interno
        sub_popup = ctk.CTkFrame(
            root_window,
            width=largura_sub,
            height=altura_sub,
            corner_radius=6,
            border_width=1,
            border_color=("gray70", "gray30")
        )
        sub_popup.place(x=sx, y=sy)
        sub_popup.lift()

        for sub_item in submenu_obj.itens:
            b = ctk.CTkButton(
                sub_popup,
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
            self.active_submenu_popup.place_forget()
            self.active_submenu_popup.destroy()
            self.active_submenu_popup = None

    def _destruir_popups(self):
        self._fechar_active_submenu()
        if self.popup and self.popup.winfo_exists():
            self.popup.place_forget()
            self.popup.destroy()
            self.popup = None

    def _executar_acao(self, comando):
        self._destruir_popups()
        if comando:
            comando()

    def _check_click_outside(self, event):
        if self.popup and self.popup.winfo_exists():
            px, py = self.popup.winfo_rootx(), self.popup.winfo_rooty()
            pw, ph = self.popup.winfo_width(), self.popup.winfo_height()

            fora_menu_principal = not (px <= event.x_root <= px + pw and py <= event.y_root <= py + ph)
            fora_submenu = True

            if self.active_submenu_popup and self.active_submenu_popup.winfo_exists():
                sx, sy = self.active_submenu_popup.winfo_rootx(), self.active_submenu_popup.winfo_rooty()
                sw, sh = self.active_submenu_popup.winfo_width(), self.active_submenu_popup.winfo_height()
                fora_submenu = not (sx <= event.x_root <= sx + sw and sy <= event.y_root <= sy + sh)

            # Verifica se o clique não foi no próprio botão hambúrguer
            if fora_menu_principal and fora_submenu and event.widget != self:
                self._destruir_popups()


class Submenu:
    def __init__(self, titulo):
        self.titulo = titulo
        self.itens = []

    def add_command(self, label, command):
        """Interface idêntica ao tk.Menu para registrar opções."""
        self.itens.append({"texto": label, "comando": command})