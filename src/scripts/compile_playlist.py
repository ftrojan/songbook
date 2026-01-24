import logging
from typeset import playlist


logging.basicConfig(level="INFO")
p = playlist.get_playlist("orion_2026-03-13")
playlist.typeset_playlist(p)
logging.info(f"output saved to {p.output_path}")
