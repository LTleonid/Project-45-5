from yandex_music import Client

client = Client('y0_AgAAAAAz5EsoAAG8XgAAAADwqKYWZE3PswvKQgqZ2J9pyYkaDrU94iw').init()
for i in range(len(client.users_likes_tracks())):
    print(client.users_likes_tracks()[i])