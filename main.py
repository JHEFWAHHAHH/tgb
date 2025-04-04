import telebot
import random
import time
import json
import os

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

STATS_FILE = "stats.json"
user_last_message_time = {}

def load_stats():
    try:
        with open(STATS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_stats(stats):
    with open(STATS_FILE, "w") as file:
        json.dump(stats, file)

user_stats = load_stats()

@bot.message_handler(commands=['start'])
def send_start(message):
    bot.reply_to(message, "Привіт! Я Потужнометр 💪 Виміряю потужність будь-якого слова, зображення або GIF у %. Відправ щось і перевір свою силу! ⚡")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "🤖 Просто відправ мені слово, фото, наліпку або GIF, і я визначу їхню потужність у %. 🚀")

@bot.message_handler(commands=['about'])
def send_about(message):
    bot.reply_to(message, "Я бот, що вимірює потужність слів, зображень та GIF у %. Написаний на Python з використанням Telebot! 💻")

@bot.message_handler(commands=['stats'])
def send_stats(message):
    user_id = str(message.chat.id)
    if user_id in user_stats:
        total_attempts = user_stats[user_id]['attempts']
        avg_power = user_stats[user_id]['total_power'] / total_attempts
        bot.reply_to(message, f"📊 Твоя статистика:\nВсього спроб: {total_attempts}\nСередня потужність: {avg_power:.2f}%")
    else:
        bot.reply_to(message, "📊 У тебе ще немає статистики. Відправ щось, щоб почати!")

@bot.message_handler(commands=['reset'])
def reset_stats(message):
    user_id = str(message.chat.id)
    if user_id in user_stats:
        del user_stats[user_id]
        save_stats(user_stats)
        bot.reply_to(message, "🔄 Твоя статистика скинута!")
    else:
        bot.reply_to(message, "📊 У тебе немає статистики для скидання.")

@bot.message_handler(content_types=['text', 'photo', 'sticker', 'animation'])
def send_random_percentage(message):
    user_id = str(message.chat.id)
    current_time = time.time()

    if user_id in user_last_message_time and current_time - user_last_message_time[user_id] < 3:
        bot.reply_to(message, "⏳ Повільніше, воїн! Чекай кілька секунд перед новим запитом. ⚡")
        return

    user_last_message_time[user_id] = current_time
    processing_message = bot.reply_to(message, "🔄 Рахую потужність...")
    time.sleep(2)
    bot.delete_message(message.chat.id, processing_message.message_id)

    random_percentage = random.randint(1, 100)

    if user_id not in user_stats:
        user_stats[user_id] = {'attempts': 0, 'total_power': 0}

    user_stats[user_id]['attempts'] += 1
    user_stats[user_id]['total_power'] += random_percentage
    save_stats(user_stats)

    text_reactions = ["💀", "😅", "🤣", "🤔", "💪", "😎", "🔥", "🚀", "🎉", "🏆", "✨", "⚡", "😈", "👑", "🦾"]
    photo_compliments = ["📸 Оце так мистецтво!", "🖼️ Це виглядає шикарно!", "✨ Просто вау!", "🎨 Так красиво, що аж очі розбігаються!", "🔥 Це справжній шедевр!", "😍 Вражаюче!", "📷 Професійний рівень!", "🌟 Неймовірно!"]
    sticker_reactions = ["👍 Крута наліпка!", "🔥 Це класика!", "😆 Дуже смішно!", "🎭 Ти справжній артист!", "🤣 Просто топ!", "💯 Легендарно!"]
    gif_reactions = ["😂 Це шикарно!", "🎬 Голлівуд нервово палить!", "🔥 Це варте Оскара!", "😆 Оце мем!", "🎭 Просто геніально!"]

    if message.content_type == 'text':
        reactions = text_reactions
        response_text = f"'{message.text}' має потужність: {random_percentage}% 💥\n{random.choice(reactions)} Спробуй ще раз!"
    elif message.content_type == 'photo':
        reactions = photo_compliments
        response_text = f"Це фото має потужність: {random_percentage}% 💥\n{random.choice(reactions)}"
    elif message.content_type == 'sticker':
        reactions = sticker_reactions
        response_text = f"Ця наліпка має потужність: {random_percentage}% 💥\n{random.choice(reactions)}"
    elif message.content_type == 'animation':
        reactions = gif_reactionsresponse_text= f"Цей GIF має потужність: {random_percentage}% 💥\n{random.choice(reactions)}"
    else:
        response_text = "🤷‍♂️ Щось цікаве, але я не знаю, як це оцінити!"

    bot.reply_to(message, response_text)

if name == "__main__":
    print("Бот запущено...")
    bot.polling(none_stop=True)