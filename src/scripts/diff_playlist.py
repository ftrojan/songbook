import logging
from typeset import playlist


logging.basicConfig(level="INFO")
name1 = "orion_2026-06-12"
name2 = "orion_2026-07-10"
p1 = playlist.get_playlist(name1)
p2 = playlist.get_playlist(name2)
s1 = {song.name for song in p1.songs}
s2 = {song.name for song in p2.songs}
d1 = s1 - s2
d2 = s2 - s1
print(f"{len(d1)} songs found in {name1} but not in {name2}")
for song in d1:
    print(song)
print(f"{len(d2)} songs found in {name2} but not in {name1}")
for song in d2:
    print(song)
