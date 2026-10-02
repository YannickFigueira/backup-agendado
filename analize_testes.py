import sys
from PyQt6.QtWidgets import QApplication
from relatorios import GerenciadorRelatorio

if __name__ == "__main__":
    # 1. Cria a instância do QApplication (necessária para eventos do Qt)
    app = QApplication(sys.argv)

    # 2. Instancia o gerenciador
    gerenciador = GerenciadorRelatorio()


    # 3. Conecta o término do último worker para fechar a aplicação com segurança
    # Quando a compactação/envio finalizar, fecha o loop do Qt
    def ao_finalizar_tudo():
        print("Envio de relatório concluído com sucesso!")
        app.quit()


    # Sobrescrevemos ou conectamos ao fim do processo
    gerenciador._ao_concluir_compactacao_original = gerenciador._ao_concluir_compactacao


    def wrapper_conclusao():
        gerenciador._ao_concluir_compactacao_original()
        ao_finalizar_tudo()


    gerenciador._ao_concluir_compactacao = wrapper_conclusao

    print("Disparando envio de teste...")
    gerenciador.iniciar_processo()

    # 4. Mantém o loop de eventos ativo aguardando a thread terminar
    sys.exit(app.exec())