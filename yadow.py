from yandex_music import Client

client = Client().init()

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

def get_best_track_info(search_result):
    if search_result.best:
        type_ = search_result.best.type
        best = search_result.best.result

        if type_ in ['track', 'podcast_episode']:
            artists = ', '.join(artist.name for artist in best.artists)
            return f'{best.title} - {artists}', best.download_info

    return None, None

def download_track(download_info, filename):
    try:
        download_url = download_info.get_download_link()
        print(f'Downloading: {filename}')
        client.downloader.download(download_url, f'{filename}.mp3')
        print('Download complete!')
    except Exception as e:
        print(f'Error during download: {e}')

def send_search_request_and_print_result(query):
    search_result = client.search(query)

    text = [f'Результаты по запросу "{query}":', '']

    best_result_text, download_info = get_best_track_info(search_result)

    if best_result_text:
        text.append(f'❗️Лучший результат: {type_to_name.get(search_result.best.type)}')
        text.append(f'Содержимое лучшего результата: {best_result_text}\n')

        download_track(download_info, best_result_text)

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

if __name__ == '__main__':
    while True:
        input_query = input('Введите поисковой запрос: ')
        send_search_request_and_print_result(input_query)
