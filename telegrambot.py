from telegram import Bot
import asyncio

def enviar_arquivo(token, chat_id, caminho):
    #return

    # Token do seu bot (fornecido pelo BotFather)
    #TOKEN = token

    # ID do chat (pode ser seu próprio ID ou de um grupo/canal)
    #CHAT_ID = chat_id

    # Caminho do arquivo .zip
    #FILE_PATH = caminho

    # Criar instância do bot
    async def enviar_xmls():
        bot = Bot(token=token)
        with open(caminho, "rb") as f:
            await bot.send_document(chat_id=chat_id, document=f)

    asyncio.run(enviar_xmls())
    #metodos.log_mensagem("Ativar envio do arquivo")

def enviar_mensagem(token, chat_id, mensagem):
    #return
    # Criar instância do bot
    async def enviar_texto():
        bot = Bot(token=token)
        await bot.send_message(chat_id=chat_id, text=mensagem)

    asyncio.run(enviar_texto())
