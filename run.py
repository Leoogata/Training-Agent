import threading
from app import create_app
from app.bot_service import bot

# Cria a instância do aplicativo Flask
app = create_app()

def run_bot():
    """Roda o bot Telegram em uma thread separada"""
    print("🤖 Bot iniciado!")
    bot.infinity_polling()

if __name__ == "__main__":
    # Inicia o bot em background
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    # Inicia o servidor Flask
    # No Render, a porta é definida pela variável PORT
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
