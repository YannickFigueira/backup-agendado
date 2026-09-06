import customtkinter as ctk

import estilo
from menu_hamburguer import MenuHamburguer


## Carregar Menus
# criar_barra_menu(view.janela_principal, view.lbl_multi_andamento)
def criar_barra_menu(view, titulo, janela, desativar):
    view.frame_titulo = ctk.CTkFrame(view.controles[janela])
    view.frame_titulo.grid(row=0, columnspan=2, padx=10, pady=10, sticky="we")
    view.controles['frame_titulo'] = view.frame_titulo

    view.menu_btn = MenuHamburguer(view.frame_titulo, font=("Arial", 18))
    view.menu_btn.pack(side="left", padx=10, pady=10, anchor="nw")
    view.controles['menu_btn'] = view.menu_btn

    # Botão Fechar (Transparente com Hover Vermelho)
    view.btn_fechar = ctk.CTkButton(
        view.frame_titulo,
        text="X",
        font=("Arial", 18),
        width=30,
        fg_color="transparent",  # Fundo transparente por padrão
        hover_color="#c0392b",  # Vermelho no hover
        text_color=("gray10", "gray90")  # Mantém o texto visível em light/dark mode
    )
    view.btn_fechar.pack(side="right", padx=(2, 10), pady=10)

    if not desativar:
        # Botão Minimizar (Transparente com Hover Azul)
        view.btn_minimizar = ctk.CTkButton(
            view.frame_titulo,
            text="-",
            font=("Arial", 18),
            width=30,
            fg_color="transparent",  # Fundo transparente por padrão
            hover_color="#1f538d",  # Azul no hover
            text_color=("gray10", "gray90")
        )
        view.btn_minimizar.pack(side="right", padx=2, pady=10)
        view.controles['btn_minimizar'] = view.btn_minimizar

    view.lbl_titulo = ctk.CTkLabel(view.frame_titulo, text=titulo,
                                   font=("Arial", 18))
    view.lbl_titulo.pack(side="left", expand=True, fill="x", padx=10, pady=10)
    view.controles['btn_fechar'] = view.btn_fechar