import logging
from typeset import playlist


logging.basicConfig(level="INFO")
nip = playlist.not_in_playlist("orion_2026-11-07")
for song in nip:
    print(f"  - name: {song.name}")
    print(f"    key: {song.key}")
    print(f"    note: {song.note}")
