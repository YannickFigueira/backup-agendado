import customtkinter as ctk

class TimeSelector(ctk.CTkButton):
    def __init__(self, master, values, initial_value="00", width=70, height=32, **kwargs):
        super().__init__(
            master,
            text=str(initial_value),
            width=width,
            height=height,
            command=self._toggle_popup,
            **kwargs
        )
        self.values = values
        self.set(initial_value)
        self.popup = None

    def _toggle_popup(self):
        if self.popup and self.popup.winfo_exists():
            self.popup.destroy()
            return

        self.popup = ctk.CTkToplevel(self)
        self.popup.overrideredirect(True)
        self.popup.attributes("-topmost", True)

        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height() + 2
        self.popup.geometry(f"{self.winfo_width()}x180+{x}+{y}")

        scroll_frame = ctk.CTkScrollableFrame(self.popup, width=self.winfo_width() - 15)
        scroll_frame.pack(fill="both", expand=True)

        for val in self.values:
            btn = ctk.CTkButton(
                scroll_frame,
                text=val,
                height=28,
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                command=lambda v=val: self._select_value(v)
            )
            btn.pack(fill="x", pady=1)

        # Monitora cliques globais na janela principal
        self.winfo_toplevel().bind("<Button-1>", self._check_click_outside, add="+")

    def _check_click_outside(self, event):
        if self.popup and self.popup.winfo_exists():
            # Captura as coordenadas do pop-up na tela
            px = self.popup.winfo_rootx()
            py = self.popup.winfo_rooty()
            pw = self.popup.winfo_width()
            ph = self.popup.winfo_height()

            # Se o clique ocorreu fora da caixa do pop-up e fora do botão acionador
            if not (px <= event.x_root <= px + pw and py <= event.y_root <= py + ph):
                if event.widget != self:
                    self.popup.destroy()

    def _select_value(self, value):
        self.selected_value = value
        self.configure(text=value)
        if self.popup:
            self.popup.destroy()

    def set(self, value):
        """
        Atualiza o valor do seletor. Aceita números (int) ou strings (ex: 5, "5", "05").
        """
        try:
            # Formata inteiros para 2 dígitos (ex: 5 -> "05")
            val_str = f"{int(value):02d}"
        except (ValueError, TypeError):
            val_str = str(value)

        self.selected_value = val_str
        self.configure(text=val_str)

    def get(self):
        return self.selected_value