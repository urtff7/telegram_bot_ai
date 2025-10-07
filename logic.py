import main
from telebot import types
import data
import requests
from io import BytesIO
@main.bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    user_answers[user_id] = []
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("/gen:"), types.KeyboardButton("/help"), types.KeyboardButton("/stop"))
    main.bot.send_message(
        user_id,
        "Сгенерирую твой любой запрос на изображение!💪💪💪\n\nПример: `/gen: чеченец на коне под луной`",
        reply_markup=keyboard
    )
@main.bot.message_handler(commands=['stop'])
def stop(message):
    user_id = message.chat.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("/start"), types.KeyboardButton("/help"))
    main.bot.send_message(
        user_id,
        "Так рано заканчиваем? 😢 Возвращайся, когда захочешь сгенерировать что-то ещё!",
        reply_markup=keyboard
    )
@main.bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "/start - начать заново\n"
        "/help - помощь\n"
        "/gen: <текст> - сгенерировать изображение\n"
        "/stop - остановка бота"
    )
    main.bot.send_message(message.chat.id, help_text)
@main.bot.message_handler(func=lambda msg: msg.text.startswith("/gen:"))
def gen(message):
    user_id = message.chat.id
    text = message.text.replace("/gen:", "").strip()
    if not text:
        main.bot.send_message(user_id, "напиши после /gen: что нужно сгенерировать.\nПример:\n`/gen: волк на горе ночью`")
        return
    main.bot.send_message(user_id, f"🧠 Думаю над твоим запросом:\n`{text}`\nПодожди немного...")
    try:
        prompt_encoded = text.replace(" ", "%20")
        image_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}"
        response = requests.get(image_url)
        if response.status_code != 200:
            raise Exception(f"Ошибка загрузки: {response.status_code}")
        img_data = response.content
        img = BytesIO(img_data)
        img.name = "ai_image.png"
        img.seek(0)
        main.bot.send_photo(user_id, img, caption=f"Сгенерировано по запросу:\n`{text}`")
    except Exception as e:
        main.bot.send_message(user_id, f"⚠️ Ошибка при генерации: {e}")
print("✅ Бот запущен и ждёт команды (Pollinations активен)...")
main.bot.polling(non_stop=True)
