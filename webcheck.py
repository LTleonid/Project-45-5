from yandex_music import Client


client = Client()
search_text = '...'
search_result = client.search(search_text)
temp = ''
if search_result.best:
    best = search_result.best.result
    print(best.title)

else:
    temp = search_text
    for i in client.search_suggest(search_text):
        if not(search_result.best):
            search_result = temp + str(i)
        else:
            break
    best = search_result.best.result
print(best.title)
