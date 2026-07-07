import logging
from typeset import playlist


logging.basicConfig(level="INFO")
nip = playlist.not_in_playlist("orion_2026-06-12")
for song in nip:
    print(song)
