import customtkinter
#import CTkMessagebox.ctkmessagebox as ctk_mb
from CTkMessagebox import CTkMessagebox

# Monkey Patch: Força o CTkButton do CTkMessagebox a aceitar height como int
_original_button_init = customtkinter.CTkButton.__init__

def _patched_button_init(self, *args, **kwargs):
    if "height" in kwargs and isinstance(kwargs["height"], float):
        kwargs["height"] = int(kwargs["height"])
    if "width" in kwargs and isinstance(kwargs["width"], float):
        kwargs["width"] = int(kwargs["width"])
    _original_button_init(self, *args, **kwargs)

# Aplica a correção de tipagem do X11 em tempo de execução
customtkinter.CTkButton.__init__ = _patched_button_init


def ok_cancel(titulo, mensagem, master=None):
    msg = CTkMessagebox(
        master=master,
        title=titulo,
        message=mensagem,
        icon="cancel",
        option_1="OK",
        option_2="Cancelar"
    )
    # Se uma janela pai foi passada, centraliza o messagebox sobre ela
    if master:
        posicionar(msg, master)
    return msg.get()

def sim_nao(titulo, mensagem, master=None):
    msg = CTkMessagebox(
        master=master,
        title=titulo,
        message=mensagem,
        icon="question",
        option_1="Não",
        option_2="Sim"
    )

    if master:
        posicionar(msg, master)

    return msg.get()

def info(titulo, mensagem, master=None):
    msg = CTkMessagebox(master=master, title=titulo, message=mensagem, icon="info")
    if master:
        posicionar(msg, master)
    return msg.get()

def cuidado(titulo, mensagem, master=None):
    msg = CTkMessagebox(master=master, title=titulo, message=mensagem, icon="warning")
    if master:
        posicionar(msg, master)
    return msg.get()

def erro(titulo, mensagem, master=None):
    msg = CTkMessagebox(master=master, title=titulo, message=mensagem, icon="cancel")
    if master:
        posicionar(msg, master)
    return msg.get()

def posicionar(msg, master):
    # 1. Oculta imediatamente o renderizador para não piscar na tela
    msg.attributes("-alpha", 0.0)

    # 2. Posiciona antes de exibir
    _posicionar_sem_flicker(msg, master)

    # 3. Exibe já no lugar correto
    msg.attributes("-alpha", 1.0)

def _posicionar_sem_flicker(janela_child, parent):
    """Calcula e move a janela de forma síncrona enquanto ela está transparente."""
    if not parent or not parent.winfo_exists() or not janela_child.winfo_exists():
        return

    # Dimensões do pai
    p_width = parent.winfo_width()
    p_height = parent.winfo_height()
    p_x = parent.winfo_rootx()
    p_y = parent.winfo_rooty()

    # Pega a dimensão do filho (se ainda não calculou, usa o tamanho padrão fixo)
    c_width = janela_child.winfo_width()
    c_height = janela_child.winfo_height()

    if c_width <= 1 or c_height <= 1:
        c_width, c_height = 400, 200

    # Coordenadas do centro
    x = p_x + (p_width // 2) - (c_width // 2)
    y = p_y + (p_height // 2) - (c_height // 2)

    # Aplica a posição exata
    janela_child.geometry(f"{c_width}x{c_height}+{x}+{y}")