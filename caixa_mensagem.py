from CTkMessagebox import CTkMessagebox

def info(titulo, mensagem):
    # Equivalente ao messagebox.showinfo
    CTkMessagebox(
        title=titulo,
        message=mensagem,
        icon="info"
    )

def cuidado(titulo, mensagem):
    # Equivalente ao messagebox.showwarning
    CTkMessagebox(
        title=titulo,
        message=mensagem,
        icon="warning"
    )

def erro(titulo, mensagem):
    # Equivalente ao messagebox.showinfo
    CTkMessagebox(
        title=titulo,
        message=mensagem,
        icon="cancel"
    )

def sim_nao(titulo, mensagem):
    # Cria a caixa de diálogo estilizada
    msg = CTkMessagebox(
        title=titulo,
        message=mensagem,
        icon="question",
        option_1="Não",
        option_2="Sim"
    )

    return msg.get()