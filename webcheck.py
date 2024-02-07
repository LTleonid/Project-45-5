from yandex_music import Client


client = Client()
search_text = 'Отпустить'
search_result = client.search(search_text)

if search_result.best:
    best = search_result.best.result
    track_id = best.trackId
    print(track_id)
else:
    print("Трек не найден")