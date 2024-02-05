import telebot
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

# Замените YOUR_BOT_TOKEN на токен вашего бота
TOKEN = "6770656878:AAHL9nYL6TZZLfZoh-NFQgU01YH4dHp7uc0"

bot = telebot.TeleBot(TOKEN)

def is_yandex_music_url(url):
    parsed_url = urlparse(url)
    # Проверяем, содержит ли домен 'music.yandex'
    return 'music.yandex' in parsed_url.netloc

def get_music_info(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Извлекаем информацию о музыке, например, заголовок трека
        track_title = soup.find('meta', property='og:title')
        
        if track_title:
            return track_title['content']
        else:
            return 'Информация о музыке не найдена'
    except Exception as e:
        print(f"Error: {e}")
        return 'Произошла ошибка при получении информации о музыке'

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, 'Привет! Я бот для проверки ссылок на наличие музыки от Яндекс.Музыки.')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if is_yandex_music_url(url):
        music_info = get_music_info(url)
        bot.send_message(message.chat.id, f'Найдена музыка: {music_info}')
    else:
        bot.send_message(message.chat.id, 'Это не ссылка на Яндекс.Музыку.')

if __name__ == "__main__":
    bot.polling(none_stop=True)
