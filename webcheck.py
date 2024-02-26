from yandex_music import Client, ArtistTracks


client = Client('y0_AgAAAAAz5EsoAAG8XgAAAADwqKYWZE3PswvKQgqZ2J9pyYkaDrU94iw').init()
c = client.tracks(['120891519:28929373'])
print(c)
print(c[0]['content_warning'])


