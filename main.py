import telebot
from config import currencies, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

LANGUAGE = "russian"


@bot.message_handler(commands=["russian"])
def to_russian(message: telebot.types.Message):
    global LANGUAGE
    LANGUAGE = "russian"
    text = "Язык был изменен на русский"
    bot.reply_to(message, text)


@bot.message_handler(commands=["english"])
def to_english(message: telebot.types.Message):
    global LANGUAGE
    LANGUAGE = "english"
    text = "Language was changed to english"
    bot.reply_to(message, text)


def is_russian():
    return LANGUAGE == "russian"


def handle_start_text(LANGUAGE, user_full_name):
    if LANGUAGE == "russian":
        return f"""Привет {user_full_name} 👋! Моё имя TransactionalBot 🤖
Я помогу узнать цену на определённое количество валюты (евро, доллар или рубль).

Чтобы начать взаимодействие с ботом, введите команду в указанном формате:
<Имя валюты, цену которой вы хотите узнать> <В какую валюту перевести> <Число переводимой валюты>

📜 Команды:

1️⃣ /start или /help - получить инструкцию.
2️⃣ /values - информация о всех доступных валютах.
3️⃣ /english - переключить язык на английский.
4️⃣ /russian - переключить язык на русский."""

    if LANGUAGE == "english":
        return f"""Hello {user_full_name} 👋! My name is TransactionalBot 🤖
I will help you find out the price for a certain amount of currency (euro, dollar or ruble).

To start interacting with the bot, enter the command in the specified format:
<Name of the currency you want to know the price of> <Which currency to convert to> <Number of currency to be transferred>

📜 Commands:

1️⃣ /start or /help - get instructions.
2️⃣ /values - information about all available currencies.
3️⃣ /english - switch the language to English.
4️⃣ /russian - switch the language to Russian."""


@bot.message_handler(commands=["start", "help"])
def instruction(message: telebot.types.Message):
    user_full_name = message.from_user.full_name
    bot.reply_to(message, handle_start_text(LANGUAGE, user_full_name))


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    title = "   💸 Перечень доступных валют 💸 \n" if is_russian() else "      💸 List of available currencies\
💸 \n"
    text = ("┌───────────────────────┐\n"
            f"{title}"
            "└───────────────────────┘")
    for key in currencies.keys():
        text = '\n'.join((text, "•  " + key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        value = message.text.split(' ')  # получить список и разделить пробелами

        if len(value) != 3:
            raise APIException("Не верное количество параметров" if is_russian() else "Incorrect number of\
parameters")
        quote, base, amount = value
        total_base = CryptoConverter.get_price(quote, base, amount, LANGUAGE)
        total_base = total_base * int(amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя\n{e}" if is_russian() else f"User error\n{e}")

    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}" if is_russian() else f"Failed to process the \
command\n{e}")
    else:
        text = f"Цена {amount} {quote} в {base} - {total_base}"
        bot.send_message(message.chat.id, text)


bot.polling()
