import telebot
import requests

TOKEN = '8031157841:AAFwAPqEY0akbAOi9myKCvAr_iuxLrxx50o'

class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float) -> float:
        url = f"https://api.exchangerate-api.com/v4/latest/{base.lower()}"
        try:
            response = requests.get(url)
            data = response.json()
        except Exception:
            raise APIException("Ошибка при подключении к API валют.")

        if 'rates' not in data:
            raise APIException("Некорректный ответ API.")

        rates = data['rates']
        if quote.lower() not in rates:
            raise APIException(f"Валюта '{quote}' недоступна или не поддерживается.")

        rate = rates[quote.lower()]
        result = rate * float(amount)
        return result

bot = telebot.TeleBot(TOKEN)

available_currencies = ['USD', 'EUR', 'RUB']

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    text = (
        "Привет! Я бот для конвертации валют.\n"
        "Чтобы узнать цену, отправьте сообщение в формате:\n"
        "<имя валюты, цену которой хотите узнать> "
        "<имя валюты, в которой нужно узнать цену> "
        "<количество первой валюты>\n"
        "Например:\nUSD EUR 100\n\n"
        "Доступные команды:\n/values — список доступных валют\n/help или /start — помощь"
    )
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def handle_values(message):
    text = "Доступные валюты:\n" + "\n".join(available_currencies)
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    try:
        parts = message.text.split()
        if len(parts) != 3:
            raise APIException("Неверный формат. Используйте:\n<валюта_источник> <валюта_цель> <количество>")
        base, quote, amount_str = parts
        base = base.upper()
        quote = quote.upper()

        if base not in available_currencies:
            raise APIException(f"Валюта '{base}' недоступна.")
        if quote not in available_currencies:
            raise APIException(f"Валюта '{quote}' недоступна.")
        amount = float(amount_str)
        if amount <= 0:
            raise APIException("Количество должно быть больше нуля.")

        total = CryptoConverter.get_price(base, quote, amount)
        reply = f"{amount} {base} стоит {total:.2f} {quote}"
        bot.send_message(message.chat.id, reply)

    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")
    except ValueError:
        bot.send_message(message.chat.id, "Некорректное число. Попробуйте еще раз.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {type(e).__name__}: {e}")

if __name__ == '__main__':
    bot.polling()