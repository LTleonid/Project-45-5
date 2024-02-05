'''from yandex_music import Client

client = Client('y0_AgAAAAAz5EsoAAG8XgAAAADwqKYWZE3PswvKQgqZ2J9pyYkaDrU94iw').init()
client.users_likes_tracks()[0].fetch_track().download('example.mp3')'''
'''import re

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
'''
def send_search_request_and_print_result(query):
    search_result = client.search(query)

    text = [f'Результаты по запросу "{query}":', '']

    best_result_text = ''
    if search_result.best:
        type_ = search_result.best.type
        best = search_result.best.result

        text.append(f'❗️Лучший результат: {type_to_name.get(type_)}')

        if type_ in ['track', 'podcast_episode']:
            artists = ''
            if best.artists:
                artists = ' - ' + ', '.join(artist.name for artist in best.artists)
            best_result_text = best.title + artists
            
            # Добавляем информацию об авторе песни
            if best.artists:
                authors = ', '.join(artist.name for artist in best.artists)
                text.append(f'Автор(ы): {authors}')
        elif type_ == 'artist':
            best_result_text = best.name
        elif type_ in ['album', 'podcast']:
            best_result_text = best.title
        elif type_ == 'playlist':
            best_result_text = best.title
        elif type_ == 'video':
            best_result_text = f'{best.title} {best.text}'

        text.append(f'Содержимое лучшего результата: {best_result_text}\n')

    if search_result.artists:
        text.append(f'Исполнителей: {search_result.artists.total}')
    if search_result.albums:
        text.append(f'Альбомов: {search_result.albums.total}')
    if search_result.tracks:
        text.append(f'Треков: {search_result.tracks.total}')
    if search_result.playlists:
        text.append(f'Плейлистов: {search_result.playlists.total}')
    if search_result.videos:
        text.append(f'Видео: {search_result.videos.total}')

    text.append('')
    print('\n'.join(text))
