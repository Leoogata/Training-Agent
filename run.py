import threading
from app import create_app
from app.bot_service import bot, set_flask_app

# Cria a instância única do aplicativo Flask
app = create_app()

def run_bot():
    """Roda o bot Telegram em uma thread separada"""
    print("🤖 Bot iniciado!")
    # Passa a instância do app para o serviço do bot
    set_flask_app(app)
    # Tenta remover o webhook caso tenha sido configurado por engano
    bot.remove_webhook()
    bot.infinity_polling()

if __name__ == "__main__":
    # Inicia o bot em background apenas se for o processo principal
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    # Inicia o servidor Flask
    import os
    port = int(os.environ.get('PORT', 5000))
    # debug=False é CRUCIAL para não iniciar o bot duas vezes
    app.run(host='0.0.0.0', port=port, debug=False)
