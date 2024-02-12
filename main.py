import telebot
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from yandex_music import Client,  # Добавлено для использования функции поиска музыки
from datetime import datetime  # Added to get the current time
from urllib.request import urlopen
import re


log_file = open("log.txt", "a", encoding="utf-8")

# Замените YOUR_BOT_TOKEN на токен вашего бота
TOKEN = "6770656878:AAHL9nYL6TZZLfZoh-NFQgU01YH4dHp7uc0"

bot = telebot.TeleBot(TOKEN)
client = Client().init()  # Инициализация Yandex.Music Client

type_to_name = {
    'track': 'трек',
    'artist': 'исполнитель',
    'album': 'альбом',
    'playlist': 'плейлист',
    'video': 'видео',
    'user': 'пользователь',
    'podcast': 'подкаст',
    'podcast_episode': 'эпизод подкаста',
}

def has_emoji(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # эмодзи с улыбающимися лицами
                               u"\U0001F300-\U0001F5FF"  # другие эмодзи и символы
                               u"\U0001F680-\U0001F6FF"  # транспорт и символы
                               u"\U0001F700-\U0001F77F"  # символы категории 'дополнительные'
                               u"\U0001F780-\U0001F7FF"  # символы категории 'эмодзи-дополнительные'
                               u"\U0001F800-\U0001F8FF"  # символы категории 'дополнительные'
                               u"\U0001F900-\U0001F9FF"  # символы категории 'эмодзи-дополнительные'
                               u"\U0001FA00-\U0001FA6F"  # символы категории 'дополнительные'
                               u"\U0001FA70-\U0001FAFF"  # символы категории 'эмодзи-дополнительные'
                               "]+", flags=re.UNICODE)
    return bool(emoji_pattern.search(text))

def is_yandex_music_url(url):
    parsed_url = urlparse(url)
    return 'music.yandex' in parsed_url.netloc

def get_music_info(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        track_title = soup.find('meta', property='og:title')

        if track_title:
            # Extracting only the artist and track name from the title
            title_content = track_title['content'].split(' слушать онлайн на Яндекс Музыке')[0]
            return title_content
        else:
            return 'Информация о музыке не найдена'
    except Exception as e:
        print(f"Error: {e}")
        return 'Произошла ошибка при получении информации о музыке'


def send_search_request(query):
    search_result = client.search(query)
    return search_result

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, 'Привет! Я бот для проверки ссылок на наличие музыки от Яндекс.Музыки.')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_info = f"{current_time} | {message.from_user.username}"

    # Log user's message
    user_message_log = f"{user_info}: {message.text}\n"
    log_file.write(user_message_log)
    log_file.flush()  # Ensure that the log is written immediately

    print(user_message_log)
    try:
        url = message.text
        if is_yandex_music_url(url):
            music_info = get_music_info(url)
            bot.send_message(message.chat.id, f'Найдена музыка: {music_info}')

            # Log bot's response
            bot_response_log = f"{current_time} | BOT -> {message.from_user.username}: Найдена музыка: {music_info}\n"
            log_file.write(bot_response_log)
            log_file.flush()  # Ensure that the log is written immediately

            print(bot_response_log)
        else:
            search_result = send_search_request(url)
            if search_result.best:
                best = search_result.best.result
            else:
                temp = search_result
                for i in client.search_suggest(search_result):
                    if not(search_result.best):
                        search_result = temp + str(i)
                    else:
                        break
                best = search_result.best.result
                type_ = search_result.best.type
                if type_ in ['track', 'podcast_episode']:
                    artists = ''
                    if best.artists:
                        artists = ' - ' + ', '.join(artist.name for artist in best.artists)
                        best_result_text = best.title + artists
            if not(search_result.best):
                bot.send_message(message.chat.id, 'Это не ссылка на Яндекс.Музыку.')

                # Log bot's response
                bot_response_log = f"{current_time} | BOT -> {message.from_user.username}: Это не ссылка на Яндекс.Музыку.\n"
                log_file.write(bot_response_log)
                log_file.flush()  # Ensure that the log is written immediately
            if best.content_warning == 'explicit':
                bot.send_message(message.chat.id, f'Песня {best_result_text} содержит маты.')
                bot_response_log = f"{current_time} | BOT -> {message.from_user.username}: Err: Песня {best_result_text} содержит маты.\n"
                log_file.write(bot_response_log)
                log_file.flush()
            url_ogg = best.get_og_image_url()
                
            photo1 = urlopen(url_ogg)
            bot.send_photo(message.chat.id, photo1)
            bot.send_message(message.chat.id, f'Лучший результат: {best_result_text}')

            # Log bot's response
            bot_response_log = f"{current_time} | BOT -> {message.from_user.username}: Лучший результат: {best_result_text}\n"
            log_file.write(bot_response_log)
            log_file.flush()  # Ensure that the log is written immediately

            print(bot_response_log)
            

            print(bot_response_log)
    except Exception as e:
        if has_emoji(message.text):
            error_message = f"{current_time} | BOT -> {message.from_user.username}: Появилась ошибка, Эмодзи в тексте\n"
            bot.send_message(message.chat.id, 'Я не могу распознать текст из-за эмодзи')
        else:
            error_message = f"{current_time} | BOT -> {message.from_user.username}: Появилась ошибка - {e}. Но я должен дальше работать\n"
            bot.send_message(message.chat.id, error_message)

        # Log bot's response
        log_file.write(error_message)
        log_file.flush()  # Ensure that the log is written immediately

        print(error_message)

if __name__ == "__main__":
    bot.polling(none_stop=True)

log_file.close()
