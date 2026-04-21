import telebot
import os
from telebot import types
from app.models import Workout, Exercise, WorkoutLog, ExerciseLog
from app import db

# Carrega o token da variável de ambiente
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Variável global para armazenar a instância do app Flask
flask_app = None

def set_flask_app(app):
    global flask_app
    flask_app = app

user_status = {}

@bot.message_handler(commands=['start'])
def start_workout(message):
    if not flask_app: return
    with flask_app.app_context():
        workouts = Workout.query.all()
        
        if not workouts:
            bot.reply_to(message, "Nenhum treino encontrado.")
            return

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        workouts_list = []
        for w in workouts:
            markup.add(w.name)
            workouts_list.append(f"• {w.name}")

        message_text = "Qual treino vamos fazer hoje?\n\nTreinos disponíveis:\n" + "\n".join(workouts_list)
        bot.send_message(message.chat.id, message_text, reply_markup=markup)

@bot.message_handler(commands=['reset'])
def reset_workout(message):
    chat_id = message.chat.id
    if chat_id in user_status:
        del user_status[chat_id]
        bot.reply_to(message, "🔄 Sessão reiniciada! Use /start para começar um novo treino.")
    else:
        bot.reply_to(message, "Você não tem uma sessão ativa no momento. Use /start para começar.")

@bot.message_handler(func=lambda message: message.chat.id not in user_status)
def select_workout(message):
    if not flask_app: return
    with flask_app.app_context():
        workout = Workout.query.filter_by(name=message.text).first()
        if not workout:
            bot.send_message(message.chat.id, "Por favor, escolha um treino válido.")
            return

        # 1. Cria o Log do Treino no Banco
        new_log = WorkoutLog(workout_id=workout.id)
        db.session.add(new_log)
        db.session.commit()

        # 2. Inicializa o estado do usuário
        user_status[message.chat.id] = {
            'workout_log_id': new_log.id,
            'workout_id': workout.id,
            'exercise_index': 0,
            'serie_atual': 1
        }

        proximo_passo(message.chat.id)

def proximo_passo(chat_id):
    if not flask_app: return
    with flask_app.app_context():
        status = user_status[chat_id]
        workout = Workout.query.get(status['workout_id'])

        # Verifica se ainda há exercícios
        if status['exercise_index'] >= len(workout.exercises):
            bot.send_message(chat_id, "✅ Treino finalizado! Monstro!")
            del user_status[chat_id]
            return

        exercicio = workout.exercises[status['exercise_index']]

        # Se terminou as séries deste exercício, pula para o próximo
        if status['serie_atual'] > exercicio.sets:
            status['exercise_index'] += 1
            status['serie_atual'] = 1
            proximo_passo(chat_id)
            return

        # Busca o último registro deste exercício
        ultimo_registro = ExerciseLog.query.filter_by(exercise_id=exercicio.id).order_by(ExerciseLog.id.desc()).first()

        reps_min = exercicio.reps - 2
        msg = f"🏋️ **{exercicio.name}**\nSérie {status['serie_atual']}/{exercicio.sets}\nReps: {reps_min} a {exercicio.reps}"

        if ultimo_registro:
            msg += f"\n\n📊 Última vez: {ultimo_registro.weight}kg × {ultimo_registro.reps_done} reps"

        msg += "\n\nEnvie o peso e reps (ex: 50 10):"
        bot.send_message(chat_id, msg, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.chat.id in user_status)
def register_series(message):
    if not flask_app: return
    with flask_app.app_context():
        chat_id = message.chat.id
        status = user_status[chat_id]
        
        try:
            # Espera algo como "50 10" (50kg e 10 reps)
            dados = message.text.split()
            peso = float(dados[0])
            reps = int(dados[1])

            # Pega o ID do exercício atual
            workout = Workout.query.get(status['workout_id'])
            exercicio_atual = workout.exercises[status['exercise_index']]

            # 3. Salva o Log da Série no Banco
            log_serie = ExerciseLog(
                workout_log_id=status['workout_log_id'],
                exercise_id=exercicio_atual.id,
                weight=peso,
                reps_done=reps
            )
            db.session.add(log_serie)
            db.session.commit()

            # Atualiza o estado para a próxima série
            status['serie_atual'] += 1
            proximo_passo(chat_id)

        except Exception:
            bot.send_message(chat_id, "❌ Formato inválido! Envie: 'peso reps' (ex: 50 10)")

if __name__ == "__main__":
    # Para testes locais, criamos um app temporário
    from app import create_app
    app = create_app()
    set_flask_app(app)
    bot.infinity_polling()
