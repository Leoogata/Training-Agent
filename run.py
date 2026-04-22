import os
import threading
from flask import request
import telebot
from app import create_app
from app.bot_service import bot, set_flask_app

# Cria a instância única do aplicativo Flask
app = create_app()

# Rota para receber updates do Telegram via Webhook
@app.route('/' + bot.token, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Forbidden', 403

def run_bot_polling():
    """Roda o bot Telegram em modo Polling (para ambiente local)"""
    print("🤖 Bot iniciado (Polling)!")
    bot.remove_webhook()
    bot.infinity_polling()

if __name__ == "__main__":
    # Passa a instância do app para o serviço do bot
    set_flask_app(app)
    
    port = int(os.environ.get('PORT', 10000))
    # O Render fornece a URL externa automaticamente nas variáveis de ambiente
    render_url = os.environ.get('RENDER_EXTERNAL_URL')

    if render_url:
        print(f"🌐 Configurando Webhook no Render: {render_url}")
        bot.remove_webhook()
        # Define o webhook apontando para a rota do Flask
        bot.set_webhook(url=f"{render_url}/{bot.token}")
    else:
        # Local: usa polling em thread separada
        bot_thread = threading.Thread(target=run_bot_polling, daemon=True)
        bot_thread.start()

    # Inicia o servidor Flask
    # debug=False é CRUCIAL para não iniciar o bot duas vezes
    app.run(host='0.0.0.0', port=port, debug=False)
