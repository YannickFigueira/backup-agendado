from tkinter import filedialog


def selecionar_pasta():
    pasta = filedialog.askdirectory(title="Selecione uma pasta")
    if pasta:  # se o usuário não cancelar
        return pasta
    else:
        return ""

class Controles:
    def __init__(self, view):
        self.view = view

        # O controlador se adapta automaticamente baseando-se em qual janela o chamou
        if hasattr(view, 'nome_janela'):
            if view.nome_janela == "configuracao":
                self._vincular_configuracoes()
            elif view.nome_janela == "nova_tarefa":
                self._vincular_nova_tarefa()


    # --- LÓGICA DA JANELA PRINCIPAL ---


    # --- LÓGICA DA JANELA DE NOVA TAREFA ---
    def _vincular_nova_tarefa(self):
        self.view.controles['btn_selecionar_origem'].config(command=lambda: self.selecionar_origem())
        self.view.controles['btn_selecionar_destino'].config(command=lambda: self.selecionar_destino())

    # Ações da janela
    def selecionar_origem(self):
        self.view.controles['txt_origem'].delete(0, "end")
        self.view.controles['txt_origem'].insert(0, selecionar_pasta())

    def selecionar_destino(self):
        self.view.controles['txt_destino'].delete(0, "end")
        self.view.controles['txt_destino'].insert(0, selecionar_pasta())

    # --- LÓGICA DA JANELA DE CONFIGURAÇÕES ---
    def _vincular_configuracoes(self):
        # Vincula o clique do botão da janela à função correspondente
        self.view.controles['btn_salvar'].config(command=self.salvar_configuracoes)