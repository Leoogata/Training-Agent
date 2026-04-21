import sys
import os

# Adiciona o diretório raiz ao path do Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.bot_service import bot, set_flask_app

if __name__ == "__main__":
    # Esta é uma forma alternativa de rodar o bot sozinho sem o servidor Flask
    app = create_app()
    set_flask_app(app)
    print("🤖 Iniciando bot standalone (sem servidor Flask)...")
    bot.remove_webhook()
    bot.infinity_polling()
