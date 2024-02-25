from yandex_music import Client, ArtistTracks


client = Client('y0_AgAAAAAz5EsoAAG8XgAAAADwqKYWZE3PswvKQgqZ2J9pyYkaDrU94iw').init()
c = client.tracks(['10994777:1193829'])
print(c)


