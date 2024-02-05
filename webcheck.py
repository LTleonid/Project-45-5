'''from yandex_music import Client

client = Client('y0_AgAAAAAz5EsoAAG8XgAAAADwqKYWZE3PswvKQgqZ2J9pyYkaDrU94iw').init()
client.users_likes_tracks()[0].fetch_track().download('example.mp3')'''
import re

def извлечь_номера_из_ссылки(ссылка):
    # Используем регулярные выражения для поиска числовых значений
    результат = re.findall(r'\d+', ссылка)
    
    # Выводим результат
    if результат:
        return результат
    else:
        return None

# Пример использования
ссылка = "https://music.yandex.ru/album/3071605/track/65111929"
номера = извлечь_номера_из_ссылки(ссылка)

if номера:
    print("Первый номер:", номера[0])
    print("Второй номер:", номера[1])
else:
    print("Числовые значения не найдены в ссылке.")
