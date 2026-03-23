import telebot
import random

# ====== Настройки ======
TOKEN = "8645126152:AAF-F622J1SIdMVwT1twSGv0-OixbZluzJc"  # Вставь сюда токен от BotFather
ADMIN_USERNAME = "Detetikl46"  # Только этот юзернейм сможет делать /generate

# ====== Инициализация бота ======
bot = telebot.TeleBot(TOKEN)

# ====== Список участников ======
players = []

# ====== Команда /start ======
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
                 "Привет! 👋\nЧтобы зарегистрироваться на турнир, отправь команду:\n/join ТВОЙ_НИК")

# ====== Команда /join ======
@bot.message_handler(commands=['join'])
def join(message):
    try:
        nick = message.text.split(" ", 1)[1]
    except IndexError:
        bot.reply_to(message, "❌ Напиши: /join ТВОЙ_НИК")
        return

    if nick in players:
        bot.reply_to(message, f"⚠️ {nick}, ты уже зарегистрирован!")
    else:
        players.append(nick)
        bot.reply_to(message, f"✅ {nick} успешно зарегистрирован!")

# ====== Команда /players ======
@bot.message_handler(commands=['players'])
def show_players(message):
    if players:
        bot.reply_to(message, "🎮 Зарегистрированные участники:\n" + "\n".join(players))
    else:
        bot.reply_to(message, "Пока нет участников.")

# ====== Команда /generate (только админ) ======
@bot.message_handler(commands=['generate'])
def generate_brackets(message):
    # Проверка, что команду выполняет админ
    if message.from_user.username != ADMIN_USERNAME:
        bot.reply_to(message, "❌ Только админ может генерировать сетку!")
        return

    if len(players) < 8:
        bot.reply_to(message, "⚠️ Недостаточно участников для турнира (минимум 8).")
        return

    # Перемешиваем участников
    shuffled = players.copy()
    random.shuffle(shuffled)

    # Делим на группы по 8 игроков
    groups = [shuffled[i:i+8] for i in range(0, len(shuffled), 8)]
    text = "🏐 Турнирные группы:\n\n"
    for idx, group in enumerate(groups):
        text += f"Группа {chr(65+idx)}:\n" + "\n".join(group) + "\n\n"

    bot.reply_to(message, text)

# ====== Запуск бота ======
bot.polling()
