import sys
import os

# Adiciona o diretório raiz ao path do Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.bot_service import bot

if __name__ == "__main__":
    bot.infinity_polling()
